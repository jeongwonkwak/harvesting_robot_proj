#!/usr/bin/env python3
"""
Eye-in-Hand 캘리브레이션 스크립트

카메라를 로봇 TCP(그리퍼)에 장착하고, 고정된 ArUco 마커를 기준으로
카메라->그리퍼 간 변환 행렬(T_cam_to_gripper)을 계산합니다.

AX = XB 공식 (OpenCV calibrateHandEye):
    T_A2B @ T_cam2gripper = T_cam2gripper @ T_target2cam

    A: gripper2base (로봇 FK)
    B: target2cam  (ArUco 감지)
    X: cam2gripper (구하고자 하는 값)

준비사항:
    - RealSense 카메라를 로봇 TCP(그리퍼)에 고정 부착
    - ArUco 마커를 작업 공간에 고정 (움직이면 안 됨)
    - 마커가 카메라 시야에 들어오는 여러 자세(최소 5개, 권장 10개 이상)

Usage:
    python eye_in_hand.py                             # 캘리브레이션 수행
    python eye_in_hand.py --test                      # 기존 캘리브레이션 테스트
    python eye_in_hand.py --robot-ip 192.168.137.100 --marker-size 0.1
    python eye_in_hand.py --print-marker --marker-id 0

Output:
    config/<timestamp>/calibration_eye_in_hand.npz
    config/<timestamp>/calibration_eye_in_hand_errors.json
"""

import numpy as np
import cv2
import time
import argparse
import os
import datetime
import json
from typing import Optional, Tuple, List
from dataclasses import dataclass

# RealSense
try:
    import pyrealsense2 as rs
    REALSENSE_AVAILABLE = True
except ImportError:
    REALSENSE_AVAILABLE = False
    print("[Warning] pyrealsense2 not found")

# ArUco
try:
    from cv2 import aruco
    ARUCO_AVAILABLE = True
except ImportError:
    ARUCO_AVAILABLE = False
    print("[Warning] cv2.aruco not found")

from scipy.spatial.transform import Rotation as ScipyR

# 로봇 인터페이스
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from robot_interface import DoosanRobot


def e0509_fk(q_rad: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Doosan E0509 정확한 Forward Kinematics (URDF 기반).

    _simple_fk 대용으로 사용. rotation = np.eye(3) 버그를 수정한 버전.

    Args:
        q_rad: (6,) 관절 각도 (라디안)

    Returns:
        position: (3,) TCP 위치 (미터, 로봇 베이스 기준)
        rotation: (3,3) TCP 회전행렬 (로봇 베이스 기준)
    """
    def _T(xyz, rpy, q=0.0):
        """Trans(xyz) @ Rot_rpy(rpy) @ Rz(q)"""
        M = np.eye(4)
        M[:3, 3] = xyz
        R_fixed = ScipyR.from_euler('xyz', rpy).as_matrix()
        R_joint = ScipyR.from_euler('z', q).as_matrix()
        M[:3, :3] = R_fixed @ R_joint
        return M

    T = np.eye(4)
    T = T @ _T([0,      0,       0.2045], [0,         0,          0      ], q_rad[0])
    T = T @ _T([0,      0,       0     ], [0,        -np.pi/2,   -np.pi/2], q_rad[1])
    T = T @ _T([0.373,  0,       0     ], [0,         0,          np.pi/2], q_rad[2])
    T = T @ _T([0,     -0.373,   0     ], [np.pi/2,   0,          0      ], q_rad[3])
    T = T @ _T([0,      0,       0     ], [-np.pi/2,  0,          0      ], q_rad[4])
    T = T @ _T([0,     -0.1725,  0     ], [np.pi/2,   0,          0      ], q_rad[5])
    T = T @ _T([0,      0,       0     ], [np.pi,    -np.pi/2,    0      ])  # TCP fixed

    return T[:3, 3], T[:3, :3]


@dataclass
class CalibrationConfig:
    """캘리브레이션 설정"""
    # 카메라
    camera_width: int = 640
    camera_height: int = 480
    camera_fps: int = 30

    # ArUco 마커
    marker_id: int = 0
    marker_size: float = 0.1             # 마커 크기 (미터)
    aruco_dict_type: int = aruco.DICT_6X6_250 if ARUCO_AVAILABLE else 0

    # 데이터 수집
    min_samples: int = 5                 # 최소 샘플 수 (calibrateHandEye 최소 요구)
    max_samples: int = 30

    # 로봇
    robot_ip: str = "110.120.1.66"

    # 출력
    output_path: str = "config/calibration_eye_in_hand.npz"

    # hand-eye 캘리브레이션 방법
    # CALIB_HAND_EYE_TSAI, CALIB_HAND_EYE_PARK, CALIB_HAND_EYE_HORAUD,
    # CALIB_HAND_EYE_ANDREFF, CALIB_HAND_EYE_DANIILIDIS
    handeye_method: int = cv2.CALIB_HAND_EYE_TSAI if hasattr(cv2, 'CALIB_HAND_EYE_TSAI') else 0


class ArucoDetector:
    """ArUco 마커 감지기"""

    DICT_TYPES = [
        (aruco.DICT_4X4_50, "4X4_50"),
        (aruco.DICT_4X4_100, "4X4_100"),
        (aruco.DICT_4X4_250, "4X4_250"),
        (aruco.DICT_5X5_50, "5X5_50"),
        (aruco.DICT_5X5_100, "5X5_100"),
        (aruco.DICT_5X5_250, "5X5_250"),
        (aruco.DICT_6X6_50, "6X6_50"),
        (aruco.DICT_6X6_100, "6X6_100"),
        (aruco.DICT_6X6_250, "6X6_250"),
        (aruco.DICT_7X7_50, "7X7_50"),
        (aruco.DICT_ARUCO_ORIGINAL, "ORIGINAL"),
    ] if ARUCO_AVAILABLE else []

    def __init__(self, marker_size: float, dict_type: int = None, auto_detect: bool = True):
        self.marker_size = marker_size
        self.auto_detect = auto_detect and (dict_type is None)
        self.detected_dict_name = None

        if ARUCO_AVAILABLE:
            self.aruco_params = aruco.DetectorParameters()

            if dict_type is not None:
                self.aruco_dict = aruco.getPredefinedDictionary(dict_type)
                self.detector = aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
                self.detectors = None
            else:
                self.detector = None
                self.detectors = []
                for dtype, name in self.DICT_TYPES:
                    d = aruco.getPredefinedDictionary(dtype)
                    detector = aruco.ArucoDetector(d, self.aruco_params)
                    self.detectors.append((detector, name))
        else:
            self.detector = None
            self.detectors = None

    def detect(self, color_image: np.ndarray, camera_matrix: np.ndarray,
               dist_coeffs: np.ndarray, target_id: int = 0) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        ArUco 마커 감지 및 pose 추정

        Returns:
            (rvec, tvec) 또는 None
            - rvec: 마커 회전 벡터 (Rodrigues), 카메라 좌표계 기준
            - tvec: 마커 이동 벡터 (미터), 카메라 좌표계 기준
        """
        corners = None
        ids = None

        if self.detector is not None:
            corners, ids, _ = self.detector.detectMarkers(color_image)
        elif self.detectors is not None:
            for detector, name in self.detectors:
                corners, ids, _ = detector.detectMarkers(color_image)
                if ids is not None and len(ids) > 0:
                    if target_id in ids.flatten():
                        if self.detected_dict_name != name:
                            self.detected_dict_name = name
                            print(f"[ArUco] 딕셔너리 감지: {name}")
                        break
            else:
                return None
        else:
            return None

        if ids is None or len(ids) == 0:
            return None

        target_idx = None
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id == target_id:
                target_idx = i
                break

        if target_idx is None:
            return None

        marker_corners = corners[target_idx].reshape(4, 2)

        half_size = self.marker_size / 2
        object_points = np.array([
            [-half_size,  half_size, 0],
            [ half_size,  half_size, 0],
            [ half_size, -half_size, 0],
            [-half_size, -half_size, 0]
        ], dtype=np.float32)

        success, rvec, tvec = cv2.solvePnP(
            object_points, marker_corners,
            camera_matrix, dist_coeffs
        )

        if not success:
            return None

        return rvec, tvec


class EyeInHandCalibrator:
    """
    Eye-in-Hand 캘리브레이션

    카메라가 TCP에 부착된 구성.
    고정된 ArUco 마커를 여러 자세에서 감지하여
    카메라->그리퍼 변환 행렬(T_cam_to_gripper)을 계산.
    """

    METHODS = {
        'tsai':      cv2.CALIB_HAND_EYE_TSAI      if hasattr(cv2, 'CALIB_HAND_EYE_TSAI')      else 0,
        'park':      cv2.CALIB_HAND_EYE_PARK       if hasattr(cv2, 'CALIB_HAND_EYE_PARK')       else 1,
        'horaud':    cv2.CALIB_HAND_EYE_HORAUD     if hasattr(cv2, 'CALIB_HAND_EYE_HORAUD')     else 2,
        'andreff':   cv2.CALIB_HAND_EYE_ANDREFF    if hasattr(cv2, 'CALIB_HAND_EYE_ANDREFF')    else 3,
        'daniilidis':cv2.CALIB_HAND_EYE_DANIILIDIS if hasattr(cv2, 'CALIB_HAND_EYE_DANIILIDIS') else 4,
    }

    def __init__(self, config: CalibrationConfig = None):
        self.config = config or CalibrationConfig()

        # RealSense
        self.pipeline = None
        self.align = None
        self.camera_matrix = None
        self.dist_coeffs = None

        # ArUco (자동 딕셔너리 탐지)
        self.aruco_detector = ArucoDetector(
            self.config.marker_size,
            dict_type=None,
            auto_detect=True
        )

        # 로봇
        self.robot = None

        # 수집된 데이터
        # Eye-in-Hand: gripper2base (로봇 FK), target2cam (ArUco 감지)
        self.R_gripper2base: List[np.ndarray] = []   # (3,3) list
        self.t_gripper2base: List[np.ndarray] = []   # (3,1) list
        self.R_target2cam:   List[np.ndarray] = []   # (3,3) list
        self.t_target2cam:   List[np.ndarray] = []   # (3,1) list

        # 결과
        self.T_cam_to_gripper: Optional[np.ndarray] = None   # 4x4
        self.T_base_to_target: Optional[np.ndarray] = None   # 4x4 (검증용)
        self.calibration_errors = None

        self.session_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_dir = None

    # ------------------------------------------------------------------ #
    # 카메라                                                               #
    # ------------------------------------------------------------------ #

    def start_camera(self) -> bool:
        if not REALSENSE_AVAILABLE:
            print("[Calibrator] RealSense not available")
            return False

        try:
            self.pipeline = rs.pipeline()
            rs_config = rs.config()
            rs_config.enable_stream(
                rs.stream.color,
                self.config.camera_width, self.config.camera_height,
                rs.format.bgr8, self.config.camera_fps
            )
            profile = self.pipeline.start(rs_config)

            color_stream = profile.get_stream(rs.stream.color)
            intrinsics = color_stream.as_video_stream_profile().get_intrinsics()

            self.camera_matrix = np.array([
                [intrinsics.fx, 0, intrinsics.ppx],
                [0, intrinsics.fy, intrinsics.ppy],
                [0, 0, 1]
            ])
            self.dist_coeffs = np.array(intrinsics.coeffs)

            self.align = rs.align(rs.stream.color)

            print("[Calibrator] Camera started")
            print(f"  Camera matrix:\n{self.camera_matrix}")
            time.sleep(0.5)
            return True

        except Exception as e:
            print(f"[Calibrator] Camera start failed: {e}")
            return False

    def stop_camera(self):
        if self.pipeline:
            self.pipeline.stop()
        print("[Calibrator] Camera stopped")

    def get_frame(self) -> Optional[np.ndarray]:
        if self.pipeline is None:
            return None
        try:
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            color_frame = frames.get_color_frame()
            if not color_frame:
                return None
            return np.asanyarray(color_frame.get_data())
        except Exception as e:
            print(f"[Calibrator] Get frame failed: {e}")
            return None

    # ------------------------------------------------------------------ #
    # 로봇                                                                 #
    # ------------------------------------------------------------------ #

    def connect_robot(self) -> bool:
        self.robot = DoosanRobot(self.config.robot_ip)
        return self.robot.connect()

    def disconnect_robot(self):
        if self.robot:
            self.robot.disconnect()

    # ------------------------------------------------------------------ #
    # 마커 감지                                                            #
    # ------------------------------------------------------------------ #

    def detect_marker(self, image: np.ndarray) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if self.camera_matrix is None:
            return None
        return self.aruco_detector.detect(
            image, self.camera_matrix, self.dist_coeffs,
            target_id=self.config.marker_id
        )

    # ------------------------------------------------------------------ #
    # 샘플 수집                                                            #
    # ------------------------------------------------------------------ #

    def capture_sample(self) -> bool:
        """
        현재 자세에서 샘플 캡처.

        수집 데이터:
            - R_gripper2base, t_gripper2base: 로봇 FK (그리퍼->베이스)
            - R_target2cam, t_target2cam:     ArUco 감지 (마커->카메라)
        """
        image = self.get_frame()
        if image is None:
            print("[Calibrator] Failed to get camera frame")
            return False

        result = self.detect_marker(image)
        if result is None:
            print("[Calibrator] Marker not detected")
            return False

        rvec, tvec = result

        # 마커->카메라 변환 (ArUco solvePnP 결과)
        R_t2c, _ = cv2.Rodrigues(rvec)
        t_t2c = tvec.reshape(3, 1)

        # 그리퍼->베이스 변환 (E0509 정확한 FK)
        joint_angles_rad = self.robot.get_joint_positions()
        joint_angles_deg = np.degrees(joint_angles_rad)
        tcp_pos, tcp_rot = e0509_fk(joint_angles_rad)

        # tcp_rot: 그리퍼->베이스 회전행렬 (3x3)
        # tcp_pos: 그리퍼->베이스 이동벡터 (3,) 미터
        R_g2b = tcp_rot                        # (3,3)
        t_g2b = tcp_pos.reshape(3, 1)          # (3,1)
        print(f"[FK] TCP pos: {tcp_pos*100} cm, det(R)={np.linalg.det(tcp_rot):.4f}")

        self.R_gripper2base.append(R_g2b)
        self.t_gripper2base.append(t_g2b)
        self.R_target2cam.append(R_t2c)
        self.t_target2cam.append(t_t2c)

        sample_num = len(self.R_gripper2base)

        # 이미지 및 CSV 저장
        if self.save_dir:
            annotated = image.copy()
            cv2.drawFrameAxes(annotated, self.camera_matrix, self.dist_coeffs,
                              rvec, tvec, self.config.marker_size * 0.5)

            # 프리뷰와 동일한 텍스트 오버레이
            t = t_t2c.flatten()
            j = joint_angles_deg.astype(int)
            cv2.putText(annotated,
                        f"Sample #{sample_num}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(annotated,
                        f"Marker XYZ: [{t[0]*100:+.1f}, {t[1]*100:+.1f}, {t[2]*100:+.1f}] cm",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(annotated,
                        f"TCP:  [{tcp_pos[0]*100:+.1f}, {tcp_pos[1]*100:+.1f}, {tcp_pos[2]*100:+.1f}] cm",
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(annotated,
                        f"J: {j[0]} {j[1]} {j[2]} {j[3]} {j[4]} {j[5]}",
                        (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

            img_path = os.path.join(self.save_dir, f"sample_{sample_num:02d}.png")
            cv2.imwrite(img_path, annotated)

            log_path = os.path.join(self.save_dir, "positions.csv")
            write_header = not os.path.exists(log_path)
            tcp_rx, tcp_ry, tcp_rz = self.robot._rotation_matrix_to_euler(tcp_rot)
            rvec_flat = rvec.flatten()
            with open(log_path, 'a') as f:
                if write_header:
                    f.write("sample,tcp_x,tcp_y,tcp_z,tcp_rx,tcp_ry,tcp_rz,"
                            "cam_x,cam_y,cam_z,cam_rvec_x,cam_rvec_y,cam_rvec_z,"
                            "j1_deg,j2_deg,j3_deg,j4_deg,j5_deg,j6_deg\n")
                f.write(f"{sample_num},"
                        f"{tcp_pos[0]:.6f},{tcp_pos[1]:.6f},{tcp_pos[2]:.6f},"
                        f"{np.degrees(tcp_rx):.4f},{np.degrees(tcp_ry):.4f},{np.degrees(tcp_rz):.4f},"
                        f"{t_t2c[0,0]:.6f},{t_t2c[1,0]:.6f},{t_t2c[2,0]:.6f},"
                        f"{rvec_flat[0]:.6f},{rvec_flat[1]:.6f},{rvec_flat[2]:.6f},"
                        f"{joint_angles_deg[0]:.0f},{joint_angles_deg[1]:.0f},{joint_angles_deg[2]:.0f},"
                        f"{joint_angles_deg[3]:.0f},{joint_angles_deg[4]:.0f},{joint_angles_deg[5]:.0f}\n")
            print(f"  [저장] {img_path}")

        t_marker = t_t2c.flatten()
        print(f"\n[Sample #{sample_num}]")
        print(f"  Marker in cam: [{t_marker[0]*100:+6.2f}, {t_marker[1]*100:+6.2f}, {t_marker[2]*100:+6.2f}] cm")
        print(f"  Gripper in base: [{tcp_pos[0]*100:+6.2f}, {tcp_pos[1]*100:+6.2f}, {tcp_pos[2]*100:+6.2f}] cm")
        print(f"  Joint angles: {joint_angles_deg.astype(int).tolist()}")

        return True

    # ------------------------------------------------------------------ #
    # 캘리브레이션                                                         #
    # ------------------------------------------------------------------ #

    def calibrate(self, method_name: str = 'tsai') -> bool:
        """
        Eye-in-Hand 캘리브레이션 수행.

        OpenCV calibrateHandEye 사용:
            AX = XB
            A = T_gripper2base (로봇 FK)
            B = T_target2cam   (ArUco)
            X = T_cam2gripper  (구하고자 하는 값)
        """
        n = len(self.R_gripper2base)
        if n < self.config.min_samples:
            print(f"[Calibrator] 샘플 부족: {n} < {self.config.min_samples}")
            return False

        method_val = self.METHODS.get(method_name, cv2.CALIB_HAND_EYE_TSAI)
        print(f"\n[Calibrator] calibrateHandEye ({method_name}, {n}개 샘플)...")

        try:
            R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(
                self.R_gripper2base,
                self.t_gripper2base,
                self.R_target2cam,
                self.t_target2cam,
                method=method_val
            )
        except Exception as e:
            print(f"[Calibrator] calibrateHandEye 실패: {e}")
            return False

        # T_cam_to_gripper 4x4 구성
        T = np.eye(4)
        T[:3, :3] = R_cam2gripper
        T[:3, 3] = t_cam2gripper.flatten()
        self.T_cam_to_gripper = T

        print(f"\n[Result] T_cam_to_gripper:\n{np.round(T, 4)}")
        print(f"  t: [{t_cam2gripper[0,0]*100:+6.2f}, {t_cam2gripper[1,0]*100:+6.2f}, {t_cam2gripper[2,0]*100:+6.2f}] cm")

        # 검증: T_base2target 일관성 확인
        # T_base2target = T_gripper2base @ T_cam2gripper @ T_target2cam
        # 모든 자세에서 같은 값이어야 함
        errors = self._validate(T)
        errors_np = np.array(errors)
        mean_err = float(np.mean(errors_np)) * 1000
        max_err  = float(np.max(errors_np))  * 1000
        min_err  = float(np.min(errors_np))  * 1000
        std_err  = float(np.std(errors_np))  * 1000

        print(f"\n[Validation] 마커 위치 일관성 (베이스 좌표계)")
        print(f"  Mean: {mean_err:.2f} mm")
        print(f"  Max:  {max_err:.2f} mm")
        print(f"  Min:  {min_err:.2f} mm")
        print(f"  Std:  {std_err:.2f} mm")

        if mean_err < 5:
            verdict = "아주 좋음"
        elif mean_err < 15:
            verdict = "좋음"
        elif mean_err < 30:
            verdict = "괜찮음"
        else:
            verdict = "재캘리브레이션 권장"
        print(f"  → {verdict}")

        self.calibration_errors = {
            'timestamp':   datetime.datetime.now().isoformat(),
            'method':      method_name,
            'num_samples': n,
            'mean_mm':     round(mean_err, 2),
            'max_mm':      round(max_err, 2),
            'min_mm':      round(min_err, 2),
            'std_mm':      round(std_err, 2),
            'verdict':     verdict,
            'T_cam_to_gripper': T.tolist(),
            'per_sample_mm':    [round(e * 1000, 2) for e in errors],
        }

        return True

    def _validate(self, T_cam2gripper: np.ndarray) -> List[float]:
        """
        검증: 각 자세에서 T_base2target = T_g2b @ T_c2g @ T_t2c 를 계산하고,
        첫 번째 자세 대비 마커 위치 차이(미터)를 반환.
        """
        base2target_list = []
        for R_g2b, t_g2b, R_t2c, t_t2c in zip(
                self.R_gripper2base, self.t_gripper2base,
                self.R_target2cam,   self.t_target2cam):
            T_g2b = np.eye(4)
            T_g2b[:3, :3] = R_g2b
            T_g2b[:3, 3]  = t_g2b.flatten()

            T_t2c = np.eye(4)
            T_t2c[:3, :3] = R_t2c
            T_t2c[:3, 3]  = t_t2c.flatten()

            # 마커 위치 (베이스 좌표계)
            T_b2t = T_g2b @ T_cam2gripper @ T_t2c
            base2target_list.append(T_b2t[:3, 3])

        # 모든 자세의 평균 마커 위치
        mean_pos = np.mean(base2target_list, axis=0)
        self.T_base_to_target = np.eye(4)
        self.T_base_to_target[:3, 3] = mean_pos

        errors = [np.linalg.norm(p - mean_pos) for p in base2target_list]
        return errors

    def calibrate_all_methods(self) -> str:
        """
        모든 방법으로 캘리브레이션하고 가장 오차가 작은 방법 반환.
        """
        print("\n[Calibrator] 모든 방법 비교...")
        best_method = None
        best_mean = float('inf')
        results = {}

        for name in self.METHODS:
            try:
                R, t = cv2.calibrateHandEye(
                    self.R_gripper2base, self.t_gripper2base,
                    self.R_target2cam,   self.t_target2cam,
                    method=self.METHODS[name]
                )
                T = np.eye(4)
                T[:3, :3] = R
                T[:3, 3]  = t.flatten()
                errors = self._validate(T)
                mean_err = float(np.mean(errors)) * 1000
                results[name] = mean_err
                print(f"  {name:12s}: mean={mean_err:.2f} mm")
                if mean_err < best_mean:
                    best_mean = mean_err
                    best_method = name
            except Exception as e:
                print(f"  {name:12s}: 실패 ({e})")

        print(f"\n  최적 방법: {best_method} (mean={best_mean:.2f} mm)")
        return best_method

    # ------------------------------------------------------------------ #
    # 저장 / 로드                                                          #
    # ------------------------------------------------------------------ #

    def save_calibration(self, path: str = None):
        if self.T_cam_to_gripper is None:
            print("[Calibrator] 저장할 캘리브레이션 결과 없음")
            return

        path = path or self.config.output_path
        config_dir = os.path.dirname(path)
        base_name  = os.path.basename(path)
        save_dir   = os.path.join(config_dir, self.session_timestamp)
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, base_name)

        np.savez(
            path,
            T_cam_to_gripper = self.T_cam_to_gripper,
            camera_matrix    = self.camera_matrix,
            dist_coeffs      = self.dist_coeffs,
            marker_size      = self.config.marker_size,
            marker_id        = self.config.marker_id,
            num_samples      = len(self.R_gripper2base),
            # raw 데이터 (재계산용)
            R_gripper2base = np.stack(self.R_gripper2base) if self.R_gripper2base else np.array([]),
            t_gripper2base = np.stack(self.t_gripper2base) if self.t_gripper2base else np.array([]),
            R_target2cam   = np.stack(self.R_target2cam)   if self.R_target2cam   else np.array([]),
            t_target2cam   = np.stack(self.t_target2cam)   if self.t_target2cam   else np.array([]),
        )

        print(f"\n[Saved] {path}")
        print(f"  T_cam_to_gripper:\n{self.T_cam_to_gripper}")

        if self.calibration_errors is not None:
            error_path = path.replace('.npz', '_errors.json')
            with open(error_path, 'w', encoding='utf-8') as f:
                json.dump(self.calibration_errors, f, indent=2, ensure_ascii=False)
            print(f"[Saved] {error_path}")

    def load_calibration(self, path: str = None) -> bool:
        path = path or self.config.output_path

        if not os.path.exists(path):
            print(f"[Calibrator] 파일 없음: {path}")
            return False

        data = np.load(path)
        self.T_cam_to_gripper = data['T_cam_to_gripper']
        self.camera_matrix    = data['camera_matrix']
        self.dist_coeffs      = data['dist_coeffs']

        if 'R_gripper2base' in data and len(data['R_gripper2base']) > 0:
            self.R_gripper2base = list(data['R_gripper2base'])
            self.t_gripper2base = list(data['t_gripper2base'])
            self.R_target2cam   = list(data['R_target2cam'])
            self.t_target2cam   = list(data['t_target2cam'])
            print(f"[Calibrator] Raw 데이터 로드: {len(self.R_gripper2base)}개 샘플")

        print(f"[Calibrator] 로드 완료: {path}")
        print(f"T_cam_to_gripper:\n{self.T_cam_to_gripper}")
        return True

    # ------------------------------------------------------------------ #
    # 좌표 변환                                                            #
    # ------------------------------------------------------------------ #

    def transform_cam_to_gripper(self, point_cam: np.ndarray) -> np.ndarray:
        """
        카메라 좌표 -> 그리퍼(TCP) 좌표 변환

        Args:
            point_cam: (3,) 카메라 좌표계 점

        Returns:
            point_gripper: (3,) 그리퍼 좌표계 점
        """
        if self.T_cam_to_gripper is None:
            raise RuntimeError("캘리브레이션 미로드")
        h = np.append(point_cam, 1.0)
        return (self.T_cam_to_gripper @ h)[:3]

    def transform_cam_to_base(self, point_cam: np.ndarray,
                               tcp_pos: np.ndarray,
                               tcp_rot: np.ndarray) -> np.ndarray:
        """
        카메라 좌표 -> 로봇 베이스 좌표 변환 (현재 TCP 자세 필요)

        Args:
            point_cam: (3,) 카메라 좌표계 점
            tcp_pos:   (3,) 현재 TCP 위치 (베이스 기준, 미터)
            tcp_rot:   (3,3) 현재 TCP 회전행렬 (베이스 기준)

        Returns:
            point_base: (3,) 로봇 베이스 좌표계 점
        """
        if self.T_cam_to_gripper is None:
            raise RuntimeError("캘리브레이션 미로드")

        # 현재 T_gripper2base
        T_g2b = np.eye(4)
        T_g2b[:3, :3] = tcp_rot
        T_g2b[:3, 3]  = tcp_pos

        T_total = T_g2b @ self.T_cam_to_gripper
        h = np.append(point_cam, 1.0)
        return (T_total @ h)[:3]

    # ------------------------------------------------------------------ #
    # 인터랙티브                                                           #
    # ------------------------------------------------------------------ #

    def interactive_capture(self, scale: float = 2.0):
        """
        인터랙티브 데이터 수집

        조작:
            Space: 현재 자세 캡처
            c: 캘리브레이션 수행 (Tsai 방법)
            a: 모든 방법 비교 후 최적 방법으로 캘리브레이션
            s: 결과 저장
            r: 데이터 초기화
            q: 종료
        """
        print("\n" + "=" * 60)
        print("Eye-in-Hand 캘리브레이션 - 데이터 수집")
        print("=" * 60)
        print("준비사항:")
        print("  1. RealSense 카메라를 로봇 TCP(그리퍼)에 고정")
        print("  2. ArUco 마커를 작업대에 고정 (절대 움직이면 안 됨)")
        print("  3. 로봇을 다양한 자세로 이동하며 마커가 보이는 곳에서 캡처")
        print("=" * 60)
        print("조작:")
        print("  Space: 현재 자세 캡처")
        print("  c:     캘리브레이션 수행 (Tsai)")
        print("  a:     모든 방법 비교 후 최적 방법으로 캘리브레이션")
        print("  s:     결과 저장")
        print("  r:     데이터 초기화")
        print("  q:     종료")
        print("=" * 60)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_dir = os.path.join(script_dir, "..", "calib_images",
                                     f"eye_in_hand_{self.session_timestamp}")
        os.makedirs(self.save_dir, exist_ok=True)
        print(f"[Calibrator] 이미지 저장 폴더: {self.save_dir}")

        while True:
            image = self.get_frame()
            if image is None:
                continue

            display = image.copy()

            result = self.detect_marker(image)

            if result is not None:
                rvec, tvec = result
                cv2.drawFrameAxes(display, self.camera_matrix, self.dist_coeffs,
                                  rvec, tvec, self.config.marker_size * 0.5)
                t = tvec.flatten()
                dict_name = self.aruco_detector.detected_dict_name or "Unknown"
                cv2.putText(display,
                            f"Marker [{dict_name}]: [{t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f}] m",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                status_color = (0, 255, 0)
            else:
                cv2.putText(display, "Marker NOT detected",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                status_color = (0, 0, 255)

            n = len(self.R_gripper2base)
            cv2.putText(display, f"Samples: {n}/{self.config.min_samples}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

            if self.robot and self.robot.connected:
                try:
                    tcp_pos, _ = self.robot.get_tcp_pose()
                    cv2.putText(display,
                                f"TCP: [{tcp_pos[0]:.3f}, {tcp_pos[1]:.3f}, {tcp_pos[2]:.3f}] m",
                                (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                except Exception:
                    pass

            if self.T_cam_to_gripper is not None:
                t_cg = self.T_cam_to_gripper[:3, 3]
                cv2.putText(display,
                            f"T_c2g t: [{t_cg[0]*100:.1f}, {t_cg[1]*100:.1f}, {t_cg[2]*100:.1f}] cm",
                            (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 128, 0), 2)

            if scale != 1.0:
                new_w = int(display.shape[1] * scale)
                new_h = int(display.shape[0] * scale)
                display = cv2.resize(display, (new_w, new_h))

            cv2.imshow("Eye-in-Hand Calibration", display)

            key = cv2.waitKey(30) & 0xFF

            if key == ord('q'):
                break
            elif key == ord(' '):
                if self.capture_sample():
                    print(f"  Total samples: {len(self.R_gripper2base)}")
            elif key == ord('c'):
                if self.calibrate(method_name='tsai'):
                    print("캘리브레이션 완료!")
                else:
                    print("캘리브레이션 실패")
            elif key == ord('a'):
                best = self.calibrate_all_methods()
                if best:
                    self.calibrate(method_name=best)
            elif key == ord('s'):
                self.save_calibration()
            elif key == ord('r'):
                self.R_gripper2base.clear()
                self.t_gripper2base.clear()
                self.R_target2cam.clear()
                self.t_target2cam.clear()
                self.T_cam_to_gripper = None
                self.T_base_to_target = None
                print("\n[Reset] 데이터 초기화됨")

        cv2.destroyAllWindows()


# ------------------------------------------------------------------ #
# 유틸                                                                 #
# ------------------------------------------------------------------ #

def print_aruco_marker(marker_id: int = 0, size_pixels: int = 200):
    if not ARUCO_AVAILABLE:
        print("ArUco not available")
        return

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    marker_image = aruco.generateImageMarker(aruco_dict, marker_id, size_pixels)

    filename = f"aruco_marker_{marker_id}.png"
    cv2.imwrite(filename, marker_image)
    print(f"저장: {filename}  (ID={marker_id}, {size_pixels}x{size_pixels}px)")
    print("인쇄 후 작업대에 고정하세요. 인쇄 크기를 측정하여 --marker-size에 지정.")


# ------------------------------------------------------------------ #
# 테스트 모드                                                          #
# ------------------------------------------------------------------ #

def run_test_mode(calibrator: 'EyeInHandCalibrator', scale: float):
    """
    기존 캘리브레이션으로 실시간 마커 위치를 베이스 좌표계로 변환하여 표시.
    카메라가 TCP에 달려 있으므로 현재 TCP 자세도 함께 사용.
    """
    print("\n테스트 모드 - 마커 위치를 베이스 좌표계로 변환")
    print("로봇을 움직여도 변환된 마커 위치가 일정해야 합니다 (고정 마커)")
    print("q 키로 종료")

    while True:
        image = calibrator.get_frame()
        if image is None:
            continue

        display = image.copy()
        result  = calibrator.detect_marker(image)

        tcp_pos, tcp_rot = None, None
        if calibrator.robot and calibrator.robot.connected:
            try:
                tcp_pos, tcp_rot = calibrator.robot.get_tcp_pose()
            except Exception:
                pass

        if result is not None:
            rvec, tvec = result
            t_cam = tvec.flatten()

            cv2.drawFrameAxes(display, calibrator.camera_matrix,
                              calibrator.dist_coeffs, rvec, tvec, 0.03)
            cv2.putText(display,
                        f"Marker in cam: [{t_cam[0]:.3f}, {t_cam[1]:.3f}, {t_cam[2]:.3f}] m",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

            if tcp_pos is not None and tcp_rot is not None:
                t_base = calibrator.transform_cam_to_base(t_cam, tcp_pos, tcp_rot)
                cv2.putText(display,
                            f"Marker in base: [{t_base[0]*100:.1f}, {t_base[1]*100:.1f}, {t_base[2]*100:.1f}] cm",
                            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
        else:
            cv2.putText(display, "Marker NOT detected",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if tcp_pos is not None:
            cv2.putText(display,
                        f"TCP: [{tcp_pos[0]*100:.1f}, {tcp_pos[1]*100:.1f}, {tcp_pos[2]*100:.1f}] cm",
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

        if scale != 1.0:
            new_w = int(display.shape[1] * scale)
            new_h = int(display.shape[0] * scale)
            display = cv2.resize(display, (new_w, new_h))

        cv2.imshow("Eye-in-Hand Test", display)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# ------------------------------------------------------------------ #
# main                                                                 #
# ------------------------------------------------------------------ #

def main():
    parser = argparse.ArgumentParser(description="Eye-in-Hand 캘리브레이션")
    parser.add_argument("--robot-ip",    type=str,   default="192.168.137.100")
    parser.add_argument("--marker-id",   type=int,   default=0)
    parser.add_argument("--marker-size", type=float, default=0.1,
                        help="마커 크기 (미터)")
    parser.add_argument("--output",      type=str,
                        default="config/calibration_eye_in_hand.npz")
    parser.add_argument("--scale",       type=float, default=2.0,
                        help="화면 확대 비율")
    parser.add_argument("--method",      type=str,   default="tsai",
                        choices=list(EyeInHandCalibrator.METHODS.keys()),
                        help="hand-eye 캘리브레이션 방법")
    parser.add_argument("--test",         action="store_true",
                        help="기존 캘리브레이션 테스트")
    parser.add_argument("--print-marker", action="store_true",
                        help="ArUco 마커 이미지 생성")
    parser.add_argument("--simulation",   action="store_true",
                        help="시뮬레이션 모드 (로봇 없이)")
    args = parser.parse_args()

    if args.print_marker:
        print_aruco_marker(args.marker_id)
        return

    config = CalibrationConfig(
        robot_ip    = args.robot_ip,
        marker_id   = args.marker_id,
        marker_size = args.marker_size,
        output_path = args.output,
    )

    calibrator = EyeInHandCalibrator(config)

    # 테스트 모드
    if args.test:
        if not calibrator.load_calibration():
            return
        if not calibrator.start_camera():
            return
        if not args.simulation:
            if not calibrator.connect_robot():
                print("[Warning] 로봇 연결 실패 - TCP 좌표 없이 동작")
        try:
            run_test_mode(calibrator, scale=args.scale)
        finally:
            calibrator.stop_camera()
            calibrator.disconnect_robot()
        return

    # 캘리브레이션 모드
    print("\n" + "=" * 60)
    print("Eye-in-Hand 캘리브레이션")
    print("=" * 60)
    print(f"로봇 IP:    {args.robot_ip}")
    print(f"마커 ID:    {args.marker_id}")
    print(f"마커 크기:  {args.marker_size} m")
    print(f"캘리브레이션 방법: {args.method}")
    print("=" * 60)

    if not calibrator.start_camera():
        return

    if not args.simulation:
        if not calibrator.connect_robot():
            calibrator.stop_camera()
            return
    else:
        print("[Calibrator] 시뮬레이션 모드 - 로봇 미연결")
        calibrator.robot = DoosanRobot(simulation=True)
        calibrator.robot.connect()

    try:
        calibrator.interactive_capture(scale=args.scale)
    finally:
        calibrator.stop_camera()
        calibrator.disconnect_robot()

    print("\n캘리브레이션 종료")


if __name__ == "__main__":
    main()
