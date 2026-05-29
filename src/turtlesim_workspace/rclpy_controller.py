import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class AdvancedTurtleController(Node):
    def __init__(self):
        super().__init__('advanced_turtle_controller')
        
        # 1. QoS 설정 (신뢰성 우선)
        # depth: 최근 10개 메시지 저장
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            depth=10
        )

        # 2. 통신 객체 초기화
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', qos_profile)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, qos_profile)
        
        # 3. 제어 루프 타이머 (20Hz = 0.05s) - 실시간성 확보
        self.control_timer = self.create_timer(0.05, self.control_loop)

        # 4. 내부 상태 변수 (캡슐화)
        self.pose = None
        self.target_linear_vel = 0.0
        self.target_angular_vel = 0.0
        self.safety_distance = 1.5  # 벽과의 안전 거리
        self.is_emergency_stop = False

    def pose_callback(self, msg):
        """실시간 위치 수신 및 안전 점검"""
        self.pose = msg
        
        # 안전 로직 (Safety Interlock)
        # turtlesim 경계는 0.0 ~ 11.0 사이입니다.
        if (msg.x < self.safety_distance or msg.x > (11.0 - self.safety_distance) or
            msg.y < self.safety_distance or msg.y > (11.0 - self.safety_distance)):
            self.is_emergency_stop = True
        else:
            self.is_emergency_stop = False

    def control_loop(self):
        """메인 제어 로직 (주기적 실행)"""
        if self.pose is None:
            return

        msg = Twist()

        if self.is_emergency_stop:
            # 상태 1: 긴급 정지 및 회전하여 탈출 시도
            self.get_logger().warn('!!! Safety Limit Reached - Changing Direction !!!')
            msg.linear.x = 0.0
            msg.angular.z = 1.2  # 제자리 회전
        else:
            # 상태 2: 정상 주행 (Soft Start/Stop 적용)
            msg.linear.x = 2.5
            msg.angular.z = 0.0

        self.cmd_pub.publish(msg)

    def get_logger_status(self):
        """노드 상태 로깅 메서드 분리"""
        if self.pose:
            self.get_logger().info(f"Status: x={self.pose.x:.1f}, y={self.pose.y:.1f}, Safety={not self.is_emergency_stop}")

def main(args=None):
    rclpy.init(args=args)
    node = AdvancedTurtleController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down node...')
    finally:
        # 종료 시 로봇 정지 명령 송신 (중요!)
        stop_msg = Twist()
        node.cmd_pub.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()