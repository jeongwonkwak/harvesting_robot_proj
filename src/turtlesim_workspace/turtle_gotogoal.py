#nano turtle_gotogoal.py 

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')
        # 발행자: 거북이에게 속도 명령 전달
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 구독자: 거북이의 현재 위치를 실시간으로 수신
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
        
        self.pose = Pose()
        self.goal_x = 9.0  # 목표 X 좌표
        self.goal_y = 9.0  # 목표 Y 좌표

    def update_pose(self, data):
        """거북이의 현재 위치가 업데이트될 때마다 호출되는 콜백 함수"""
        self.pose = data
        self.move_to_goal()

    def move_to_goal(self):
        msg = Twist()
        
        # 1. 목표까지의 거리 차이 계산
        diff_x = self.goal_x - self.pose.x
        diff_y = self.goal_y - self.pose.y
        
        # 유클리드 거리 공식
        distance = math.sqrt(diff_x**2 + diff_y**2)

        # 2. 오차(Distance)가 0.1보다 크면 계속 이동
        if distance > 0.1:
            # 방향 제어: 목표 지점의 각도와 현재 각도의 차이만큼 회전
            target_angle = math.atan2(diff_y, diff_x)
            
            # P 제어 (비례 제어): 오차가 클수록 빠르게, 작을수록 느리게 회전/전진
            msg.angular.z = 1.5 * (target_angle - self.pose.theta)
            msg.linear.x = 0.5 * distance
        else:
            # 목표 도달 시 정지
            msg.linear.x = 0.0
            msg.angular.z = 0.0 
            self.get_logger().info('목표 지점에 성공적으로 도착했습니다!')
            # 도착 후 노드 종료를 원한다면 여기서 rclpy.shutdown()을 호출할 수도 있습니다.
        
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    
    node = GoToGoal()
    
    try:
        # 실시간으로 Pose를 구독하고 제어 명령을 내리기 위해 무한 루프(spin)를 돕니다.
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('사용자에 의해 종료되었습니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()