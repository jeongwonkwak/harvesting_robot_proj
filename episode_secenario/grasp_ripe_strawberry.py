#!/usr/bin/env python3
"""
grasp_ripe_strawberry.py

에피소드 시나리오: 익은 딸기(ripe_strawberry) 검출 → 접근 → 파지 → 후퇴

실행:
  python3 episode_secenario/grasp_ripe_strawberry.py

사전 조건:
  - 로봇 bringup 실행 중 (dsr01)
  - RealSense D455 연결됨
  - dynamixel_sdk 설치됨 (그리퍼 실제 제어 시)
"""

import sys
import time
import threading
import numpy as np
import cv2

# ROS2
import rclpy
from rclpy.executors import MultiThreadedExecutor

# grasp_vla 패키지 경로 추가
sys.path.insert(0, '/home/user/robot_workspace/vla_ws')
sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController

from scipy.spatial.transform import Rotation as R
from ultralytics import YOLO

# ── 설정 ─────────────────────────────────────────────────────────────────────

YOLO_MODEL   = "/home/user/robot_workspace/vla_ws/models/strawberry_yolo26m_unified/weights/best.pt"
CALIB_PATH   = (
    "/home/user/robot_workspace/sim2real/sim2real/calibration"
    "/config/20260515_145627/calibration_eye_in_hand.npz"
)

GRIPPER_PORT      = "/dev/ttyUSB0"
ROBOT_ID          = "dsr01"
CONF_THRESHOLD    = 0.3      # YOLO 최소 신뢰도
PRE_GRASP_Z_OFFSET = 80.0   # 파지 전 물체 위 높이 (mm)
GRASP_Z_OFFSET     = 10.0   # 파지 시 물체 위 높이 (mm)
RETREAT_DELTA      = [-150.0, 0.0, 0.0, 0.0, 0.0, 0.0]   # 후퇴 델타 (mm)

# ── ROS2 노드 ─────────────────────────────────────────────────────────────────

class StrawberryGraspNode:
    def __init__(self):
        rclpy.init()
        self._node = rclpy.create_node("strawberry_grasp_episode")
        self._executor = MultiThreadedExecutor(num_threads=4)
        self._executor.add_node(self._node)

        self._logger = self._node.get_logger()

        # 카메라 (ROS2 토픽 구독 – bag recorder와 동일한 소스)
        self._camera = CameraNode(
            ros_image_topic="/camera/camera/color/image_raw",
            ros_depth_topic="/camera/camera/aligned_depth_to_color/image_raw",
            ros_node=self._node,
        )

        # 로봇 / 그리퍼
        self._robot   = DoosanController(self._node, robot_id=ROBOT_ID, action_mode="cartesian")
        self._gripper = GripperController(port=GRIPPER_PORT)

        # YOLO 모델
        self._logger.info(f"YOLO 로드: {YOLO_MODEL}")
        self._yolo = YOLO(YOLO_MODEL)

        # 시각화 스레드
        self._vis_running = False
        self._vis_thread: threading.Thread = None

        # 캘리브레이션
        data = np.load(CALIB_PATH)
        self._T_cam_to_grip = data['T_cam_to_gripper']   # (4, 4)
        K = data['camera_matrix']
        self._fx, self._fy = K[0, 0], K[1, 1]
        self._cx, self._cy = K[0, 2], K[1, 2]
        self._logger.info("캘리브레이션 로드 완료.")

    # ── 시각화 스레드 ─────────────────────────────────────────────────────────

    def _vis_loop(self):
        """백그라운드에서 카메라 프레임에 YOLO 박스를 그려 화면에 표시."""
        CLASS_COLORS = {0: (0, 200, 0), 1: (0, 0, 255)}  # unripe=green, ripe=red (BGR)
        cv2.namedWindow("Strawberry Detection (q=quit)", cv2.WINDOW_NORMAL)
        while self._vis_running:
            rgb, depth = self._camera.get_images()
            if rgb is None:
                time.sleep(0.05)
                continue

            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            results = self._yolo.predict(rgb, verbose=False, conf=CONF_THRESHOLD)
            boxes = results[0].boxes

            for box in boxes:
                cls_id = int(box.cls[0])
                conf   = float(box.conf[0])
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                color = CLASS_COLORS.get(cls_id, (200, 200, 200))
                thickness = 3 if cls_id == 1 else 2

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

                u = (x1 + x2) // 2
                v = (y1 + y2) // 2
                cv2.circle(frame, (u, v), 5, color, -1)

                label = f"{self._yolo.names[cls_id]} {conf:.2f}"
                if depth is not None:
                    r = 5
                    roi   = depth[max(0, v-r):v+r+1, max(0, u-r):u+r+1]
                    valid = roi[roi > 0]
                    if len(valid) > 0:
                        z_mm = float(np.median(valid))
                        label += f"  d={z_mm:.0f}mm"

                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
                ty = max(y1 - 6, th + 4)
                cv2.rectangle(frame, (x1, ty - th - 4), (x1 + tw + 4, ty + 2), color, -1)
                cv2.putText(frame, label, (x1 + 2, ty - 1),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("Strawberry Detection (q=quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self._vis_running = False
                break

        cv2.destroyAllWindows()

    def start_visualization(self):
        self._vis_running = True
        self._vis_thread = threading.Thread(target=self._vis_loop, daemon=True)
        self._vis_thread.start()

    def stop_visualization(self):
        self._vis_running = False
        if self._vis_thread and self._vis_thread.is_alive():
            self._vis_thread.join(timeout=2.0)

    # ── 메인 에피소드 ─────────────────────────────────────────────────────────

    def run(self) -> bool:
        self._logger.info("=" * 50)
        self._logger.info(" 에피소드 시작: 익은 딸기 파지")
        self._logger.info("=" * 50)

        self.start_visualization()

        # 1. 카메라 준비
        self._logger.info("[1/5] 카메라 프레임 대기 …")
        deadline = time.time() + 15.0
        while not self._camera.ready:
            self._executor.spin_once(timeout_sec=0.1)
            if time.time() > deadline:
                self._logger.error("카메라 타임아웃.")
                return False
        self._executor.spin_once(timeout_sec=0.1)
        rgb, depth = self._camera.get_images()
        if rgb is None or depth is None:
            self._logger.error("RGB/Depth 프레임 없음.")
            return False

        # 2. YOLO 딸기 검출
        self._logger.info("[2/5] 익은 딸기 검출 …")
        obj_mm = self._detect_strawberry_3d(rgb, depth)
        if obj_mm is None:
            self._logger.error("딸기 미검출. 에피소드 종료.")
            return False
        self._logger.info(f"  딸기 위치 (로봇 베이스): {np.round(obj_mm, 1).tolist()} mm")

        # 3. 그리퍼 열기
        self._logger.info("[3/5] 그리퍼 열기 …")
        self._gripper.open()
        time.sleep(0.3)

        # 현재 EEF 자세 (회전 유지)
        eef = self._robot.get_eef_pose()
        if eef is None:
            self._logger.error("EEF pose 획득 실패.")
            return False
        rot = eef[3:].tolist()   # [Rx, Ry, Rz] ZYZ degrees

        # 4. 접근 – pre-grasp (물체 위 80mm)
        pre = [obj_mm[0], obj_mm[1], obj_mm[2] + PRE_GRASP_Z_OFFSET] + rot
        self._logger.info(f"[4/5] Pre-grasp 이동 → {np.round(pre[:3], 1).tolist()} mm")
        self._robot.move_line(pre, velocity=30.0, acceleration=60.0)

        # 4b. 하강 – grasp
        grasp = [obj_mm[0], obj_mm[1], obj_mm[2] + GRASP_Z_OFFSET] + rot
        self._logger.info(f"       하강 → {np.round(grasp[:3], 1).tolist()} mm")
        self._robot.move_line(grasp, velocity=15.0, acceleration=30.0)

        # 5. 그리퍼 닫기 → 후퇴
        self._logger.info("[5/5] 그리퍼 닫기 …")
        self._gripper.close()
        time.sleep(0.8)

        self._logger.info("후퇴 …")
        self._retreat(eef)

        self._logger.info("=" * 50)
        self._logger.info(" 에피소드 완료: 파지 성공")
        self._logger.info("=" * 50)
        return True

    # ── 딸기 검출 + 3D 변환 ───────────────────────────────────────────────────

    def _detect_strawberry_3d(self, rgb: np.ndarray, depth: np.ndarray):
        results = self._yolo.predict(rgb, verbose=False, conf=CONF_THRESHOLD)
        boxes   = results[0].boxes

        # ripe_strawberry(1) 만 사용
        best_box, best_conf = None, 0.0
        for box in boxes:
            if int(box.cls[0]) == 1 and float(box.conf[0]) > best_conf:
                best_box  = box
                best_conf = float(box.conf[0])
        if best_box is None:
            self._logger.warn("ripe_strawberry 미검출 – 에피소드 종료.")
            return None

        x1, y1, x2, y2 = best_box.xyxy[0].tolist()
        u = int((x1 + x2) / 2)
        v = int((y1 + y2) / 2)
        cls_name = self._yolo.names[int(best_box.cls[0])]
        self._logger.info(
            f"  {cls_name} conf={best_conf:.2f}  "
            f"bbox=[{int(x1)},{int(y1)},{int(x2)},{int(y2)}]  중심=({u},{v})"
        )

        # Depth 샘플링 (11×11 패치 중앙값)
        r = 5
        roi   = depth[max(0, v-r):v+r+1, max(0, u-r):u+r+1]
        valid = roi[roi > 0]
        if len(valid) == 0:
            self._logger.warn("유효 depth 없음.")
            return None
        Z_m = float(np.median(valid)) / 1000.0   # mm → m
        if not (0.05 < Z_m < 1.5):
            self._logger.warn(f"Depth 범위 초과: {Z_m*1000:.1f} mm")
            return None
        self._logger.info(f"  Depth: {Z_m*1000:.1f} mm")

        # 카메라 좌표 → 그리퍼 좌표
        P_cam  = np.array([(u - self._cx) * Z_m / self._fx,
                           (v - self._cy) * Z_m / self._fy,
                           Z_m, 1.0])
        P_grip = self._T_cam_to_grip @ P_cam   # (4,)  metres

        # 그리퍼 좌표 → 로봇 베이스 좌표 (ZYZ Euler)
        eef   = self._robot.get_eef_pose()
        if eef is None:
            return None
        R_mat = R.from_euler('ZYZ', eef[3:], degrees=True).as_matrix()
        t_m   = eef[:3] / 1000.0

        P_base_m = R_mat @ P_grip[:3] + t_m
        return P_base_m * 1000.0   # m → mm

    # ── 후퇴 ─────────────────────────────────────────────────────────────────

    def _retreat(self, eef: np.ndarray) -> None:
        delta = np.array(RETREAT_DELTA)
        if not any(delta):
            return
        target = (eef + delta).tolist()
        self._logger.info(f"  Cartesian 후퇴 → {np.round(target[:3], 1).tolist()}")
        self._robot.move_line(target, velocity=30.0, acceleration=60.0)

    # ── 정리 ─────────────────────────────────────────────────────────────────

    def shutdown(self):
        self.stop_visualization()
        self._camera.release()
        self._node.destroy_node()
        rclpy.shutdown()


# ── 실행 ─────────────────────────────────────────────────────────────────────

def main():
    episode = StrawberryGraspNode()
    try:
        success = episode.run()
        print(f"\n에피소드 결과: {'성공' if success else '실패'}")
    except KeyboardInterrupt:
        print("\n중단됨.")
    finally:
        episode.shutdown()


if __name__ == "__main__":
    main()
