import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class IntelligentTurtleNode(Node): #반드시 node를 상속받아야 한다 
    def __init__(self):
        # 1. 노드 이름 초기화
        super().__init__('intelligent_turtle_node')
        
        # 2. 퍼블리셔 설정: 거북이에게 속도 명령 전달 (/turtle1/cmd_vel)
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # 3. 서브스크라이버 설정: 거북이의 현재 위치 수신 (/turtle1/pose)
        self.subscriber = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # 4. 타이머 설정: 0.5초마다 주기적인 행동 수행
        self.timer = self.create_timer(0.5, self.timer_callback)
        
        # 내부 상태 변수
        self.current_pose = None
        self.get_logger().info('객체지향 거북이 노드가 시작되었습니다.')

    def pose_callback(self, msg):
        """서브스크라이버 콜백: 실시간 위치 데이터를 self에 저장"""
        self.current_pose = msg
        # self.get_logger().info(f'현재 위치: x={msg.x:.2f}, y={msg.y:.2f}')

    def timer_callback(self):
        """타이머 콜백: 로직 판단 후 명령 발행"""
        if self.current_pose is None:
            return

        msg = Twist()
        # 간단한 로직: 화면 중앙을 벗어나면 회전, 아니면 직진
        if self.current_pose.x > 8.0 or self.current_pose.x < 3.0:
            msg.linear.x = 1.0
            msg.angular.z = 1.5
        else:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    # 노드 인스턴스 생성
    node = IntelligentTurtleNode()
    try:
        # 이벤트 루프 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('사용자에 의해 종료되었습니다.')
    finally:
        # 자원 해제
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()