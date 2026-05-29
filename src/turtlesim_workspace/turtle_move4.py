import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, tty, termios

class TurtleControlNode(Node):
    def __init__(self):
        super().__init__('turtle_control_node')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('=== 거북이 조종기 가동 ===')
        self.get_logger().info('t: 전진, b: 후진, l: 좌회전, r: 우회전, q: 종료')

    def get_key(self):
        # 터미널에서 키 한 글자를 즉시 읽어오는 설정
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        msg = Twist()
        while True:
            key = self.get_key()
            
            if key == 't':    # Top (전진)
                msg.linear.x = 2.0; msg.angular.z = 0.0
            elif key == 'b':  # Bottom (후진)
                msg.linear.x = -2.0; msg.angular.z = 0.0
            elif key == 'l':  # Left (좌회전)
                msg.linear.x = 0.0; msg.angular.z = 2.0
            elif key == 'r':  # Right (우회전)
                msg.linear.x = 0.0; msg.angular.z = -2.0
            elif key == 'q':  # 종료
                break
            else:             # 다른 키 누르면 멈춤
                msg.linear.x = 0.0; msg.angular.z = 0.0

            self.publisher.publish(msg)
            print(f"\r입력된 키: {key} | 전진: {msg.linear.x}, 회전: {msg.angular.z}", end="")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControlNode()
    try:
        node.run()
    except Exception as e:
        print(e)
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()