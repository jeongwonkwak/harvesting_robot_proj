#!/usr/bin/env python3
"""
teleop_record_and_convert.py

텔레오퍼레이션(CSV 기록) + ROS2 bag 녹화 + LeRobot 변환을 한 번에 수행합니다.
Esc 키를 누르면 bag이 저장되고 자동으로 LeRobot 데이터셋으로 변환됩니다.

실행:
  python3 src/teleop_record_and_convert.py
  python3 src/teleop_record_and_convert.py --episode 003
  python3 src/teleop_record_and_convert.py --task "Pick up the red object."

기존 파일은 그대로 유지됩니다:
  src/teleop_record.py              : 수동 조작만 (bag/변환 없음)
  src/collect_vision_and_convert.sh : 재생 기반 파이프라인
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

import cv2
import numpy as np
import rclpy
from rclpy.executors import MultiThreadedExecutor

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
RAW_DIR        = str(WS_DIR / 'data/raw')
QOS_FILE       = str(WS_DIR / 'config/bag_qos_overrides.yaml')
CAMERA_TOPIC        = '/camera/camera/color/image_raw'
DEFAULT_TASK        = 'Approach the red object closely and pick it up.'
GRIPPER_CLOSE_POS   = 500   # 0~740 raw (740 = 완전 닫힘, 500 = 적당히 닫힘)
GRIPPER_MAX_POS     = 740


def _auto_episode(raw_dir: str) -> str:
    existing = sorted(Path(raw_dir).glob('episode_*'))
    return f'{len(existing) + 1:03d}'


class TeleopRecordAndConvert:
    def __init__(self, episode: str, task: str):
        self._episode = episode
        self._task = task
        self._procs: list = []

        rclpy.init()
        self._node = rclpy.create_node('teleop_record_and_convert')
        self._executor = MultiThreadedExecutor(num_threads=4)
        self._executor.add_node(self._node)
        threading.Thread(target=self._executor.spin, daemon=True).start()
        self._logger = self._node.get_logger()

        # ROS2 토픽 구독 — RealSense 노드가 하드웨어를 점유하므로 직접 접근 금지
        self._camera = CameraNode(
            ros_image_topic=CAMERA_TOPIC,
            ros_node=self._node,
        )

        self._robot   = DoosanController(self._node, robot_id=ROBOT_ID, action_mode='cartesian')
        # ros_node 없이 시리얼 직접 접근 → 목표 위치(500) 제어 가능
        # gripper_state_publisher_node를 별도로 띄우지 않고 여기서 직접 /gripper/position 퍼블리시
        self._gripper = GripperController(ros_node=self._node, robot_id=ROBOT_ID)
        from std_msgs.msg import Float32
        self._gripper_pub = self._node.create_publisher(Float32, '/gripper/position', 10)

        self._logger.info(f'YOLO 로드: {YOLO_MODEL}')
        self._yolo = YOLO(YOLO_MODEL)

        os.makedirs(RECORD_DIR, exist_ok=True)
        run_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._csv_file = os.path.join(RECORD_DIR, f'{run_ts}.csv')
        with open(self._csv_file, 'w', newline='') as f:
            csv.writer(f).writerow(['Timestamp', 'J1_rad', 'J2_rad', 'J3_rad',
                                    'J4_rad', 'J5_rad', 'J6_rad', 'Gripper_Pos'])

        os.makedirs(RAW_DIR, exist_ok=True)
        self._bag_dir  = os.path.join(RAW_DIR, f'episode_{episode}_{run_ts}')
        self._is_moving = False
        self._gripper_target = 0      # 현재 목표 그리퍼 위치 (0~740)
        self._gripper_input  = ''     # 숫자 입력 버퍼

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

        # gripper_state_publisher_node 대신 스크립트 내에서 직접 퍼블리시하므로 별도 실행 불필요

        # 고정 sleep 대신 카메라가 실제로 프레임을 내보낼 때까지 대기
        self._logger.info('카메라 첫 프레임 대기 중 (최대 30초)...')
        deadline = time.time() + 30.0
        while not self._camera.ready:
            if time.time() > deadline:
                raise RuntimeError('카메라 타임아웃 (30초). RealSense 연결을 확인하세요.')
            time.sleep(0.2)
        self._logger.info('카메라 준비 완료.')

        bag = subprocess.Popen([
            'ros2', 'bag', 'record',
            '--qos-profile-overrides-path', QOS_FILE,
            '-o', self._bag_dir,
            '/dsr01/joint_states',
            '/camera/camera/color/image_raw',
            '/gripper/position',
        ])
        self._procs.append(bag)
        time.sleep(1)
        self._logger.info('인프라 준비 완료 (RealSense + 그리퍼 퍼블리셔 + bag recorder).')

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

    def _publish_gripper(self):
        from std_msgs.msg import Float32
        msg = Float32()
        msg.data = float(self._gripper.get_position())
        self._gripper_pub.publish(msg)

    # ── 메인 루프 ──────────────────────────────────────────────────────────────

    def run(self):
        self._start_infra()

        WIN = 'Teleop+Record+Convert  (Esc → 저장 & 변환)'
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
                self._logger.error('카메라 타임아웃. RealSense 연결을 확인하세요.')
                cv2.destroyAllWindows()
                self._stop_infra()
                return

        self._logger.info('카메라 준비 완료. 텔레오퍼레이션 시작.')
        print('\n================ 조작 방법 ================')
        print(' [A]/[D]   : X축 (좌/우)')
        print(' [W]/[S]   : Y축 (앞/뒤)')
        print(' [Q]/[E]   : Z축 (위/아래)')
        print(' [J]/[L]   : Rx (+/-)')
        print(' [I]/[K]   : Ry (+/-)')
        print(' [N]/[M]   : Rz (+/-)')
        print(' [O]/[P]   : 그리퍼 완전 열기/닫기(500)')
        print(' [0~9...]  : 그리퍼 위치 직접 입력 (0~740) → Enter 전송')
        print(' [Space]   : 현재 관절·그리퍼 상태 기록')
        print(' [Esc]     : 종료 → bag 저장 → LeRobot 변환')
        print('==========================================')
        print(f' Episode: {self._episode}')
        print(f' CSV:     {self._csv_file}')
        print(f' Bag:     {self._bag_dir}')
        print(f' Task:    {self._task}')
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

            # 카메라 끊김 경고 (마지막 프레임이 1초 이상 지난 경우)
            age = self._camera.frame_age
            if age > 1.0:
                msg = f'CAMERA OFFLINE ({age:.0f}s) - frames lost!'
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 180), -1)
                cv2.putText(frame, msg, (10, 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            self._publish_gripper()
            # 그리퍼 숫자 입력 오버레이
            if self._gripper_input:
                overlay_txt = f'Gripper > {self._gripper_input}_  (Enter: 전송 / Esc: 취소)'
                cv2.rectangle(frame, (0, frame.shape[0] - 40), (frame.shape[1], frame.shape[0]), (30, 30, 30), -1)
                cv2.putText(frame, overlay_txt, (10, frame.shape[0] - 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow(WIN, frame)
            key = cv2.waitKey(1) & 0xFF

            # 숫자 입력 모드
            if self._gripper_input:
                if ord('0') <= key <= ord('9'):
                    self._gripper_input += chr(key)
                elif key == 8:   # Backspace
                    self._gripper_input = self._gripper_input[:-1]
                elif key in (13, 10):  # Enter
                    try:
                        self._move_gripper_to_async(int(self._gripper_input))
                        print(f'[Gripper] → {self._gripper_target}')
                    except ValueError:
                        pass
                    self._gripper_input = ''
                elif key == 27:  # Esc → 입력 취소
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
                self._gripper_input = chr(key)   # 숫자 입력 모드 시작
            elif key == ord(' '):
                j_state = self._robot.get_joint_state()
                g_pos   = self._gripper.get_position() * 500
                if j_state is not None:
                    ts  = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    row = [ts] + j_state.tolist() + [g_pos]
                    with open(self._csv_file, 'a', newline='') as f:
                        csv.writer(f).writerow(row)
                    print(f'[{ts}] 기록 | Joint: {np.round(np.degrees(j_state), 1).tolist()} | Gripper: {g_pos:.1f}')
                else:
                    self._logger.warn('관절 상태를 가져오지 못했습니다.')

        cv2.destroyAllWindows()
        print('\n인프라 종료 중...')
        self._stop_infra()
        self._convert()

    def _convert(self):
        print('\n================================================')
        print(' LeRobot 데이터셋 변환 시작')
        print('================================================')
        result = subprocess.run(
            ['python3', str(WS_DIR / 'src/bag_to_lerobot.py'), '--task', self._task],
            check=False,
        )
        if result.returncode == 0:
            print(f'\n완료 → {WS_DIR}/data/mid/')
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
        description='텔레오퍼레이션 + bag 녹화 + LeRobot 변환 통합 스크립트'
    )
    parser.add_argument('--episode', default=None,
                        help='에피소드 번호 (기본: data/raw 폴더 수 + 1, e.g. 003)')
    parser.add_argument('--task', default=DEFAULT_TASK,
                        help='태스크 설명 (LeRobot 메타데이터에 기록됨)')
    args = parser.parse_args()

    os.makedirs(RAW_DIR, exist_ok=True)
    episode = args.episode or _auto_episode(RAW_DIR)

    print(f'에피소드: {episode}')
    print(f'태스크:   {args.task}')

    app = TeleopRecordAndConvert(episode=episode, task=args.task)
    try:
        app.run()
    except KeyboardInterrupt:
        print('\n중단됨.')
    finally:
        app.shutdown()


if __name__ == '__main__':
    main()
