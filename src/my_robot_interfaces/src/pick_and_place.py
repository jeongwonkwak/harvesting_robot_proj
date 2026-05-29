import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from dsr_msgs2.srv import MoveJoint, MoveLine, Fkin
from std_msgs.msg import Int32
from sensor_msgs.msg import JointState
import math
import time


class PickAndPlaceNode(Node):
    GRIPPER_OPEN  = 0
    GRIPPER_CLOSE = 700

    # 픽앤플레이스 파라미터 (mm)
    OBJECT_POS  = [400.0,   0.0,   0.0]  # 물체 초기 위치 (바닥 Z=0)
    PLACE_POS   = [300.0, 200.0,   0.0]  # 놓을 목표 위치
    APPROACH_H  = 200.0                  # 접근/후퇴 Z 오프셋
    GRIP_OFFSET = 120.0                  # TCP 픽 높이 (그리퍼 끝이 물체에 닿는 TCP Z)
    ORIENT      = [45.0, 180.0, 45.0]   # TCP 자세 (RX RY RZ)

    def __init__(self):
        super().__init__('pick_and_place')

        self.marker_pub  = self.create_publisher(Marker, '/object_marker', 10)
        self.gripper_pub = self.create_publisher(Int32,  '/dsr01/gripper/position_cmd', 10)

        self.joint_client = self.create_client(MoveJoint, '/dsr01/motion/move_joint')
        self.line_client  = self.create_client(MoveLine,  '/dsr01/motion/move_line')
        self.fkin_client  = self.create_client(Fkin,      '/dsr01/motion/fkin')

        self.current_joints  = None
        self.object_pos      = list(self.OBJECT_POS)
        self.object_attached = False

        self.create_subscription(JointState, '/dsr01/joint_states', self._joint_cb, 10)

        self.get_logger().info('서비스 연결 대기 중...')
        for client, name in [
            (self.joint_client, 'MoveJoint'),
            (self.line_client,  'MoveLine'),
            (self.fkin_client,  'Fkin'),
        ]:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'{name} 대기 중...')

        self.create_timer(0.1, self._publish_marker)
        self.get_logger().info('준비 완료')

    # ── 콜백 ──────────────────────────────────────────────────────
    def _joint_cb(self, msg):
        idx   = {name: i for i, name in enumerate(msg.name)}
        order = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        self.current_joints = [math.degrees(msg.position[idx[n]]) for n in order]

    def _publish_marker(self):
        m = Marker()
        m.header.frame_id    = 'base_link'
        m.header.stamp       = self.get_clock().now().to_msg()
        m.ns                 = 'object'
        m.id                 = 0
        m.type               = Marker.CUBE
        m.action             = Marker.ADD
        m.pose.position.x    = self.object_pos[0] / 1000.0
        m.pose.position.y    = self.object_pos[1] / 1000.0
        m.pose.position.z    = self.object_pos[2] / 1000.0
        m.pose.orientation.w = 1.0
        m.scale.x = m.scale.y = m.scale.z = 0.05  # 50mm 큐브

        if self.object_attached:
            m.color.r, m.color.g, m.color.b = 0.0, 1.0, 0.0  # 초록: 파지 중
        else:
            m.color.r, m.color.g, m.color.b = 1.0, 0.5, 0.0  # 주황: 대기
        m.color.a = 1.0
        self.marker_pub.publish(m)

    # ── 유틸리티 ──────────────────────────────────────────────────
    def _get_tcp_pos(self):
        if self.current_joints is None:
            return None
        req     = Fkin.Request()
        req.pos = list(self.current_joints)
        req.ref = 0
        future  = self.fkin_client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.done() or future.result() is None:
            return None
        p = future.result().conv_posx
        return [float(p[0]), float(p[1]), float(p[2])]

    def _move_joint(self, angles, vel=20.0, acc=20.0):
        req      = MoveJoint.Request()
        req.pos  = [float(a) for a in angles]
        req.vel  = vel
        req.acc  = acc
        req.mode = 0
        future   = self.joint_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        ok = future.result().success if future.result() else False
        self.get_logger().info(f'MoveJoint {"완료" if ok else "실패"}')
        return ok

    def _move_line(self, xyz, orient=None, vel=None, acc=None):
        pos      = [float(v) for v in xyz] + [float(v) for v in (orient or self.ORIENT)]
        req      = MoveLine.Request()
        req.pos  = pos
        req.vel  = vel or [50.0, 20.0]
        req.acc  = acc or [100.0, 40.0]
        req.ref  = 0
        req.mode = 0
        future   = self.line_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        ok = future.result().success if future.result() else False
        self.get_logger().info(f'MoveLine {"완료" if ok else "실패"}: {[round(v,1) for v in xyz]}')
        return ok

    def _set_gripper(self, value, wait=1.2):
        msg      = Int32()
        msg.data = int(value)
        self.gripper_pub.publish(msg)
        time.sleep(wait)

    def _sync_object_to_tcp(self):
        tcp = self._get_tcp_pos()
        if tcp:
            self.object_pos = tcp

    # ── 메인 시퀀스 ───────────────────────────────────────────────
    def run(self):
        o  = self.OBJECT_POS
        pl = self.PLACE_POS
        h  = self.APPROACH_H
        g  = self.GRIP_OFFSET

        print('\n' + '='*45)
        print('  픽앤플레이스 시뮬레이션 시작')
        print(f'  물체 위치: X={o[0]}, Y={o[1]}, Z={o[2]}')
        print(f'  목표 위치: X={pl[0]}, Y={pl[1]}, Z={pl[2]}')
        print('='*45)

        # 1. 안전 자세
        print('\n[1/11] 안전 자세로 이동...')
        self._move_joint([0, 0, 90, 0, 90, 0])

        # 2. 그리퍼 열기
        print('[2/11] 그리퍼 열기...')
        self._set_gripper(self.GRIPPER_OPEN)

        # 3. 물체 위 접근
        print('[3/11] 물체 위로 접근...')
        self._move_line([o[0], o[1], o[2] + h])

        # 4. 물체로 하강 (TCP는 GRIP_OFFSET 높이까지만 내려옴)
        print('[4/11] 물체로 하강...')
        self._move_line([o[0], o[1], o[2] + g], vel=[30.0, 10.0], acc=[60.0, 20.0])

        # 5. 그리퍼 닫기 + 물체 부착
        print('[5/11] 그리퍼 닫기 (파지)...')
        self._set_gripper(self.GRIPPER_CLOSE)
        self.object_attached = True
        self._sync_object_to_tcp()

        # 6. 들어올리기
        print('[6/11] 물체 들어올리기...')
        self._move_line([o[0], o[1], o[2] + h])

        self._sync_object_to_tcp()

        # 7. 목표 위치 위로 이동
        print('[7/11] 목표 위치로 이동...')
        self._move_line([pl[0], pl[1], pl[2] + h])
        self._sync_object_to_tcp()

        # 8. 하강 (TCP는 GRIP_OFFSET 높이까지만)
        print('[8/11] 물체 내려놓기...')
        self._move_line([pl[0], pl[1], pl[2] + g], vel=[30.0, 10.0], acc=[60.0, 20.0])
        self._sync_object_to_tcp()

        # 9. 그리퍼 열기 + 분리
        print('[9/11] 그리퍼 열기 (릴리즈)...')
        self._set_gripper(self.GRIPPER_OPEN)
        self.object_attached = False
        self.object_pos = list(pl)  # 최종 위치에 고정

        # 10. 후퇴
        print('[10/11] 후퇴...')
        self._move_line([pl[0], pl[1], pl[2] + h])

        # 11. 안전 자세 복귀
        print('[11/11] 안전 자세 복귀...')
        self._move_joint([0, 0, 90, 0, 90, 0])

        print('\n' + '='*45)
        print('  픽앤플레이스 완료!')
        print(f'  물체 이동: {o[:2]} → {pl[:2]} (mm)')
        print('='*45)


def main():
    rclpy.init()
    node = PickAndPlaceNode()

    print('\n[RViz 설정 안내]')
    print('  1. RViz 좌측 Add 버튼 클릭')
    print('  2. By topic → /object_marker → Marker 선택')
    print('  3. Fixed Frame을 "base_link" 로 설정')
    print()
    input('RViz 준비 완료 후 엔터를 누르면 시작합니다...')

    try:
        node.run()
        input('\n엔터를 누르면 종료합니다...')
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
