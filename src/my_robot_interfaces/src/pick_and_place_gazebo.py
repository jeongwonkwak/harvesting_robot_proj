import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray, Int32
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker
from builtin_interfaces.msg import Duration
import math
import time

JOINT_NAMES    = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
GRIPPER_JOINTS = ['gripper_rh_r1', 'gripper_rh_r2', 'gripper_rh_l1', 'gripper_rh_l2']


class PickAndPlaceGazeboNode(Node):
    GRIPPER_OPEN  = 0
    GRIPPER_CLOSE = 700

    # ── 관절 웨이포인트 (도 단위) ─────────────────────────────────
    # 아래 값들은 실제 로봇/시뮬레이터에서 직접 측정 후 교체 필요
    # robot_move3_gazebo.py 옵션 0으로 관절값 확인 → 여기 입력
    SAFE_JOINTS          = [  0.0,   0.0,  90.0,  0.0,  90.0,  0.0]
    PICK_APPROACH_JOINTS = [  0.0, -20.0,  80.0,  0.0, 110.0,  0.0]  # 물체 위 접근
    PICK_JOINTS          = [  0.0, -30.0,  85.0,  0.0, 115.0,  0.0]  # 물체 픽업 위치
    PLACE_APPROACH_JOINTS= [ 45.0, -20.0,  80.0,  0.0, 110.0,  0.0]  # 목표 위 접근
    PLACE_JOINTS         = [ 45.0, -30.0,  85.0,  0.0, 115.0,  0.0]  # 물체 놓는 위치

    # ── Marker 파라미터 (시각화용, mm) ───────────────────────────
    OBJECT_POS = [400.0,   0.0,   0.0]
    PLACE_POS  = [300.0, 200.0,   0.0]

    def __init__(self):
        super().__init__('pick_and_place_gazebo')

        self.joint_pub = self.create_publisher(
            JointTrajectory,
            '/dsr01/joint_trajectory_controller/joint_trajectory',
            10
        )
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
        self.marker_pub = self.create_publisher(Marker, '/object_marker', 10)

        self.current_joints  = None
        self.object_pos      = list(self.OBJECT_POS)
        self.object_attached = False

        self.create_subscription(JointState, '/dsr01/joint_states', self._joint_cb, 10)
        self.create_timer(0.1, self._publish_marker)

        self.get_logger().info('Gazebo 픽앤플레이스 준비 완료')

    # ── 콜백 ─────────────────────────────────────────────────────
    def _joint_cb(self, msg):
        idx = {name: i for i, name in enumerate(msg.name)}
        self.current_joints = {
            name: math.degrees(msg.position[idx[name]])
            for name in JOINT_NAMES if name in idx
        }

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
        m.scale.x = m.scale.y = m.scale.z = 0.05
        if self.object_attached:
            m.color.r, m.color.g, m.color.b = 0.0, 1.0, 0.0
        else:
            m.color.r, m.color.g, m.color.b = 1.0, 0.5, 0.0
        m.color.a = 1.0
        self.marker_pub.publish(m)

    # ── 이동 유틸리티 ─────────────────────────────────────────────
    def _move_joint(self, angles_deg, duration_sec=3.0):
        traj = JointTrajectory()
        traj.joint_names = JOINT_NAMES

        pt = JointTrajectoryPoint()
        pt.positions = [math.radians(a) for a in angles_deg]
        secs = int(duration_sec)
        pt.time_from_start = Duration(sec=secs, nanosec=int((duration_sec - secs) * 1e9))

        traj.points = [pt]
        self.joint_pub.publish(traj)
        self.get_logger().info(f'MoveJoint: {[round(a,1) for a in angles_deg]}')

        self._wait_joints(angles_deg, timeout=duration_sec + 2.0)

    def _wait_joints(self, target_deg, timeout=10.0, tol=1.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.current_joints is None:
                continue
            errors = [
                abs(self.current_joints.get(JOINT_NAMES[i], 0.0) - target_deg[i])
                for i in range(6)
            ]
            if all(e < tol for e in errors):
                return
        self.get_logger().warn('관절 이동 타임아웃')

    def _set_gripper(self, value_0_700, wait=1.2):
        value_0_700 = max(0, min(700, int(value_0_700)))
        # Int32로 gripper_service_node에 전달 (real 모드 대응)
        int_msg = Int32()
        int_msg.data = value_0_700
        self.gripper_real_pub.publish(int_msg)
        # Gazebo 단독 모드 대응 (Float64MultiArray 병행 발행)
        rad = float(value_0_700) / 700.0
        gz_msg = Float64MultiArray()
        gz_msg.data = [rad] * 4
        self.gripper_gz_pub.publish(gz_msg)
        time.sleep(wait)

    def _move_marker_to_joints(self):
        """현재 관절 기준 Marker 위치 업데이트 (간이 추정)"""
        # Gazebo에서는 TF2로 정확한 TCP 위치를 얻을 수 있지만
        # 여기서는 파지/놓기 시점에만 위치를 수동 갱신
        pass

    # ── 픽앤플레이스 시퀀스 ───────────────────────────────────────
    def run(self):
        print('\n' + '='*50)
        print('  Gazebo 픽앤플레이스 시뮬레이션')
        print('  ※ 관절 웨이포인트를 먼저 교정하세요')
        print('     (robot_move3_gazebo.py 옵션 0으로 확인)')
        print('='*50)
        input('\n준비되면 엔터...')

        steps = [
            ('[1/11] 안전 자세',         lambda: self._move_joint(self.SAFE_JOINTS)),
            ('[2/11] 그리퍼 열기',       lambda: self._set_gripper(self.GRIPPER_OPEN)),
            ('[3/11] 물체 위 접근',      lambda: self._move_joint(self.PICK_APPROACH_JOINTS)),
            ('[4/11] 물체로 하강',       lambda: self._move_joint(self.PICK_JOINTS, duration_sec=2.0)),
            ('[5/11] 그리퍼 닫기',       lambda: (self._set_gripper(self.GRIPPER_CLOSE),
                                                   setattr(self, 'object_attached', True),
                                                   setattr(self, 'object_pos', list(self.PLACE_POS)))),
            ('[6/11] 들어올리기',        lambda: self._move_joint(self.PICK_APPROACH_JOINTS)),
            ('[7/11] 목표 위치로 이동',  lambda: self._move_joint(self.PLACE_APPROACH_JOINTS)),
            ('[8/11] 물체 내려놓기',     lambda: self._move_joint(self.PLACE_JOINTS, duration_sec=2.0)),
            ('[9/11] 그리퍼 열기',       lambda: (self._set_gripper(self.GRIPPER_OPEN),
                                                   setattr(self, 'object_attached', False))),
            ('[10/11] 후퇴',             lambda: self._move_joint(self.PLACE_APPROACH_JOINTS)),
            ('[11/11] 안전 자세 복귀',   lambda: self._move_joint(self.SAFE_JOINTS)),
        ]

        for name, fn in steps:
            print(f'\n{name}')
            fn()

        print('\n' + '='*50)
        print('  픽앤플레이스 완료!')
        print('='*50)


def main():
    rclpy.init()
    node = PickAndPlaceGazeboNode()

    print('\n[RViz 설정 안내]')
    print('  Add → By topic → /object_marker → Marker')
    print('  Fixed Frame: base_link')

    try:
        node.run()
        input('\n엔터를 누르면 종료...')
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
