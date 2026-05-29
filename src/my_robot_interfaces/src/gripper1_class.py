import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import time


class SimpleGripperController(Node):
    OPEN_VAL = 0
    CLOSE_VAL = 700

    def __init__(self):
        super().__init__('simple_gripper_test')
        self.pub = self.create_publisher(Int32, '/dsr01/gripper/position_cmd', 10)

    def open_gripper(self):
        self._publish(self.OPEN_VAL)
        print(f'>> 그리퍼를 엽니다! (값: {self.OPEN_VAL})')

    def close_gripper(self):
        self._publish(self.CLOSE_VAL)
        print(f'>> 그리퍼를 닫습니다! (값: {self.CLOSE_VAL})')

    def _publish(self, value):
        msg = Int32()
        msg.data = value
        self.pub.publish(msg)
        time.sleep(0.1)

    def run(self):
        print('--- 실물 로봇 그리퍼 테스트 시작 ---')
        try:
            while True:
                cmd = input('명령을 입력하세요 (1: 열기, 2: 닫기, q: 종료): ')
                if cmd == '1':
                    self.open_gripper()
                elif cmd == '2':
                    self.close_gripper()
                elif cmd.lower() == 'q':
                    print('프로그램을 종료합니다.')
                    break
                else:
                    print('잘못된 입력입니다. 1, 2, q 중에서 골라주세요.')
        except KeyboardInterrupt:
            pass


def main():
    rclpy.init()
    node = SimpleGripperController()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
