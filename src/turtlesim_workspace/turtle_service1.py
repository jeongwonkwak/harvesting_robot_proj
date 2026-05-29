import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

class TurtleServiceNode(Node):
    def __init__(self):
        super().__init__('turtle_service_node')
        
        # 1. 거북이 소환(Spawn) 클라이언트 생성
        self.spawn_client = self.create_client(Spawn, 'spawn')
        
        # 2. 배경색 변경 클라이언트 생성
        self.param_client = self.create_client(SetParameters, '/turtlesim/set_parameters')

    def spawn_turtle(self, x, y, name):
        # 서비스가 켜질 때까지 대기
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn 서비스 대기 중...')
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.name = name
        
        # 서비스 호출 (비동기)
        # 응답이 필요없는 코드기 때문에 비동기 처리
        self.spawn_client.call_async(request)
        self.get_logger().info(f'[{name}] 거북이 소환 요청 완료!')

    def change_bg_color(self, r, g, b):
        while not self.param_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('파라미터 서비스 대기 중...')
            
        # 배경색(r, g, b) 파라미터 설정
        req = SetParameters.Request()
        req.parameters = [
            Parameter(name='background_r', value=ParameterValue(type=ParameterType.PARAMETER_INTEGER, integer_value=r)),
            Parameter(name='background_g', value=ParameterValue(type=ParameterType.PARAMETER_INTEGER, integer_value=g)),
            Parameter(name='background_b', value=ParameterValue(type=ParameterType.PARAMETER_INTEGER, integer_value=b))
        ]
        # 응답이 필요없는 코드기 때문에 비동기 처리
        self.param_client.call_async(req)
        self.get_logger().info(f'배경색 변경 완료: RGB({r}, {g}, {b})')

def main():
    rclpy.init()
    node = TurtleServiceNode()
    
    # 실행: 5, 5 좌표에 'turtle2' 소환하고 배경을 녹색으로 변경
    node.spawn_turtle(5.0, 5.0, 'turtle2')
    node.change_bg_color(0, 150, 0) # 진한 녹색
    
    rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()