import rclpy
from rclpy.node import Node
from dsr_msgs2.srv import MoveJoint
import os
import time

class E0509JointManager(Node):
    def __init__(self):
        super().__init__('e0509_joint_manager')
        # 서비스 클라이언트 설정
        self.client = self.create_client(MoveJoint, '/dsr01/motion/move_joint')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('두산 로봇 컨트롤러 연결 대기 중...')
            
        # 초기 설정값
        self.target_angles = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
        self.joint_names = ['J1(Base)', 'J2(Shoulder)', 'J3(Elbow)', 'J4(Wrist1)', 'J5(Wrist2)', 'J6(Wrist3)']
        
        # [중요] 안전을 위한 순차 이동 순서 정의 (Index 기준: 4는 J5, 5는 J6 ...)
        # 예: J5부터 순서대로 움직여야 한다면 아래와 같이 정의
        self.move_order = [4, 5, 3, 2, 1, 0] 

    def send_sequential_move(self):
        """설정된 순서(move_order)에 따라 관절을 하나씩 이동시킵니다."""
        current_pose = [0.0] * 6 # 현재 로봇의 상태를 가져오는 로직이 있다면 연동 권장
        
        for idx in self.move_order:
            self.get_logger().info(f'🔄 {self.joint_names[idx]} 이동 시작...')
            
            # 이동할 목표 배열 생성 (해당 관절만 변경하고 나머지는 유지하는 전략이 필요할 수 있음)
            # 여기서는 최종 target_angles 중 해당 인덱스 값만 타겟으로 하여 하나씩 도달하게 합니다.
            request = MoveJoint.Request()
            
            # 순차 이동의 핵심: 다른 관절은 고정하고 현재 순서의 관절만 목표값으로 설정
            # 실제 환경에서는 현재 로봇 각도를 반영한 배열에서 해당 index만 바꿔야 안전합니다.
            temp_pose = list(self.target_angles) 
            request.pos = temp_pose
            request.vel = 20.0 # 안전을 위해 속도를 낮춤
            request.acc = 20.0
            
            future = self.client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            
            if future.result() is not None:
                self.get_logger().info(f'✅ {self.joint_names[idx]} 이동 완료')
                time.sleep(0.5) # 물리적 안정화를 위한 짧은 대기
            else:
                self.get_logger().error(f'❌ {self.joint_names[idx]} 이동 실패!')
                break

def print_interface(angles, names, order):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("="*60)
    print("      Doosan E0509 Sequential Joint Manager")
    print("="*60)
    print(" [이동 순서]: " + " -> ".join([names[i] for i in order]))
    print("-" * 60)
    for i, (name, angle) in enumerate(zip(names, angles)):
        print(f"  [{i+1}] {name.ljust(12)} : {angle:>6.1f} 도")
    print("-" * 60)
    print("  [S] 순차 이동 시작 (Safety Move)")
    print("  [R] 각도 초기화 / [Q] 종료")
    print("="*60)

def main():
    rclpy.init()
    node = E0509JointManager()

    try:
        while rclpy.ok():
            print_interface(node.target_angles, node.joint_names, node.move_order)
            choice = input("입력: ").upper()

            if choice.upper() == 'Q':
                break
            elif choice.upper() == 'S':
                node.send_sequential_move()
                input("\n전체 이동 완료! 엔터를 누르세요.")
            elif choice.upper() == 'R':
                node.target_angles = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
            elif choice.isdigit() and 1 <= int(choice) <= 6:
                idx = int(choice) - 1
                node.target_angles[idx] = float(input(f" ▶ {node.joint_names[idx]} 각도: "))
            
            rclpy.spin_once(node, timeout_sec=0.1)

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()