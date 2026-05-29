import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleMoveNode(Node):
    def __init__(self): #생성자에서 몇개의 변수를 선언함
        super().__init__('turtle_move_node')
        # /turtle1/cmd_vel 토픽으로 Twist 메시지 발행하는 Publisher 생성
        #전 세계 대부분의 바퀴 달린 로봇(Mobile Robot)은 속도 명령을 받을 때 **geometry_msgs/msg/Twist**를 쓰기로 약속되어 있습니다
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 0.5초마다 타이머 콜백 실행
        self.timer = self.create_timer(0.5, self.move_callback)
        self.get_logger().info('Turtle Move Node has been started.')

    def move_callback(self):
        """
            linear (선속도: m/s)
                x: 전진 및 후진. (터틀심이 가장 많이 쓰는 값)
                y: 좌/우 횡이동. (드론이나 전방향 휠 로봇은 쓰지만, 거북이는 못 함)
                z: 상/하 이동. (드론이나 수중 로봇이 사용)
                
                angular (각속도: rad/s)
                x: Roll (좌우로 기우뚱)
                y: Pitch (앞뒤로 끄덕끄덕)
                z: Yaw (좌/우 회전). (터틀심이 방향을 틀 때 쓰는 유일한 값)
        """
        msg = Twist() # 메시지 생성 
        # 직선 속도 설정 (x축 전진: 2.0 m/s)
        msg.linear.x = 2.0
        # 회전 속도 설정 (z축 회전: 0.0 rad/s)
        msg.angular.z = 0.0

        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: Linear={msg.linear.x}, Angular={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleMoveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
