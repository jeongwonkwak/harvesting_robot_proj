#!/usr/bin/env python3
"""
Eye-in-Hand 자동 캘리브레이션 스크립트

calibration_joint_poses_eye_in_hand.txt의 포즈를 순서대로 이동하고,
settle_time 후 자동으로 샘플을 캡처한 뒤 캘리브레이션 및 저장까지 수행합니다.

이동 속도는 각 포즈 간 최대 관절 이동량을 기준으로 자동 계산하여
항상 --move-duration초 동안 이동합니다 (기본 10초).

Usage:
    python eye_in_hand_auto.py
    python eye_in_hand_auto.py --robot-ip 192.168.137.100 --marker-size 0.1
    python eye_in_hand_auto.py --move-duration 10 --settle 2.0
    python eye_in_hand_auto.py --dry-run   # 로봇 이동 없이 흐름만 확인
"""

import numpy as np
import cv2
import time
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calibrate_eye_in_hand import EyeInHandCalibrator, CalibrationConfig
from robot_interface import DoosanRobot

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POSES_FILE = os.path.join(SCRIPT_DIR, "calibration_joint_poses_eye_in_hand.txt")


def vel_for_duration(current_deg: np.ndarray, target_deg: np.ndarray,
                     duration: float, min_vel: float = 1.0) -> tuple:
    """
    현재 → 목표 이동이 duration초 걸리도록 vel/acc 계산.

    acc = vel/2 사다리꼴 프로파일 기준:
        가감속 각 2초 고정 → 등속 구간 = (duration - 4)초
        T = 4 + D/vel  →  vel = D / (duration - 4)
    """
    max_diff = float(np.max(np.abs(target_deg - current_deg)))
    if max_diff < 0.5:
        return min_vel, min_vel * 0.5
    effective = max(duration - 4.0, 1.0)   # 가감속 총 4초 제외
    vel = max(min_vel, max_diff / effective)
    acc = vel / 2.0
    return round(vel, 2), round(acc, 2)


def load_poses(path: str) -> list:
    """포즈 파일 로드. 주석(#) 및 괄호 주석 제거."""
    poses = []
    with open(path) as f:
        for line in f:
            line = line.split('(')[0].split('#')[0].strip()
            if not line:
                continue
            vals = list(map(float, line.split()))
            if len(vals) == 6:
                poses.append(np.array(vals))
    return poses


def wait_until_stopped(robot, target_rad: np.ndarray,
                       timeout: float = 20.0, tol_deg: float = 0.5):
    """
    관절 위치가 목표에 tol_deg 이내로 수렴할 때까지 대기.
    ROS2 모드에서는 get_joint_velocities()가 0을 반환하므로
    위치 기반 체크 사용.
    """
    target_deg = np.degrees(target_rad)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            cur_deg = np.degrees(robot.get_joint_positions())
            if np.max(np.abs(cur_deg - target_deg)) < tol_deg:
                time.sleep(0.5)   # 수렴 후 진동 해소 추가 대기
                return
        except Exception:
            pass
        time.sleep(0.1)
    print("[Warning] wait_until_stopped: timeout, proceeding anyway")


def wait_with_preview(calibrator: EyeInHandCalibrator, seconds: float,
                      label: str = "", scale: float = 1.5):
    """카메라 화면 보여주면서 대기."""
    deadline = time.time() + seconds
    while time.time() < deadline:
        remaining = deadline - time.time()
        image = calibrator.get_frame()
        if image is None:
            time.sleep(0.05)
            continue

        display = image.copy()
        result = calibrator.detect_marker(image)

        if result is not None:
            rvec, tvec = result
            cv2.drawFrameAxes(display, calibrator.camera_matrix,
                              calibrator.dist_coeffs, rvec, tvec,
                              calibrator.config.marker_size * 0.5)
            t = tvec.flatten()
            cv2.putText(display,
                        f"Marker: [{t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f}] m",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(display, "Marker NOT detected",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if label:
            cv2.putText(display, label,
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(display, f"Capturing in {remaining:.1f}s ...",
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

        if scale != 1.0:
            display = cv2.resize(display,
                                 (int(display.shape[1] * scale),
                                  int(display.shape[0] * scale)))
        cv2.imshow("Eye-in-Hand Auto Calibration", display)
        cv2.waitKey(30)


def show_result(calibrator: EyeInHandCalibrator, pose_idx: int,
                total: int, success: bool, scale: float = 1.5):
    """샘플 캡처 결과를 1초 동안 표시."""
    deadline = time.time() + 1.0
    while time.time() < deadline:
        image = calibrator.get_frame()
        if image is None:
            time.sleep(0.05)
            continue
        display = image.copy()
        color = (0, 255, 0) if success else (0, 0, 255)
        msg = f"[{pose_idx}/{total}] {'CAPTURED' if success else 'FAILED - SKIPPED'}"
        cv2.putText(display, msg, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(display, f"Total captured: {len(calibrator.R_gripper2base)}",
                    (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        if scale != 1.0:
            display = cv2.resize(display,
                                 (int(display.shape[1] * scale),
                                  int(display.shape[0] * scale)))
        cv2.imshow("Eye-in-Hand Auto Calibration", display)
        cv2.waitKey(30)


def main():
    parser = argparse.ArgumentParser(description="Eye-in-Hand 자동 캘리브레이션")
    parser.add_argument("--robot-ip",    type=str,   default="192.168.137.100")
    parser.add_argument("--marker-id",   type=int,   default=0)
    parser.add_argument("--marker-size", type=float, default=0.1)
    parser.add_argument("--output",      type=str,
                        default="config/calibration_eye_in_hand.npz")
    parser.add_argument("--poses-file",  type=str,   default=POSES_FILE)
    parser.add_argument("--settle",        type=float, default=1.0,
                        help="로봇 정지 후 캡처까지 대기 시간 (초)")
    parser.add_argument("--move-duration", type=float, default=10.0,
                        help="각 포즈 이동에 걸리는 목표 시간 (초, 기본 10)")
    parser.add_argument("--scale",       type=float, default=1.5,
                        help="화면 확대 비율")
    parser.add_argument("--method",      type=str,   default="tsai",
                        choices=list(EyeInHandCalibrator.METHODS.keys()))
    parser.add_argument("--dry-run",     action="store_true",
                        help="로봇 이동 없이 흐름만 확인")
    args = parser.parse_args()

    # 포즈 파일 로드
    if not os.path.exists(args.poses_file):
        print(f"[Error] 포즈 파일 없음: {args.poses_file}")
        return

    poses_deg = load_poses(args.poses_file)
    if not poses_deg:
        print("[Error] 포즈 파일이 비어있습니다")
        return

    print(f"\n{'='*60}")
    print(f"Eye-in-Hand 자동 캘리브레이션")
    print(f"{'='*60}")
    print(f"포즈 수:    {len(poses_deg)}개")
    print(f"대기 시간:  {args.settle}초")
    print(f"이동 시간:  {args.move_duration}초/포즈 (속도 자동 계산)")
    print(f"방법:       {args.method}")
    if args.dry_run:
        print("** DRY-RUN 모드 (로봇 미이동) **")
    print(f"{'='*60}")

    for i, deg in enumerate(poses_deg):
        print(f"  포즈 {i+1:2d}: {deg.astype(int).tolist()}")
    print()

    # 캘리브레이터 초기화
    config = CalibrationConfig(
        robot_ip    = args.robot_ip,
        marker_id   = args.marker_id,
        marker_size = args.marker_size,
        output_path = args.output,
    )
    calibrator = EyeInHandCalibrator(config)

    # 카메라 시작
    if not calibrator.start_camera():
        return

    # 로봇 연결
    if args.dry_run:
        robot = DoosanRobot(simulation=True)
        robot.connect()
        calibrator.robot = robot
    else:
        if not calibrator.connect_robot():
            calibrator.stop_camera()
            return

    # 이미지 저장 폴더
    save_dir = os.path.join(
        SCRIPT_DIR, "..", "calib_images",
        f"eye_in_hand_{calibrator.session_timestamp}"
    )
    os.makedirs(save_dir, exist_ok=True)
    calibrator.save_dir = save_dir
    print(f"[Calibrator] 이미지 저장 폴더: {save_dir}")

    cv2.namedWindow("Eye-in-Hand Auto Calibration", cv2.WINDOW_NORMAL)

    try:
        # --------------------------------------------------------
        # 각 포즈 순회
        # --------------------------------------------------------
        for i, deg in enumerate(poses_deg):
            pose_label = f"Pose {i+1}/{len(poses_deg)}: {deg.astype(int).tolist()}"
            print(f"\n[포즈 {i+1}/{len(poses_deg)}] {deg.astype(int).tolist()} 이동 중...")

            # 현재 관절 위치 기준으로 속도 계산
            current_rad = calibrator.robot.get_joint_positions()
            current_deg = np.degrees(current_rad)
            target_rad  = np.radians(deg)
            vel, acc = vel_for_duration(current_deg, deg, args.move_duration)
            print(f"  최대 이동량: {np.max(np.abs(deg - current_deg)):.1f}°  →  vel={vel} deg/s, acc={acc} deg/s²")

            calibrator.robot.move_joint(target_rad, vel=vel, acc=acc, wait=True)

            # 관절 위치가 목표에 수렴할 때까지 대기 (ROS2는 속도 읽기 불가 → 위치 기반)
            wait_until_stopped(calibrator.robot, target_rad)

            # settle 대기 (카메라 프리뷰 표시)
            wait_with_preview(calibrator, args.settle,
                              label=pose_label, scale=args.scale)

            # 샘플 캡처
            success = calibrator.capture_sample()
            show_result(calibrator, i + 1, len(poses_deg), success, scale=args.scale)

            if not success:
                print(f"  [스킵] 마커 미감지 또는 캡처 실패")

        # --------------------------------------------------------
        # 캘리브레이션
        # --------------------------------------------------------
        n = len(calibrator.R_gripper2base)
        print(f"\n{'='*60}")
        print(f"수집 완료: {n}개 샘플")
        print(f"{'='*60}")

        if n < calibrator.config.min_samples:
            print(f"[Error] 샘플 부족: {n} < {calibrator.config.min_samples}")
            return

        # 단일 방법으로 캘리브레이션
        print(f"\n[캘리브레이션] {args.method} 방법으로 계산 중...")
        if not calibrator.calibrate(method_name=args.method):
            print("[Error] 캘리브레이션 실패")
            return

        # 전체 방법 비교 (참고용)
        print("\n[참고] 전체 방법 비교:")
        best = calibrator.calibrate_all_methods()
        if best and best != args.method:
            print(f"\n최적 방법({best})으로 재계산 중...")
            calibrator.calibrate(method_name=best)

        # 저장
        calibrator.save_calibration()
        print("\n[완료] 캘리브레이션 결과 저장 완료")

    except KeyboardInterrupt:
        print("\n\n[중단] 사용자 종료")
    finally:
        calibrator.stop_camera()
        calibrator.disconnect_robot()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
