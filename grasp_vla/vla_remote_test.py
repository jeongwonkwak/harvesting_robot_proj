#!/usr/bin/env python3
"""
Remote VLA 테스트: 192.168.50.79:18003 서버에서 VLA 추론 결과를 받아서 로봇 구동.
- 카메라 2개에서 이미지 수신
- 로봇 상태 읽기
- VLA 서버에 POST 요청
- 응답받은 action으로 로봇 제어
"""

import json
import base64
import time
import threading
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
import requests
from typing import Optional

# 로컬 모듈
import sys
sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')
from robot_controller import DoosanController
from gripper_controller import GripperController

VLA_SERVER = "http://192.168.50.79:18003"
VLA_VELOCITY = 100.0
VLA_ACCELERATION = 200.0
INFERENCE_INTERVAL = 0.2  # 5Hz


class VLARemoteTestNode(Node):
    def __init__(self):
        super().__init__("vla_remote_test")
        self.get_logger().info("VLA Remote Test Node 초기화 중...")

        # 로봇 제어
        self._robot = DoosanController(self, robot_id="dsr01", action_mode="cartesian")
        self._gripper = GripperController(ros_node=self)
        self._bridge = CvBridge()

        # 카메라 이미지 저장
        self._image_base = None
        self._image_left = None
        self._image_right = None
        self._image_lock = threading.Lock()

        # 구독
        self.create_subscription(Image, "/camera/camera/color/image_raw", self._image_base_cb, 10)
        self.create_subscription(Image, "/camera2/camera2/color/image_raw", self._image_left_cb, 10)

        self.get_logger().info(f"VLA 서버: {VLA_SERVER}")
        self.get_logger().info("카메라 이미지 대기 중...")

    def _image_base_cb(self, msg: Image):
        """메인 카메라"""
        with self._image_lock:
            self._image_base = self._bridge.imgmsg_to_cv2(msg, "rgb8")

    def _image_left_cb(self, msg: Image):
        """왼쪽 카메라"""
        with self._image_lock:
            self._image_left = self._bridge.imgmsg_to_cv2(msg, "rgb8")

    def _encode_image(self, img_cv2) -> str:
        """OpenCV 이미지를 base64 문자열로 변환"""
        if img_cv2 is None:
            return None
        import cv2
        _, buffer = cv2.imencode('.jpg', img_cv2)
        return base64.b64encode(buffer).decode('utf-8')

    def _get_robot_state(self) -> Optional[list]:
        """로봇 상태 [x, y, z, rx, ry, rz, gripper] 반환 (7개 float)"""
        pose = self._robot.get_eef_pose()
        if pose is None:
            return None
        grip = self._gripper.get_position()
        return pose.tolist() + [grip]

    def _predict(self, instruction: str) -> Optional[list]:
        """VLA 서버에 요청, action 반환"""
        with self._image_lock:
            if self._image_base is None:
                self.get_logger().warn("메인 카메라 이미지 없음")
                return None
            base_img = self._encode_image(self._image_base)
            left_img = self._encode_image(self._image_left) if self._image_left is not None else None

        state = self._get_robot_state()
        if state is None:
            self.get_logger().warn("로봇 상태 읽기 실패")
            return None

        payload = {
            "state": state,
            "base_image": base_img,
            "left_wrist_image": left_img,
            "instruction": instruction,
            "reset_episode": False,
        }

        try:
            start = time.time()
            resp = requests.post(f"{VLA_SERVER}/predict", json=payload, timeout=5.0)
            latency = time.time() - start

            if resp.status_code != 200:
                self.get_logger().error(f"VLA 요청 실패: {resp.status_code} {resp.text}")
                return None

            data = resp.json()
            action = np.array(data['action'], dtype=np.float32)
            vla_latency = data.get('latency_ms', 0)

            self.get_logger().info(
                f"VLA 추론: action={np.round(action, 3).tolist()} "
                f"(VLA={vla_latency:.0f}ms, 네트워크={latency*1000:.0f}ms)"
            )
            return action

        except Exception as e:
            self.get_logger().error(f"VLA 요청 예외: {e}")
            return None

    def _execute_action(self, action: np.ndarray) -> None:
        """action [dx, dy, dz, drot_x, drot_y, drot_z] 실행"""
        if len(action) < 6:
            self.get_logger().warn(f"Invalid action length: {len(action)}")
            return

        # EEF Cartesian delta
        action_eef_delta = action[:3]  # 회전은 무시
        action_grip = action[5]  # 마지막 원소를 그리퍼로 사용

        # 클립
        action_grip = np.clip(action_grip, 0.0, 1.0)

        # EEF 이동
        current = self._robot.get_eef_pose()
        if current is not None:
            delta_mm = np.clip(
                action_eef_delta * 1000.0,  # m -> mm
                -1000.0, 1000.0
            )
            target = current + np.concatenate([delta_mm, np.zeros(3)])

            self.get_logger().info(
                f"EEF 목표: {np.round(target[:3], 1).tolist()} "
                f"(Δ={np.round(delta_mm, 1).tolist()}mm)"
            )

            # 스레드에서 move_line 실행
            def move_task():
                self._robot.move_line(target.tolist(), velocity=VLA_VELOCITY, acceleration=VLA_ACCELERATION)
            threading.Thread(target=move_task, daemon=True).start()

        # 그리퍼
        self._gripper.set_ratio(action_grip)
        self.get_logger().info(f"그리퍼: {action_grip:.3f}")

    def run_inference_loop(self, instruction: str, max_steps: int = 50) -> None:
        """VLA 추론 루프"""
        self.get_logger().info(f"시작 명령어: {instruction}")
        self.get_logger().info(f"최대 {max_steps} 스텝 실행")

        for step in range(max_steps):
            self.get_logger().info(
                f"\n{'='*60} Step {step:02d}/{max_steps} {'='*60}"
            )

            # VLA 추론
            action = self._predict(instruction)
            if action is None:
                self.get_logger().error(f"Step {step}: 추론 실패. 5초 후 재시도...")
                time.sleep(5.0)
                continue

            # action 실행
            self._execute_action(action)

            # 다음 스텝까지 대기
            time.sleep(INFERENCE_INTERVAL)

        self.get_logger().info(f"\n{'='*60} 완료 {'='*60}")


def main():
    rclpy.init()
    node = VLARemoteTestNode()

    # 카메라가 준비될 때까지 대기
    for _ in range(40):
        if node._image_base is not None:
            break
        time.sleep(1)
    else:
        node.get_logger().error("카메라 이미지 수신 실패!")
        rclpy.shutdown()
        return

    node.get_logger().info("카메라 준비 완료! 2초 후 시작...")
    time.sleep(2.0)

    # VLA 서버 헬스 체크
    try:
        resp = requests.get(f"{VLA_SERVER}/health", timeout=2.0)
        if resp.status_code == 200:
            info = resp.json()
            node.get_logger().info(f"VLA 서버 상태: {info}")
        else:
            node.get_logger().error(f"VLA 서버 응답 이상: {resp.status_code}")
            rclpy.shutdown()
            return
    except Exception as e:
        node.get_logger().error(f"VLA 서버 연결 실패: {e}")
        rclpy.shutdown()
        return

    # 그리퍼 초기화
    node.get_logger().info("그리퍼를 열기로 설정...")
    node._gripper.set_ratio(0.0)
    time.sleep(1.0)

    # 추론 루프 실행
    instruction = "Approach the red object closely and pick it up."
    node.run_inference_loop(instruction, max_steps=50)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
