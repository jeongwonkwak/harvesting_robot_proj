"""
GraspPipelineNode – main ROS2 node that drives the full grasp sequence.

Flow per episode
----------------
1. health-check SmolVLA server
2. open gripper
3. (optional) move to a user-defined pre-grasp home pose
4. VLA control loop  ←  repeats for max_steps
     a. capture RGB frame from D455
     b. read joint positions from Doosan e0509
     c. POST to SmolVLA server  →  6-DoF action
     d. execute action on robot
     e. if close_trigger_step reached → close gripper → done
5. report success / failure

Run
---
  ros2 run grasp_vla grasp_pipeline_node
or
  ros2 launch grasp_vla grasp.launch.py instruction:="pick up the silver connector"
"""

from __future__ import annotations

import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import rclpy
from rcl_interfaces.msg import ParameterDescriptor, ParameterType
from rclpy.node import Node
from scipy.spatial.transform import Rotation as R

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController
from grasp_vla.smolvla_client import SmolVLAClient

_CALIB_PATH = (
    "/home/user/robot_workspace/sim2real/sim2real/calibration"
    "/config/20260515_145627/calibration_eye_in_hand.npz"
)
_YOLO_MODEL_PATH = (
    "/home/user/robot_workspace/vla_ws/models"
    "/strawberry_yolo26m_unified/weights/stem_best.pt"
)


class GraspPipelineNode(Node):
    def __init__(self):
        super().__init__("grasp_pipeline")

        # ----------------------------------------------------------------
        # Declare ROS2 parameters (overridable from launch / yaml)
        # ----------------------------------------------------------------
        self._declare("smolvla_url",     "http://192.168.50.79:16003")
        self._declare("instruction",     "Approach the red object closely and pick it up.")
        self._declare("action_mode",     "cartesian")   # "cartesian" | "joint"
        self._declare("max_steps",       30)
        self._declare("step_hz",         10)           # control frequency
        self._declare("gripper_port",    "/dev/ttyUSB0")
        self._declare("robot_id",        "dsr01")
        self._declare("home_pose",       "")             # "" = skip; "j1,j2,j3,j4,j5,j6" (degrees)
        self._declare("retreat_delta",   [-150.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self._declare("camera_topic",    "")            # ROS2 image topic; "" = use direct camera
        self._declare("depth_topic",     "")            # ROS2 depth topic; "" = use direct camera
        self._declare("mode",            "vla")         # "vla" | "vision"
        self._declare("min_grasp_step",  2)             # 이 스텝 이전에는 그리퍼 close 무시
        self._declare("gripper_close_ratio", 0.85)   # 이 ratio 이상이면 grasp 완료로 판단
        self._declare("record_video",    True)          # 에피소드 영상 저장 여부
        self._declare("video_save_dir",  "/home/user/robot_workspace/vla_ws/logs/videos")

        # ----------------------------------------------------------------
        # Instantiate sub-components
        # ----------------------------------------------------------------
        url       = self.get_parameter("smolvla_url").value
        gport     = self.get_parameter("gripper_port").value
        robot_id  = self.get_parameter("robot_id").value
        act_mode  = self.get_parameter("action_mode").value
        cam_topic   = self.get_parameter("camera_topic").value
        depth_topic = self.get_parameter("depth_topic").value

        self._vla     = SmolVLAClient(base_url=url)
        self._camera  = CameraNode(
            ros_image_topic=cam_topic   if cam_topic   else None,
            ros_depth_topic=depth_topic if depth_topic else None,
            ros_node=self if cam_topic else None,
        )
        self._robot   = DoosanController(self, robot_id=robot_id, action_mode=act_mode)
        self._gripper = GripperController(port=gport, ros_node=self, robot_id=robot_id)

        # ----------------------------------------------------------------
        # Load hand-eye calibration (eye-in-hand)
        # ----------------------------------------------------------------
        self._T_cam_to_grip: Optional[np.ndarray] = None
        self._cam_intr: Optional[dict] = None
        try:
            data = np.load(_CALIB_PATH)
            self._T_cam_to_grip = data['T_cam_to_gripper']   # (4, 4)
            K = data['camera_matrix']                         # (3, 3)
            self._cam_intr = dict(fx=K[0,0], fy=K[1,1], cx=K[0,2], cy=K[1,2])
            self.get_logger().info("Hand-eye calibration loaded.")
        except Exception as e:
            self.get_logger().warn(f"Calibration not loaded: {e}")

        # ----------------------------------------------------------------
        # Load YOLO strawberry detector
        # ----------------------------------------------------------------
        self._yolo = None
        try:
            from ultralytics import YOLO as _YOLO
            self._yolo = _YOLO(_YOLO_MODEL_PATH)
            self.get_logger().info(f"YOLO model loaded: {_YOLO_MODEL_PATH}")
        except Exception as e:
            self.get_logger().warn(f"YOLO not loaded: {e}")

        self.get_logger().info("GraspPipelineNode initialised. Call execute_grasp() to start.")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def execute_grasp(self, instruction: Optional[str] = None) -> bool:
        """
        Run a full grasp episode.
        Returns True if the episode completed without error.
        """
        instruction = instruction or self.get_parameter("instruction").value
        max_steps        = self.get_parameter("max_steps").value
        step_period      = 1.0 / self.get_parameter("step_hz").value
        close_ratio_thr  = self.get_parameter("gripper_close_ratio").value

        # 1. Health check
        if not self._vla.health():
            self.get_logger().error(f"SmolVLA server not reachable: {self._vla.base_url}")
            return False
        self.get_logger().info(f'SmolVLA OK. Instruction: "{instruction}"')

        # 2. Wait for first camera frame
        self.get_logger().info("Waiting for camera frames …")
        deadline = time.time() + 10.0
        while not self._camera.ready:
            self._camera.grab()
            if time.time() > deadline:
                self.get_logger().error("Camera timeout – check camera (device 6).")
                return False
        self.get_logger().info("Camera ready.")

        # 3. Open gripper
        self.get_logger().info("Opening gripper …")
        self._gripper.open()

        # 4. Optional: move to pre-grasp home pose
        home_str = self.get_parameter("home_pose").value
        if home_str:
            home = [float(x) for x in home_str.split(',')]
            self.get_logger().info(f"Moving to home pose: {home}")
            self._robot.move_joint(home, velocity=30.0, acceleration=60.0)

        # 5. VLA control loop
        self.get_logger().info("Starting VLA control loop …")
        min_grasp = self.get_parameter("min_grasp_step").value
        reset = True
        grasped = False

        # 영상 녹화 준비
        record_video = self.get_parameter("record_video").value
        video_frames = []

        for step in range(max_steps):
            t0 = time.time()
            self.get_logger().info(f"{'━'*30} Step {step:02d} / {max_steps} {'━'*30}")

            # 5a. Get camera image
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                self.get_logger().warn(f"Step {step}: no camera frame, skipping.")
                continue

            if record_video:
                video_frames.append(rgb.copy())

            # 5b. Get robot state (joint 6 + gripper 1 = 7-dim)
            joint_state = self._robot.get_joint_state()
            if joint_state is None:
                self.get_logger().warn(f"Step {step}: no joint state, using zeros.")
                joint_state = np.zeros(6, dtype=np.float64)
            joint_state_deg = np.degrees(joint_state[:6])   # 로그 표시용
            gripper_pos = self._gripper.get_position()        # [0.0, 1.0]
            state7 = np.append(joint_state[:6], gripper_pos).astype(np.float32)

            j = np.round(joint_state_deg, 2).tolist()
            self.get_logger().info(
                f"  현재 관절(°)  {j}  grip={gripper_pos:.3f}"
            )

            # 5c. Call SmolVLA
            try:
                result = self._vla.predict(
                    state=state7,
                    image_top=rgb,
                    instruction=instruction,
                    reset_episode=reset,
                )
                reset = False
                action = result.action  # shape (7,)
                a = np.round(action, 3).tolist()
                self.get_logger().info(
                    f"  모델 액션     {a[:6]}  grip={a[6]}  ({result.latency_ms:.0f}ms)"
                )
            except Exception as e:
                self.get_logger().error(f"Step {step}: VLA call failed: {e}")
                break

            # 5d. 절대 관절 위치로 이동 (서버가 postprocessor에서 역정규화 완료)
            a_deg = np.degrees(action[:6])
            self.get_logger().info(
                f"  액션(°)       {np.round(a_deg, 2).tolist()}  grip={action[6]:.3f}"
            )
            self._robot.move_joint(
                a_deg.tolist(),
                velocity=20.0,
                acceleration=40.0,
            )

            # 5e. 그리퍼 (0~1 ratio로 클램프)
            grip_ratio = max(0.0, min(1.0, float(action[6])))
            self._gripper.set_ratio(grip_ratio)
            self.get_logger().info(
                f"  그리퍼        {action[6]:+.4f}  →  ratio={grip_ratio:.3f}  ({int(grip_ratio * 740)}/740)"
            )

            if grip_ratio >= close_ratio_thr and step >= min_grasp and not grasped:
                grasped = True
                self.get_logger().info(
                    f"Step {step}: grasp detected (ratio={grip_ratio:.2f}). Retreating …"
                )
                self._retreat()
                break

            # Rate limiting
            elapsed = time.time() - t0
            sleep_t = step_period - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

        # 영상 저장
        if record_video and video_frames:
            self._save_video(video_frames)

        return grasped

    def _save_video(self, frames: list) -> None:
        save_dir = Path(self.get_parameter("video_save_dir").value)
        save_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = save_dir / f"episode_{ts}.mp4"

        h, w = frames[0].shape[:2]
        cmd = [
            'ffmpeg', '-y',
            '-f', 'rawvideo', '-vcodec', 'rawvideo',
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
        self.get_logger().info(f"영상 저장 완료: {out_path}  ({len(frames)} frames)")

    # ------------------------------------------------------------------
    # Vision-based grasp
    # ------------------------------------------------------------------

    def approach_and_grasp_red(
        self,
        pre_grasp_z_offset: float = 80.0,
        grasp_z_offset: float = 10.0,
    ) -> bool:
        """HSV 빨간 물체 검출 + 캘리브레이션으로 파지. 학습 데이터 수집용."""
        if self._T_cam_to_grip is None:
            self.get_logger().error("캘리브레이션 없음 – vision grasp 불가.")
            return False

        self.get_logger().info("카메라 프레임 대기 …")
        deadline = time.time() + 10.0
        while not self._camera.ready:
            self._camera.grab()
            if time.time() > deadline:
                self.get_logger().error("카메라 타임아웃.")
                return False
        self._camera.grab()
        rgb, depth = self._camera.get_images()

        if rgb is None:
            self.get_logger().error("RGB 프레임 없음.")
            return False
        if depth is None:
            self.get_logger().error("Depth 프레임 없음 – depth_topic 설정 확인.")
            return False

        obj_mm = self._detect_red_3d(rgb, depth)
        if obj_mm is None:
            self.get_logger().error("빨간 물체 미검출.")
            return False
        self.get_logger().info(f"물체 위치 (로봇 베이스): {np.round(obj_mm, 1).tolist()} mm")

        eef = self._robot.get_eef_pose()
        if eef is None:
            self.get_logger().error("EEF pose 획득 실패.")
            return False
        rot = eef[3:].tolist()

        # 그리퍼 열기
        self._gripper.open()
        time.sleep(0.3)

        # pre-grasp: 물체 위 80mm
        pre = [obj_mm[0], obj_mm[1], obj_mm[2] + pre_grasp_z_offset] + rot
        self.get_logger().info(f"Pre-grasp 이동 → {np.round(pre[:3], 1).tolist()} mm")
        self._robot.move_line(pre, velocity=30.0, acceleration=60.0)

        # 하강
        grasp = [obj_mm[0], obj_mm[1], obj_mm[2] + grasp_z_offset] + rot
        self.get_logger().info(f"파지 하강 → {np.round(grasp[:3], 1).tolist()} mm")
        self._robot.move_line(grasp, velocity=15.0, acceleration=30.0)

        # 그리퍼 닫기
        self.get_logger().info("그리퍼 닫기 …")
        self._gripper.close()
        time.sleep(0.8)

        self._retreat()
        return True

    def _detect_red_3d(self, rgb: np.ndarray, depth: np.ndarray) -> Optional[np.ndarray]:
        """
        YOLO로 딸기(ripe_strawberry) 검출 후 로봇 베이스 좌표 (mm) 반환.
        Doosan EEF 회전 표현: ZYZ Euler (degrees).
        """
        if self._yolo is None:
            self.get_logger().error("YOLO 모델 미로드.")
            return None

        # YOLO 추론 (RGB → BGR 변환 불필요, ultralytics는 RGB 직접 지원)
        results = self._yolo.predict(rgb, verbose=False, conf=0.3)
        boxes = results[0].boxes

        # stem(0) 만 사용
        best_box = None
        best_conf = 0.0
        for box in boxes:
            if int(box.cls[0]) == 0 and float(box.conf[0]) > best_conf:
                best_box  = box
                best_conf = float(box.conf[0])

        if best_box is None:
            self.get_logger().warn("YOLO: stem 미검출 – 에피소드 종료.")
            return None

        x1, y1, x2, y2 = best_box.xyxy[0].tolist()
        u = int((x1 + x2) / 2)
        v = int((y1 + y2) / 2)
        cls_name = self._yolo.names[int(best_box.cls[0])]
        self.get_logger().info(f"  YOLO 검출: {cls_name} conf={best_conf:.2f}  bbox=[{int(x1)},{int(y1)},{int(x2)},{int(y2)}]  중심=({u},{v})")

        r = 5
        roi = depth[max(0, v-r):v+r+1, max(0, u-r):u+r+1]
        valid = roi[roi > 0]
        if len(valid) == 0:
            self.get_logger().warn("유효 depth 없음.")
            return None
        Z_m = float(np.median(valid)) / 1000.0   # mm → m
        if not (0.05 < Z_m < 1.5):
            self.get_logger().warn(f"Depth 범위 초과: {Z_m*1000:.1f} mm")
            return None
        self.get_logger().info(f"  Depth: {Z_m*1000:.1f} mm")

        fx = self._cam_intr['fx']; fy = self._cam_intr['fy']
        cx = self._cam_intr['cx']; cy = self._cam_intr['cy']
        P_cam = np.array([(u - cx) * Z_m / fx,
                          (v - cy) * Z_m / fy,
                          Z_m, 1.0])

        P_grip = self._T_cam_to_grip @ P_cam         # 카메라 → 그리퍼 (m)

        eef = self._robot.get_eef_pose()             # [X_mm, Y_mm, Z_mm, Rx, Ry, Rz]
        if eef is None:
            return None
        R_mat = R.from_euler('ZYZ', eef[3:], degrees=True).as_matrix()
        t_m   = eef[:3] / 1000.0                    # mm → m

        P_base_m = R_mat @ P_grip[:3] + t_m
        return P_base_m * 1000.0                     # m → mm

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _retreat(self) -> None:
        delta = list(self.get_parameter("retreat_delta").value)
        if not any(delta):
            return

        # 1순위: Cartesian 후퇴 (Doosan 서비스 있을 때)
        current_eef = self._robot.get_eef_pose()
        if current_eef is not None:
            target = (np.array(current_eef) + np.array(delta)).tolist()
            self.get_logger().info(f"Cartesian retreat delta: {delta}")
            self._robot.move_line(target, velocity=30.0, acceleration=60.0)
            self.get_logger().info("Retreat complete.")
            return

        # 2순위: 관절 공간 후퇴 (Doosan 서비스 없을 때)
        current_rad = self._robot.get_joint_state()
        if current_rad is None:
            self.get_logger().error("Cannot get joint state for retreat.")
            return
        import math as _math
        cur = [_math.degrees(j) for j in current_rad]
        # J2 어깨 들어올리기 -20°, J3 팔꿈치 접기 -20° → 벽에서 멀어짐
        retreat = [cur[0], cur[1] - 20.0, cur[2] - 20.0,
                   cur[3], cur[4], cur[5]]
        self.get_logger().info(f"Joint-space retreat: {np.round(retreat, 1).tolist()}")
        self._robot.move_joint(retreat, velocity=30.0, acceleration=60.0)
        self.get_logger().info("Retreat complete.")

    def _declare(self, name: str, default) -> None:
        self.declare_parameter(
            name, default, ParameterDescriptor(description=name))


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = GraspPipelineNode()

    import threading
    from rclpy.executors import MultiThreadedExecutor

    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)

    def run():
        mode = node.get_parameter("mode").value
        if mode == "vision":
            success = node.approach_and_grasp_red()
        else:
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
