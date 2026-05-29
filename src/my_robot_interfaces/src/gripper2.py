#토픽 확인을 해본다 
#ros2 topi  list
#ros2 topic pub /dsr01/gripper/position_cmd std_msgs/msg/Int32 "{data: 350}" --once
# 사용 예시: 완전 열기 -> 0, 완전 닫기 -> 700
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import sys

class DoosanGripperController(Node):
    def __init__(self):
        super().__init__('doosan_gripper_controller')
        
        # 1. 기본설정
        self.publisher_ = self.create_publisher(
            Int32, 
            '/dsr01/gripper/position_cmd', 
            10
        )
        
        # 2. 그리퍼 가동 범위 상수 정의
        self.OPEN_VAL = 0
        self.CLOSE_VAL = 700
        
        self.get_logger().info('E0509 실물 그리퍼 제어 노드가 활성화되었습니다.')
        self.get_logger().info(f'가동 범위: {self.OPEN_VAL}(열림) ~ {self.CLOSE_VAL}(닫힘)')

    def send_gripper_cmd(self, value):
        """그리퍼에 위치 명령을 전송 (안전 범위 체크 포함)"""
        msg = Int32()
        
        # 입력값 클램핑 (범위를 벗어나 로봇이 멈추는 것 방지)
        target = max(self.OPEN_VAL, min(value, self.CLOSE_VAL))
        msg.data = int(target)
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'전송된 명령 값: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = DoosanGripperController()

    print("\n" + "="*30)
    print("  E0509 그리퍼 제어 프로그램")
    print("  0: 완전 열림 / 700: 완전 닫힘")
    print("  (종료하려면 'q' 입력)")
    print("="*30)

    try:
        while rclpy.ok():
            user_input = input("\n목표 값을 입력하세요 (0~700): ")
            
            if user_input.lower() == 'q':
                break
            
            try:
                val = int(user_input)
                node.send_gripper_cmd(val)
            except ValueError:
                print("숫자 또는 'q'를 입력해주세요.")
                
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()