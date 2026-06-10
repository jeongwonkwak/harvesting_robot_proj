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
import threading
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 파라미터 설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PI05_URL                = "http://192.168.50.79:18003"
DEFAULT_INSTRUCTION     = "Approach the red object closely and pick it up."
MAX_STEPS               = 50
STEP_HZ                 = 5
GRIPPER_PORT            = "/dev/ttyUSB0"
ROBOT_ID                = "dsr01"
CAMERA_TOPIC            = "/camera/camera/color/image_raw"
CAMERA2_TOPIC           = "/camera2/camera2/color/image_raw"
DEPTH_TOPIC             = ""
MIN_GRASP_STEP          = 10
GRIPPER_CLOSE_POS       = 740         # 그리퍼 위치 0~740 (기본=600, 이 값 이상이면 물건 집었다고 판단)
RECORD_VIDEO            = True
VIDEO_SAVE_DIR          = "/home/user/robot_workspace/vla_ws/logs/videos"

# 로봇 이동 파라미터
HOME_VELOCITY           = 2500.0
HOME_ACCELERATION       = 250.0
VLA_VELOCITY            = 5000.0      # VLA 제어 루프에서의 로봇 이동 속도
VLA_ACCELERATION        = 500.0       # VLA 제어 루프에서의 로봇 이동 가속도

# pi05_base: 최대 state/action 차원 (zero-padding 대상)
_MAX_DIM = 32
# Doosan e0509: 실사용 차원 (관절 6 + 그리퍼 1)
_ROBOT_DIM = 7

# ── 홈 포즈 ── TCP [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg] ──────────────
# NW=top_left / NE=top_right / SE=bottom_right / SW=bottom_left
HOME_POSES = {
    'top_right':    [ 314.90, 279.89, 883.40,  89.90, 86.29, -89.62],  # NE
    'top_left':     [-225.46, 338.93, 902.31,  88.42, 87.31, -89.88],  # NW
    'bottom_right': [ 312.61, 302.83, 529.32,  89.90, 86.29, -89.62],  # SE
    'bottom_left':  [-247.70, 317.34, 533.88,  87.75, 86.31, -89.49],  # SW
    'NE':           [ 285.75, 347.14, 730.58,  85.94, 65.09, -88.59],  # 테스트용
}
HOME_POSE_DEFAULT = 'top_right'


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


def _encode_image(image: np.ndarray) -> str:
    pil = Image.fromarray(image.astype(np.uint8))
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------------------
# GraspPipelinePi05Node
# ---------------------------------------------------------------------------

class GraspPipelinePi05Node(Node):
    def __init__(self):
        super().__init__("grasp_pipeline_pi05")

        self._declare("pi05_url",          PI05_URL)
        self._declare("instruction",        DEFAULT_INSTRUCTION)
        self._declare("max_steps",          MAX_STEPS)
        self._declare("step_hz",            STEP_HZ)
        self._declare("gripper_port",       GRIPPER_PORT)
        self._declare("robot_id",           ROBOT_ID)
        self._declare("home_pose",          HOME_POSE_DEFAULT)  # 'top_left', 'top_right', 'bottom_left', 'bottom_right'
        self._declare("camera_topic",       CAMERA_TOPIC)
        self._declare("camera2_topic",      CAMERA2_TOPIC)
        self._declare("depth_topic",        DEPTH_TOPIC)
        self._declare("min_grasp_step",     MIN_GRASP_STEP)
        self._declare("gripper_close_pos",  GRIPPER_CLOSE_POS)
        self._declare("record_video",       RECORD_VIDEO)
        self._declare("video_save_dir",     VIDEO_SAVE_DIR)

        url         = self.get_parameter("pi05_url").value
        gport       = self.get_parameter("gripper_port").value
        robot_id    = self.get_parameter("robot_id").value
        cam_topic   = self.get_parameter("camera_topic").value
        cam2_topic  = self.get_parameter("camera2_topic").value
        depth_topic = self.get_parameter("depth_topic").value

        self._pi05     = Pi05Client(base_url=url)
        self._camera   = CameraNode(
            ros_image_topic=cam_topic    if cam_topic    else None,
            ros_depth_topic=depth_topic  if depth_topic  else None,
            ros_node=self if cam_topic else None,
        )
        self._camera2  = CameraNode(
            ros_image_topic=cam2_topic   if cam2_topic   else None,
            ros_node=self if cam2_topic else None,
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
        close_pos_thr    = self.get_parameter("gripper_close_pos").value
        min_grasp        = self.get_parameter("min_grasp_step").value

        # 1. Health check
        if not self._pi05.health():
            self.get_logger().error(f"Pi05 server not reachable: {self._pi05.base_url}")
            return False
        self.get_logger().info(f'Pi05 OK. Instruction: "{instruction}"')

        # 2. 카메라 대기 (카메라 1 필수, 카메라 2 옵션)
        self.get_logger().info('두 카메라 첫 프레임 대기 중 (최대 40초)...')
        deadline = time.time() + 40.0
        while True:
            c1_ok = self._camera.ready
            c2_ok = self._camera2.ready
            if c1_ok:
                break
            if time.time() > deadline:
                self.get_logger().error("Camera timeout (카메라 1 필수).")
                return False
            self._camera.grab()
            self._camera2.grab()
            time.sleep(0.2)

        has_cam2 = c2_ok
        if has_cam2:
            self.get_logger().info("두 카메라 준비 완료.")
        else:
            self.get_logger().info("[INFO] 카메라 2 없음 — 단일 카메라 모드로 진행.")

        # 3. 그리퍼를 600 위치로 설정
        self.get_logger().info("Setting gripper to position 600...")
        try:
            self._gripper.move_to(600)
            time.sleep(1.0)  # 그리퍼가 움직일 때간 대기
            self.get_logger().info("Gripper set to 600.")
        except Exception as e:
            self.get_logger().warn(f"Gripper move_to error: {e}. Continuing...")

        # 4. Home pose 스킵 - 현재 위치에서 바로 VLA 루프 시작
        # (로봇 제어 문제를 회피하기 위해 홈 포즈 이동 제거)
        self.get_logger().info("Skipping home pose - starting from current position.")

        self.get_logger().info("Waiting 2 seconds before starting VLA inference…")
        time.sleep(2.0)

        # 5. Pi05 서버 에피소드 리셋
        self._pi05.reset()

        # 6. VLA 제어 루프
        self.get_logger().info("Starting pi05 VLA control loop …")
        reset    = True
        grasped  = False
        record_video = self.get_parameter("record_video").value
        video_frames = []
        video2_frames = [] if has_cam2 else None

        for step in range(max_steps):
            t0 = time.time()
            self.get_logger().info(f"{'━'*28} Step {step:02d}/{max_steps} {'━'*28}")

            # 6a. 카메라 1 (필수)
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                self.get_logger().warn(f"Step {step}: no camera frame, skipping.")
                continue
            if record_video:
                video_frames.append(rgb.copy())

            # 6a-2. 카메라 2 (옵션)
            rgb2 = None
            if has_cam2:
                self._camera2.grab()
                rgb2, _ = self._camera2.get_images()
                if rgb2 is not None and record_video:
                    video2_frames.append(rgb2.copy())

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

            # 6d. EEF 카테시안 델타 실행 (스레드에서 비동기 실행 - teleop 방식)
            current = self._robot.get_eef_pose()
            if current is not None:
                delta_mm = np.clip(
                    action_eef_delta[:3] * 1000.0,  # m → mm 변환
                    -1000.0, 1000.0  # VLA 모델의 큰 델타에 대응
                )
                target = current + np.concatenate([delta_mm, np.zeros(3)])
                self.get_logger().info(f"  [move_line] Sending target: {np.round(target[:3], 1).tolist()}")
                # 별도 스레드에서 move_line 실행 (teleop과 동일한 방식)
                def move_task():
                    self._robot.move_line(target.tolist(), velocity=VLA_VELOCITY, acceleration=VLA_ACCELERATION)
                threading.Thread(target=move_task, daemon=True).start()
            else:
                self.get_logger().warn(f"  [ERROR] get_eef_pose() returned None")

            # 6e. 그리퍼
            self._gripper.set_ratio(action_grip)
            grip_pos = int(action_grip * 740)
            self.get_logger().info(
                f"  그리퍼       {action_grip:.3f}  ({grip_pos}/740)"
            )

            if grip_pos >= close_pos_thr and step >= min_grasp and not grasped:
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
            self._save_video(video_frames, camera_name="camera1")
        if record_video and video2_frames:
            self._save_video(video2_frames, camera_name="camera2")

        return grasped

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _retreat(self) -> None:
        """EEF를 +Z 방향으로 들어올려 후퇴."""
        eef = self._robot.get_eef_pose()
        if eef is None:
            return
        target = eef.copy()
        target[2] += 80.0
        self.get_logger().info(f"Retreat: Z {eef[2]:.1f} → {target[2]:.1f} mm")
        self._robot.move_line(target.tolist(), velocity=30.0, acceleration=60.0)
        self.get_logger().info("Retreat complete.")

    def _save_video(self, frames: list, camera_name: str = "camera1") -> None:
        save_dir = Path(self.get_parameter("video_save_dir").value)
        save_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = save_dir / f"episode_pi05_{camera_name}_{ts}.mp4"
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
        node._camera2.release()
        node.destroy_node()


if __name__ == "__main__":
    main()
