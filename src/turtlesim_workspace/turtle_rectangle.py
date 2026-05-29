import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class SquareDrawer(Node):
    def __init__(self):
        super().__init__('square_drawer')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

		#사각형 그리는 함수 - 한번만 , timer 쓸 필요가 없다. 
    def run_square(self):
        msg = Twist() #발행하기 위한 정보 객체를 만든다 
        for _ in range(4): #4번 작동
            # 1. 직진
            msg.linear.x = 2.0; 
            msg.angular.z = 0.0
            self.publisher.publish(msg)
            time.sleep(2.0)
            # 2초 동안 직진하라는 속도 명령을 publish

            # 2. 정지 후 회전
            msg.linear.x = 0.0; 
            msg.angular.z = 1.5708
            self.publisher.publish(msg)
            time.sleep(1.0)
            # 1초 동안 회전하라는 속도 명령을 publish
            # 초당 1.5708 라디안 회전하라는 속도 명령을 1초 동안 publish (딱 90도 회전)
            
            """
            ┌────┬──────────────┐
            │  도형  │  회전 각도                  │        
            ├────┼──────────────┤      
            │ 삼각형 │ 360/3 = 120도 = 2.0944 rad │
            ├────┼──────────────┤
            │ 사각형 │ 360/4 = 90도 = 1.5708 rad  │        
            ├────┼──────────────┤        
            │ 오각형 │ 360/5 = 72도 = 1.2566 rad  │        
            ├────┼──────────────┤        
            │ 육각형 │ 360/6 = 60도 = 1.0472 rad  │      
            └────┴──────────────┘ 
            """

        # 3. 최종 정지
        self.publisher.publish(Twist())
        self.get_logger().info('정사각형 그리기 완료!')



def main():
    rclpy.init()
    node = SquareDrawer()
    node.run_square()
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
