"""
GraspPipelinePi05Node – pi05_base HTTP 서버 기반 관절각도 VLA 파이프라인.

모델 입출력 (192.168.50.79:18003):
  state  입력: 32-dim float list  [j1..j6 (rad), gripper (0~1), 0*25]
  action 출력: 32-dim float list  [j1..j6 (rad, 절대값), gripper (0~1), ...]

카메라:
  base_image       – 필수, 메인(탑/전방) 카메라 RGB
  left_wrist_image  – 옵션 (없으면 null)
  right_wrist_image – 옵션 (없으면 null)

Run:
  ros2 run grasp_vla grasp_pipeline_pi05_node
  ros2 launch grasp_vla grasp.launch.py \
      pi05_url:=http://192.168.50.79:18003 \
      instruction:="pick up the red object"
"""

from __future__ import annotations

import base64
import io
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import requests
import rclpy
from PIL import Image
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController

# pi05_base: 최대 state/action 차원 (zero-padding 대상)
_MAX_DIM = 32
# Doosan e0509: 실사용 차원 (관절 6 + 그리퍼 1)
_ROBOT_DIM = 7
# 안전 관절 이동 한계 (한 스텝)
_MAX_JOINT_DELTA_DEG = 10.0


# ---------------------------------------------------------------------------
# Pi05Client
# ---------------------------------------------------------------------------

@dataclass
class Pi05Response:
    action: np.ndarray  # shape (32,) – 앞 7개만 유효 [j1..j6 rad, gripper 0~1]
    latency_ms: float


class Pi05Client:
    """pi05_base HTTP 서버 클라이언트."""

    def __init__(self, base_url: str = "http://192.168.50.79:18003", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=2.0)
            return r.ok
        except Exception:
            return False

    def reset(self) -> None:
        try:
            requests.post(f"{self.base_url}/reset", timeout=2.0)
        except Exception:
            pass

    def predict(
        self,
        state: np.ndarray,                    # shape (7,) [j1..j6 rad, gripper] → 패딩해서 전송
        base_image: np.ndarray,               # RGB uint8 (H, W, 3)
        instruction: str,
        left_wrist_image: Optional[np.ndarray] = None,
        right_wrist_image: Optional[np.ndarray] = None,
        reset_episode: bool = False,
    ) -> Pi05Response:
        # state를 32-dim으로 zero-pad
        state_padded = np.zeros(_MAX_DIM, dtype=np.float32)
        state_padded[:len(state)] = state

        payload = {
            "state": state_padded.tolist(),
            "base_image": _encode_image(base_image),
            "left_wrist_image": _encode_image(left_wrist_image) if left_wrist_image is not None else None,
            "right_wrist_image": _encode_image(right_wrist_image) if right_wrist_image is not None else None,
            "instruction": instruction,
            "reset_episode": reset_episode,
        }

        t0 = time.perf_counter()
        resp = requests.post(f"{self.base_url}/predict", json=payload, timeout=self.timeout)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        if not resp.ok:
            raise RuntimeError(f"[Pi05] {resp.status_code}: {resp.text[:300]}")

        data = resp.json()
        action = np.array(data["action"], dtype=np.float32)  # (32,)
        server_latency = data.get("latency_ms", latency_ms)

        return Pi05Response(action=action, latency_ms=server_latency)


def _encode_image(image: np.ndarray, size: tuple = (224, 224)) -> str:
    pil = Image.fromarray(image.astype(np.uint8)).resize(size)
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------------------
# GraspPipelinePi05Node
# ---------------------------------------------------------------------------

class GraspPipelinePi05Node(Node):
    def __init__(self):
        super().__init__("grasp_pipeline_pi05")

        self._declare("pi05_url",          "http://192.168.50.79:18003")
        self._declare("instruction",        "Approach the red object closely and pick it up.")
        self._declare("max_steps",          50)
        self._declare("step_hz",            5)
        self._declare("gripper_port",       "/dev/ttyUSB0")
        self._declare("robot_id",           "dsr01")
        self._declare("home_pose",          "67.3,-3.3,65.3,-6.5,25.8,-86.4")  # raw bag 실측 평균 (20260526)
        self._declare("camera_topic",       "")
        self._declare("depth_topic",        "")
        self._declare("min_grasp_step",     10)
        self._declare("gripper_close_ratio", 0.065)
        self._declare("record_video",       True)
        self._declare("video_save_dir",     "/home/user/robot_workspace/vla_ws/logs/videos")
        # 관절 이동 안전 한계 (deg/step). 0이면 비활성화.
        self._declare("max_joint_delta_deg", 20.0)

        url        = self.get_parameter("pi05_url").value
        gport      = self.get_parameter("gripper_port").value
        robot_id   = self.get_parameter("robot_id").value
        cam_topic  = self.get_parameter("camera_topic").value
        depth_topic = self.get_parameter("depth_topic").value

        self._pi05    = Pi05Client(base_url=url)
        self._camera  = CameraNode(
            ros_image_topic=cam_topic    if cam_topic    else None,
            ros_depth_topic=depth_topic  if depth_topic  else None,
            ros_node=self if cam_topic else None,
        )
        # pi05 EEF 델타 제어: 학습 데이터가 [dx_m, dy_m, dz_m, drx_rad, dry_rad, drz_rad] 형식
        self._robot   = DoosanController(self, robot_id=robot_id, action_mode="cartesian")
        self._gripper = GripperController(port=gport, ros_node=self, robot_id=robot_id)

        self.get_logger().info("GraspPipelinePi05Node initialized.")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def execute_grasp(self, instruction: Optional[str] = None) -> bool:
        instruction      = instruction or self.get_parameter("instruction").value
        max_steps        = self.get_parameter("max_steps").value
        step_period      = 1.0 / self.get_parameter("step_hz").value
        close_ratio_thr  = self.get_parameter("gripper_close_ratio").value
        min_grasp        = self.get_parameter("min_grasp_step").value

        # 1. Health check
        if not self._pi05.health():
            self.get_logger().error(f"Pi05 server not reachable: {self._pi05.base_url}")
            return False
        self.get_logger().info(f'Pi05 OK. Instruction: "{instruction}"')

        # 2. 카메라 대기
        deadline = time.time() + 10.0
        while not self._camera.ready:
            self._camera.grab()
            if time.time() > deadline:
                self.get_logger().error("Camera timeout.")
                return False
        self.get_logger().info("Camera ready.")

        # 3. 그리퍼 열기
        self._gripper.open()

        # 4. Home pose (옵션)
        home_str = self.get_parameter("home_pose").value
        if home_str:
            home = [float(x) for x in home_str.split(',')]
            self.get_logger().info(f"Moving to home: {home}")
            self._robot.move_joint(home, velocity=10.0, acceleration=20.0)

        # 5. Pi05 서버 에피소드 리셋
        self._pi05.reset()

        # 6. VLA 제어 루프
        self.get_logger().info("Starting pi05 VLA control loop …")
        reset    = True
        grasped  = False
        record_video = self.get_parameter("record_video").value
        video_frames = []

        for step in range(max_steps):
            t0 = time.time()
            self.get_logger().info(f"{'━'*28} Step {step:02d}/{max_steps} {'━'*28}")

            # 6a. 카메라
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                self.get_logger().warn(f"Step {step}: no camera frame, skipping.")
                continue
            if record_video:
                video_frames.append(rgb.copy())

            # 6b. 로봇 state: EEF 직교 좌표 (학습 데이터 형식: [x_m, y_m, z_m, rx_rad, ry_rad, rz_rad, gripper])
            eef_mm_deg = self._robot.get_eef_pose()  # [X,Y,Z,Rx,Ry,Rz] mm/deg
            if eef_mm_deg is None:
                self.get_logger().warn(f"Step {step}: no EEF pose, using zeros.")
                eef_mm_deg = np.zeros(6, dtype=np.float64)
            gripper_pos = self._gripper.get_position()  # 0~1
            # Doosan → 학습 단위 변환: mm→m, deg→rad
            eef_m_rad = np.array([
                eef_mm_deg[0] / 1000.0,
                eef_mm_deg[1] / 1000.0,
                eef_mm_deg[2] / 1000.0,
                np.radians(eef_mm_deg[3]),
                np.radians(eef_mm_deg[4]),
                np.radians(eef_mm_deg[5]),
            ], dtype=np.float32)
            state7 = np.append(eef_m_rad, gripper_pos).astype(np.float32)

            self.get_logger().info(
                f"  EEF(m) xyz={np.round(eef_m_rad[:3],3).tolist()}  "
                f"rot(deg)={np.round(eef_mm_deg[3:6],1).tolist()}  grip={gripper_pos:.3f}"
            )

            # 6c. Pi05 predict
            try:
                result = self._pi05.predict(
                    state=state7,
                    base_image=rgb,
                    instruction=instruction,
                    reset_episode=reset,
                )
                reset = False
                action = result.action  # (32,) – 앞 7개만 사용
            except Exception as e:
                self.get_logger().error(f"Step {step}: Pi05 call failed: {e}")
                break

            # action[0:6]: EEF 델타 [dx_m, dy_m, dz_m, drx_rad, dry_rad, drz_rad]
            # action[6]:   다음 그리퍼 위치 (0~1)
            action_eef_delta = action[:6].astype(np.float64)
            action_grip      = float(np.clip(action[6], 0.0, 1.0))

            delta_mm = np.round(action_eef_delta[:3] * 1000, 2).tolist()
            self.get_logger().info(
                f"  EEF delta(mm) {delta_mm}  grip={action_grip:.3f}  ({result.latency_ms:.0f}ms)"
            )

            # 6d. EEF 카테시안 델타 실행 (DoosanController._execute_cartesian_delta 사용)
            self._robot.execute_action(action_eef_delta)

            # 6e. 그리퍼
            self._gripper.set_ratio(action_grip)
            self.get_logger().info(
                f"  그리퍼       {action_grip:.3f}  ({int(action_grip * 740)}/740)"
            )

            if action_grip >= close_ratio_thr and step >= min_grasp and not grasped:
                grasped = True
                self.get_logger().info(
                    f"Step {step}: grasp detected (grip={action_grip:.2f}). Retreating …"
                )
                self._retreat()
                break

            elapsed = time.time() - t0
            sleep_t = step_period - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

        if record_video and video_frames:
            self._save_video(video_frames)

        return grasped

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _retreat(self) -> None:
        """EEF를 +Z 방향으로 80mm 들어올려 후퇴."""
        eef = self._robot.get_eef_pose()
        if eef is None:
            return
        target = eef.copy()
        target[2] += 80.0  # Z +80mm
        self.get_logger().info(f"Retreat: Z {eef[2]:.1f} → {target[2]:.1f} mm")
        self._robot.move_line(target.tolist(), velocity=30.0, acceleration=60.0)
        self.get_logger().info("Retreat complete.")

    def _save_video(self, frames: list) -> None:
        save_dir = Path(self.get_parameter("video_save_dir").value)
        save_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = save_dir / f"episode_pi05_{ts}.mp4"
        h, w = frames[0].shape[:2]
        cmd = [
            'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
            '-s', f'{w}x{h}', '-pix_fmt', 'rgb24',
            '-r', str(self.get_parameter("step_hz").value),
            '-i', 'pipe:0',
            '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            str(out_path),
        ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        for frame in frames:
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        proc.wait()
        self.get_logger().info(f"영상 저장: {out_path}  ({len(frames)} frames)")

    def _declare(self, name: str, default) -> None:
        self.declare_parameter(name, default, ParameterDescriptor(description=name))


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = GraspPipelinePi05Node()

    import threading
    from rclpy.executors import MultiThreadedExecutor

    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)

    def run():
        success = node.execute_grasp()
        node.get_logger().info(f"Episode finished. Success={success}")
        executor.shutdown(timeout_sec=1.0)

    t = threading.Thread(target=run, daemon=True)
    t.start()

    try:
        executor.spin()
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        node._camera.release()
        node.destroy_node()


if __name__ == "__main__":
    main()
