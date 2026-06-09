#!/usr/bin/env python3
"""
최소 버전: VLA 서버에 요청 + 로봇 제어
카메라는 subprocess로 병렬 수집
"""

import json
import base64
import time
import threading
import numpy as np
import requests
import subprocess
import sys

sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')
from robot_controller import DoosanController
from gripper_controller import GripperController

VLA_SERVER = "http://192.168.50.79:18003"


def capture_images(node):
    """ROS2 노드를 통해 이미지 캡처"""
    from sensor_msgs.msg import Image
    from cv_bridge import CvBridge

    images = {}

    def on_base(msg):
        try:
            images['base'] = CvBridge().imgmsg_to_cv2(msg, "rgb8")
        except:
            pass

    def on_left(msg):
        try:
            images['left'] = CvBridge().imgmsg_to_cv2(msg, "rgb8")
        except:
            pass

    node.create_subscription(Image, "/camera/camera/color/image_raw", on_base, 10)
    node.create_subscription(Image, "/camera2/camera2/color/image_raw", on_left, 10)

    # 20초 동안 이미지 수집
    import rclpy
    deadline = time.time() + 20
    while time.time() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)
        if 'base' in images:
            return images

    return images


def encode_image(img):
    if img is None:
        return None
    import cv2
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf).decode('utf-8')


def main():
    import rclpy
    from rclpy.node import Node

    rclpy.init()
    node_temp = Node("cam_node")

    print("[INFO] 이미지 캡처 시작...")
    images = capture_images(node_temp)

    if 'base' not in images:
        print("[ERROR] 메인 카메라 이미지 수신 실패!")
        return False

    print("[OK] 이미지 수신 완료")

    # 로봇 제어
    print("[INFO] 로봇 제어 초기화...")
    node = Node("vla_test")

    robot = DoosanController(node, robot_id="dsr01", action_mode="cartesian")
    gripper = GripperController(ros_node=node)

    # VLA 서버 헬스 체크
    print("[INFO] VLA 서버 확인...")
    try:
        r = requests.get(f"{VLA_SERVER}/health", timeout=2)
        if r.status_code != 200:
            print(f"[ERROR] VLA 서버 {r.status_code}")
            return False
        print(f"[OK] VLA 서버 준비됨")
    except Exception as e:
        print(f"[ERROR] VLA 서버: {e}")
        return False

    # 그리퍼 초기화
    print("[INFO] 그리퍼 오픈...")
    gripper.set_ratio(0.0)
    time.sleep(1.0)

    # VLA 추론 루프
    instruction = "Grasp the strawberry stem and pick it."
    print(f"\n[START] {instruction}\n")

    base_img_b64 = encode_image(images['base'])
    left_img_b64 = encode_image(images.get('left'))

    for step in range(50):
        print(f"=== Step {step:02d} ===")

        # 로봇 상태
        pose = robot.get_eef_pose()
        if pose is None:
            print("[WARN] 로봇 상태 읽기 실패")
            continue

        joint = robot.get_joint_state()
        grip = gripper.get_position()

        # 32차원 state: EEF(6) + Grip(1) + Joint(6) + padding(19)
        state = pose.tolist() + [grip]
        if joint is not None:
            state += np.degrees(joint).tolist()  # joint in degrees
        else:
            state += [0.0] * 6
        state += [0.0] * 19  # padding

        print(f"State: EEF={np.round(pose[:3], 1)}, Grip={grip:.3f}")

        # VLA 요청
        payload = {
            "state": state,
            "base_image": base_img_b64,
            "left_wrist_image": left_img_b64,
            "instruction": instruction,
            "reset_episode": False,
        }

        try:
            t0 = time.time()
            r = requests.post(f"{VLA_SERVER}/predict", json=payload, timeout=5)
            elapsed = time.time() - t0

            if r.status_code != 200:
                print(f"[ERROR] VLA {r.status_code}: {r.text[:200]}")
                continue

            data = r.json()
            action = np.array(data['action'])

            # 액션 정규화 (SmolVLA normalization: mean_std 기반)
            # 원본 action이 정규화되어 있으면, denormalize
            action_norm = np.clip(action, -1.0, 1.0)  # 클립 먼저

            print(f"Action: {np.round(action_norm[:3], 3)} | Grip: {action_norm[5]:.3f} ({elapsed*1000:.0f}ms)")

            # 로봇 제어
            delta_m = action_norm[:3]
            grip_cmd = np.clip((action_norm[5] + 1.0) / 2.0, 0.0, 1.0)  # -1~1 → 0~1

            # EEF 이동 (델타 클립) - 스케일 50mm per step
            delta_mm = np.clip(delta_m * 50.0, -50.0, 50.0)
            target = pose + np.concatenate([delta_mm, np.zeros(3)])

            # 안전 범위 제한 (로봇 workspace)
            target[0] = np.clip(target[0], 100.0, 800.0)   # X: 100-800mm
            target[1] = np.clip(target[1], 100.0, 800.0)   # Y: 100-800mm
            target[2] = np.clip(target[2], 600.0, 1200.0)  # Z: 600-1200mm

            print(f"Target: {np.round(target[:3], 1)}")

            # 로봇 이동 (teleop_api HTTP를 통해 move_delta 호출)
            print(f"[move] delta={np.round(delta_mm, 1)}")
            try:
                payload = {"dx": float(delta_mm[0]), "dy": float(delta_mm[1]), "dz": float(delta_mm[2])}
                r = requests.post("http://localhost:8767/move", json=payload, timeout=2)
                if r.status_code == 200:
                    result = r.json()
                    if result.get('ok'):
                        print(f"[move] ✅ {result}")
                    else:
                        print(f"[move] ⚠️  {result.get('message')}")
                else:
                    print(f"[move] ❌ HTTP {r.status_code}: {r.text[:100]}")
            except Exception as e:
                print(f"[move] ❌ {e}")

            # 그리퍼
            gripper.set_ratio(grip_cmd)

        except Exception as e:
            print(f"[ERROR] {e}")

        # 로봇 이동 완료 대기 (충분한 시간 필요!)
        for _ in range(30):  # 1.5초 대기
            rclpy.spin_once(node, timeout_sec=0.05)
            time.sleep(0.05)

    print("\n[DONE]")
    rclpy.shutdown()
    return True


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPTED]")
    except Exception as e:
        print(f"[FATAL] {e}")
        import traceback
        traceback.print_exc()
