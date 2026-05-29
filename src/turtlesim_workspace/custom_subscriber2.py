import rclpy
from rclpy.node import Node
# 1. 빌드한 커스텀 메시지 타입을 가져옵니다.
from my_robot_interfaces.msg import TurtleStatus 

class TurtleStatusSubscriber(Node):
    def __init__(self):
        # 노드 이름은 자유롭게! 여기서는 'turtle_status_sub'로 정해볼까요?
        super().__init__('turtle_status_sub')
        
        # 2. 구독자 설정: (메시지 타입, 토픽 이름, 콜백 함수, 큐 사이즈)
        # ★ 주의: 발행자의 토픽 이름('/custom_order')과 반드시 일치해야 합니다!
        self.subscription = self.create_subscription(
            TurtleStatus, 
            '/custom_order', 
            self.listener_callback, 
            10)
        self.get_logger().info('거북이 상태 모니터링을 시작합니다! 🐢')

    def listener_callback(self, msg):
        # 3. 수신된 데이터를 가공하여 출력합니다.
        status_icon = "🟢" if msg.is_moving else "🔴"
        
        self.get_logger().info(
            f'\n[수신 데이터]\n'
            f'- 벽까지의 거리: {msg.distance_to_wall:.2f}m\n'
            f'- 현재 상태: {msg.current_state}\n'
            f'- 이동 여부: {status_icon}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = TurtleStatusSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()