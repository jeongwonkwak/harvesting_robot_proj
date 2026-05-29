import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class DoosanGripperController(Node):
    OPEN_VAL = 0
    CLOSE_VAL = 740

    def __init__(self):
        super().__init__('doosan_gripper_controller')
        self.publisher_ = self.create_publisher(Int32, '/dsr01/gripper/position_cmd', 10)
        self.get_logger().info('E0509 실물 그리퍼 제어 노드가 활성화되었습니다.')
        self.get_logger().info(f'가동 범위: {self.OPEN_VAL}(열림) ~ {self.CLOSE_VAL}(닫힘)')

    def send_gripper_cmd(self, value):
        msg = Int32()
        msg.data = int(max(self.OPEN_VAL, min(value, self.CLOSE_VAL)))
        self.publisher_.publish(msg)
        self.get_logger().info(f'전송된 명령 값: {msg.data}')

    def run(self):
        print('\n' + '='*30)
        print('  E0509 그리퍼 제어 프로그램')
        print(f'  {self.OPEN_VAL}: 완전 열림 / {self.CLOSE_VAL}: 완전 닫힘')
        print("  (종료하려면 'q' 입력)")
        print('='*30)

        try:
            while rclpy.ok():
                user_input = input(f'\n목표 값을 입력하세요 ({self.OPEN_VAL}~{self.CLOSE_VAL}): ')
                if user_input.lower() == 'q':
                    break
                try:
                    self.send_gripper_cmd(int(user_input))
                except ValueError:
                    print("숫자 또는 'q'를 입력해주세요.")
        except KeyboardInterrupt:
            pass


def main():
    rclpy.init()
    node = DoosanGripperController()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
