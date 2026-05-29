import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json  # 데이터를 문자열로 변환하기 위해 필요

class VirtualCustomPublisher(Node):
    def __init__(self):
        super().__init__('virtual_custom_publisher')
        # 표준 String 메시지 타입을 사용합니다.
        self.publisher = self.create_publisher(String, '/robot_status_json', 10)
        # ① String — 메시지 타입
        # 토픽으로 어떤 형태의 데이터를 보낼지 지정해요. (String, Int32, Float64, Twist 등)
        # ② '/robot_status_json' — 토픽 이름
        # 라디오로 치면 주파수예요. 이 이름을 subscribe하는 노드만 내 데이터를 들을 수 있습니다.
        # ③ 10 — 큐 사이즈 (Queue Size)
        # 만약 발행자가 너무 빠르게 데이터를 보내고 구독자가 이를 처리하지 못 할 경우, 최대 몇 개의 메시지를 버퍼에 쌓아둘지를 정합니다. 10은 넉넉한 편입니다.
        self.timer = self.create_timer(1.0, self.timer_callback)
        # 1초마다 timer_callback 함수를 실행
        self.get_logger().info('가상 커스텀 발행자가 시작되었습니다.')

    def timer_callback(self):
        # 1. 내가 보내고 싶은 복잡한 데이터 구조 (딕셔너리)
        custom_data = {
            "robot_id": "Conan_Bot_01",
            "battery": 92.5,
            "mode": "Autonomous",
            "location": {"x": 1.2, "y": 3.4}
        }

        # 2. 딕셔너리를 JSON 문자열로 변환 (직렬화)
        # 문자열로 토픽을 전송하고, 받는 쪽에서 문자열을 JSON으로 변환해서 딕셔너리를 사용
        msg = String()
        msg.data = json.dumps(custom_data)

        # 3. 메시지 발행
        self.publisher.publish(msg)
        self.get_logger().info(f'데이터 발행 완료: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = VirtualCustomPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main() 