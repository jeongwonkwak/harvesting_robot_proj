import sys
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetTurtleMode

class ModeServiceClient(Node):
    def __init__(self):
        super().__init__('mode_service_client')
        self.client = self.create_client(SetTurtleMode, 'set_robot_mode')
        
        # 서버가 활성화될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('서비스 서버를 기다리는 중...')

    def send_request(self, mode, speed):
        req = SetTurtleMode.Request()
        req.mode_name = mode
        req.target_speed = speed
        
        # 비동기 요청 호출
        self.future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    client = ModeServiceClient()
    
    # 예시 요청 전달
    response = client.send_request("Autonomous", 1.5)
    
    if response.success:
        client.get_logger().info(f'결과: {response.message}')
    else:
        client.get_logger().error(f'에러: {response.message}')

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
