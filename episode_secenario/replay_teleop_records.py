#!/usr/bin/env python3
"""
replay_teleop_records.py

teleop_records.csv에 기록된 관절 각도 웨이포인트를 순서대로 재생합니다.
bag recorder가 백그라운드에서 실행 중이면
  /dsr01/joint_states, /camera/camera/color/image_raw, /gripper/position
을 자동으로 수집합니다.

실행:
  python3 episode_secenario/replay_teleop_records.py [--csv <경로>]

사전 조건:
  - Doosan 로봇 bringup 실행 중 (dsr01)
  - RealSense 카메라 ROS2 노드 실행 중
  - (선택) ros2 bag record 실행 중
"""

import argparse
import csv
import math
import sys
import threading
import time
from pathlib import Path

import cv2
import numpy as np

import rclpy
from rclpy.executors import MultiThreadedExecutor

sys.path.insert(0, '/home/user/robot_workspace/vla_ws')
sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController

# ── 설정 ──────────────────────────────────────────────────────────────────────
DEFAULT_CSV       = '/home/user/robot_workspace/vla_ws/src/teleop_records.csv'
GRIPPER_PORT      = '/dev/ttyUSB0'
ROBOT_ID          = 'dsr01'
MOVE_VELOCITY     = 10.0   # deg/s
MOVE_ACCELERATION = 20.0   # deg/s²
# Gripper_Pos: CSV 저장값 기준 0 = 완전 열림, 740 = 완전 닫힘
GRIPPER_CLOSE_THRESHOLD = 370.0  # 이 값 이상이면 close 명령


def load_waypoints(csv_path: str) -> list:
    """CSV에서 웨이포인트 목록 로드. 각 항목: {joints_rad, gripper_pos, timestamp}"""
    waypoints = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            waypoints.append({
                'joints_rad':  [float(row[f'J{i}_rad']) for i in range(1, 7)],
                'gripper_pos': float(row['Gripper_Pos']),
                'timestamp':   row.get('Timestamp', ''),
            })
    return waypoints


class ReplayEpisode:
    def __init__(self, csv_path: str):
        rclpy.init()
        self._node = rclpy.create_node('replay_teleop_records')
        self._executor = MultiThreadedExecutor(num_threads=4)
        self._executor.add_node(self._node)
        self._logger = self._node.get_logger()

        # rclpy spin을 백그라운드에서 실행 (서비스/토픽 콜백 처리)
        self._spin_thread = threading.Thread(target=self._executor.spin, daemon=True)
        self._spin_thread.start()

        # 카메라: ROS2 토픽 구독 (bag recorder와 동일 소스)
        self._camera = CameraNode(
            ros_image_topic='/camera/camera/color/image_raw',
            ros_depth_topic='/camera/camera/aligned_depth_to_color/image_raw',
            ros_node=self._node,
        )

        self._robot   = DoosanController(self._node, robot_id=ROBOT_ID, action_mode='joint')
        self._gripper = GripperController(port=GRIPPER_PORT, ros_node=self._node, robot_id=ROBOT_ID)

        self._waypoints = load_waypoints(csv_path)
        self._logger.info(f'{len(self._waypoints)}개 웨이포인트 로드: {csv_path}')

        self._vis_running = False

    # ── 시각화 스레드 ─────────────────────────────────────────────────────────

    def _vis_loop(self, wp_ref: list) -> None:
        """백그라운드 스레드: 카메라 프레임 + 진행 오버레이 표시."""
        cv2.namedWindow('Replay Teleop (q=quit)', cv2.WINDOW_NORMAL)
        while self._vis_running:
            rgb, _ = self._camera.get_images()
            if rgb is None:
                time.sleep(0.05)
                continue

            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            # 진행 상황 오버레이
            idx, total = wp_ref[0], wp_ref[1]
            ratio = idx / total if total > 0 else 0.0
            label = f'Waypoint {idx} / {total}'
            cv2.putText(frame, label, (10, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 230, 0), 2, cv2.LINE_AA)

            bar_w = frame.shape[1] - 20
            cv2.rectangle(frame, (10, 42), (10 + bar_w, 56), (60, 60, 60), -1)
            cv2.rectangle(frame, (10, 42), (10 + int(bar_w * ratio), 56), (0, 200, 0), -1)

            cv2.imshow('Replay Teleop (q=quit)', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self._vis_running = False
                break

        cv2.destroyAllWindows()

    # ── 메인 에피소드 ─────────────────────────────────────────────────────────

    def run(self) -> bool:
        if not self._waypoints:
            self._logger.error('웨이포인트가 없습니다. CSV를 확인하세요.')
            return False

        # 카메라 준비 대기 (최대 15초)
        self._logger.info('카메라 프레임 대기 중 ...')
        deadline = time.time() + 15.0
        while not self._camera.ready:
            if time.time() > deadline:
                self._logger.error('카메라 타임아웃 – RealSense 노드가 실행 중인지 확인하세요.')
                return False
            time.sleep(0.1)
        self._logger.info('카메라 준비 완료.')

        # 시각화 스레드 시작
        wp_ref = [0, len(self._waypoints)]
        self._vis_running = True
        vis_thread = threading.Thread(target=self._vis_loop, args=(wp_ref,), daemon=True)
        vis_thread.start()

        self._logger.info('=' * 52)
        self._logger.info(f' 재생 시작: {len(self._waypoints)}개 웨이포인트')
        self._logger.info('=' * 52)

        prev_gripper_closed = None  # 불필요한 그리퍼 명령 반복 방지

        for idx, wp in enumerate(self._waypoints):
            if not self._vis_running:
                self._logger.info('시각화 창 닫힘 – 재생 중단.')
                break

            wp_ref[0] = idx + 1
            joints_deg = [math.degrees(r) for r in wp['joints_rad']]
            gripper_raw = wp['gripper_pos']
            now_closed = gripper_raw >= GRIPPER_CLOSE_THRESHOLD

            self._logger.info(
                f'[{idx+1:02d}/{len(self._waypoints):02d}] '
                f'J(deg)={[round(d, 1) for d in joints_deg]}  '
                f'Gripper={gripper_raw:.0f} ({"close" if now_closed else "open"})'
            )

            # 관절 이동 (blocking — 다음 웨이포인트로 이동 완료 후 다음 단계)
            self._robot.move_joint(
                joints_deg,
                velocity=MOVE_VELOCITY,
                acceleration=MOVE_ACCELERATION,
            )

            # 그리퍼 상태 변화 시에만 명령 전송
            if now_closed != prev_gripper_closed:
                if now_closed:
                    self._gripper.close()
                else:
                    self._gripper.open()
                prev_gripper_closed = now_closed

        self._logger.info('=' * 52)
        self._logger.info(' 재생 완료')
        self._logger.info('=' * 52)

        self._vis_running = False
        if vis_thread.is_alive():
            vis_thread.join(timeout=3.0)

        return True

    # ── 정리 ─────────────────────────────────────────────────────────────────

    def shutdown(self) -> None:
        self._vis_running = False
        self._camera.release()
        self._node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


# ── 실행 ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='teleop_records.csv 웨이포인트 재생')
    parser.add_argument('--csv', default=DEFAULT_CSV, help='CSV 파일 경로')
    args = parser.parse_args()

    if not Path(args.csv).exists():
        print(f'[ERROR] CSV 파일을 찾을 수 없습니다: {args.csv}')
        sys.exit(1)

    episode = ReplayEpisode(args.csv)
    try:
        success = episode.run()
        print(f'\n에피소드 결과: {"성공" if success else "실패"}')
    except KeyboardInterrupt:
        print('\n사용자에 의해 중단됨.')
    finally:
        episode.shutdown()


if __name__ == '__main__':
    main()
