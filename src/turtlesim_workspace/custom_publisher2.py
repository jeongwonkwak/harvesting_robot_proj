import rclpy
from rclpy.node import Node
# ★ 핵심: 내가 만든 패키지에서 메시지 클래스를 불러옵니다.
from my_robot_interfaces.msg import TurtleStatus

class CustomMsgPublisher(Node):
    def __init__(self):
        super().__init__('custom_msg_publisher')
        # 메시지 타입을 MyOrder로 설정합니다.
        self.publisher = self.create_publisher(TurtleStatus, '/custom_order', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.distance = 5.0

    def timer_callback(self):
        # 벽을 향해 접근 → 정지 → 리셋 사이클 시뮬레이션
        if self.distance > 0.0:
            self.distance = round(self.distance - 0.3, 2)
        else:
            self.distance = 5.0  # 리셋

        if self.distance > 3.0:
            state = "NORMAL"
            moving = True
        elif self.distance > 1.0:
            state = "WARN"
            moving = True
        else:
            state = "STOP"
            moving = False

        msg = TurtleStatus()
        msg.distance_to_wall = self.distance
        msg.current_state = state
        msg.is_moving = moving

        self.publisher.publish(msg)
        self.get_logger().info(f'발행 중: dist={msg.distance_to_wall:.2f} state={msg.current_state} moving={msg.is_moving}')

def main(args=None):
    rclpy.init(args=args)
    node = CustomMsgPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()