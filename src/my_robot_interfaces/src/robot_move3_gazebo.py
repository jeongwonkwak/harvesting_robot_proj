import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray, Int32
from dsr_msgs2.srv import MoveJoint, MoveLine, MoveCircle, Fkin, GetCurrentPose
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Duration
import math
import os
import time
import numpy as np


JOINT_NAMES = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']

# E0509 URDF 기준 관절 한계 (degree)
JOINT_LIMITS = [
    (-360.0, 360.0),   # J1
    ( -95.0,  95.0),   # J2  (±1.658 rad)
    (-135.0, 135.0),   # J3  (±2.356 rad)
    (-360.0, 360.0),   # J4
    (-135.0, 135.0),   # J5  (±2.356 rad)
    (-360.0, 360.0),   # J6
]

# E0509 작업공간 한계 (mm)
TCP_MAX_REACH = 900.0   # 베이스로부터 최대 도달 거리
TCP_MIN_REACH =  150.0  # 특이점 회피를 위한 최소 거리
TCP_Z_MIN     = -200.0  # 베이스 아래로 내려갈 수 있는 최대 깊이


def _fkin_e0509(joints_deg: list) -> list:
    """E0509 URDF 기반 소프트웨어 순기구학. 단위: mm, degree (ZYX Euler)."""
    q = [math.radians(d) for d in joints_deg]
    p2 = math.pi / 2
    # (rpy, xyz_m) — URDF joint origins
    params = [
        ((0,    0,   0),   (0,      0,       0.2045)),
        ((0,   -p2, -p2),  (0,      0,       0)),
        ((0,    0,   p2),  (0.373,  0,       0)),
        ((p2,   0,   0),   (0,     -0.373,   0)),
        ((-p2,  0,   0),   (0,      0,       0)),
        ((p2,   0,   0),   (0,     -0.1725,  0)),
    ]
    T = np.eye(4)
    for i, ((r, p, y), (tx, ty, tz)) in enumerate(params):
        cr, sr = math.cos(r), math.sin(r)
        cp, sp = math.cos(p), math.sin(p)
        cy, sy = math.cos(y), math.sin(y)
        Ro = np.array([
            [cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
            [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
            [-sp,   cp*sr,             cp*cr            ],
        ])
        cq, sq = math.cos(q[i]), math.sin(q[i])
        Rj = np.array([[cq, -sq, 0], [sq, cq, 0], [0, 0, 1]])
        Ti = np.eye(4)
        Ti[:3, :3] = Ro @ Rj
        Ti[:3, 3]  = [tx, ty, tz]
        T = T @ Ti
    pos = T[:3, 3] * 1000.0
    R   = T[:3, :3]
    sy  = math.sqrt(R[0, 0]**2 + R[1, 0]**2)
    if sy > 1e-6:
        rx = math.degrees(math.atan2( R[2, 1],  R[2, 2]))
        ry = math.degrees(math.atan2(-R[2, 0],  sy))
        rz = math.degrees(math.atan2( R[1, 0],  R[0, 0]))
    else:
        rx = math.degrees(math.atan2(-R[1, 2],  R[1, 1]))
        ry = math.degrees(math.atan2(-R[2, 0],  sy))
        rz = 0.0
    return [float(pos[0]), float(pos[1]), float(pos[2]), rx, ry, rz]


def _validate_joints(angles_deg: list) -> tuple[bool, str]:
    """관절 각도가 한계 범위 안에 있는지 검사. (ok, 에러메시지) 반환."""
    if len(angles_deg) != 6:
        return False, f'관절값 개수 오류: {len(angles_deg)}개 (6개 필요)'
    errors = []
    for i, (angle, (lo, hi)) in enumerate(zip(angles_deg, JOINT_LIMITS), start=1):
        if not (lo <= angle <= hi):
            errors.append(f'  J{i}: {angle:.1f}°  (허용범위: {lo}° ~ {hi}°)')
    if errors:
        return False, '관절 한계 초과:\n' + '\n'.join(errors)
    return True, ''


def _validate_tcp(pos: list) -> tuple[bool, str]:
    """TCP 위치가 작업공간 안에 있는지 검사. (ok, 에러메시지) 반환."""
    x, y, z = pos[0], pos[1], pos[2]
    reach_xy = math.sqrt(x**2 + y**2)
    reach_3d = math.sqrt(x**2 + y**2 + z**2)
    errors = []
    if reach_3d > TCP_MAX_REACH:
        errors.append(f'  도달 거리 초과: {reach_3d:.1f}mm (최대 {TCP_MAX_REACH}mm)')
    if reach_xy < TCP_MIN_REACH:
        errors.append(f'  중심축 근접 (특이점 위험): XY거리 {reach_xy:.1f}mm (최소 {TCP_MIN_REACH}mm)')
    if z < TCP_Z_MIN:
        errors.append(f'  Z 하한 초과: {z:.1f}mm (최소 {TCP_Z_MIN}mm)')
    if errors:
        return False, 'TCP 작업공간 범위 초과:\n' + '\n'.join(errors)
    return True, ''


def _validate_duration(dur: float) -> tuple[bool, str]:
    if dur < 0.5:
        return False, f'이동 시간이 너무 짧습니다: {dur}초 (최소 0.5초)'
    if dur > 60.0:
        return False, f'이동 시간이 너무 깁니다: {dur}초 (최대 60초)'
    return True, ''


class E0509GazeboController(Node):
    GRIPPER_OPEN  = 0.0
    GRIPPER_CLOSE = 1.0

    def __init__(self):
        super().__init__('e0509_gazebo_controller')

        # ── JointTrajectoryController (MoveJoint용) ───────────────
        self.joint_pub = self.create_publisher(
            JointTrajectory,
            '/gz/joint_trajectory_controller/joint_trajectory',
            10
        )

        # ── 그리퍼 ─────────────────────────────────────────────────
        # 모드 B(real+gazebo): Int32 → gripper_service_node → 실제 로봇 + gazebo_bridge → Gazebo
        # 모드 A(gazebo 단독): Float64MultiArray → gripper_controller 직접
        self.gripper_real_pub = self.create_publisher(
            Int32,
            '/dsr01/gripper/position_cmd',
            10
        )
        self.gripper_gz_pub = self.create_publisher(
            Float64MultiArray,
            '/gz/gripper_controller/commands',
            10
        )

        # ── Doosan 서비스 (MoveJoint / MoveLine / MoveCircle / Fkin / GetCurrentPose) ──
        # bringup_real_gazebo.launch.py 사용 시 활성화됨
        self.joint_svc_client  = self.create_client(MoveJoint,      '/dsr01/motion/move_joint')
        self.line_client       = self.create_client(MoveLine,        '/dsr01/motion/move_line')
        self.circle_client     = self.create_client(MoveCircle,      '/dsr01/motion/move_circle')
        self.fkin_client       = self.create_client(Fkin,            '/dsr01/motion/fkin')
        self.pose_client       = self.create_client(GetCurrentPose,  '/dsr01/system/get_current_pose')

        # ── 관절 상태 ─────────────────────────────────────────────
        self.current_joints   = None
        self.last_pose        = None
        self._joints_from_real = False
        self._doosan_available = self.joint_svc_client.wait_for_service(timeout_sec=2.0)
        if self._doosan_available:
            self.pose_client.wait_for_service(timeout_sec=2.0)
            self.line_client.wait_for_service(timeout_sec=2.0)
            self.circle_client.wait_for_service(timeout_sec=2.0)

        # 실제 로봇 관절 상태 (우선), Gazebo 관절 상태 (폴백)
        self.create_subscription(JointState, '/dsr01/joint_states', self._joint_cb, 10)
        self.create_subscription(JointState, '/gz/joint_states',    self._joint_cb_gz, 10)

        if self._doosan_available:
            self.get_logger().info('실제 로봇 감지 → 모드 B (real+gazebo)')
        else:
            self.get_logger().info('실제 로봇 없음 → 모드 A (Gazebo 단독)')
        self.get_logger().info('컨트롤러 준비 완료')

    # ── 콜백 ─────────────────────────────────────────────────────
    def _joint_cb(self, msg):
        """실제 로봇 /dsr01/joint_states 콜백 (우선순위 높음)."""
        idx = {name: i for i, name in enumerate(msg.name)}
        joints = {
            name: math.degrees(msg.position[idx[name]])
            for name in JOINT_NAMES if name in idx
        }
        if len(joints) == 6:
            self.current_joints = joints
            self._joints_from_real = True

    def _joint_cb_gz(self, msg):
        """Gazebo /gz/joint_states 콜백 (폴백: 실제 로봇 데이터 없을 때만 사용)."""
        if getattr(self, '_joints_from_real', False):
            return
        idx = {name: i for i, name in enumerate(msg.name)}
        joints = {
            name: math.degrees(msg.position[idx[name]])
            for name in JOINT_NAMES if name in idx
        }
        if len(joints) == 6:
            self.current_joints = joints

    # ── MoveJoint ─────────────────────────────────────────────────
    def move_joint(self, angles_deg, duration_sec=3.0):
        self.get_logger().info(f'MoveJoint: {[round(a,1) for a in angles_deg]}')
        if self._doosan_available:
            return self._move_joint_doosan(angles_deg, duration_sec)
        return self._move_joint_traj(angles_deg, duration_sec)

    def _move_joint_doosan(self, angles_deg, duration_sec=3.0):
        req = MoveJoint.Request()
        req.pos        = [float(a) for a in angles_deg]
        req.vel        = 60.0
        req.acc        = 60.0
        req.time       = float(duration_sec)
        req.mode       = 0
        req.blend_type = 0
        req.sync_type  = 1  # 동기: 이동 완료까지 서비스가 블록
        future = self.joint_svc_client.call_async(req)
        timeout = duration_sec + 10.0  # 이동 시간 + 여유 10초
        rclpy.spin_until_future_complete(self, future, timeout_sec=timeout)
        if not future.done() or future.result() is None:
            print('[MoveJoint] Doosan 서비스 응답 없음')
            return False
        ok = future.result().success
        self.get_logger().info(f'MoveJoint {"완료" if ok else "실패"}')
        return ok

    def _move_joint_traj(self, angles_deg, duration_sec=3.0):
        traj = JointTrajectory()
        traj.joint_names = JOINT_NAMES
        pt = JointTrajectoryPoint()
        pt.positions = [math.radians(a) for a in angles_deg]
        secs = int(duration_sec)
        pt.time_from_start = Duration(sec=secs, nanosec=int((duration_sec - secs) * 1e9))
        traj.points = [pt]
        self.joint_pub.publish(traj)
        self._wait_for_joints(angles_deg, timeout=duration_sec + 8.0)
        return True

    def _wait_for_joints(self, target_deg, timeout=10.0, tol=1.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.current_joints is None:
                continue
            errors = [abs(self.current_joints.get(JOINT_NAMES[i], 0.0) - target_deg[i]) for i in range(6)]
            if all(e < tol for e in errors):
                self.get_logger().info('MoveJoint 완료')
                return
        self.get_logger().warn('MoveJoint 타임아웃')

    # ── MoveLine (Doosan 서비스) ───────────────────────────────────
    def move_line(self, pos, vel=None, acc=None):
        req      = MoveLine.Request()
        req.pos  = [float(p) for p in pos]
        req.vel  = vel or [100.0, 30.0]
        req.acc  = acc or [200.0, 60.0]
        req.ref  = 0
        req.mode = 0
        future   = self.line_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=30.0)
        if not future.done() or future.result() is None:
            print('[MoveLine] 서비스 응답 없음 — bringup_real_gazebo.launch.py mode:=virtual 확인')
            return False
        ok = future.result().success
        self.get_logger().info(f'MoveLine {"완료" if ok else "실패"}: {pos}')
        return ok

    # ── MoveCircle (Doosan 서비스) ────────────────────────────────
    def move_circle(self, via_pos, end_pos, vel=None, acc=None):
        req  = MoveCircle.Request()
        p1   = Float64MultiArray(); p1.data = [float(v) for v in via_pos]
        p2   = Float64MultiArray(); p2.data = [float(v) for v in end_pos]
        req.pos  = [p1, p2]
        req.vel  = vel or [100.0, 30.0]
        req.acc  = acc or [200.0, 60.0]
        req.ref  = 0
        req.mode = 0
        print(f'[MoveCircle] 경유점: {via_pos}')
        print(f'[MoveCircle] 끝점:   {end_pos}')
        future = self.circle_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)
        if not future.done() or future.result() is None:
            print('[MoveCircle] 서비스 응답 없음 — bringup_real_gazebo.launch.py mode:=virtual 확인')
            return False
        result = future.result()
        print(f'[MoveCircle] {"완료" if result.success else "실패"}')
        return result.success

    # ── 현재 TCP 위치 ─────────────────────────────────────────────
    def get_current_pose(self):
        if self._doosan_available:
            return self._get_pose_doosan()
        return self._get_pose_fkin()

    def _get_pose_doosan(self):
        """실제 로봇: GetCurrentPose 서비스로 TCP 위치 직접 조회."""
        req = GetCurrentPose.Request()
        req.space_type = 1  # task space
        future = self.pose_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.done():
            print('[현재 위치] GetCurrentPose 서비스 타임아웃 → Fkin 폴백')
            return self._get_pose_fkin()
        if future.result() is None or not future.result().success:
            print(f'[현재 위치] GetCurrentPose 실패(success=False) → Fkin 폴백')
            return self._get_pose_fkin()
        pos = list(future.result().pos)
        self.last_pose = pos
        joints = self.get_current_joints() or []
        if joints:
            print(f'현재 관절 각도: {[round(j,2) for j in joints]}')
        print(f'\n현재 TCP 위치 (실제 로봇):')
        print(f'  X={pos[0]:.2f}  Y={pos[1]:.2f}  Z={pos[2]:.2f}')
        print(f'  RX={pos[3]:.2f}  RY={pos[4]:.2f}  RZ={pos[5]:.2f}')
        return pos

    def _get_pose_fkin(self):
        """Gazebo 전용: joint_states + Fkin 서비스로 TCP 위치 계산."""
        # joint state 수신 보장: 최대 3초간 루프
        deadline = time.time() + 3.0
        while self.current_joints is None and time.time() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)
        if self.current_joints is None:
            print('[현재 위치] joint_states 수신 실패')
            return None
        order  = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        joints = [self.current_joints.get(n, 0.0) for n in order]
        print(f'현재 관절 각도: {[round(j,2) for j in joints]}')
        req     = Fkin.Request()
        req.pos = joints
        req.ref = 0
        future  = self.fkin_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.done() or future.result() is None:
            print('[현재 위치] Fkin 서비스 없음 → 소프트웨어 FK 사용')
            pos = _fkin_e0509(joints)
            self.last_pose = pos
            print(f'\n현재 TCP 위치 (SW FK):')
            print(f'  X={pos[0]:.2f}  Y={pos[1]:.2f}  Z={pos[2]:.2f}')
            print(f'  RX={pos[3]:.2f}  RY={pos[4]:.2f}  RZ={pos[5]:.2f}')
            return pos
        pos = list(future.result().conv_posx)
        self.last_pose = pos
        print(f'\n현재 TCP 위치 (Gazebo):')
        print(f'  X={pos[0]:.2f}  Y={pos[1]:.2f}  Z={pos[2]:.2f}')
        print(f'  RX={pos[3]:.2f}  RY={pos[4]:.2f}  RZ={pos[5]:.2f}')
        return pos

    # ── 자동 원호 (끝점만 입력) ───────────────────────────────────
    def auto_circle(self, end_xyz):
        pose = self.get_current_pose()
        if pose is None:
            return False
        start = pose[:3]
        rx, ry, rz = pose[3], pose[4], pose[5]
        mid  = [(s + e) / 2 for s, e in zip(start, end_xyz)]
        d    = [e - s for s, e in zip(start, end_xyz)]
        length = math.sqrt(sum(v**2 for v in d))
        if length < 1.0:
            print('시작점과 끝점이 너무 가깝습니다.')
            return False
        perp = [-d[1], d[0], 0.0]
        perp_len = math.sqrt(perp[0]**2 + perp[1]**2)
        if perp_len < 0.001:
            perp = [1.0, 0.0, 0.0]; perp_len = 1.0
        radius = length / 2
        perp   = [v / perp_len * radius for v in perp]
        via    = [float(m + p) for m, p in zip(mid, perp)]
        via_full = via + [float(rx), float(ry), float(rz)]
        end_full = [float(v) for v in end_xyz] + [float(rx), float(ry), float(rz)]
        print(f'자동 계산 경유점: {[round(v, 2) for v in via[:3]]}')
        return self.move_circle(via_full, end_full)

    # ── 그리퍼 ────────────────────────────────────────────────────
    def set_gripper(self, value_0_740, wait=1.2):
        value_0_740 = max(0, min(740, int(value_0_740)))
        rad = float(value_0_740) / 740.0 * self.GRIPPER_CLOSE
        rad = max(self.GRIPPER_OPEN, min(rad, self.GRIPPER_CLOSE))

        gz_msg = Float64MultiArray()
        gz_msg.data = [rad, rad, rad, rad]  # r1, r2, l1, l2
        self.gripper_gz_pub.publish(gz_msg)

        if self._doosan_available:
            # 모드 B: real 그리퍼 → gripper_service_node + Gazebo 직접 제어
            msg = Int32()
            msg.data = value_0_740
            self.gripper_real_pub.publish(msg)
            self.get_logger().info(f'그리퍼(실제+Gazebo): {value_0_740} (→ {rad:.3f} rad)')
        else:
            # 모드 A: Gazebo 그리퍼 controller 직접 제어
            self.get_logger().info(f'그리퍼(Gazebo): {value_0_740} (→ {rad:.3f} rad)')
        time.sleep(wait)

    def open_gripper(self):  self.set_gripper(0)
    def close_gripper(self): self.set_gripper(740)

    # ── 현재 관절 확인 ────────────────────────────────────────────
    def get_current_joints(self):
        deadline = time.time() + 3.0
        while self.current_joints is None and time.time() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)
        if self.current_joints is None:
            print('[현재 관절] joint_states 수신 실패')
            return None
        vals = [self.current_joints.get(n, 0.0) for n in JOINT_NAMES]
        return vals

    # ── 메뉴 ─────────────────────────────────────────────────────
    def run(self):
        while True:
            os.system('clear')
            print('='*52)
            mode = 'real+gazebo' if self._doosan_available else 'Gazebo 단독'
            print(f'   E0509 로봇 제어  [{mode}]')
            print('='*52)
            print('  0: 현재 위치 확인 (관절 + TCP)')
            print('  1: MoveJoint  - 관절 각도 이동')
            print('  2: MoveLine   - 직선 이동')
            print('  3: MoveCircle - 원호 이동')
            print('  4: 그리퍼 제어 (0=열림 / 740=닫힘)')
            print('  5: MoveCircle 자동 (끝점만 입력)')
            print('  q: 종료')
            print('='*52)
            choice = input('선택: ').strip().lower()

            try:
                if choice == '0':
                    if self.get_current_pose() is None:
                        self.get_current_joints()
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '1':
                    raw = input('6개 관절 각도 입력 (예: 0 0 90 0 90 0): ')
                    vals = [float(x) for x in raw.split()]
                    ok, err = _validate_joints(vals)
                    if not ok:
                        print(f'[오류] {err}')
                    else:
                        dur_str = input('이동 시간(초, 기본=3.0): ').strip()
                        dur = float(dur_str) if dur_str else 3.0
                        ok2, err2 = _validate_duration(dur)
                        if not ok2:
                            print(f'[오류] {err2}')
                        else:
                            self.move_joint(vals, dur)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '2':
                    raw = input('목표 위치 입력 (X Y Z, 자세 유지): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) not in (3, 6):
                        print('3개 또는 6개 값을 입력해주세요.')
                    else:
                        ok, err = _validate_tcp(vals)
                        if not ok:
                            print(f'[오류] {err}')
                        else:
                            if len(vals) == 3:
                                pose = self.get_current_pose()
                                rx, ry, rz = (pose[3], pose[4], pose[5]) if pose else (0.0, 0.0, 0.0)
                                vals += [rx, ry, rz]
                            self.move_line(vals)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '3':
                    raw1 = input('경유점 입력 (X Y Z, 자세 유지): ')
                    raw2 = input('끝점 입력  (X Y Z, 자세 유지): ')
                    v1 = [float(x) for x in raw1.split()]
                    v2 = [float(x) for x in raw2.split()]
                    if len(v1) not in (3, 6) or len(v2) not in (3, 6):
                        print('각각 3개 또는 6개 값을 입력해주세요.')
                    else:
                        ok1, err1 = _validate_tcp(v1)
                        ok2, err2 = _validate_tcp(v2)
                        if not ok1:
                            print(f'[오류] 경유점 - {err1}')
                        elif not ok2:
                            print(f'[오류] 끝점 - {err2}')
                        else:
                            if len(v1) == 3:
                                pose = self.get_current_pose()
                                rx, ry, rz = (pose[3], pose[4], pose[5]) if pose else (0.0, 0.0, 0.0)
                                v1 += [rx, ry, rz]; v2 += [rx, ry, rz]
                            self.move_circle(v1, v2)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '4':
                    val = input('그리퍼 값 입력 (0~740): ')
                    ival = int(val)
                    if not (0 <= ival <= 740):
                        print(f'[오류] 그리퍼 범위 초과: {ival} (허용범위: 0 ~ 740)')
                    else:
                        self.set_gripper(ival)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '5':
                    raw = input('끝점 입력 (X Y Z): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) != 3:
                        print('X Y Z 3개 값을 입력해주세요.')
                    else:
                        ok, err = _validate_tcp(vals)
                        if not ok:
                            print(f'[오류] {err}')
                        else:
                            self.auto_circle(vals)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == 'q':
                    break

                else:
                    print('잘못된 입력입니다.')
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f'오류: {e}')
                input('엔터를 누르면 메뉴로 돌아갑니다...')


def main():
    rclpy.init()
    node = E0509GazeboController()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
