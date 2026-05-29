import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class MonitoringNode(Node):
    def __init__(self):
        super().__init__('monitoring_node')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.timer = self.create_timer(0.5, self.diag_loop)
        
        self.curr_pose = None
        self.get_logger().info('모니터링 노드가 활성화되었습니다. rqt_graph를 켜서 확인하세요.')

    def pose_callback(self, msg):
        self.curr_pose = msg

    def diag_loop(self):
        """자가 진단 및 상태 보고 루프"""
        if self.curr_pose is None:
            self.get_logger().error('데이터 수신 불가: turtlesim 노드가 켜져 있습니까?')
            return

        # 런타임 데이터 로깅 (4단계 핵심)
        self.get_logger().info(f'현재 좌표: ({self.curr_pose.x:.2f}, {self.curr_pose.y:.2f})')
        
        # 특정 상황 검증
        if self.curr_pose.x > 10.0 or self.curr_pose.x < 1.0:
            self.get_logger().fatal('임계 구역 이탈! 즉시 점검 필요.')

def main():
    rclpy.init()
    node = MonitoringNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().warn('사용자에 의해 중단됨.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()