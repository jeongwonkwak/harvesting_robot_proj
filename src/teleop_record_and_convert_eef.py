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
STEP_MM        = 60.0
STEP_DEG       = 20.0
VELOCITY       = 3000.0
ACCELERATION   = 800.0
RECORD_DIR     = str(WS_DIR / 'src/teleop_records')
RAW_DIR        = str(WS_DIR / 'data/raw/final_project')
DATASET_NAME   = 'vla_dataset_v0.3.0'
QOS_FILE       = str(WS_DIR / 'config/bag_qos_overrides.yaml')
CAMERA_TOPIC        = '/camera/camera/color/image_raw'
CAMERA2_TOPIC       = '/camera2/camera2/color/image_raw'
# RealSense 시리얼 번호 (ros2 device-list 로 확인 후 입력. 빈 칸 = 먼저 발견된 장치 사용)
# 두 카메라가 동시에 연결되어 있을 때는 반드시 시리얼 번호를 지정해야 함
SERIAL_CAM1         = ''   # YOLO 인식 카메라 시리얼 (예: '123622270786')
SERIAL_CAM2         = ''   # 전경 카메라 시리얼     (예: '215122253389')
DEFAULT_TASK        = 'Approach the red object closely and pick it up.'
GRIPPER_CLOSE_POS   = 500
GRIPPER_MAX_POS     = 740

# ── 홈 포즈 ── TCP [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg] ──────────────
# NW=top_left / NE=top_right / SE=bottom_right / SW=bottom_left
HOME_POSES = {
    'top_right':    [ 285.75, 347.14, 730.58,  85.94, 65.09, -88.59],  # NE
    'top_left':     [-245.34, 373.90, 741.39,  86.46, 66.60, -88.80],  # NW
    'bottom_right': [ 284.91, 346.35, 342.92,  86.37, 64.04, -89.22],  # SE
    'bottom_left':  [-248.59, 366.73, 348.70,  86.47, 64.81, -88.15],  # SW
}
HOME_POSE_DEFAULT = 'top_left'


def _auto_episode(raw_dir: str) -> str:
    existing = sorted(Path(raw_dir).glob('episode_*'))
    return f'{len(existing) + 1:03d}'


class TeleopRecordAndConvertEEF:
    def __init__(self, episode: str, task: str, category: str = '', raw_dir: str = '', mid_dir: str = '',
                 skip_convert: bool = False, home_pose: str = HOME_POSE_DEFAULT,
                 serial_cam1: str = '', serial_cam2: str = ''):
        self._episode      = episode
        self._task         = task
        self._category     = category
        self._raw_dir      = raw_dir or RAW_DIR
        self._mid_dir      = mid_dir or str(WS_DIR / 'data/mid')
        self._skip_convert = skip_convert
        self._home_pose    = HOME_POSES.get(home_pose, HOME_POSES[HOME_POSE_DEFAULT])
        self._home_pose_name = home_pose
        self._serial_cam1  = serial_cam1
        self._serial_cam2  = serial_cam2
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
        self._camera2 = CameraNode(
            ros_image_topic=CAMERA2_TOPIC,
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

        # YOLO 비동기 워커
        self._yolo_raw   = None
        self._yolo_lock  = threading.Lock()
        self._yolo_boxes = []
        threading.Thread(target=self._yolo_worker, daemon=True).start()

        # 상태 퍼블리시 백그라운드 워커 (20Hz, 메인 루프 비차단)
        self._publish_running = True
        threading.Thread(target=self._publish_worker, daemon=True).start()

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
        # ── 카메라 1: YOLO 인식 (camera_namespace=camera) ────────────────────
        rs1_cmd = [
            'ros2', 'launch', 'realsense2_camera', 'rs_launch.py',
            'camera_namespace:=camera', 'camera_name:=camera',
            'enable_color:=true', 'enable_depth:=true',
            'rgb_camera.color_profile:=640x480x30',
            'depth_module.depth_profile:=640x480x30',
            'align_depth.enable:=true',
        ]
        if self._serial_cam1:
            rs1_cmd.append(f"serial_no:='{self._serial_cam1}'")
        rs1 = subprocess.Popen(rs1_cmd)
        self._procs.append(rs1)

        # ── 카메라 2: 전경 (camera_namespace=camera2) ─────────────────────────
        rs2_cmd = [
            'ros2', 'launch', 'realsense2_camera', 'rs_launch.py',
            'camera_namespace:=camera2', 'camera_name:=camera2',
            'enable_color:=true', 'enable_depth:=false',
            'rgb_camera.color_profile:=640x480x30',
        ]
        if self._serial_cam2:
            rs2_cmd.append(f"serial_no:='{self._serial_cam2}'")
        rs2 = subprocess.Popen(rs2_cmd)
        self._procs.append(rs2)

        # ── 두 카메라 모두 준비될 때까지 대기 ────────────────────────────────
        self._logger.info('두 카메라 첫 프레임 대기 중 (최대 40초)...')
        deadline = time.time() + 40.0
        while True:
            c1_ok = self._camera.ready
            c2_ok = self._camera2.ready
            if c1_ok and c2_ok:
                break
            if time.time() > deadline:
                missing = []
                if not c1_ok: missing.append('YOLO 카메라 (/camera)')
                if not c2_ok: missing.append('전경 카메라 (/camera2)')
                raise RuntimeError(f'카메라 타임아웃: {", ".join(missing)} — 연결 및 시리얼 번호를 확인하세요.')
            time.sleep(0.2)
        self._logger.info('두 카메라 준비 완료.')

        bag = subprocess.Popen([
            'ros2', 'bag', 'record',
            '--qos-profile-overrides-path', QOS_FILE,
            '-o', self._bag_dir,
            '/dsr01/joint_states',
            '/dsr01/tcp_pose',
            CAMERA_TOPIC,
            CAMERA2_TOPIC,
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

    # ── YOLO 백그라운드 워커 ───────────────────────────────────────────────────

    def _yolo_worker(self):
        """전용 스레드에서 YOLO 추론. 메인 루프 블로킹 없음."""
        while True:
            with self._yolo_lock:
                frame = self._yolo_raw
                self._yolo_raw = None
            if frame is None:
                time.sleep(0.005)
                continue
            try:
                boxes = []
                for box in self._yolo.predict(frame, verbose=False, conf=CONF_THRESHOLD)[0].boxes:
                    cls_id = int(box.cls[0])
                    boxes.append((
                        cls_id,
                        [int(v) for v in box.xyxy[0].tolist()],
                        float(box.conf[0]),
                        self._yolo.names[cls_id],
                    ))
                with self._yolo_lock:
                    self._yolo_boxes = boxes
            except Exception:
                pass

    def _publish_worker(self):
        """20Hz로 EEF pose + 그리퍼 상태를 퍼블리시. 메인 루프와 완전히 분리."""
        interval = 1.0 / 20.0
        while self._publish_running:
            try:
                self._publish_state()
            except Exception:
                pass
            time.sleep(interval)

    # ── 로봇 제어 ──────────────────────────────────────────────────────────────

    def _move_robot_async(self, dx=0, dy=0, dz=0, drx=0, dry=0, drz=0):
        if self._is_moving:
            return
        # 스레드 시작 전에 플래그 설정 → 레이스 컨디션 방지
        self._is_moving = True
        eef = self._robot.get_eef_pose()
        if eef is None:
            self._is_moving = False
            return
        target = eef.copy()
        target[0] += dx;  target[1] += dy;  target[2] += dz
        target[3] += drx; target[4] += dry; target[5] += drz

        def task():
            try:
                self._robot.move_line(target.tolist(), velocity=VELOCITY, acceleration=ACCELERATION)
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
        deadline = time.time() + 5.0
        while self._is_moving and time.time() < deadline:
            time.sleep(0.1)
        print(f'[홈] {self._home_pose_name} → {[round(v, 2) for v in self._home_pose]}')
        self._robot.move_line(self._home_pose, velocity=VELOCITY, acceleration=ACCELERATION)
        self._move_gripper_to_async(600)
        # 그리퍼 + 로봇이 완전히 정지할 때까지 대기
        time.sleep(1.0)

    # ── 메인 루프 ──────────────────────────────────────────────────────────────

    def run(self):
        # ── 녹화 시작 전 홈 포즈 이동 ─────────────────────────────────────────
        print('\n================================================')
        print(f' 홈 포즈로 이동 중 (녹화 시작 전) : {self._home_pose_name}')
        print('================================================')
        self._move_to_home()

        print('\n홈 포즈 도달 완료. 녹화를 시작합니다...')
        self._start_infra()

        WIN  = 'YOLO 인식 카메라  (Esc → 홈 복귀 & 종료)'
        WIN2 = '전경 카메라'
        cv2.namedWindow(WIN,  cv2.WINDOW_NORMAL)
        cv2.namedWindow(WIN2, cv2.WINDOW_NORMAL)

        waiting = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(waiting, 'Waiting for cameras...', (100, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2, cv2.LINE_AA)

        deadline = time.time() + 20.0
        while not (self._camera.ready and self._camera2.ready):
            cv2.imshow(WIN, waiting)
            cv2.imshow(WIN2, waiting)
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
        print(f' Cam1     : {CAMERA_TOPIC}  (YOLO 인식)')
        print(f' Cam2     : {CAMERA2_TOPIC}  (전경)')
        print('==========================================\n')

        while True:
            # ── 카메라 1: YOLO 인식 ───────────────────────────────────────────
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                time.sleep(0.05)
                continue

            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            # YOLO 워커에 최신 프레임 전달 (즉시 리턴)
            with self._yolo_lock:
                self._yolo_raw = frame.copy()
                boxes = list(self._yolo_boxes)
            # 이전 추론 결과를 현재 프레임에 오버레이
            for cls_id, (x1, y1, x2, y2), conf, name in boxes:
                color = (0, 0, 255) if cls_id == 0 else (0, 200, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f'{name} {conf:.2f}',
                            (x1, max(y1 - 10, 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            age = self._camera.frame_age
            if age > 1.0:
                msg_txt = f'CAMERA1 OFFLINE ({age:.0f}s) - frames lost!'
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 180), -1)
                cv2.putText(frame, msg_txt, (10, 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            if self._gripper_input:
                overlay_txt = f'Gripper > {self._gripper_input}_  (Enter: 전송 / Esc: 취소)'
                cv2.rectangle(frame, (0, frame.shape[0] - 40), (frame.shape[1], frame.shape[0]), (30, 30, 30), -1)
                cv2.putText(frame, overlay_txt, (10, frame.shape[0] - 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow(WIN, frame)

            # ── 카메라 2: 전경 ────────────────────────────────────────────────
            self._camera2.grab()
            rgb2, _ = self._camera2.get_images()
            if rgb2 is not None:
                frame2 = cv2.cvtColor(rgb2, cv2.COLOR_RGB2BGR)
                age2 = self._camera2.frame_age
                if age2 > 1.0:
                    msg2 = f'CAMERA2 OFFLINE ({age2:.0f}s)'
                    cv2.rectangle(frame2, (0, 0), (frame2.shape[1], 40), (0, 0, 180), -1)
                    cv2.putText(frame2, msg2, (10, 28),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow(WIN2, frame2)

            key = cv2.waitKey(33) & 0xFF  # ~30fps, 자동 반복 억제

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

        # ── 홈 포즈 복귀 (bag 녹화 중, 카메라 화면 유지) ────────────────────
        print('\n================================================')
        print(f' 홈 포즈로 복귀 중 (녹화 중) : {self._home_pose_name}')
        print('================================================')
        home_done = threading.Event()
        threading.Thread(
            target=lambda: (self._move_to_home(), home_done.set()),
            daemon=True,
        ).start()

        loop_start = time.time()
        while not home_done.is_set() or time.time() - loop_start < 3.0:
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is not None:
                frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
                if home_done.is_set():
                    label, color = '홈 복귀 완료 — 녹화 종료 중...', (0, 200, 200)
                else:
                    label, color = '홈 복귀 중... (녹화 중)', (0, 255, 100)
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 44), (0, 80, 0), -1)
                cv2.putText(frame, label, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)
                cv2.imshow(WIN, frame)
            self._camera2.grab()
            rgb2, _ = self._camera2.get_images()
            if rgb2 is not None:
                cv2.imshow(WIN2, cv2.cvtColor(rgb2, cv2.COLOR_RGB2BGR))
            cv2.waitKey(30)

        cv2.destroyAllWindows()
        self._publish_running = False
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
        self._camera2.release()
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
    parser.add_argument('--serial-cam1', default='',
                        help='YOLO 인식 카메라 RealSense 시리얼 번호 (빈 칸 = 자동)')
    parser.add_argument('--serial-cam2', default='',
                        help='전경 카메라 RealSense 시리얼 번호 (빈 칸 = 자동)')
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
    print(f'CAM1 시리얼: {args.serial_cam1 or "(자동)"}')
    print(f'CAM2 시리얼: {args.serial_cam2 or "(자동)"}')

    app = TeleopRecordAndConvertEEF(episode=episode, task=args.task,
                                    category=args.category, raw_dir=raw_dir,
                                    mid_dir=args.mid_dir,
                                    skip_convert=args.skip_convert,
                                    home_pose=args.home_pose,
                                    serial_cam1=args.serial_cam1,
                                    serial_cam2=args.serial_cam2)
    try:
        app.run()
    except KeyboardInterrupt:
        print('\n중단됨.')
    finally:
        app.shutdown()


if __name__ == '__main__':
    main()
