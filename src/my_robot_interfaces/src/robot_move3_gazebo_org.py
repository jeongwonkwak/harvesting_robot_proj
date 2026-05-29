import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray, Int32
from dsr_msgs2.srv import MoveJoint, MoveLine, MoveCircle, Fkin
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Duration
import math
import os
import time


JOINT_NAMES = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']


class E0509GazeboController(Node):
    GRIPPER_OPEN  = 0.0
    GRIPPER_CLOSE = 1.0

    def __init__(self):
        super().__init__('e0509_gazebo_controller')

        # ── JointTrajectoryController (MoveJoint용) ───────────────
        self.joint_pub = self.create_publisher(
            JointTrajectory,
            '/dsr01/joint_trajectory_controller/joint_trajectory',
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
            '/dsr01/gripper_controller/commands',
            10
        )

        # ── Doosan 서비스 (MoveJoint / MoveLine / MoveCircle / Fkin) ──
        # bringup_real_gazebo.launch.py 사용 시 활성화됨
        self.joint_svc_client  = self.create_client(MoveJoint, '/dsr01/motion/move_joint')
        self.line_client       = self.create_client(MoveLine,  '/dsr01/motion/move_line')
        self.circle_client     = self.create_client(MoveCircle,'/dsr01/motion/move_circle')
        self.fkin_client       = self.create_client(Fkin,      '/dsr01/motion/fkin')

        # ── 관절 상태 ─────────────────────────────────────────────
        self.current_joints = None
        self.last_pose      = None
        self.create_subscription(JointState, '/dsr01/joint_states', self._joint_cb, 10)

        # Doosan 서비스 가용 여부 확인 (1초 내 응답 없으면 미지원)
        self._doosan_available = self._check_doosan_services()

        self.get_logger().info('Gazebo 컨트롤러 준비 완료')
        if not self._doosan_available:
            self.get_logger().warn(
                'MoveLine/MoveCircle 비활성 — '
                'bringup_real_gazebo.launch.py mode:=virtual 사용 시 활성화됩니다.'
            )

    def _check_doosan_services(self):
        return (
            self.joint_svc_client.wait_for_service(timeout_sec=1.0) and
            self.line_client.wait_for_service(timeout_sec=1.0) and
            self.circle_client.wait_for_service(timeout_sec=1.0) and
            self.fkin_client.wait_for_service(timeout_sec=1.0)
        )

    # ── 콜백 ─────────────────────────────────────────────────────
    def _joint_cb(self, msg):
        idx = {name: i for i, name in enumerate(msg.name)}
        self.current_joints = {
            name: math.degrees(msg.position[idx[name]])
            for name in JOINT_NAMES if name in idx
        }

    # ── MoveJoint ─────────────────────────────────────────────────
    def move_joint(self, angles_deg, duration_sec=3.0):
        self.get_logger().info(f'MoveJoint: {[round(a,1) for a in angles_deg]}')
        if self._doosan_available:
            return self._move_joint_doosan(angles_deg, duration_sec)
        else:
            return self._move_joint_traj(angles_deg, duration_sec)

    def _move_joint_doosan(self, angles_deg, duration_sec=3.0):
        req = MoveJoint.Request()
        req.pos       = [float(a) for a in angles_deg]
        req.vel       = 60.0
        req.acc       = 60.0
        req.time      = float(duration_sec)
        req.mode      = 0
        req.blend_type = 0
        req.sync_type  = 0
        future = self.joint_svc_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=duration_sec + 5.0)
        ok = future.result().success if future.result() else False
        self.get_logger().info(f'MoveJoint(Doosan) {"완료" if ok else "실패"}')
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
        self._wait_for_joints(angles_deg, timeout=duration_sec + 2.0)
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
        if not self._doosan_available:
            print('[MoveLine] Doosan 서비스 없음 → bringup_real_gazebo.launch.py mode:=virtual 필요')
            return False
        req      = MoveLine.Request()
        req.pos  = [float(p) for p in pos]
        req.vel  = vel or [100.0, 30.0]
        req.acc  = acc or [200.0, 60.0]
        req.ref  = 0
        req.mode = 0
        future   = self.line_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        ok = future.result().success if future.result() else False
        self.get_logger().info(f'MoveLine {"완료" if ok else "실패"}: {pos}')
        return ok

    # ── MoveCircle (Doosan 서비스) ────────────────────────────────
    def move_circle(self, via_pos, end_pos, vel=None, acc=None):
        if not self._doosan_available:
            print('[MoveCircle] Doosan 서비스 없음 → bringup_real_gazebo.launch.py mode:=virtual 필요')
            return False
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
        if not future.done():
            print('[MoveCircle] 타임아웃')
            return False
        result = future.result()
        if result is None:
            print('[MoveCircle] 실패: None')
            return False
        print(f'[MoveCircle] {"완료" if result.success else "실패"}')
        return result.success

    # ── 현재 TCP 위치 (Fkin) ──────────────────────────────────────
    def get_current_pose(self):
        joint_future = rclpy.Future()
        def _cb(msg):
            if not joint_future.done():
                joint_future.set_result(msg)
        sub = self.create_subscription(JointState, '/dsr01/joint_states', _cb, 10)
        rclpy.spin_until_future_complete(self, joint_future, timeout_sec=3.0)
        self.destroy_subscription(sub)
        if not joint_future.done():
            print('[현재 위치] joint_states 수신 실패')
            return None
        msg   = joint_future.result()
        idx   = {name: i for i, name in enumerate(msg.name)}
        order = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        joints = [float(math.degrees(msg.position[idx[n]])) for n in order]
        print(f'현재 관절 각도: {[round(j,2) for j in joints]}')
        if not self._doosan_available:
            print('[현재 위치] Fkin 서비스 없음 (관절값만 표시)')
            return None
        req     = Fkin.Request()
        req.pos = joints
        req.ref = 0
        future  = self.fkin_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.done() or future.result() is None:
            if self.last_pose is not None:
                print('[현재 위치] Fkin 실패 → 마지막 저장 위치 사용')
                return self.last_pose
            return None
        pos = future.result().conv_posx
        self.last_pose = pos
        print(f'\n현재 TCP 위치:')
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
    def set_gripper(self, value_0_700, wait=1.2):
        value_0_700 = max(0, min(700, int(value_0_700)))
        if self._doosan_available:
            # 모드 B: real 그리퍼 → gripper_service_node (gazebo_bridge가 Gazebo로 미러링)
            msg = Int32()
            msg.data = value_0_700
            self.gripper_real_pub.publish(msg)
            self.get_logger().info(f'그리퍼(실제): {value_0_700}')
        else:
            # 모드 A: Gazebo 그리퍼 controller 직접 제어
            rad = float(value_0_700) / 700.0 * self.GRIPPER_CLOSE
            rad = max(self.GRIPPER_OPEN, min(rad, self.GRIPPER_CLOSE))
            msg = Float64MultiArray()
            msg.data = [rad] * 4
            self.gripper_gz_pub.publish(msg)
            self.get_logger().info(f'그리퍼(Gazebo): {value_0_700} (→ {rad:.3f} rad)')
        time.sleep(wait)

    def open_gripper(self):  self.set_gripper(0)
    def close_gripper(self): self.set_gripper(700)

    # ── 현재 관절 확인 ────────────────────────────────────────────
    def get_current_joints(self):
        rclpy.spin_once(self, timeout_sec=1.0)
        if self.current_joints is None:
            print('[현재 관절] joint_states 수신 실패')
            return None
        vals = [self.current_joints.get(n, 0.0) for n in JOINT_NAMES]
        print(f'현재 관절 각도: {[round(v,2) for v in vals]}')
        return vals

    # ── 메뉴 ─────────────────────────────────────────────────────
    def run(self):
        doosan_note = '' if self._doosan_available else ' [비활성 - real_gazebo launch 필요]'
        while True:
            os.system('clear')
            print('='*52)
            print('   E0509 Gazebo 로봇 제어')
            print('='*52)
            print('  0: 현재 위치 확인 (관절 + TCP)')
            print('  1: MoveJoint  - 관절 각도 이동')
            print(f'  2: MoveLine   - 직선 이동{doosan_note}')
            print(f'  3: MoveCircle - 원호 이동{doosan_note}')
            print('  4: 그리퍼 제어 (0=열림 / 700=닫힘)')
            print(f'  5: MoveCircle 자동 (끝점만 입력){doosan_note}')
            print('  q: 종료')
            print('='*52)
            choice = input('선택: ').strip().lower()

            try:
                if choice == '0':
                    self.get_current_pose() or self.get_current_joints()
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '1':
                    raw = input('6개 관절 각도 입력 (예: 0 0 90 0 90 0): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) != 6:
                        print('6개 값을 입력해주세요.')
                    else:
                        dur = input('이동 시간(초, 기본=3.0): ').strip()
                        self.move_joint(vals, float(dur) if dur else 3.0)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '2':
                    raw = input('목표 위치 입력 (X Y Z, 자세 유지): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) not in (3, 6):
                        print('3개 또는 6개 값을 입력해주세요.')
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
                        if len(v1) == 3:
                            pose = self.get_current_pose()
                            rx, ry, rz = (pose[3], pose[4], pose[5]) if pose else (0.0, 0.0, 0.0)
                            v1 += [rx, ry, rz]; v2 += [rx, ry, rz]
                        self.move_circle(v1, v2)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '4':
                    val = input('그리퍼 값 입력 (0~700): ')
                    self.set_gripper(int(val))
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '5':
                    raw = input('끝점 입력 (X Y Z): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) != 3:
                        print('X Y Z 3개 값을 입력해주세요.')
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
