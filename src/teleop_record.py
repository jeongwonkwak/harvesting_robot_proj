#!/usr/bin/env python3
"""
teleop_record.py

실시간 카메라 영상(YOLO 오버레이) 확인과 함께
키보드로 로봇을 제어하고, 스페이스바 입력 시 관절/그리퍼 상태를 기록합니다.

실행 환경:
  conda activate robot_env
  python3 /home/user/robot_workspace/vla_ws/src/teleop_record.py

키맵:
  - W/S : X축 전진/후진
  - A/D : Y축 좌/우
  - Q/E : Z축 상/하
  - O/P : 그리퍼 열기/닫기
  - Space : 현재 상태 기록 (teleop_records.csv)
  - Esc : 종료
"""

import sys
import time
import threading
import csv
from datetime import datetime
import numpy as np
import cv2

import rclpy
from rclpy.executors import MultiThreadedExecutor

# grasp_vla 패키지 경로 추가
sys.path.insert(0, '/home/user/robot_workspace/vla_ws')
sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController
from ultralytics import YOLO

# ── 설정 ─────────────────────────────────────────────────────────────────────
YOLO_MODEL = "/home/user/robot_workspace/vla_ws/models/strawberry_yolo26m_unified/weights/last.pt"
GRIPPER_PORT = "/dev/ttyUSB0"
ROBOT_ID = "dsr01"
CONF_THRESHOLD = 0.3
STEP_MM  = 10.0   # 키보드 입력 시 이동할 거리 (mm)
STEP_DEG =  5.0   # 키보드 입력 시 회전할 각도 (deg)
RECORD_DIR  = "/home/user/robot_workspace/vla_ws/src/teleop_records"
CAMERA_INDEX = 4   # /dev/video4 = RealSense 컬러 스트림 (YUYV)


class TeleopRecordNode:
    def __init__(self):
        rclpy.init()
        self._node = rclpy.create_node("teleop_record_node")
        self._executor = MultiThreadedExecutor(num_threads=4)
        self._executor.add_node(self._node)

        # 백그라운드에서 rclpy spin 실행 (서비스 콜백 처리를 위함)
        self._spin_thread = threading.Thread(target=self._executor.spin, daemon=True)
        self._spin_thread.start()

        self._logger = self._node.get_logger()

        # 카메라 노드 초기화 (pyrealsense2 SDK 사용)
        self._camera = CameraNode(use_realsense=True)

        # 로봇 컨트롤러 (Cartesian 모드) 및 그리퍼 제어 초기화
        self._robot = DoosanController(self._node, robot_id=ROBOT_ID, action_mode="cartesian")
        self._gripper = GripperController(port=GRIPPER_PORT, ros_node=self._node, robot_id=ROBOT_ID)
        
        # 파인튜닝된 YOLO 모델 로드
        self._logger.info(f"YOLO 로드 중: {YOLO_MODEL}")
        self._yolo = YOLO(YOLO_MODEL)
        
        # 실행 시각 기반 CSV 파일 생성
        import os
        os.makedirs(RECORD_DIR, exist_ok=True)
        run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._record_file = os.path.join(RECORD_DIR, f"{run_ts}.csv")
        with open(self._record_file, 'w', newline='') as f:
            csv.writer(f).writerow([
                "Timestamp",
                "J1_rad", "J2_rad", "J3_rad", "J4_rad", "J5_rad", "J6_rad",
                "X_mm", "Y_mm", "Z_mm", "Rx_deg", "Ry_deg", "Rz_deg",
                "Gripper_Pos",
            ])
        
        self._is_moving = False

    def _move_robot_async(self, dx=0, dy=0, dz=0, drx=0, dry=0, drz=0):
        """비동기로 EEF 이동/회전 수행 (영상 지연 방지). 단위: mm / deg"""
        if self._is_moving:
            return

        eef = self._robot.get_eef_pose()
        if eef is None:
            self._logger.warn("EEF 자세를 가져올 수 없습니다.")
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
        threading.Thread(target=self._gripper.open, daemon=True).start()
        
    def _close_gripper_async(self):
        threading.Thread(target=self._gripper.close, daemon=True).start()

    def run(self):
        WIN = "Teleop & Record (Esc to Quit)"
        cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)

        self._logger.info("카메라 준비 대기 중...")
        waiting = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(waiting, "Waiting for camera...", (120, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2, cv2.LINE_AA)

        deadline = time.time() + 15.0
        while not self._camera.ready:
            self._camera.grab()
            cv2.imshow(WIN, waiting)
            if cv2.waitKey(100) & 0xFF == 27:   # Esc → 중단
                return
            if time.time() > deadline:
                self._logger.error("카메라 타임아웃 (15s). 카메라 인덱스/연결을 확인하세요.")
                return

        self._logger.info("카메라 준비 완료. 텔레오퍼레이션 시작.")
        print("\n================ 조작 방법 ================")
        print(" [W]/[S]   : Y축 (앞/뒤)")
        print(" [A]/[D]   : X축 (좌/우)")
        print(" [Q]/[E]   : Z축 (위/아래)")
        print(" [I]/[K]   : Rx (X축 회전 +/-)")
        print(" [J]/[L]   : Ry (Y축 회전 +/-)")
        print(" [N]/[M]   : Rz (Z축 회전 +/-)")
        print(" [O]/[P]   : 그리퍼 열기/닫기")
        print(" [Space]   : 현재 관절 및 그리퍼 상태 기록")
        print(" [Esc]     : 프로그램 종료")
        print("===========================================\n")
        print(f"기록 파일 위치: {self._record_file}\n")
        
        while True:
            # 1. 영상 가져오기
            self._camera.grab()
            rgb, depth = self._camera.get_images()
            if rgb is None:
                time.sleep(0.05)
                continue
                
            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            
            # 2. YOLO 객체 인식 (Ultralytics YOLO는 numpy array 입력 시 BGR을 기대함)
            results = self._yolo.predict(frame, verbose=False, conf=CONF_THRESHOLD)
            boxes = results[0].boxes
            
            # 3. 바운딩 박스 오버레이
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                
                # 클래스 0(stem)은 빨간색, 그 외는 초록색
                color = (0, 0, 255) if cls_id == 0 else (0, 200, 0)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                label = f"{self._yolo.names[cls_id]} {conf:.2f}"
                cv2.putText(frame, label, (x1, max(y1 - 10, 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
            # 4. 화면 출력 및 키 입력 처리
            cv2.imshow("Teleop & Record (Esc to Quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27: # Esc
                break
            elif key in (ord('w'), ord('W')):
                self._move_robot_async(dy= STEP_MM)
            elif key in (ord('s'), ord('S')):
                self._move_robot_async(dy=-STEP_MM)
            elif key in (ord('a'), ord('A')):
                self._move_robot_async(dx= STEP_MM)
            elif key in (ord('d'), ord('D')):
                self._move_robot_async(dx=-STEP_MM)
            elif key in (ord('q'), ord('Q')):
                self._move_robot_async(dz= STEP_MM)
            elif key in (ord('e'), ord('E')):
                self._move_robot_async(dz=-STEP_MM)
            elif key in (ord('i'), ord('I')):
                self._move_robot_async(drx= STEP_DEG)
            elif key in (ord('k'), ord('K')):
                self._move_robot_async(drx=-STEP_DEG)
            elif key in (ord('j'), ord('J')):
                self._move_robot_async(dry= STEP_DEG)
            elif key in (ord('l'), ord('L')):
                self._move_robot_async(dry=-STEP_DEG)
            elif key in (ord('n'), ord('N')):
                self._move_robot_async(drz= STEP_DEG)
            elif key in (ord('m'), ord('M')):
                self._move_robot_async(drz=-STEP_DEG)
            elif key in (ord('o'), ord('O')):
                self._open_gripper_async()
            elif key in (ord('p'), ord('P')):
                self._close_gripper_async()
            elif key == ord(' '): # Space
                # 기록 로직
                j_state = self._robot.get_joint_state()
                eef     = self._robot.get_eef_pose()        # [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]
                g_pos   = self._gripper.get_position() * 740.0  # 0~1 비율 → 0~740 raw

                if j_state is not None:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    eef_vals  = eef.tolist() if eef is not None else [None] * 6
                    row = [timestamp] + j_state.tolist() + eef_vals + [g_pos]
                    with open(self._record_file, 'a', newline='') as f:
                        csv.writer(f).writerow(row)

                    deg_state = np.round(np.degrees(j_state), 1)
                    eef_str   = [round(v, 2) for v in eef_vals] if eef is not None else 'N/A'
                    print(f"[{timestamp}] 기록 완료 | Joint(deg): {deg_state.tolist()} | EEF: {eef_str} | Gripper: {g_pos:.2f}")
                else:
                    self._logger.warn("관절 상태를 가져오지 못해 기록할 수 없습니다.")

        cv2.destroyAllWindows()
        
    def shutdown(self):
        """종료 시 자원 반납"""
        try:
            self._executor.shutdown()
        except Exception:
            pass
        self._camera.release()
        self._node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

def main():
    app = TeleopRecordNode()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n사용자에 의해 강제 종료되었습니다.")
    finally:
        app.shutdown()

if __name__ == "__main__":
    main()
