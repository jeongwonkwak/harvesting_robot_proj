import rclpy
from rclpy.node import Node
from dsr_msgs2.srv import MoveJoint

def main():
    rclpy.init()
    node = rclpy.create_node('joint_mover_client')
    client = node.create_client(MoveJoint, '/dsr01/motion/move_joint')

    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('로봇 서비스 대기 중...')

    # 사용자로부터 6개 각도 입력 받기
    user_input = input("6개 관절 각도를 입력하세요 (예: 0 0 90 0 90 0): ")
    angles = [float(x) for x in user_input.split()]

    request = MoveJoint.Request()
    request.pos = angles
    request.vel = 20.0
    request.acc = 20.0

    node.get_logger().info(f'로봇 이동 명령 전송 중: {angles}')
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info('명령 전송 완료')
    else:
        node.get_logger().error('서비스 호출 실패')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()