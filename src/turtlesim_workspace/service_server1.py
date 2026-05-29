import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetTurtleMode # 사용자 정의 서비스 임포트

class ModeServiceServer(Node):
    def __init__(self):
        super().__init__('mode_service_server')
        # 서비스 서버 생성 (서비스 타입, 서비스 이름, 콜백 함수)
        self.srv = self.create_service(SetTurtleMode, 'set_robot_mode', self.set_mode_callback)
        self.get_logger().info('Mode Service Server가 시작되었습니다.')

    def set_mode_callback(self, request, response):
        # 비즈니스 로직 처리
        self.get_logger().info(f'요청 수신: Mode={request.mode_name}, Speed={request.target_speed}')
        
        if request.target_speed < 0:
            response.success = False
            response.message = "실패: 속도는 0보다 작을 수 없습니다."
        else:
            response.success = True
            response.message = f"성공: {request.mode_name} 모드로 전환되었습니다."
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ModeServiceServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
