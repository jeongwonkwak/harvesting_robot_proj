# vla_ws 워크스페이스 구조 정리

> 경로: `/home/user/robot_workspace/vla_ws`
> 목적: Doosan e0509 로봇으로 딸기 파지(grasp)를 수행하는 VLA(Vision-Language-Action) 기반 ROS2 워크스페이스

---

## 전체 디렉토리 구조

```
vla_ws/
├── grasp_vla/              # 핵심 ROS2 패키지 (소스)
├── src/                    # 실행 스크립트, 데이터 변환 툴
├── launch/                 # ROS2 launch 파일
├── config/                 # YAML 파라미터
├── data/                   # 데이터셋 (raw → mid → fin)
├── models/                 # YOLO 모델, pi05 모델
├── logs/                   # 실행 로그, 녹화 영상
├── episode_secenario/      # 에피소드 시나리오 스크립트
├── lerobot/                # HuggingFace LeRobot (서브모듈)
├── sroi_rosbag_utilities/  # ROS bag 유틸리티 (서브모듈)
├── build/                  # colcon 빌드 산출물 (자동생성)
├── install/                # colcon 설치 산출물 (자동생성)
├── log/                    # colcon 로그 (자동생성)
├── requirements.txt        # Python 의존성
├── setup.py / setup.cfg    # ROS2 패키지 설치 설정
└── resource/               # ROS2 ament 리소스 마커
```

---

## grasp_vla/ — 핵심 ROS2 패키지

VLA 기반 파지 파이프라인의 실질적인 구현이 담긴 메인 패키지.

| 파일 | 역할 |
|------|------|
| `__init__.py` | 패키지 초기화 |
| `grasp_pipeline.py` | **메인 VLA 파이프라인** — SmolVLA 서버 호출, 관절각도 기반 제어 |
| `grasp_pipeline_eef.py` | EEF delta action 기반 파이프라인 (Octo 등 EEF 출력 모델용) |
| `grasp_pipeline_pi05.py` | pi05_base HTTP 서버 기반 파이프라인 (32-dim 입출력) |
| `robot_controller.py` | Doosan e0509 제어 래퍼 (dsr_ros2 서비스 호출) |
| `gripper_controller.py` | Robotis RH-P12-RN-DF 그리퍼 제어 (Dynamixel SDK) |
| `gripper_state_publisher.py` | 그리퍼 위치를 ROS2 토픽으로 퍼블리시 |
| `camera_node.py` | RealSense D455 카메라 추상화 (ROS2 토픽 / RealSense SDK / OpenCV 폴백) |
| `smolvla_client.py` | SmolVLA HTTP API 클라이언트 |

### grasp_pipeline.py 주요 흐름

```
1. SmolVLA 서버 헬스체크
2. 그리퍼 열기
3. 홈 포즈로 이동 (선택)
4. VLA 제어 루프 (max_steps 반복)
   a. 카메라 프레임 캡처
   b. 관절 상태 + 그리퍼 위치 읽기 (7-dim state)
   c. SmolVLA 서버에 POST → 6-DoF action 수신
   d. 로봇 이동 (move_joint)
   e. 그리퍼 비율 설정
   f. grip_ratio >= threshold → 파지 성공 → 후퇴
5. 에피소드 영상 저장 (ffmpeg)
```

### robot_controller.py 주요 API

| 메서드 | 설명 |
|--------|------|
| `get_joint_state()` | 현재 관절 위치 반환 (rad, shape=(6,)) |
| `get_eef_pose()` | EEF pose 반환 [X,Y,Z,Rx,Ry,Rz] mm/deg |
| `move_joint(positions_deg)` | 절대 관절각도로 이동 (blocking) |
| `move_line(pose_mm_deg)` | 절대 Cartesian pose로 이동 (blocking) |
| `execute_action(action)` | VLA action 한 스텝 실행 (delta) |

- Doosan dsr_ros2 서비스 미사용 시 JointTrajectoryController 폴백
- Safety clamp: 위치 ±20mm/step, 회전 ±10deg/step, 관절 ±5deg/step

### camera_node.py 카메라 우선순위

```
0순위: ROS2 토픽 (Gazebo bridge, /camera/camera/color/image_raw 등)
1순위: Intel RealSense SDK (pyrealsense2)
2순위: OpenCV VideoCapture (/dev/video4, YUYV 포맷)
더미:  검정 프레임 (시뮬레이션 모드)
```

### smolvla_client.py

- 서버 주소: `http://192.168.50.79:16003` (기본값)
- `POST /predict` → action (7-dim float32): `[dx,dy,dz,drx,dry,drz,gripper]`
- 이미지는 256×256 JPEG base64로 인코딩하여 전송
- `reset_episode=True`로 에피소드 시작 시 액션 청크 버퍼 초기화

---

## src/ — 실행 스크립트 및 변환 툴

| 파일/폴더 | 역할 |
|-----------|------|
| `move_to_pose.py` | 로봇을 지정 포즈로 이동 (TCP/joint 모드, CLI) |
| `teleop_record.py` | 키보드 텔레오퍼레이션 + YOLO 오버레이 + 상태 기록 |
| `teleop_record_and_convert.py` | 텔레오퍼레이션 + bag 녹화 + LeRobot 변환 일괄처리 |
| `teleop_record_and_convert_eef.py` | EEF delta 기반 버전 (TCP pose bag 추가 녹화) |
| `teleop_record_and_convert_eef_org.py` | EEF 버전 원본 백업 |
| `bag_to_lerobot.py` | ROS2 bag → LeRobot v3.0 데이터셋 변환 (관절각도) |
| `bag_to_lerobot_eef.py` | ROS2 bag → LeRobot 변환 (EEF delta action) |
| `make_sample_dataset.py` | 샘플 데이터셋 생성 유틸 |
| `strawberry_occlusion_meter.py` | 딸기 가림(occlusion) 측정 |
| `harvest_dashboard.py` | 수확 대시보드 |
| `test_smolvla.py` | SmolVLA 서버 연결 테스트 |
| `teleop_records/` | 텔레오퍼레이션 기록 CSV (`YYYYMMDD_HHMMSS[_eef].csv`) |
| `dashboard/` | 대시보드 Docker 구성 |
| `collect_and_convert.sh` | 수집 + 변환 쉘 스크립트 |
| `collect_and_curobo_convert.sh` | curobo 수집 + 변환 |
| `collect_vision_and_convert.sh` | 비전 수집 + 변환 |
| `teleop_collect_eef.sh` | EEF 텔레오퍼레이션 수집 |
| `teleop_convert_eef.sh` | EEF 데이터 변환 |

### teleop_record.py 키맵

| 키 | 동작 |
|----|------|
| W/S | X축 전진/후진 (±10mm) |
| A/D | Y축 좌/우 (±10mm) |
| Q/E | Z축 상/하 (±10mm) |
| O/P | 그리퍼 열기/닫기 |
| Space | 현재 상태 기록 |
| Esc | 종료 |

### bag_to_lerobot.py 변환 구조

```
입력 ROS2 토픽:
  /dsr01/joint_states   → observation.state (관절각도 6-dim)
  /gripper/position     → observation.state (그리퍼 1-dim)
  /camera/camera/color/image_raw → observation.images.camera1

출력 LeRobot v3.0:
  data/chunk-000/file-000.parquet
  videos/observation.images.camera1/chunk-000/file-000.mp4
  meta/{info.json, stats.json, tasks.parquet}
```

---

## launch/ — ROS2 Launch 파일

| 파일 | 역할 |
|------|------|
| `grasp.launch.py` | **메인 VLA 파지 파이프라인** 실행 |
| `collect_episode.launch.py` | 에피소드 데이터 수집 |
| `collect_curobo.launch.py` | cuRobo 기반 수집 |
| `collect_vision.launch.py` | 비전 기반 수집 |
| `strawberry_harvest.launch.py` | 딸기 수확 전체 시나리오 |

### grasp.launch.py 주요 파라미터

| 파라미터 | 기본값 | 설명 |
|----------|--------|------|
| `smolvla_url` | `http://192.168.50.79:16003` | VLA 서버 주소 |
| `instruction` | `"Approach the red object..."` | 언어 명령 |
| `action_mode` | `cartesian` | `cartesian` 또는 `joint` |
| `max_steps` | `30` | 최대 제어 스텝 수 |
| `step_hz` | `5.0` | 제어 루프 주파수 |
| `gripper_port` | `/dev/ttyUSB0` | 그리퍼 시리얼 포트 |
| `robot_id` | `dsr01` | Doosan 네임스페이스 |
| `retreat_delta` | `[0,-137,61,0,0,0]` | 파지 후 후퇴 벡터 (mm) |
| `home_pose` | `""` | 사전 홈 포즈 (비어있으면 스킵) |

---

## config/ — 설정 파일

| 파일 | 역할 |
|------|------|
| `params.yaml` | ROS2 노드 파라미터 (data_collection, grasp_pipeline) |
| `bag_qos_overrides.yaml` | ros2 bag play 시 QoS 재설정 |

### params.yaml 주요 설정

```yaml
data_collection:
  bag_save_path: "/home/user/robot_workspace/vla_ws/data/raw"

grasp_pipeline:
  smolvla_url:   "http://192.168.50.79:16003"
  action_mode:   "cartesian"
  max_steps:     30
  step_hz:       10.0
  gripper_port:  "/dev/ttyUSB0"
  retreat_delta: [0.0, -137.0, 61.0, 0.0, 0.0, 0.0]
```

---

## data/ — 데이터셋

```
data/
├── raw/                    # ROS2 bag 원본
│   ├── final_project/
│   └── mini_project/
├── mid/                    # LeRobot v3.0 변환 결과
│   └── vla_dataset_v0.2.0/
│       ├── data/chunk-000/file-000.parquet
│       ├── videos/observation.images.camera1/chunk-000/*.mp4
│       └── meta/{info.json, stats.json, tasks.parquet, episodes/}
└── fin/                    # 최종 정제 데이터 (예정)
```

- `raw/` → bag 수집 → `mid/` 변환: `bag_to_lerobot.py` 또는 `bag_to_lerobot_eef.py`
- LeRobot 포맷은 HuggingFace datasets 호환

---

## models/ — 모델 파일

```
models/
├── strawberry_yolo26m_unified/   # 딸기 + 줄기 감지 YOLO 모델
│   ├── weights/
│   │   ├── best.pt               # 최적 체크포인트
│   │   ├── last.pt               # 마지막 체크포인트
│   │   └── stem_best.pt          # 줄기 전용 최적 체크포인트
│   ├── realsense_live.py         # RealSense 실시간 추론
│   ├── realsense_stem_pipeline.py
│   ├── stem_roi_utils.py
│   ├── args.yaml / args_832b8.yaml
│   ├── results.csv / results.png
│   └── [val_batch, confusion_matrix 등 학습 결과 이미지]
└── public/
    └── pi05_base/                # pi05 VLA 모델 (베이스)
```

- YOLO 모델: YOLOv8/v9 기반, 클래스: `stem(0)`, `ripe_strawberry` 등
- 입력 해상도: 832×832 (`args_832b8.yaml`)

---

## logs/ — 로그 및 녹화 영상

```
logs/
├── episode_001_*.log           # 에피소드 실행 로그
├── curobo_curobo_001_*.log     # cuRobo 세션 로그
├── vision_episode_001_*.log    # 비전 모드 로그
└── videos/
    ├── episode_YYYYMMDD_HHMMSS.mp4           # 관절 제어 에피소드
    ├── episode_eef_YYYYMMDD_HHMMSS.mp4       # EEF delta 에피소드
    └── episode_pi05_YYYYMMDD_HHMMSS.mp4      # pi05 모델 에피소드
```

- 영상은 `grasp_pipeline.py`의 `record_video=True` 옵션 시 ffmpeg로 자동 저장
- 저장 경로: `/home/user/robot_workspace/vla_ws/logs/videos/`

---

## episode_secenario/ — 에피소드 시나리오

| 파일 | 역할 |
|------|------|
| `grasp_ripe_strawberry.py` | YOLO 검출 + 캘리브레이션 기반 딸기 파지 시나리오 |
| `replay_teleop_records.py` | 텔레오퍼레이션 기록 재생 |

### grasp_ripe_strawberry.py 흐름

```
1. YOLO로 ripe_strawberry 검출 (신뢰도 >= 0.3)
2. Depth 이미지로 3D 위치 계산 (카메라 내부파라미터 사용)
3. 핸드-아이 캘리브레이션(eye-in-hand)으로 로봇 베이스 좌표 변환
4. pre-grasp 위치(물체 위 +80mm)로 이동
5. 하강 (+10mm 위에서 정지)
6. 그리퍼 닫기 → 후퇴
```

- 캘리브레이션 파일: `/home/user/robot_workspace/sim2real/sim2real/calibration/config/20260515_145627/calibration_eye_in_hand.npz`

---

## lerobot/ — HuggingFace LeRobot (서브모듈)

```
lerobot/
├── src/lerobot/        # 메인 라이브러리 소스
├── examples/           # 사용 예제
├── tests/              # 테스트
├── docker/             # Dockerfile 다수 (benchmark용)
└── scripts/ci/         # CI 스크립트
```

- HuggingFace LeRobot 공식 저장소를 서브모듈로 포함
- 데이터셋 포맷 정의, 학습 코드, 로봇 제어 예제 제공
- LeRobot v3.0 포맷(`data/`, `videos/`, `meta/` 구조)을 이 워크스페이스의 변환 출력으로 사용

---

## sroi_rosbag_utilities/ — ROS Bag 유틸리티 (서브모듈)

```
sroi_rosbag_utilities/
├── extract_rgbd/           # RGB-D 이미지 추출 스크립트
├── lerobot/                # bag → LeRobot 변환 유틸 (초기 버전)
├── notebooks/              # 분석 노트북
└── orb_slam_yaml/          # ORB-SLAM3 캘리브레이션 YAML
```

- ROS1/ROS2 bag에서 RGB-D, 스테레오, 관절 상태 등을 추출하는 유틸 모음
- `lerobot/bag_to_lerobot.py`는 현재 사용하는 변환 스크립트의 원형

---

## 하드웨어 구성

| 항목 | 사양 |
|------|------|
| 로봇 암 | Doosan Robotics e0509 |
| 그리퍼 | Robotis RH-P12-RN-DF (Dynamixel SDK, Protocol 2.0) |
| 카메라 | Intel RealSense D455 (`/dev/video4`, RGB 640×480 30fps) |
| VLA 서버 | SmolVLA HTTP 서버 (`192.168.50.79:16003`) |
| pi05 서버 | pi05_base HTTP 서버 (`192.168.50.79:18003`) |
| 그리퍼 포트 | `/dev/ttyUSB0` (Baudrate 2,000,000) |

---

## 의존성 (requirements.txt)

```
requests>=2.31.0        # SmolVLA 서버 통신
Pillow>=10.0.0          # 이미지 인코딩
numpy>=1.24.0
opencv-python>=4.8.0
dynamixel-sdk>=3.7.51   # 그리퍼 제어

# ROS2 (apt/rosdep으로 설치)
# ros-humble-rclpy
# ros-humble-sensor-msgs
# ros-humble-dsr-msgs2   ← Doosan ROS2 메시지
```

---

## 주요 실행 명령어

```bash
# VLA 파지 파이프라인 실행
ros2 launch grasp_vla grasp.launch.py \
    instruction:="pick up the red object"

# 관절 모드로 실행
ros2 launch grasp_vla grasp.launch.py action_mode:=joint

# 특정 포즈로 이동
python3 src/move_to_pose.py --target top_right

# 텔레오퍼레이션 + 자동 변환
python3 src/teleop_record_and_convert_eef.py

# ROS2 bag → LeRobot 변환
python3 src/bag_to_lerobot.py

# 딸기 파지 시나리오 (비전 기반)
python3 episode_secenario/grasp_ripe_strawberry.py
```

---

## 파이프라인 버전 비교

| 파이프라인 | 서버 | state 입력 | action 출력 | 파일 |
|-----------|------|-----------|------------|------|
| SmolVLA (관절) | `:16003` | 7-dim (joint 6 + gripper) | 7-dim 절대 관절각도 | `grasp_pipeline.py` |
| SmolVLA (EEF) | `:16003` | 7-dim (EEF 6 + gripper) | 7-dim EEF delta | `grasp_pipeline_eef.py` |
| pi05_base | `:18003` | 32-dim (joint 6 + gripper + 패딩) | 32-dim 절대 관절각도 | `grasp_pipeline_pi05.py` |

---

*작성일: 2026-05-28*
