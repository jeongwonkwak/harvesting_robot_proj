import rclpy
from gripper1_class import SimpleGripperController
from gripper2_class import DoosanGripperController
from robot_move2 import E0509JointManager, print_interface
from robot_move3 import E0509RobotController


def show_menu():
    print('\n' + '='*40)
    print('  제어 프로그램 선택')
    print('  1: 그리퍼 단순 제어 (열기/닫기)')
    print('  2: 그리퍼 정밀 제어 (0~700 직접 입력)')
    print('  3: 관절 순차 이동 (E0509JointManager)')
    print('  4: 통합 제어 (Joint+Line+Circle+그리퍼)')
    print('  q: 종료')
    print('='*40)


def run_gripper1():
    node = SimpleGripperController()
    try:
        node.run()
    finally:
        node.destroy_node()


def run_gripper2():
    node = DoosanGripperController()
    try:
        node.run()
    finally:
        node.destroy_node()


def run_joint_manager():
    node = E0509JointManager()
    try:
        while rclpy.ok():
            print_interface(node.target_angles, node.joint_names, node.move_order)
            choice = input('입력: ').upper()
            if choice == 'Q':
                break
            elif choice == 'S':
                node.send_sequential_move()
                input('\n전체 이동 완료! 엔터를 누르세요.')
            elif choice == 'R':
                node.target_angles = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
            elif choice.isdigit() and 1 <= int(choice) <= 6:
                idx = int(choice) - 1
                node.target_angles[idx] = float(input(f' ▶ {node.joint_names[idx]} 각도: '))
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        node.destroy_node()


def run_robot_controller():
    node = E0509RobotController()
    try:
        node.run()
    finally:
        node.destroy_node()


def main():
    rclpy.init()
    try:
        while True:
            show_menu()
            choice = input('선택하세요 (1 / 2 / 3 / 4 / q): ').strip().lower()

            if choice == '1':
                run_gripper1()
            elif choice == '2':
                run_gripper2()
            elif choice == '3':
                run_joint_manager()
            elif choice == '4':
                run_robot_controller()
            elif choice == 'q':
                print('프로그램을 종료합니다.')
                break
            else:
                print('잘못된 입력입니다. 1, 2, 3, 4, q 중에서 선택하세요.')
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
