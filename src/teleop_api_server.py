#!/usr/bin/env python3
"""
teleop_api_server.py — 텔레오퍼레이션 백엔드 API (포트 8767)

harvest_dashboard.py(8765) 의 버튼 클릭 → 실제 로봇 제어 + bag 녹화 관리.

환경변수:
  WS_DIR   작업 디렉토리 (기본: /home/user/robot_workspace/vla_ws)
  RAW_DIR  bag 저장 루트 (기본: WS_DIR/data/raw/final_project)
"""

import os, signal, subprocess, sys, threading, time
from datetime import datetime
from pathlib import Path

# ROS2 환경 초기화 (setup.bash를 subprocess로 source)
try:
    env_setup = subprocess.run(
        'bash -c "source /opt/ros/humble/setup.bash && source /home/user/robot_workspace/doosan_ws/install/setup.bash 2>/dev/null && env"',
        shell=True, capture_output=True, text=True, timeout=5
    )
    if env_setup.returncode == 0:
        for line in env_setup.stdout.split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                os.environ[k] = v
        print("[INFO] ROS2 환경 초기화 완료")
except Exception as e:
    print(f"[WARN] ROS2 환경 초기화 실패: {e}")

WS_DIR  = Path(os.environ.get('WS_DIR',  '/home/user/robot_workspace/vla_ws'))
# 기존 teleop_collect_eef.sh 와 동일한 경로
RAW_DIR = os.environ.get('RAW_DIR', str(WS_DIR / 'data/raw/final_project/vla_dataset_v0.3.0'))

# grasp_vla
sys.path.insert(0, str(WS_DIR))
sys.path.insert(0, str(WS_DIR / 'grasp_vla'))

# ROS2 기본 패키지 (rosidl_parser 등)
for _p in [
    '/opt/ros/humble/local/lib/python3.10/dist-packages',
    '/opt/ros/humble/lib/python3.10/dist-packages',
]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# doosan 워크스페이스 Python 패키지 (dsr_msgs2 등)
# install/ 내 .py 파일이 build/ 를 심볼릭 링크하므로 호스트 원본 경로 그대로 사용
import glob as _glob
for _p in _glob.glob('/home/user/robot_workspace/doosan_ws/install/*/lib/python3.10/site-packages'):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# ── 상수 ──────────────────────────────────────────────────────────────────────
ROBOT_ID          = 'dsr01'
VELOCITY          = 1500.0  # mm/s (일반 이동)
ACCELERATION      = 250.0   # mm/s²
HOME_VELOCITY     = 200.0   # mm/s (홈 포즈 이동만 더 느리게)
HOME_ACCELERATION = 20.0    # mm/s²
GRIPPER_HOME_POS  = 600
GRIPPER_MAX_POS   = 740  # 파지: 0~740
STEP_MM           = 20.0  # 한 번 이동 거리 (mm) — 현재 미사용 (jog 모드로 대체)
STEP_DEG          = 5.0  # Rx, Ry, Rz 회전 각도

# ── 관절 소프트 리미트 (MoveIt joint_limits.yaml 기준, 추가 5° 마진) ───────────
def _load_joint_soft_limits():
    import yaml, math
    _YAML  = ('/home/user/robot_workspace/doosan_ws/install/'
              'dsr_moveit_config_e0509/share/dsr_moveit_config_e0509/'
              'config/joint_limits.yaml')
    _MARGIN_RAD = math.radians(5.0)  # MoveIt 리미트에서 추가 5° 여유
    _NAMES = ['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6']
    try:
        with open(_YAML) as f:
            cfg = yaml.safe_load(f)
        jl = cfg.get('joint_limits', {})
        ordered = []
        for n in _NAMES:
            lo = float(jl[n]['min_position']) + _MARGIN_RAD
            hi = float(jl[n]['max_position']) - _MARGIN_RAD
            ordered.append((lo, hi))
        print('[LIMIT] 소프트 리미트 (MoveIt ±5°):',
              [(round(math.degrees(l),1), round(math.degrees(h),1)) for l,h in ordered])
        return ordered
    except Exception as e:
        print(f'[LIMIT] yaml 파싱 실패, 기본값 사용: {e}')
        return [(-3.05, 3.05), (-1.57, 1.57), (-2.27, 2.27),
                (-3.05, 3.05), (-2.27, 2.27), (-3.05, 3.05)]

JOINT_SOFT_LIMITS = _load_joint_soft_limits()  # [(lo_rad, hi_rad), ...]

# ── jog 모드 상수 (jog_multi 서비스 기반 — 드라이버가 직접 연속 속도 제어) ────
# JogMulti 최대 속도: 250mm/s × 1.73 ≈ 432mm/s
# JOG_SPEED_PCT=20 → 평행이동 ~85mm/s (안정적인 속도)
JOG_SPEED_PCT    = 20.0  # 기본 jog 속도 (%) — speed_scale로 조정 가능
JOG_AXIS_MAP = {
    'forward':   [ 0,  1,  0,  0,  0,  0],  # +Y
    'backward':  [ 0, -1,  0,  0,  0,  0],  # -Y
    'left':      [-1,  0,  0,  0,  0,  0],  # -X
    'right':     [ 1,  0,  0,  0,  0,  0],  # +X
    'up':        [ 0,  0,  1,  0,  0,  0],  # +Z
    'down':      [ 0,  0, -1,  0,  0,  0],  # -Z
    'rx_plus':   [ 0,  0,  0,  1,  0,  0],
    'rx_minus':  [ 0,  0,  0, -1,  0,  0],
    'ry_plus':   [ 0,  0,  0,  0,  1,  0],
    'ry_minus':  [ 0,  0,  0,  0, -1,  0],
    'rz_plus':   [ 0,  0,  0,  0,  0,  1],
    'rz_minus':  [ 0,  0,  0,  0,  0, -1],
    'rotate_cw': [ 0,  0,  0,  0,  0,  1],  # Rz+ (시계방향)
    'rotate_ccw':[ 0,  0,  0,  0,  0, -1],  # Rz- (반시계방향)
}
QOS_FILE          = str(WS_DIR / 'config/bag_qos_overrides.yaml')
CAMERA_TOPIC      = '/camera/camera/color/image_raw'
CAMERA2_TOPIC     = '/camera2/camera2/color/image_raw'
# teleop_record_and_convert_eef.py 와 동일한 시리얼 번호 (환경변수로 재정의 가능)
SERIAL_CAM1       = os.environ.get('SERIAL_CAM1', '215122254786')
SERIAL_CAM2       = os.environ.get('SERIAL_CAM2', '342622303457')

HOME_POSES = {
    'top_right':    [ 314.90, 279.89, 883.40,  89.90, 86.29, -89.62],  # NE
    'top_left':     [-225.46, 338.93, 902.31,  88.42, 87.31, -89.88],  # NW
    'bottom_right': [ 312.61, 302.83, 529.32,  89.90, 86.29, -89.62],  # SE
    'bottom_left':  [-247.70, 317.34, 533.88,  87.75, 86.31, -89.49],  # SW
}
HOME_POSE_DEFAULT = 'top_left'

MOVE_MAP = {
    'forward':    {'dy':  STEP_MM},  'backward':   {'dy': -STEP_MM},
    'left':       {'dx': -STEP_MM},  'right':      {'dx':  STEP_MM},
    'up':         {'dz':  STEP_MM},  'down':       {'dz': -STEP_MM},
    'rotate_cw':  {'drz':  STEP_DEG}, 'rotate_ccw': {'drz': -STEP_DEG},
    'rx_plus':    {'drx':  STEP_DEG}, 'rx_minus':   {'drx': -STEP_DEG},
    'ry_plus':    {'dry':  STEP_DEG}, 'ry_minus':   {'dry': -STEP_DEG},
    'rz_plus':    {'drz':  STEP_DEG}, 'rz_minus':   {'drz': -STEP_DEG},
}


def _auto_episode(raw_dir: str) -> str:
    existing = sorted(Path(raw_dir).glob('episode_*'))
    return f'{len(existing) + 1:03d}'


class TeleopAPIServer:
    def __init__(self, home_pose: str = HOME_POSE_DEFAULT):
        self._home_pose      = HOME_POSES.get(home_pose, HOME_POSES[HOME_POSE_DEFAULT])
        self._home_pose_name = home_pose
        self._is_moving      = False
        self._recording      = False
        self._starting       = False
        self._stopping       = False
        self._bag_proc       = None
        self._eef_cache      = None
        self._eef_lock       = threading.Lock()
        self._episode        = None
        self._task           = ''
        self._category       = ''
        self._bag_dir        = None
        self._cam_procs      = []   # 카메라 subprocess 목록

        # 로봇 연결 상태
        self._robot_ready    = False
        self._robot_error    = ''
        self._robot          = None
        self._gripper        = None
        self._node           = None

        # 데이터 변환 상태
        self._converting     = False
        self._convert_progress = 0  # 0-100

        # jog 모드 상태
        self._jogging  = False  # 현재 jog 중 여부

        # 카메라는 호스트에서 실행 (컨테이너 내 librealsense는 D455 펌웨어와 호환되지 않아
        # 프레임이 수신되지 않음). start_cameras.sh 로 호스트에서 띄운다.
        self._init_ros()

    def _start_cameras(self):
        """teleop_record_and_convert_eef.py 와 동일하게 rs_launch.py 로 카메라를 시작."""
        print('[카메라] RealSense 노드 시작 중...')
        rs1_cmd = [
            'ros2', 'launch', 'realsense2_camera', 'rs_launch.py',
            'camera_namespace:=camera', 'camera_name:=camera',
            'enable_color:=true', 'enable_depth:=true',
            'rgb_camera.color_profile:=640x480x30',
            'depth_module.depth_profile:=640x480x30',
            'align_depth.enable:=true',
        ]
        if SERIAL_CAM1:
            rs1_cmd.append(f"serial_no:='{SERIAL_CAM1}'")
        self._cam_procs.append(subprocess.Popen(rs1_cmd))

        rs2_cmd = [
            'ros2', 'launch', 'realsense2_camera', 'rs_launch.py',
            'camera_namespace:=camera2', 'camera_name:=camera2',
            'enable_color:=true', 'enable_depth:=false',
            'rgb_camera.color_profile:=640x480x30',
        ]
        if SERIAL_CAM2:
            rs2_cmd.append(f"serial_no:='{SERIAL_CAM2}'")
        self._cam_procs.append(subprocess.Popen(rs2_cmd))
        print('[카메라] 카메라 노드 시작됨 (준비까지 약 8~10초)')

    def _stop_cameras(self):
        for p in self._cam_procs:
            try: p.send_signal(signal.SIGINT)
            except ProcessLookupError: pass
        time.sleep(1)
        for p in self._cam_procs:
            try: p.wait(timeout=5)
            except subprocess.TimeoutExpired: p.kill()
        self._cam_procs.clear()

    def _init_ros(self):
        """ROS2 노드만 즉시 생성. 로봇 컨트롤러는 백그라운드에서 초기화해 서버 시작을 막지 않음."""
        try:
            import rclpy
            from rclpy.executors import MultiThreadedExecutor
            from std_msgs.msg import Float32, Float32MultiArray

            rclpy.init()
            self._node     = rclpy.create_node('teleop_api_server')
            self._executor = MultiThreadedExecutor(num_threads=4)
            self._executor.add_node(self._node)
            threading.Thread(target=self._executor.spin, daemon=True).start()
            self._logger = self._node.get_logger()

            self._Float32           = Float32
            self._Float32MultiArray = Float32MultiArray

            self._gripper_pub = self._node.create_publisher(Float32, '/gripper/position', 10)
            self._eef_pub     = self._node.create_publisher(Float32MultiArray, '/dsr01/tcp_pose', 10)

            # DoosanController 초기화는 서비스 대기(최대 15초)가 있으므로 백그라운드 실행
            threading.Thread(target=self._init_robot, daemon=True).start()

        except ImportError as e:
            self._robot_error = f'패키지 없음: {e}'
            print(f'[WARN] 로봇 비활성 — {self._robot_error}')
        except Exception as e:
            self._robot_error = str(e)
            print(f'[WARN] ROS2 초기화 실패 — {self._robot_error}')

    def _init_robot(self):
        """로봇·그리퍼 컨트롤러 초기화 (백그라운드). 서버는 이미 응답 중."""
        try:
            from grasp_vla.robot_controller import DoosanController
            from grasp_vla.gripper_controller import GripperController

            self._robot   = DoosanController(self._node, robot_id=ROBOT_ID, action_mode='cartesian')
            self._gripper = GripperController(ros_node=self._node, robot_id=ROBOT_ID)

            self._robot_ready = True
            self._robot_error = ''
            print('[OK] 로봇 초기화 완료')

            threading.Thread(target=self._publish_worker, daemon=True).start()

        except Exception as e:
            self._robot_error = str(e)
            print(f'[WARN] 로봇 초기화 실패 — {self._robot_error}')

    # ── 퍼블리시 워커 ────────────────────────────────────────────────────────────

    def _publish_worker(self):
        """20Hz EEF + 그리퍼 퍼블리시. 로봇 미응답 시 폴링 간격 늘림."""
        fail_count = 0
        while True:
            try:
                # jog 중에는 GetCurrentPose 서비스 호출을 건너뜀.
                # jog_multi 와 동시에 20Hz 서비스 콜이 들어가면 드라이버 큐가
                # 포화되어 흔들림·연결 끊김의 원인이 된다.
                if not self._jogging:
                    eef = self._robot.get_eef_pose()
                    if eef is not None:
                        with self._eef_lock:
                            self._eef_cache = eef
                        msg = self._Float32MultiArray()
                        msg.data = eef.tolist()
                        self._eef_pub.publish(msg)
                        fail_count = 0
                    else:
                        fail_count += 1

                grip_msg = self._Float32()
                # get_position()은 이미 0~1 ratio 반환 (0=열림, 1=닫힘)
                pos = float(self._gripper.get_position())
                grip_msg.data = max(0.0, min(1.0, pos))
                self._gripper_pub.publish(grip_msg)

            except Exception:
                fail_count += 1

            # 연속 실패 시 간격 점진적 증가 (최대 2초), 성공하면 50ms 복귀
            sleep_s = 0.05 if fail_count == 0 else min(2.0, 0.1 * (2 ** min(fail_count, 4)))
            time.sleep(sleep_s)

    # ── 로봇 이동 ────────────────────────────────────────────────────────────────

    def move_delta(self, dx=0, dy=0, dz=0, drx=0, dry=0, drz=0) -> tuple[bool, str]:
        if not self._robot_ready:
            return False, '로봇 미연결'
        if self._is_moving:
            return False, '이동 중'
        with self._eef_lock:
            eef = self._eef_cache
        if eef is None:
            return False, '로봇 위치 정보 없음 (로봇 드라이버 실행 여부 확인)'
        self._is_moving = True
        target = eef.copy()
        target[0]+=dx; target[1]+=dy; target[2]+=dz
        target[3]+=drx; target[4]+=dry; target[5]+=drz

        def _run():
            try:
                self._robot.move_line(target.tolist(), velocity=VELOCITY, acceleration=ACCELERATION)
            finally:
                self._is_moving = False

        threading.Thread(target=_run, daemon=True).start()
        return True, 'OK'

    # ── jog 모드 (jog_multi 서비스 — 드라이버가 직접 연속 속도 제어) ──────────────

    def start_jog(self, cmd: str, speed_scale: float = 1.0, angle_scale: float = 1.0):
        """방향 버튼 press → jog 시작. jog_multi 서비스 한 번 호출로 연속 이동."""
        if not self._robot_ready:
            return
        axis = JOG_AXIS_MAP.get(cmd)
        if axis is None:
            return

        # 이미 jog 중이면 먼저 정지 후 드라이버가 처리할 시간을 준다.
        # move_stop 과 jog_multi 가 call_async 로 순서 보장 없이 도착하면 흔들림 발생.
        if self._jogging:
            self._jogging = False
            self._robot.move_stop(stop_mode=3)
            time.sleep(0.12)  # 드라이버 감속 처리 대기

        is_rotation = any(axis[3:])
        scale = angle_scale if is_rotation else speed_scale
        self._jogging = True
        self._robot.jog_multi(axis, JOG_SPEED_PCT * scale)
        threading.Thread(target=self._jog_watchdog, daemon=True).start()

    def stop_jog(self):
        """방향 버튼 release → move_stop으로 즉시 정지."""
        self._jogging = False
        if self._robot_ready:
            self._robot.move_stop(stop_mode=3)  # DR_HOLD: 부드럽게 감속 정지

    def _jog_watchdog(self):
        """jog 중 50ms마다 관절각 감시 → 소프트 리미트 초과 시 즉시 정지."""
        import math
        while self._jogging:
            js = self._robot.get_joint_state()  # radians, ndarray(6) or None
            if js is not None:
                for i, (lo, hi) in enumerate(JOINT_SOFT_LIMITS):
                    if js[i] < lo or js[i] > hi:
                        deg = math.degrees(js[i])
                        print(f'[JOG LIMIT] J{i+1} = {deg:.1f}° 소프트 리미트 초과 → 정지')
                        self._jogging = False
                        self._robot.move_stop(stop_mode=3)
                        return
            time.sleep(0.05)

    def move_gripper(self, pos: int):
        if not self._robot_ready:
            return
        pos = max(0, min(GRIPPER_MAX_POS, pos))
        threading.Thread(target=lambda: self._gripper.move_to(pos), daemon=True).start()

    def move_to_home(self, move_gripper=True):
        """홈 포즈로 이동. move_gripper=False이면 그리퍼를 움직이지 않음 (녹화 종료 후)"""
        if not self._robot_ready:
            return
        deadline = time.time() + 5.0
        while self._is_moving and time.time() < deadline:
            time.sleep(0.1)
        self._robot.move_line(self._home_pose, velocity=HOME_VELOCITY, acceleration=HOME_ACCELERATION)
        if move_gripper:
            self.move_gripper(GRIPPER_HOME_POS)
        time.sleep(3.0)

    # ── 녹화 ────────────────────────────────────────────────────────────────────

    def start_recording(self, episode, task, category, raw_dir, home_pose=''):
        if not self._robot_ready:
            return False, '로봇 미연결 — 녹화 불가'
        if self._recording or self._starting:
            return False, '이미 녹화 중이거나 시작 진행 중'
        if home_pose and home_pose in HOME_POSES:
            self._home_pose      = HOME_POSES[home_pose]
            self._home_pose_name = home_pose
        self._starting = True
        self._episode  = episode
        self._task     = task
        self._category = category
        run_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._bag_dir  = os.path.join(raw_dir, f'episode_{episode}_{run_ts}_eef')

        def _start():
            try:
                print(f'[녹화] 홈 이동 중 ({self._home_pose_name})...')
                self.move_to_home()
                print(f'[녹화] bag 시작: {self._bag_dir}')
                self._bag_proc = subprocess.Popen([
                    'ros2', 'bag', 'record',
                    '--qos-profile-overrides-path', QOS_FILE,
                    '-o', self._bag_dir,
                    '/dsr01/joint_states', '/dsr01/tcp_pose',
                    CAMERA_TOPIC, CAMERA2_TOPIC, '/gripper/position',
                ])
                time.sleep(1)
                self._recording = True
                print(f'[녹화] 시작 — episode {self._episode}')
            except Exception as e:
                print(f'[녹화] 시작 실패: {e}')
            finally:
                self._starting = False

        threading.Thread(target=_start, daemon=True).start()
        return True, 'OK'

    def stop_recording(self):
        if not self._recording and not self._starting:
            return False, '녹화 중이 아님'
        if self._stopping:
            return False, '종료 진행 중'
        self._stopping  = True
        self._recording = False

        def _stop():
            try:
                # print('[녹화] 홈 복귀 중...')
                # self.move_to_home(move_gripper=False)  # 그리퍼는 파지 상태 유지, 3초 대기
                # print('[녹화] 로봇 정지 상태 녹화 중...')
                # time.sleep(5)  # 완전히 정지한 상태를 5초간 추가 녹화
                print('[녹화] 종료 중...')
                if self._bag_proc:
                    try:
                        self._bag_proc.send_signal(signal.SIGINT)
                        self._bag_proc.wait(timeout=10)
                    except (subprocess.TimeoutExpired, ProcessLookupError):
                        try: self._bag_proc.kill()
                        except ProcessLookupError: pass
                    self._bag_proc = None
                print('[녹화] 종료 완료')
            except Exception as e:
                print(f'[녹화] 종료 실패: {e}')
            finally:
                self._stopping = False

        threading.Thread(target=_stop, daemon=True).start()
        return True, 'OK'

    # ── 상태 ────────────────────────────────────────────────────────────────────

    def get_status(self) -> dict:
        with self._eef_lock:
            eef = self._eef_cache
        if   self._starting:  phase = 'starting'
        elif self._stopping:  phase = 'stopping'
        elif self._recording: phase = 'recording'
        else:                 phase = 'idle'

        # bridge(ros2_bridge.py)가 관리하는 상태파일도 함께 읽어서 반환
        state = {
            'phase':        phase,
            'recording':    self._recording,
            'is_moving':    self._is_moving,
            'robot_ready':  self._robot_ready,
            'robot_error':  self._robot_error,
            'eef_ready':    eef is not None,
            'episode':      self._episode,
            'task':         self._task,
            'category':     self._category,
            'bag_dir':      str(self._bag_dir) if self._bag_dir else None,
            'home_pose':    self._home_pose_name,
            'converting':   self._converting,
            'convert_progress': self._convert_progress,
        }
        # _eef_cache: 로봇에서 직접 읽은 TCP pose — 브리지 파일보다 우선
        if eef is not None:
            state['tcp_pose'] = eef.tolist()

        try:
            import json
            state_file = os.environ.get('HARVEST_STATE_FILE', '/data/harvest_state.json')
            if os.path.exists(state_file):
                with open(state_file) as f:
                    bridge_state = json.load(f)
                # None이 아닌 값만 반영 (유효값을 None으로 덮어쓰지 않음)
                tcp  = bridge_state.get('tcp_pose')
                ja   = bridge_state.get('joint_angles')
                grip = bridge_state.get('gripper')
                if tcp  is not None: state['tcp_pose']      = tcp
                if ja   is not None: state['joint_angles']  = ja
                if grip is not None: state['gripper']       = grip
        except Exception:
            pass
        return state


# ── FastAPI ────────────────────────────────────────────────────────────────────

_server: TeleopAPIServer = None
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])


@app.get('/status')
async def api_status():
    return JSONResponse(_server.get_status() if _server else {'robot_ready': False, 'robot_error': '서버 초기화 중'})


@app.post('/move')
async def api_move(request: Request):
    if not _server._robot_ready:
        return JSONResponse({'ok': False, 'message': '로봇 미연결'})

    b   = await request.json()

    # VLA 직접 delta 명령: dx, dy, dz, drx, dry, drz를 직접 받음
    if any(k in b for k in ['dx', 'dy', 'dz', 'drx', 'dry', 'drz']):
        delta = {k: b[k] for k in ['dx', 'dy', 'dz', 'drx', 'dry', 'drz'] if k in b}
        ok, msg = _server.move_delta(**delta)
        return JSONResponse({'ok': ok, 'message': msg})

    # 일반 명령
    cmd = b.get('command', 'stop')

    if cmd == 'stop':
        _server.stop_jog()
        return JSONResponse({'ok': True})
    elif cmd == 'joint':
        angles = b.get('angles', [0]*6)
        velocity = float(b.get('velocity', 50))
        threading.Thread(target=lambda: _server._robot.move_joint(angles, velocity=velocity), daemon=True).start()
        return JSONResponse({'ok': True})
    elif cmd == 'tcp':
        pose = b.get('pose', [0]*6)
        velocity = float(b.get('velocity', 100))
        threading.Thread(target=lambda: _server._robot.move_line(pose, velocity=velocity), daemon=True).start()
        return JSONResponse({'ok': True})

    if cmd not in JOG_AXIS_MAP:
        return JSONResponse({'ok': False, 'error': f'알 수 없는 커맨드: {cmd}'}, status_code=400)

    # 버튼 hold → jog 모드로 연속 이동
    speed_scale = float(b.get('speed_scale', 1.0))
    angle_scale = float(b.get('angle_scale', 1.0))
    _server.start_jog(cmd, speed_scale=speed_scale, angle_scale=angle_scale)
    return JSONResponse({'ok': True, 'message': f'jog 시작: {cmd}'})


@app.post('/spline')
async def api_spline(request: Request):
    if not _server._robot_ready:
        return JSONResponse({'ok': False, 'message': '로봇 미연결'})
    b = await request.json()
    waypoints = b.get('waypoints', [])
    if len(waypoints) < 2:
        return JSONResponse({'ok': False, 'error': '웨이포인트 2개 이상 필요'}, status_code=400)
    velocity     = float(b.get('velocity', 50.0))
    acceleration = float(b.get('acceleration', velocity * 2))
    threading.Thread(
        target=lambda: _server._robot.move_spline_task(
            waypoints, velocity=velocity, acceleration=acceleration),
        daemon=True,
    ).start()
    return JSONResponse({'ok': True, 'message': f'spline 이동 시작: {len(waypoints)}pts'})


@app.post('/gripper')
async def api_gripper(request: Request):
    if not _server._robot_ready:
        return JSONResponse({'ok': False, 'message': '로봇 미연결'})
    b = await request.json()
    _server.move_gripper(int(b.get('position', GRIPPER_HOME_POS)))
    return JSONResponse({'ok': True})


@app.post('/home')
async def api_home(request: Request):
    if not _server._robot_ready:
        return JSONResponse({'ok': False, 'message': '로봇 미연결'})
    try:
        b = await request.json()
        home_pose = b.get('home_pose', '')
    except:
        home_pose = ''

    def _move():
        if home_pose and home_pose in HOME_POSES:
            _server._home_pose = HOME_POSES[home_pose]
            _server._home_pose_name = home_pose
        _server.move_to_home()

    threading.Thread(target=_move, daemon=True).start()
    return JSONResponse({'ok': True})


@app.post('/record/start')
async def api_record_start(request: Request):
    b       = await request.json()
    raw_dir = b.get('raw_dir', RAW_DIR)
    os.makedirs(raw_dir, exist_ok=True)
    episode = b.get('episode') or _auto_episode(raw_dir)
    ok, msg = _server.start_recording(
        episode=episode, task=b.get('task',''),
        category=b.get('category',''), raw_dir=raw_dir,
        home_pose=b.get('home_pose',''),
    )
    return JSONResponse({'ok': ok, 'episode': episode, 'message': msg})


@app.post('/record/stop')
async def api_record_stop():
    ok, msg = _server.stop_recording()
    return JSONResponse({'ok': ok, 'message': msg})


@app.post('/convert')
async def api_convert():
    if _server._converting:
        return JSONResponse({'ok': False, 'message': '변환 진행 중'})

    script = str(WS_DIR / 'src/teleop_convert_eef.sh')
    if not Path(script).exists():
        return JSONResponse({'ok': False, 'message': f'스크립트 없음: {script}'})

    def _convert():
        _server._converting = True
        _server._convert_progress = 10
        try:
            print('[변환] 시작... (bag → LeRobot 변환 중)')

            # 변환 실행 (진행률 주기적 업데이트)
            proc = subprocess.Popen(['bash', script], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True)

            # 별도 스레드에서 진행률 업데이트
            import time
            start_time = time.time()
            while proc.poll() is None:
                elapsed = time.time() - start_time
                # 시간 기반 진행률 추정 (bag 변환 ~3-5분, quantile ~2-3분)
                progress = min(int(10 + elapsed / 360), 99)  # 10분에 90%
                _server._convert_progress = progress
                time.sleep(2)  # 2초마다 업데이트

            # 프로세스 완료 대기
            stdout, stderr = proc.communicate()

            if proc.returncode == 0:
                print('[변환] 완료!')
                _server._convert_progress = 100
            else:
                print(f'[WARN] 변환 실패 (exit code {proc.returncode})')
                if stderr:
                    print(f'오류: {stderr[:500]}')
                _server._convert_progress = 0

        except Exception as e:
            print(f'[WARN] 변환 실패: {e}')
            _server._convert_progress = 0
        finally:
            _server._converting = False

    threading.Thread(target=_convert, daemon=True).start()
    return JSONResponse({'ok': True, 'message': '변환 시작됨'})


@app.get('/health')
async def health():
    ready = _server is not None and _server._robot_ready
    return JSONResponse({'ok': ready}, status_code=200 if ready else 503)


# ── 진입점 ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--host',      default='0.0.0.0')
    p.add_argument('--port',      type=int, default=8767)
    p.add_argument('--home-pose', default=HOME_POSE_DEFAULT, choices=list(HOME_POSES.keys()))
    args = p.parse_args()

    global _server
    print('\n  텔레오퍼레이션 API 서버 시작 중...')
    _server = TeleopAPIServer(home_pose=args.home_pose)
    status = '연결됨' if _server._robot_ready else f'로봇 없음 ({_server._robot_error})'
    print(f'  로봇 상태: {status}')
    print(f'  API 주소: http://{args.host}:{args.port}\n')
    uvicorn.run(app, host=args.host, port=args.port, log_level='warning')


if __name__ == '__main__':
    main()
