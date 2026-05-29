import rclpy
from rclpy.node import Node
from dsr_msgs2.srv import MoveJoint, MoveLine, MoveCircle, Fkin
from std_msgs.msg import Int32, Float64MultiArray
from sensor_msgs.msg import JointState
import math
import os
import time


class E0509RobotController(Node):
    GRIPPER_OPEN  = 0
    GRIPPER_CLOSE = 700

    def __init__(self):
        super().__init__('e0509_robot_controller')

        # 서비스 클라이언트
        self.joint_client  = self.create_client(MoveJoint, '/dsr01/motion/move_joint')
        self.line_client   = self.create_client(MoveLine,  '/dsr01/motion/move_line')
        self.circle_client = self.create_client(MoveCircle,'/dsr01/motion/move_circle')
        self.fkin_client   = self.create_client(Fkin,      '/dsr01/motion/fkin')

        # 그리퍼 퍼블리셔
        self.gripper_pub = self.create_publisher(Int32, '/dsr01/gripper/position_cmd', 10)

        # 관절 상태 구독
        self.current_joints = None
        self.create_subscription(JointState, '/dsr01/joint_states', self._joint_cb, 10)

        self.get_logger().info('서비스 연결 대기 중...')
        for client, name in [
            (self.joint_client,  'MoveJoint'),
            (self.line_client,   'MoveLine'),
            (self.circle_client, 'MoveCircle'),
            (self.fkin_client,   'Fkin'),
        ]:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'{name} 서비스 대기 중...')
        self.get_logger().info('모든 서비스 연결 완료')
        self.last_pose = None
        self.last_orientation = [0.0, 0.0, 0.0]  # 마지막 사용한 RX RY RZ

    def _joint_cb(self, msg):
        # 토픽 순서: joint_1,2,4,5,3,6 → J1,J2,J3,J4,J5,J6 로 정렬
        idx = {name: i for i, name in enumerate(msg.name)}
        order = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        self.current_joints = [math.degrees(msg.position[idx[n]]) for n in order]

    # ── MoveJoint ──────────────────────────────────────────────
    def move_joint(self, angles, vel=20.0, acc=20.0):
        """관절 각도로 이동 (절대값, 단위: 도)"""
        req = MoveJoint.Request()
        req.pos  = [float(a) for a in angles]
        req.vel  = vel
        req.acc  = acc
        req.mode = 0  # ABSOLUTE
        future = self.joint_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        success = future.result().success if future.result() else False
        self.get_logger().info(f'MoveJoint {"완료" if success else "실패"}: {angles}')
        return success

    # ── MoveLine ───────────────────────────────────────────────
    def move_line(self, pos, vel=None, acc=None):
        """직선 이동 (XYZ + RX RY RZ, 절대값)"""
        req = MoveLine.Request()
        req.pos  = [float(p) for p in pos]
        req.vel  = vel if vel else [100.0, 30.0]
        req.acc  = acc if acc else [200.0, 60.0]
        req.ref  = 0  # DR_BASE
        req.mode = 0  # ABSOLUTE
        future = self.line_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        success = future.result().success if future.result() else False
        self.get_logger().info(f'MoveLine {"완료" if success else "실패"}: {pos}')
        return success

    # ── MoveCircle ─────────────────────────────────────────────
    def move_circle(self, via_pos, end_pos, vel=None, acc=None):
        """원호 이동 (경유점 + 끝점, 각각 XYZ + RX RY RZ)"""
        req = MoveCircle.Request()
        p1 = Float64MultiArray()
        p1.data = [float(v) for v in via_pos]
        p2 = Float64MultiArray()
        p2.data = [float(v) for v in end_pos]
        req.pos  = [p1, p2]
        req.vel  = vel if vel else [100.0, 30.0]
        req.acc  = acc if acc else [200.0, 60.0]
        req.ref  = 0  # DR_BASE
        req.mode = 0  # ABSOLUTE

        print(f'[MoveCircle] 경유점: {via_pos}')
        print(f'[MoveCircle] 끝점:   {end_pos}')
        print(f'[MoveCircle] vel={req.vel}, acc={req.acc}, ref={req.ref}, mode={req.mode}')

        future = self.circle_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)

        if not future.done():
            print('[MoveCircle] 타임아웃: 서비스 응답 없음 (10초 초과)')
            return False

        result = future.result()
        if result is None:
            print('[MoveCircle] 실패: 서비스 결과가 None')
            return False

        if result.success:
            print('[MoveCircle] 완료')
        else:
            print('[MoveCircle] 실패: 서비스가 요청을 거부함')
            print('  → 좌표가 로봇 작업 범위를 벗어났거나 경유점/끝점이 일직선일 수 있음')

        return result.success

    # ── 현재 위치 확인 ────────────────────────────────────────────
    def get_current_pose(self):
        # joint_states 수신을 Future로 대기
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

        msg = joint_future.result()
        idx = {name: i for i, name in enumerate(msg.name)}
        order = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        joints = [float(math.degrees(msg.position[idx[n]])) for n in order]
        print(f'현재 관절 각도: {[round(j,2) for j in joints]}')

        req = Fkin.Request()
        req.pos = joints
        req.ref = 0
        future = self.fkin_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.done() or future.result() is None:
            if self.last_pose is not None:
                print('[현재 위치] Fkin 실패 → 마지막 저장 위치 사용')
                print(f'  X={self.last_pose[0]:.2f}  Y={self.last_pose[1]:.2f}  Z={self.last_pose[2]:.2f}')
                print(f'  RX={self.last_pose[3]:.2f}  RY={self.last_pose[4]:.2f}  RZ={self.last_pose[5]:.2f}')
                return self.last_pose
            print('[현재 위치] Fkin 실패 (저장된 위치 없음)')
            return None

        pos = future.result().conv_posx
        self.last_pose = pos
        print(f'\n현재 TCP 위치:')
        print(f'  X={pos[0]:.2f}  Y={pos[1]:.2f}  Z={pos[2]:.2f}')
        print(f'  RX={pos[3]:.2f}  RY={pos[4]:.2f}  RZ={pos[5]:.2f}')
        return pos

    # ── 자동 원호 이동 (끝점만 입력) ──────────────────────────────
    def auto_circle(self, end_xyz):
        pose = self.get_current_pose()
        if pose is None:
            return False

        start = pose[:3]
        rx, ry, rz = pose[3], pose[4], pose[5]

        # 중간점 계산
        mid = [(s + e) / 2 for s, e in zip(start, end_xyz)]

        # 시작→끝 방향벡터
        d = [e - s for s, e in zip(start, end_xyz)]
        length = math.sqrt(sum(v ** 2 for v in d))

        if length < 1.0:
            print('시작점과 끝점이 너무 가까워요.')
            return False

        # XY 평면에서 수직 방향 계산
        perp = [-d[1], d[0], 0.0]
        perp_len = math.sqrt(perp[0] ** 2 + perp[1] ** 2)
        if perp_len < 0.001:  # Z축 방향 이동이면 X방향으로 오프셋
            perp = [1.0, 0.0, 0.0]
            perp_len = 1.0

        # 반지름 = 거리의 절반 (반원)
        radius = length / 2
        perp = [v / perp_len * radius for v in perp]

        via = [float(m + p) for m, p in zip(mid, perp)]
        via_full = via + [float(rx), float(ry), float(rz)]
        end_full = [float(v) for v in end_xyz] + [float(rx), float(ry), float(rz)]

        print(f'자동 계산 경유점: {[round(v, 2) for v in via[:3]]}')
        return self.move_circle(via_full, end_full)

    # ── Gripper ────────────────────────────────────────────────
    def set_gripper(self, value):
        """그리퍼 위치 설정 (0=열림, 700=닫힘)"""
        msg = Int32()
        msg.data = int(max(self.GRIPPER_OPEN, min(value, self.GRIPPER_CLOSE)))
        self.gripper_pub.publish(msg)
        self.get_logger().info(f'그리퍼 명령: {msg.data}')

    def open_gripper(self):
        self.set_gripper(self.GRIPPER_OPEN)

    def close_gripper(self):
        self.set_gripper(self.GRIPPER_CLOSE)

    # ── 메뉴 ───────────────────────────────────────────────────
    def run(self):
        while True:
            os.system('clear')
            print('='*45)
            print('   E0509 통합 로봇 제어')
            print('='*45)
            print('  0: 현재 TCP 위치 확인')
            print('  1: MoveJoint  - 관절 각도 이동')
            print('  2: MoveLine   - 직선 이동')
            print('  3: MoveCircle - 원호 이동')
            print('  4: 그리퍼 제어 (0=열림 / 700=닫힘 / 중간값 가능)')
            print('  5: MoveCircle 자동 (끝점 X Y Z만 입력)')
            print('  q: 종료')
            print('='*45)
            choice = input('선택: ').strip().lower()

            try:
                if choice == '0':
                    self.get_current_pose()
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '1':
                    raw = input('6개 관절 각도 입력 (예: 0 0 90 0 90 0): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) != 6:
                        print('6개 값을 입력해주세요.')
                    else:
                        self.move_joint(vals)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '2':
                    raw = input('목표 위치 입력 (X Y Z, 자세 유지): ')
                    vals = [float(x) for x in raw.split()]
                    if len(vals) not in (3, 6):
                        print('3개 또는 6개 값을 입력해주세요.')
                    else:
                        if len(vals) == 3:
                            pose = self.get_current_pose()
                            rx, ry, rz = (pose[3], pose[4], pose[5]) if pose is not None else (0.0, 0.0, 0.0)
                            vals += [rx, ry, rz]
                        self.move_line(vals)
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

                elif choice == '3':
                    raw1 = input('경유점 입력 (X Y Z, 자세 유지): ')
                    raw2 = input('끝점 입력  (X Y Z, 자세 유지): ')
                    vals1 = [float(x) for x in raw1.split()]
                    vals2 = [float(x) for x in raw2.split()]
                    if len(vals1) not in (3, 6) or len(vals2) not in (3, 6):
                        print('각각 3개 또는 6개 값을 입력해주세요.')
                    else:
                        if len(vals1) == 3:
                            pose = self.get_current_pose()
                            rx, ry, rz = (pose[3], pose[4], pose[5]) if pose is not None else (0.0, 0.0, 0.0)
                            vals1 += [rx, ry, rz]
                            vals2 += [rx, ry, rz]
                        self.move_circle(vals1, vals2)
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
                    print('잘못된 입력입니다. 0~5 또는 q를 선택하세요.')
                    input('엔터를 누르면 메뉴로 돌아갑니다...')

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f'오류 발생: {e}')
                input('엔터를 누르면 메뉴로 돌아갑니다...')

            time.sleep(0.3)


def main():
    rclpy.init()
    node = E0509RobotController()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
