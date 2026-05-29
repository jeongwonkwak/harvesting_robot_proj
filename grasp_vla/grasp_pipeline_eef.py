"""
GraspPipelineEEFNode – EEF delta action 기반 VLA 파이프라인.

Octo 등 EEF delta 출력 모델 전용.
모델 출력: [Δx_mm, Δy_mm, Δz_mm, Δrx_deg, Δry_deg, Δrz_deg, gripper]
state 입력: [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg, gripper]

Flow per episode
----------------
1. health-check VLA server
2. open gripper
3. (optional) move to pre-grasp home pose
4. VLA control loop (max_steps)
     a. capture RGB
     b. read EEF pose + gripper → state 7-dim
     c. POST to VLA server → EEF delta 7-dim
     d. 역정규화 → current EEF + delta → move_line()
     e. gripper close threshold 도달 시 종료
5. report success / failure

Run
---
  python3 grasp_pipeline_eef.py
"""

from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import rclpy
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController
from grasp_vla.smolvla_client import SmolVLAClient

# LIBERO 학습 데이터 state 분포 (policy_preprocessor safetensors에서 추출)
# observation.state: [x_m, y_m, z_m, rx_rad, ry_rad, rz_rad]
_LIBERO_STATE_MEAN = np.array([-0.04652, 0.03441, 0.76455, 2.97221, -0.22047, -0.12558], dtype=np.float32)
_LIBERO_STATE_STD  = np.array([ 0.10494, 0.15177, 0.37852, 0.34427,  0.90695,  0.32539], dtype=np.float32)

# 우리 Doosan 로봇의 작업 공간 state 분포 (m/rad 단위, 홈포즈 기준)
# 홈포즈: J=[0,0,90,0,90,0]° → EEF x=373mm, y=0mm, z=245mm, rx≈176°, ry=+180°, rz≈176°
# ※ ry=±180° gimbal lock 구간으로 rx/rz는 실행마다 달라질 수 있음 → 각도 wrapping으로 처리
_OUR_STATE_MEAN = np.array([ 0.30,   0.00,  0.15,   3.08,   3.14,   3.08], dtype=np.float32)
_OUR_STATE_STD  = np.array([ 0.08,   0.05,  0.10,   0.20,   0.20,   0.20], dtype=np.float32)


class GraspPipelineEEFNode(Node):
    def __init__(self):
        super().__init__("grasp_pipeline_eef")

        self._declare("smolvla_url",         "http://192.168.50.79:16003")
        self._declare("instruction",         "Approach the red object closely")
        self._declare("max_steps",           10)
        self._declare("step_hz",             1)
        self._declare("gripper_port",        "/dev/ttyUSB0")
        self._declare("robot_id",            "dsr01")
        self._declare("home_pose",           "")        # "j1,j2,...,j6" degrees; "" = skip
        self._declare("camera_topic",        "")
        self._declare("depth_topic",         "")
        self._declare("min_grasp_step",      5)
        self._declare("gripper_close_ratio", 0.85)
        self._declare("record_video",        True)
        self._declare("video_save_dir",      "/home/user/robot_workspace/vla_ws/logs/videos")
        # stats.json 없으면 역정규화 생략 (identity)
        self._declare("stats_path",          "")
        # EEF delta 클리핑 (안전 범위)
        self._declare("max_pos_delta_mm",    50.0)      # 한 스텝 최대 xy 위치 변화량 (mm)
        self._declare("max_z_delta_mm",      100.0)     # 한 스텝 최대 z 위치 변화량 (mm) — xy보다 크게
        self._declare("max_rot_delta_deg",   10.0)      # 한 스텝 최대 자세 변화량 (deg)

        url         = self.get_parameter("smolvla_url").value
        gport       = self.get_parameter("gripper_port").value
        robot_id    = self.get_parameter("robot_id").value
        cam_topic   = self.get_parameter("camera_topic").value
        depth_topic = self.get_parameter("depth_topic").value

        self._vla     = SmolVLAClient(base_url=url)
        self._camera  = CameraNode(
            ros_image_topic=cam_topic   if cam_topic   else None,
            ros_depth_topic=depth_topic if depth_topic else None,
            ros_node=self  if cam_topic else None,
        )
        self._robot   = DoosanController(self, robot_id=robot_id, action_mode="cartesian")
        self._gripper = GripperController(port=gport, ros_node=self, robot_id=robot_id)

        self.get_logger().info("GraspPipelineEEFNode initialized.")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def execute_grasp(self, instruction: Optional[str] = None) -> bool:
        instruction     = instruction or self.get_parameter("instruction").value
        max_steps       = self.get_parameter("max_steps").value
        step_period     = 1.0 / self.get_parameter("step_hz").value
        close_ratio_thr = self.get_parameter("gripper_close_ratio").value
        min_grasp       = self.get_parameter("min_grasp_step").value
        max_pos         = self.get_parameter("max_pos_delta_mm").value
        max_z           = self.get_parameter("max_z_delta_mm").value
        max_rot         = self.get_parameter("max_rot_delta_deg").value

        # 1. Health check
        if not self._vla.health():
            self.get_logger().error(f"VLA server not reachable: {self._vla.base_url}")
            return False
        self.get_logger().info(f'VLA OK. Instruction: "{instruction}"')

        # 2. Wait for camera
        deadline = time.time() + 10.0
        while not self._camera.ready:
            self._camera.grab()
            if time.time() > deadline:
                self.get_logger().error("Camera timeout.")
                return False
        self.get_logger().info("Camera ready.")

        # 3. Open gripper
        self._gripper.open()

        # 4. Home pose
        home_str = self.get_parameter("home_pose").value
        if home_str:
            home = [float(x) for x in home_str.split(',')]
            self.get_logger().info(f"Moving to home: {home}")
            self._robot.move_joint(home, velocity=30.0, acceleration=60.0)

        # 5. Load stats (optional)
        # 6. VLA loop
        self.get_logger().info("Starting EEF-delta VLA loop …")
        reset   = True
        grasped = False
        record_video = self.get_parameter("record_video").value
        video_frames = []

        for step in range(max_steps):
            t0 = time.time()
            self.get_logger().info(f"{'━'*30} Step {step:02d}/{max_steps} {'━'*30}")

            # 6a. Camera
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                self.get_logger().warn(f"Step {step}: no frame, skipping.")
                continue
            if record_video:
                video_frames.append(rgb.copy())

            # 6b. State: EEF pose → LIBERO 단위(m/rad)로 변환 후 전송
            eef = self._robot.get_eef_pose()   # Doosan: [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]
            if eef is None:
                self.get_logger().warn(f"Step {step}: EEF pose unavailable, skipping.")
                continue

            # 단위 변환: Doosan mm/deg → m/rad
            state_mrad = np.empty(6, dtype=np.float32)
            state_mrad[:3] = eef[:3] / 1000.0
            state_mrad[3:6] = np.radians(eef[3:6])

            # state 캘리브레이션: 위치만 affine 매핑, 자세는 LIBERO mean 고정
            # gimbal lock(ry=±180°) 구간에서 rx/rz가 신뢰 불가능하므로 orientation은 보정하지 않음
            state = _LIBERO_STATE_MEAN.copy()
            diff_pos = state_mrad[:3] - _OUR_STATE_MEAN[:3]
            state[:3] = _LIBERO_STATE_MEAN[:3] + diff_pos / _OUR_STATE_STD[:3] * _LIBERO_STATE_STD[:3]

            self.get_logger().info(
                f"  EEF(mm/°) x={eef[0]:.1f} y={eef[1]:.1f} z={eef[2]:.1f} "
                f"rx={eef[3]:.1f} ry={eef[4]:.1f} rz={eef[5]:.1f}"
            )
            self.get_logger().info(
                f"  state(calib) {np.round(state, 4).tolist()}"
            )

            # 6c. VLA predict
            try:
                result = self._vla.predict(
                    state=state,
                    image_top=rgb,
                    instruction=instruction,
                    reset_episode=reset,
                )
                reset = False
                action = result.action   # shape (7,) LIBERO 단위: [Δx_m, Δy_m, Δz_m, Δrx_rad, Δry_rad, Δrz_rad, grip]
                self.get_logger().info(
                    f"  action(m/rad) {np.round(action, 4).tolist()}  ({result.latency_ms:.0f}ms)"
                )
            except Exception as e:
                self.get_logger().error(f"Step {step}: VLA error: {e}")
                break

            # 6d. LIBERO 정규화 제어신호 → Doosan delta 변환
            # 좌표계 remapping: LIBERO(Franka) 접근 방향(-x) = Doosan 앞(+y)
            # z는 별도 스케일(max_z)로 하강 신호를 강조
            pos_delta = np.array([
                 action[1] * max_pos,   # LIBERO y → Doosan x (횡방향)
                -action[0] * max_pos,   # LIBERO -x(앞) → Doosan +y(앞)
                 action[2] * max_z,     # LIBERO z → Doosan z (별도 스케일)
            ], dtype=np.float32)
            rot_raw = action[3:6] * max_rot  # deg, LIBERO frame
            rot_delta = np.array([
                 rot_raw[1],   # LIBERO ry → Doosan rx
                -rot_raw[0],   # LIBERO rx → Doosan ry
                 rot_raw[2],   # LIBERO rz → Doosan rz
            ], dtype=np.float32)
            self.get_logger().info(
                f"  delta(mm/°) Δx={pos_delta[0]:.2f} Δy={pos_delta[1]:.2f} Δz={pos_delta[2]:.2f} "
                f"Δrx={rot_delta[0]:.2f} Δry={rot_delta[1]:.2f} Δrz={rot_delta[2]:.2f}  grip={action[6]:.3f}"
            )

            # 6e. 목표 EEF = 현재 EEF(mm/°) + delta(mm/°)
            target_eef = eef.copy()
            target_eef[:3] += pos_delta
            target_eef[3:] += rot_delta
            self.get_logger().info(
                f"  target EEF  x={target_eef[0]:.1f} y={target_eef[1]:.1f} z={target_eef[2]:.1f} "
                f"rx={target_eef[3]:.1f} ry={target_eef[4]:.1f} rz={target_eef[5]:.1f}"
            )
            self._robot.move_line(target_eef.tolist(), velocity=20.0, acceleration=40.0)

            # 6f. 그리퍼
            grip_ratio = float(np.clip(action[6], 0.0, 1.0))
            self._gripper.set_ratio(grip_ratio)
            self.get_logger().info(
                f"  gripper  {grip_ratio:.3f}  ({int(grip_ratio*740)}/740)"
            )

            if grip_ratio >= close_ratio_thr and step >= min_grasp and not grasped:
                grasped = True
                self.get_logger().info(f"Step {step}: grasp detected. Retreating …")
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

    def _load_stats(self) -> tuple[np.ndarray, np.ndarray]:
        """stats.json 로드. 없으면 identity (mean=0, std=1) 반환."""
        stats_path = self.get_parameter("stats_path").value
        if stats_path:
            try:
                with open(stats_path) as f:
                    s = json.load(f)
                mean = np.array(s["action"]["mean"], dtype=np.float32)
                std  = np.array(s["action"]["std"],  dtype=np.float32)
                self.get_logger().info(f"Stats loaded: {stats_path}")
                return mean, std
            except Exception as e:
                self.get_logger().warn(f"Stats 로드 실패 ({e}). 역정규화 생략.")
        else:
            self.get_logger().warn("stats_path 미설정. 역정규화 생략.")
        return np.zeros(7, dtype=np.float32), np.ones(7, dtype=np.float32)

    def _retreat(self) -> None:
        eef = self._robot.get_eef_pose()
        if eef is None:
            return
        target = eef.copy()
        target[2] += 100.0   # z 방향으로 100mm 후퇴
        self._robot.move_line(target.tolist(), velocity=30.0, acceleration=60.0)
        self.get_logger().info("Retreat complete.")

    def _save_video(self, frames: list) -> None:
        save_dir = Path(self.get_parameter("video_save_dir").value)
        save_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = save_dir / f"episode_eef_{ts}.mp4"
        h, w = frames[0].shape[:2]
        cmd = [
            'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
            '-s', f'{w}x{h}', '-pix_fmt', 'rgb24',
            '-r', str(self.get_parameter("step_hz").value),
            '-i', 'pipe:0',
            '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            str(out_path),
        ]
        import subprocess
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        for frame in frames:
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        proc.wait()
        self.get_logger().info(f"영상 저장: {out_path} ({len(frames)} frames)")

    def _declare(self, name: str, default) -> None:
        self.declare_parameter(name, default, ParameterDescriptor(description=name))


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = GraspPipelineEEFNode()

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
