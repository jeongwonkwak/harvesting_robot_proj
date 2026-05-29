import rclpy
from robot_move3_gazebo import E0509GazeboController
from pick_and_place_gazebo import PickAndPlaceGazeboNode


def show_menu():
    print('\n' + '='*45)
    print('  Gazebo 제어 프로그램')
    print('  1: 관절 제어 (MoveJoint + 그리퍼)')
    print('  2: 픽앤플레이스 시뮬레이션')
    print('  q: 종료')
    print('='*45)


def run_robot_controller():
    node = E0509GazeboController()
    try:
        node.run()
    finally:
        node.destroy_node()


def run_pick_and_place():
    node = PickAndPlaceGazeboNode()
    try:
        node.run()
        input('\n엔터를 누르면 메뉴로 돌아갑니다...')
    finally:
        node.destroy_node()


def main():
    print('\n[실행 전 확인]')
    print('  ros2 launch e0509_gripper_description bringup_gazebo.launch.py')
    print('  위 명령으로 Gazebo가 실행 중이어야 합니다.\n')

    rclpy.init()
    try:
        while True:
            show_menu()
            choice = input('선택 (1 / 2 / q): ').strip().lower()

            if choice == '1':
                run_robot_controller()
            elif choice == '2':
                run_pick_and_place()
            elif choice == 'q':
                print('종료합니다.')
                break
            else:
                print('1, 2, q 중에서 선택하세요.')
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
