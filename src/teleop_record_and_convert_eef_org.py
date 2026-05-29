#!/usr/bin/env python3
"""
teleop_record_and_convert_eef.py

EEF delta 기반 데이터셋 수집용 텔레오퍼레이션 스크립트.
teleop_record_and_convert.py 와 동일하되 아래 항목이 추가됨:
  - /dsr01/tcp_pose (Float32MultiArray [x,y,z,rx,ry,rz] mm/deg) 퍼블리시 & bag 녹화
  - 변환 시 bag_to_lerobot_eef.py 호출 (EEF delta action 계산)

실행:
  python3 src/teleop_record_and_convert_eef.py
  python3 src/teleop_record_and_convert_eef.py --episode 003
  python3 src/teleop_record_and_convert_eef.py --task "Pick up the red object."
"""

import argparse
import csv
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import yaml

import cv2
import numpy as np
import rclpy
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Float32, Float32MultiArray

WS_DIR = Path('/home/user/robot_workspace/vla_ws')
sys.path.insert(0, str(WS_DIR))
sys.path.insert(0, str(WS_DIR / 'grasp_vla'))

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController
from ultralytics import YOLO

YOLO_MODEL     = str(WS_DIR / 'models/strawberry_yolo26m_unified/weights/last.pt')
GRIPPER_PORT   = '/dev/ttyUSB0'
ROBOT_ID       = 'dsr01'
CONF_THRESHOLD = 0.3
STEP_MM        = 10.0
STEP_DEG       =  5.0
RECORD_DIR     = str(WS_DIR / 'src/teleop_records')
RAW_DIR        = str(WS_DIR / 'data/raw/final_project')
DATASET_NAME   = 'vla_dataset_v0.3.0'
QOS_FILE       = str(WS_DIR / 'config/bag_qos_overrides.yaml')
CAMERA_TOPIC        = '/camera/camera/color/image_raw'
DEFAULT_TASK        = 'Approach the red object closely and pick it up.'
GRIPPER_CLOSE_POS   = 500
GRIPPER_MAX_POS     = 740

# ── 홈 포즈 ── TCP [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg] ──────────────
# 중심: x=85.91  y=-385.37  z=569.66  rx=86.05  ry=67.57  rz=-89.18
#   좌/우: x ±270 mm (27 cm),  상/하: z ±185 mm (18.5 cm)
HOME_POSES = {
    # 기준(top_right): [-30.89, 153.46, 728.41, 101.39, 64.83, -93.78]
    # left = +X +520 mm  /  bottom = -Z -300 mm
    'top_right':    [ -30.89, 153.46, 728.41, 101.39, 64.83, -93.78],
    'top_left':     [ 489.11, 153.46, 728.41, 101.39, 64.83, -93.78],
    'bottom_right': [ -30.89, 153.46, 428.41, 101.39, 64.83, -93.78],
    'bottom_left':  [ 489.11, 153.46, 428.41, 101.39, 64.83, -93.78],
}
HOME_POSE_DEFAULT = 'top_right'


def _auto_episode(raw_dir: str) -> str:
    existing = sorted(Path(raw_dir).glob('episode_*'))
    return f'{len(existing) + 1:03d}'


class TeleopRecordAndConvertEEF:
    def __init__(self, episode: str, task: str, category: str = '', raw_dir: str = '', mid_dir: str = '',
                 skip_convert: bool = False, home_pose: str = HOME_POSE_DEFAULT):
        self._episode      = episode
        self._task         = task
        self._category     = category
        self._raw_dir      = raw_dir or RAW_DIR
        self._mid_dir      = mid_dir or str(WS_DIR / 'data/mid')
        self._skip_convert = skip_convert
        self._home_pose    = HOME_POSES.get(home_pose, HOME_POSES[HOME_POSE_DEFAULT])
        self._home_pose_name = home_pose
        self._procs: list  = []

        rclpy.init()
        self._node = rclpy.create_node('teleop_record_and_convert_eef')
        self._executor = MultiThreadedExecutor(num_threads=4)
        self._executor.add_node(self._node)
        threading.Thread(target=self._executor.spin, daemon=True).start()
        self._logger = self._node.get_logger()

        self._camera  = CameraNode(
            ros_image_topic=CAMERA_TOPIC,
            ros_node=self._node,
        )
        self._robot   = DoosanController(self._node, robot_id=ROBOT_ID, action_mode='cartesian')
        self._gripper = GripperController(ros_node=self._node, robot_id=ROBOT_ID)

        # 퍼블리셔
        self._gripper_pub = self._node.create_publisher(Float32, '/gripper/position', 10)
        # EEF pose 퍼블리셔 (추가)  [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]
        self._eef_pub = self._node.create_publisher(Float32MultiArray, '/dsr01/tcp_pose', 10)

        self._logger.info(f'YOLO 로드: {YOLO_MODEL}')
        self._yolo = YOLO(YOLO_MODEL)

        os.makedirs(RECORD_DIR, exist_ok=True)
        run_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._csv_file = os.path.join(RECORD_DIR, f'{run_ts}_eef.csv')
        with open(self._csv_file, 'w', newline='') as f:
            csv.writer(f).writerow([
                'Timestamp',
                'X_mm', 'Y_mm', 'Z_mm', 'Rx_deg', 'Ry_deg', 'Rz_deg',
                'Gripper_ratio',
            ])

        os.makedirs(self._raw_dir, exist_ok=True)
        self._bag_dir   = os.path.join(self._raw_dir, f'episode_{episode}_{run_ts}_eef')
        self._is_moving = False
        self._gripper_target = 0
        self._gripper_input  = ''

    # ── 인프라 관리 ────────────────────────────────────────────────────────────

    def _start_infra(self):
        rs = subprocess.Popen([
            'ros2', 'launch', 'realsense2_camera', 'rs_launch.py',
            'enable_color:=true', 'enable_depth:=true',
            'rgb_camera.color_profile:=640x480x30',
            'depth_module.depth_profile:=640x480x30',
            'align_depth.enable:=true',
        ])
        self._procs.append(rs)

        self._logger.info('카메라 첫 프레임 대기 중 (최대 30초)...')
        deadline = time.time() + 30.0
        while not self._camera.ready:
            if time.time() > deadline:
                raise RuntimeError('카메라 타임아웃. RealSense 연결을 확인하세요.')
            time.sleep(0.2)
        self._logger.info('카메라 준비 완료.')

        bag = subprocess.Popen([
            'ros2', 'bag', 'record',
            '--qos-profile-overrides-path', QOS_FILE,
            '-o', self._bag_dir,
            '/dsr01/joint_states',
            '/dsr01/tcp_pose',               # ← EEF pose 추가
            '/camera/camera/color/image_raw',
            '/gripper/position',
        ])
        self._procs.append(bag)
        time.sleep(1)
        self._logger.info('인프라 준비 완료.')

    def _stop_infra(self):
        for p in reversed(self._procs):
            try:
                p.send_signal(signal.SIGINT)
            except ProcessLookupError:
                pass
        time.sleep(1)
        for p in self._procs:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
        self._procs.clear()

    # ── 로봇 제어 ──────────────────────────────────────────────────────────────

    def _move_robot_async(self, dx=0, dy=0, dz=0, drx=0, dry=0, drz=0):
        if self._is_moving:
            return
        eef = self._robot.get_eef_pose()
        if eef is None:
            return
        target = eef.copy()
        target[0] += dx;  target[1] += dy;  target[2] += dz
        target[3] += drx; target[4] += dry; target[5] += drz

        def task():
            self._is_moving = True
            try:
                self._robot.move_line(target.tolist(), velocity=40.0, acceleration=80.0)
            finally:
                self._is_moving = False
        threading.Thread(target=task, daemon=True).start()

    def _open_gripper_async(self):
        self._gripper_target = 0
        threading.Thread(target=self._gripper.open, daemon=True).start()

    def _close_gripper_async(self):
        self._gripper_target = GRIPPER_CLOSE_POS
        threading.Thread(
            target=lambda: self._gripper.close(target_pos=GRIPPER_CLOSE_POS),
            daemon=True,
        ).start()

    def _move_gripper_to_async(self, pos: int):
        pos = max(0, min(GRIPPER_MAX_POS, pos))
        self._gripper_target = pos
        threading.Thread(target=lambda: self._gripper.move_to(pos), daemon=True).start()

    def _publish_state(self):
        """그리퍼 + EEF pose 동시 퍼블리시."""
        # 그리퍼
        grip_msg = Float32()
        grip_msg.data = float(self._gripper.get_position())
        self._gripper_pub.publish(grip_msg)

        # EEF pose
        eef = self._robot.get_eef_pose()
        if eef is not None:
            eef_msg = Float32MultiArray()
            eef_msg.data = eef.tolist()   # [x,y,z,rx,ry,rz]
            self._eef_pub.publish(eef_msg)

    def _move_to_home(self) -> None:
        """홈 포즈로 이동 (blocking). 진행 중인 비동기 이동 완료 후 실행."""
        # 비동기 이동 완료 대기 (최대 5초)
        deadline = time.time() + 5.0
        while self._is_moving and time.time() < deadline:
            time.sleep(0.1)
        print(f'[홈] {self._home_pose_name} → {[round(v, 2) for v in self._home_pose]}')
        self._robot.move_line(self._home_pose, velocity=30.0, acceleration=60.0)
        self._move_gripper_to_async(350)

    # ── 메인 루프 ──────────────────────────────────────────────────────────────

    def run(self):
        # ── 녹화 시작 전 홈 포즈 이동 ─────────────────────────────────────────
        print('\n================================================')
        print(f' 홈 포즈로 이동 중 (녹화 시작 전) : {self._home_pose_name}')
        print('================================================')
        self._move_to_home()

        self._start_infra()

        WIN = 'Teleop+Record+Convert (EEF)  (Esc → 홈 복귀 & 종료)'
        cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)

        waiting = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(waiting, 'Waiting for camera...', (120, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2, cv2.LINE_AA)

        deadline = time.time() + 20.0
        while not self._camera.ready:
            cv2.imshow(WIN, waiting)
            if cv2.waitKey(100) & 0xFF == 27:
                cv2.destroyAllWindows()
                self._stop_infra()
                return
            if time.time() > deadline:
                self._logger.error('카메라 타임아웃.')
                cv2.destroyAllWindows()
                self._stop_infra()
                return

        self._logger.info('텔레오퍼레이션 시작.')
        print('\n================ 조작 방법 ================')
        print(' [A]/[D]   : X축 (좌/우)')
        print(' [W]/[S]   : Y축 (앞/뒤)')
        print(' [Q]/[E]   : Z축 (위/아래)')
        print(' [J]/[L]   : Rx (+/-)')
        print(' [I]/[K]   : Ry (+/-)')
        print(' [N]/[M]   : Rz (+/-)')
        print(' [O]/[P]   : 그리퍼 완전 열기/닫기(500)')
        print(' [0~9...]  : 그리퍼 위치 직접 입력 → Enter 전송')
        print(' [Space]   : 현재 EEF pose·그리퍼 상태 CSV 기록')
        print(' [Esc]     : 홈 포즈 복귀 → 녹화 종료')
        print('==========================================')
        print(f' Episode  : {self._episode}')
        print(f' Bag      : {self._bag_dir}')
        print(f' Task     : {self._task}')
        print(f' Home     : {self._home_pose_name}')
        print('==========================================\n')

        while True:
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                time.sleep(0.05)
                continue

            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            for box in self._yolo.predict(frame, verbose=False, conf=CONF_THRESHOLD)[0].boxes:
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                color = (0, 0, 255) if cls_id == 0 else (0, 200, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f'{self._yolo.names[cls_id]} {float(box.conf[0]):.2f}',
                            (x1, max(y1 - 10, 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            age = self._camera.frame_age
            if age > 1.0:
                msg_txt = f'CAMERA OFFLINE ({age:.0f}s) - frames lost!'
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 180), -1)
                cv2.putText(frame, msg_txt, (10, 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            self._publish_state()   # 그리퍼 + EEF 동시 퍼블리시

            if self._gripper_input:
                overlay_txt = f'Gripper > {self._gripper_input}_  (Enter: 전송 / Esc: 취소)'
                cv2.rectangle(frame, (0, frame.shape[0] - 40), (frame.shape[1], frame.shape[0]), (30, 30, 30), -1)
                cv2.putText(frame, overlay_txt, (10, frame.shape[0] - 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow(WIN, frame)
            key = cv2.waitKey(1) & 0xFF

            if self._gripper_input:
                if ord('0') <= key <= ord('9'):
                    self._gripper_input += chr(key)
                elif key == 8:
                    self._gripper_input = self._gripper_input[:-1]
                elif key in (13, 10):
                    try:
                        self._move_gripper_to_async(int(self._gripper_input))
                        print(f'[Gripper] → {self._gripper_target}')
                    except ValueError:
                        pass
                    self._gripper_input = ''
                elif key == 27:
                    self._gripper_input = ''
                continue

            if   key == 27: break
            elif key in (ord('w'), ord('W')): self._move_robot_async(dy= STEP_MM)
            elif key in (ord('s'), ord('S')): self._move_robot_async(dy=-STEP_MM)
            elif key in (ord('a'), ord('A')): self._move_robot_async(dx= STEP_MM)
            elif key in (ord('d'), ord('D')): self._move_robot_async(dx=-STEP_MM)
            elif key in (ord('q'), ord('Q')): self._move_robot_async(dz= STEP_MM)
            elif key in (ord('e'), ord('E')): self._move_robot_async(dz=-STEP_MM)
            elif key in (ord('j'), ord('J')): self._move_robot_async(drx= STEP_DEG)
            elif key in (ord('l'), ord('L')): self._move_robot_async(drx=-STEP_DEG)
            elif key in (ord('i'), ord('I')): self._move_robot_async(dry= STEP_DEG)
            elif key in (ord('k'), ord('K')): self._move_robot_async(dry=-STEP_DEG)
            elif key in (ord('n'), ord('N')): self._move_robot_async(drz= STEP_DEG)
            elif key in (ord('m'), ord('M')): self._move_robot_async(drz=-STEP_DEG)
            elif key in (ord('o'), ord('O')): self._open_gripper_async()
            elif key in (ord('p'), ord('P')): self._close_gripper_async()
            elif ord('0') <= key <= ord('9'):
                self._gripper_input = chr(key)
            elif key == ord(' '):
                eef = self._robot.get_eef_pose()
                g   = self._gripper.get_position()
                if eef is not None:
                    ts  = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    row = [ts] + eef.tolist() + [g]
                    with open(self._csv_file, 'a', newline='') as f:
                        csv.writer(f).writerow(row)
                    print(f'[{ts}] EEF: {np.round(eef, 2).tolist()}  grip={g:.3f}')
                else:
                    self._logger.warn('EEF pose를 가져오지 못했습니다.')

        cv2.destroyAllWindows()
        # ── 홈 포즈 복귀 (bag 녹화 중) ───────────────────────────────────────
        print('\n================================================')
        print(f' 홈 포즈로 복귀 중 (녹화 중) : {self._home_pose_name}')
        print('================================================')
        self._move_to_home()
        print('\n인프라 종료 중...')
        self._stop_infra()
        if self._skip_convert:
            self._append_to_catalog()
            print(f'\n[녹화 완료] bag 저장 경로: {self._bag_dir}')
            print('변환은 건너뜁니다 (--skip-convert). teleop_convert_eef.sh 로 별도 변환하세요.')
        else:
            self._convert()

    def _append_to_catalog(self):
        """녹화 완료 후 episodes_catalog.yaml에 새 항목을 추가."""
        catalog_path = Path(self._raw_dir) / 'episodes_catalog.yaml'
        ep_name = Path(self._bag_dir).name

        new_entry = (
            f'\n  {ep_name}:\n'
            f'    category: "{self._category}"\n'
            f'    task: "{self._task}"\n'
            f'    quality: good\n'
            f'    notes: ""\n'
        )

        if catalog_path.exists():
            with open(catalog_path, 'a', encoding='utf-8') as f:
                f.write(new_entry)
        else:
            header = (
                '# VLA 데이터셋 에피소드 카탈로그\n'
                '# quality: good / review / skip\n\n'
                'episodes:\n'
            )
            with open(catalog_path, 'w', encoding='utf-8') as f:
                f.write(header + new_entry)

        print(f'[카탈로그] 항목 추가: {ep_name}')

    def _convert(self):
        self._append_to_catalog()
        print('\n================================================')
        print(' LeRobot EEF 데이터셋 변환 시작')
        print('================================================')
        cmd = ['python3', str(WS_DIR / 'src/bag_to_lerobot_eef.py'),
               '--task',       self._task,
               '--raw-dir',    self._raw_dir,
               '--output-dir', str(Path(self._mid_dir) / DATASET_NAME)]
        if self._category:
            cmd += ['--category', self._category]
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print(f'\n완료 → {self._mid_dir}/{DATASET_NAME}')
        else:
            print(f'\n변환 실패 (종료 코드: {result.returncode})')

    def shutdown(self):
        self._stop_infra()
        try:
            self._executor.shutdown()
        except Exception:
            pass
        self._camera.release()
        self._node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description='EEF delta 데이터셋 수집용 텔레오퍼레이션 + bag 녹화 + LeRobot 변환'
    )
    parser.add_argument('--episode',  default=None)
    parser.add_argument('--task',     default=DEFAULT_TASK)
    parser.add_argument('--category', default='',
                        help='데이터 카테고리 (예: baseline_no_occlusion, leaf_occlusion, ...)')
    parser.add_argument('--raw-dir',  default='',
                        help='raw bag 저장 경로 (기본값: <ws>/data/raw/final_project)')
    parser.add_argument('--mid-dir',  default='',
                        help='변환 데이터셋 저장 경로 (기본값: <ws>/data/mid)')
    parser.add_argument('--skip-convert', action='store_true',
                        help='녹화만 수행하고 LeRobot 변환은 건너뜀 (teleop_convert_eef.sh 로 별도 변환)')
    parser.add_argument('--home-pose', default=HOME_POSE_DEFAULT,
                        choices=list(HOME_POSES.keys()),
                        help=f'시작/종료 홈 포즈 선택 (기본값: {HOME_POSE_DEFAULT})')
    args = parser.parse_args()

    raw_dir = args.raw_dir or RAW_DIR
    os.makedirs(raw_dir, exist_ok=True)
    episode = args.episode or _auto_episode(raw_dir)

    print(f'에피소드: {episode}')
    print(f'태스크:   {args.task}')
    print(f'카테고리: {args.category or "(없음)"}')
    print(f'홈 포즈:  {args.home_pose}  {HOME_POSES[args.home_pose]}')
    print(f'raw 경로: {raw_dir}')
    print(f'mid 경로: {args.mid_dir or str(WS_DIR / "data/mid")}')

    app = TeleopRecordAndConvertEEF(episode=episode, task=args.task,
                                    category=args.category, raw_dir=raw_dir,
                                    mid_dir=args.mid_dir,
                                    skip_convert=args.skip_convert,
                                    home_pose=args.home_pose)
    try:
        app.run()
    except KeyboardInterrupt:
        print('\n중단됨.')
    finally:
        app.shutdown()


if __name__ == '__main__':
    main()
