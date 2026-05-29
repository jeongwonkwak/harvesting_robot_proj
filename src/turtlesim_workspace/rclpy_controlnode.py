import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class SafetyControlNode(Node):
    def __init__(self):
        super().__init__('safety_control_node')
        
        # 1. 인터페이스 정의
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # 2. 제어 주기 설정 (10Hz = 0.1초 마다 실행)
        self.timer = self.create_timer(0.1, self.control_loop)

        # 3. 상태 변수 (캡슐화)
        self.current_pose = None
        self.is_danger = False  # 안전 상태 플래그
        self.safety_boundary = 2.0 # 벽과의 경계 거리
        
        self.get_logger().info('안전 제어 로직이 활성화되었습니다.')

    def pose_callback(self, msg):
        """
        [Sense] 실시간으로 데이터를 수신하고 상황을 판단함
        이 콜백은 데이터가 들어올 때마다 비동기적으로 실행됨
        """
        self.current_pose = msg
        
        # 벽에 너무 가까운지 판단 (Logic Layer)
        if (msg.x < self.safety_boundary or msg.x > (11.0 - self.safety_boundary) or
            msg.y < self.safety_boundary or msg.y > (11.0 - self.safety_boundary)):
            if not self.is_danger:
                self.get_logger().warn('!!! 위험 구역 진입 !!!')
            self.is_danger = True
        else:
            self.is_danger = False

    def control_loop(self):
        """
        [Think & Act] 결정된 상태에 따라 실제 명령을 발행함
        이 루프는 정해진 주기(0.1초)마다 동기적으로 실행됨
        """
        if self.current_pose is None:
            return

        msg = Twist()

        if self.is_danger:
            # 상태 1: 위험 상황 - 제자리 회전하여 탈출 시도
            msg.linear.x = 0.0
            msg.angular.z = 1.5
        else:
            # 상태 2: 안전 상황 - 전진 주행
            msg.linear.x = 2.0
            msg.angular.z = 0.0

        self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SafetyControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 종료 시 로봇을 멈추는 명령 발행 (Best Practice)
        stop_msg = Twist()
        node.cmd_pub.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
