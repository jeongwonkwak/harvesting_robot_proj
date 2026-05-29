import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class BoundaryGuard(Node):
    def __init__(self):
        super().__init__('boundary_guard')
        # 발행자: 회피 명령 전달
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 구독자: 현재 위치 실시간 모니터링
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.get_logger().info('벽 충돌 방지 노드가 시작되었습니다.')

    def pose_callback(self, msg):
        twist = Twist()
        
        # 터틀심 맵 크기: 0.0 ~ 11.0
        # 안전 구역 설정 (상하좌우 벽으로부터 1.5 유닛 안쪽)
        safe_min = 1.5
        safe_max = 9.5

        # 1. 경계 검사 (Wall Detection)
        if msg.x > safe_max or msg.x < safe_min or msg.y > safe_max or msg.y < safe_min:
            self.get_logger().warn(f'위험 감지! 현재 위치: ({msg.x:.2f}, {msg.y:.2f})')
            
            # 2. 회피 기동 (Avoidance Maneuver)
            # 벽에 가까워지면 뒤로 살짝 빼면서 급회전합니다.
            twist.linear.x = -0.5  # 후진
            twist.angular.z = 1.2  # 회전
        else:
            # 3. 안전 구역일 때 (Normal Cruise)
            # 평소에는 앞으로 전진하며 순찰합니다.
            twist.linear.x = 2.0
            twist.angular.z = 0.5  # 큰 원을 그리며 이동

        self.pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = BoundaryGuard()
    
    try:
        # 실시간 모니터링을 위해 무한 루프 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('사용자에 의해 종료되었습니다.')
    finally:
        # 종료 시 로봇 정지 명령 발행
        stop_msg = Twist()
        node.pub.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()