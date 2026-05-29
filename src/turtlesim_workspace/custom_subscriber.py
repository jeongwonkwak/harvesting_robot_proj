import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class VirtualCustomSubscriber(Node):
    def __init__(self):
        super().__init__('virtual_custom_subscriber')
        self.subscription = self.create_subscription(
            String, '/robot_status_json', self.listener_callback, 10)
        # ① String — 메시지 타입
        # 토픽으로 어떤 형태의 데이터를 보낼지 지정해요. (String, Int32, Float64, Twist 등)
        # ② '/robot_status_json' — 토픽 이름
        # 라디오로 치면 주파수예요. 이 이름을 subscribe하는 노드만 내 데이터를 들을 수 있습니다.
        # ③ self.listener_callback — 콜백 함수
        # 메시지가 도착했을 때 실행할 함수를 지정합니다.
        # ④ 10 — 큐 사이즈 (Queue Size)
        # 만약 발행자가 너무 빠르게 데이터를 보내고 구독자가 이를 처리하지 못 할 경우, 최대 몇 개의 메시지를 버퍼에 쌓아둘지를 정합니다. 10은 넉넉한 편입니다. publisher와 subscriber가 서로 달라도 됨
        self.get_logger().info('가상 커스텀 구독자가 시작되었습니다.')

    def listener_callback(self, msg):
        # 1. 받은 JSON 문자열을 다시 파이썬 딕셔너리로 변환 (역직렬화)
        data = json.loads(msg.data)

        # 2. 데이터 활용
        name = data['robot_id']
        bat = data['battery']
        mode = data['mode']
        location = data['location']
        
        self.get_logger().info(f'>>> [수신] 로봇:{name} | 배터리:{bat}% | 모드:{mode} | 위치:{location}')

def main(args=None):
    rclpy.init(args=args)
    node = VirtualCustomSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main() 