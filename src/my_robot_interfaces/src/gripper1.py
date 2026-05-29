# 그리퍼이동명령어 
# 그리퍼 열기
# ros2 service call /dsr01/gripper/open std_srvs/srv/Trigger

# 그리퍼 닫기
# ros2 service call /dsr01/gripper/close std_srvs/srv/Trigger

# 그리퍼 특정 위치 (0=열림, 700=닫힘)
# ros2 topic pub /dsr01/gripper/position_cmd std_msgs/msg/Int32 "{data: 350}" --once
# ros2 topic list  #/dsr01/gripper_cmd 가 있어야 한다 
# ros2 topic echo /dsr01/gripper_cmd   #오는 신호 확인


import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import time

def main():
    # 1. ROS 2 통신 시작 준비
    rclpy.init()
    node = rclpy.create_node('simple_gripper_test')
    
    # 2. 로봇에게 명령을 보낼 '통로(Publisher)' 만들기
    # (어디로: /dsr01/..., 어떤 타입: Int32)
    pub = node.create_publisher(Int32, '/dsr01/gripper/position_cmd', 10)
    
    msg = Int32()

    print("--- 실물 로봇 그리퍼 테스트 시작 ---")

    try:
        while True:
            # 3. 사용자로부터 명령 입력받기
            cmd = input("명령을 입력하세요 (1: 열기, 2: 닫기, q: 종료): ")

            if cmd == '1':
                msg.data = 0  # 0이 열림
                pub.publish(msg)
                print(">> 그리퍼를 엽니다! (값: 0)")

            elif cmd == '2':
                msg.data = 700  # 700이 닫힘
                pub.publish(msg)
                print(">> 그리퍼를 닫습니다! (값: 700)")

            elif cmd.lower() == 'q':
                print("프로그램을 종료합니다.")
                break

            else:
                print("잘못된 입력입니다. 1, 2, q 중에서 골라주세요.")
            
            # 명령이 전달될 수 있도록 아주 잠깐 대기
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        # 4. 안전하게 종료
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
