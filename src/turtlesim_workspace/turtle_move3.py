import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import random

class TurtleWallAvoider(Node):
    def __init__(self):
        super().__init__('turtle_wall_avoider')
        # 1. 속도 명령을 보낼 Publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 2. 터틀의 위치를 받을 Subscriber
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.timer = self.create_timer(0.1, self.move_turtle)
        self.current_pose = None

    def pose_callback(self, msg):
        self.current_pose = msg
        # 호출자가 시스템이라 매개변수가 다 정해져있음

    def move_turtle(self):
        # 현재 위치를 모르면 함수를 종료하겠다.
        # timer가 호출
        if self.current_pose is None:
            return

        msg = Twist()
        
        # 벽 감지 로직 (경계값: 1.0 ~ 10.0)
        # phi=180니까, 90도는 1.5707963...
        if (self.current_pose.x < 1.5 or self.current_pose.x > 9.5 or 
            self.current_pose.y < 1.5 or self.current_pose.y > 9.5):
            # 벽에 가까워지면: 전진을 멈추고 제자리에서 회전
            msg.linear.x = 0.5 
            msg.angular.z = 1.5  # 초당 약 85도 회전
        else:
            # 안전한 구역: 직진
            msg.linear.x = 2.0
            msg.angular.z = 0.0

        self.cmd_vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleWallAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()