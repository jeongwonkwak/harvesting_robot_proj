#!/usr/bin/env python3
"""
Remote VLA 테스트: VLA 서버(192.168.50.79:18003)에서 추론 후 로봇 구동
"""

import json
import base64
import time
import threading
import numpy as np
import requests
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import sys

sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')
from robot_controller import DoosanController
from gripper_controller import GripperController

VLA_SERVER = "http://192.168.50.79:18003"
VLA_VELOCITY = 100.0
VLA_ACCELERATION = 200.0


class SimpleVLATest(Node):
    def __init__(self):
        super().__init__("vla_simple_test")
        print("[INFO] Node 초기화...")

        # 로봇 & 그리퍼
        self.robot = DoosanController(self, robot_id="dsr01", action_mode="cartesian")
        self.gripper = GripperController(ros_node=self)
        self.bridge = CvBridge()

        # 이미지
        self.image_base = None
        self.image_left = None

        # 구독
        self.sub_base = self.create_subscription(
            Image, "/camera/camera/color/image_raw", self.on_image_base, 10)
        self.sub_left = self.create_subscription(
            Image, "/camera2/camera2/color/image_raw", self.on_image_left, 10)

        print("[INFO] VLA 서버:", VLA_SERVER)

    def on_image_base(self, msg):
        try:
            self.image_base = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        except Exception as e:
            print(f"[ERROR] 메인 카메라: {e}")

    def on_image_left(self, msg):
        try:
            self.image_left = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        except Exception as e:
            print(f"[ERROR] 좌측 카메라: {e}")

    def encode_image(self, img):
        if img is None:
            return None
        import cv2
        _, buf = cv2.imencode('.jpg', img)
        return base64.b64encode(buf).decode('utf-8')

    def get_state(self):
        pose = self.robot.get_eef_pose()
        if pose is None:
            return None
        grip = self.gripper.get_position()
        return (pose.tolist() + [grip])

    def vla_predict(self, instruction):
        if self.image_base is None:
            print("[WARN] 이미지 없음")
            return None

        state = self.get_state()
        if state is None:
            print("[WARN] 로봇 상태 읽기 실패")
            return None

        payload = {
            "state": state,
            "base_image": self.encode_image(self.image_base),
            "left_wrist_image": self.encode_image(self.image_left),
            "instruction": instruction,
            "reset_episode": False,
        }

        try:
            t0 = time.time()
            r = requests.post(f"{VLA_SERVER}/predict", json=payload, timeout=5)
            elapsed = time.time() - t0

            if r.status_code != 200:
                print(f"[ERROR] VLA {r.status_code}: {r.text}")
                return None

            data = r.json()
            action = np.array(data['action'])
            print(f"[VLA] action={np.round(action[:3], 3)} grip={action[5]:.3f} ({elapsed*1000:.0f}ms)")
            return action
        except Exception as e:
            print(f"[ERROR] VLA 요청: {e}")
            return None

    def execute_action(self, action):
        if action is None or len(action) < 6:
            return

        # EEF 이동
        delta_m = action[:3]
        grip_cmd = np.clip(action[5], 0.0, 1.0)

        current = self.robot.get_eef_pose()
        if current is not None:
            delta_mm = np.clip(delta_m * 1000.0, -1000.0, 1000.0)
            target = current + np.concatenate([delta_mm, np.zeros(3)])
            print(f"[MOVE] {np.round(target[:3], 1)}")

            def move_task():
                self.robot.move_line(target.tolist(),
                                    velocity=VLA_VELOCITY,
                                    acceleration=VLA_ACCELERATION)
            threading.Thread(target=move_task, daemon=True).start()

        # 그리퍼
        self.gripper.set_ratio(grip_cmd)
        print(f"[GRIP] {grip_cmd:.3f}")

    def run(self, instruction, max_steps=50):
        print(f"\n[START] 명령어: {instruction}")
        print(f"[INFO] 카메라 대기 중...\n")

        # 카메라 준비 대기
        for i in range(40):
            if self.image_base is not None:
                print(f"[INFO] 카메라 준비 완료 (시도 {i+1})")
                break
            time.sleep(0.5)
        else:
            print("[ERROR] 카메라 준비 실패!")
            return False

        time.sleep(1.0)

        # VLA 서버 헬스 체크
        try:
            r = requests.get(f"{VLA_SERVER}/health", timeout=2)
            if r.status_code == 200:
                print(f"[INFO] VLA 서버 OK: {r.json()}")
            else:
                print(f"[ERROR] VLA 서버 {r.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] VLA 서버 연결 실패: {e}")
            return False

        # 그리퍼 초기화
        print("[INFO] 그리퍼 초기화...")
        self.gripper.set_ratio(0.0)
        time.sleep(1.0)

        # 추론 루프
        print(f"\n{'='*60} VLA 추론 루프 시작 {'='*60}\n")

        for step in range(max_steps):
            print(f"--- Step {step:02d}/{max_steps} ---")
            action = self.vla_predict(instruction)
            if action is not None:
                self.execute_action(action)
            time.sleep(0.2)

        print(f"\n{'='*60} 완료 {'='*60}\n")
        return True


def main():
    rclpy.init()
    node = SimpleVLATest()

    try:
        success = node.run(
            instruction="Grasp the strawberry stem and pick it.",
            max_steps=50
        )
        print(f"[RESULT] {'성공' if success else '실패'}")
    except KeyboardInterrupt:
        print("\n[INFO] 사용자 중단")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
