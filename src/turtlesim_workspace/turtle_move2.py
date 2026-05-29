import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import time

class TurtleEightLoop(Node):
    def __init__(self):
        super().__init__('turtle_eight_loop')
        
        # 1. Pub/Sub 및 Service Client 초기화
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        
        # 2. 실행 즉시 펜 설정 변경 (빨간색, 두께 5)
        self.set_red_pen()
        
        # 3. 제어 루프 타이머 (0.1초마다 move_eight 실행)
        self.timer = self.create_timer(0.1, self.move_eight)
        self.start_time = time.time()

    def set_red_pen(self):
        """거북이의 펜 색상을 변경하는 서비스 호출"""
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('turtlesim 서비스 대기 중...')
        
        req = SetPen.Request()
        req.r, req.g, req.b = 255, 0, 0
        req.width = 5
        req.off = 0
        self.pen_client.call_async(req) # set_red_pen이 생각보다 지연이 될 수 있어서 동기를 비동기로 바꾸는 것

        # server: turtlesim (서비스를 제공하는 측)
        # client: /turtle1/set_pen (서비스를 요청하는 측)

    def move_eight(self):
        """8자 궤적 계산 및 속도 명령 발행"""
        msg = Twist()
        elapsed = time.time() - self.start_time
        
        msg.linear.x = 2.0  # 전진 속도 고정
        
        # 3초마다 회전 방향을 반대로 바꾸어 8자 구현
        circle_duration = (2 * 3.14159) / 1.5
        if int(elapsed / circle_duration) % 2 == 0:
            msg.angular.z = 1.5  # 좌회전
        else:
            msg.angular.z = -1.5 # 우회전
            
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = TurtleEightLoop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\n사용자에 의해 종료되었습니다.")
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
main()