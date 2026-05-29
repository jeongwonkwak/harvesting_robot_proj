import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class TurtleActionClient(Node):
    def __init__(self):
        super().__init__('turtle_action_client')
        # 1. 액션 클라이언트 생성
        self._action_client = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')

    def send_goal(self, angle):
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = angle

        self._action_client.wait_for_server()#action이 끝날때까지
        
        # 2. 목표 전달 및 피드백 콜백 등록
        #시간이 오래걸리는 작업을 할때는 비동기로 전송한다. 비동기 완료시점은 
        #시스템만 안다. 그래서 반드시 콜백함수를 데리고 다닌다 
        #send_goal_async - 비동기 매개변수로는 msg와 콜백함수
        #반환값 future타입
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback
        )
        #response : 응답, request:요청 
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        print(type( self._send_goal_future ))
        
    def feedback_callback(self, feedback_msg):
        # [Feedback] 실시간 피드백 데이터 처리
        feedback = feedback_msg.feedback
        self.get_logger().info(f'남은 회전 각도: {feedback.remaining:.4f} rad')

    def goal_response_callback(self, future):
        goal_handle = future.result() #미래상태의 결과를 가져와서 
        if not goal_handle.accepted:
            self.get_logger().info('목표가 서버에 의해 거절되었습니다.')
            return

        self.get_logger().info('목표 수락! 회전을 시작합니다.')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        # [Result] 최종 결과 처리
        result = future.result().result
        self.get_logger().info('성공: 목표 각도에 도착했습니다!')
        rclpy.shutdown()

def main():
    rclpy.init()
    action_client = TurtleActionClient()
    # 3.14 라디안(180도) 회전 명령
    action_client.send_goal(0.0) 
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()