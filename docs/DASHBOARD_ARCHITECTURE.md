# 대시보드 아키텍처 (Dashboard Architecture)

## 개요

`harvest_dashboard.py`는 딸기 수확 로봇의 중앙 제어 및 모니터링 시스템입니다. 
웹 기반 대시보드로 실시간 카메라 스트림, 로봇 상태, 수확 현황을 표시하고, 수동 제어 및 자동 수확을 조율합니다.

---

## 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    harvest_dashboard.py (포트 8765)              │
│                   (FastAPI + WebSocket + MJPEG)                 │
└────────┬──────────────────────────────────────────────────────┬─┘
         │                                                      │
    ┌────▼─────────────┐                            ┌──────────▼──────┐
    │  ros2_bridge.py  │                            │ teleop_api_server│
    │  (포트 8766)      │                            │   (포트 8767)    │
    └────┬─────────────┘                            └──────────┬──────┘
         │ MJPEG 스트림                                  │ REST API
         │ + ROS2 상태                                   │ 로봇 제어
         │                                              │
    ┌────▼──────────────────────────────────────────────▼──────┐
    │             VLA API Server (포트 18003)                   │
    │        (딸기 수확 추론, /predict 엔드포인트)             │
    └───────────────────────────────────────────────────────────┘
         │
    ┌────▼──────────────────────────────────────────────────────┐
    │         데이터 수집 및 변환 파이프라인                    │
    │  (teleop_record_and_convert_eef.py → bag_to_lerobot_eef.py) │
    └────┬──────────────────────────────────────────────────────┘
         │
    ┌────▼──────────────────────────────────────────────────────┐
    │    학습 데이터셋 저장                                     │
    │    /home/user/robot_workspace/vla_ws/data/mid/            │
    └───────────────────────────────────────────────────────────┘
```

---

## 핵심 파일 목록

### 1. **harvest_dashboard.py** (158KB)
**역할**: 중앙 제어 대시보드 및 VLA 추론 조율

**주요 기능**:
- 웹 기반 UI (포트 8765)
- WebSocket 실시간 통신
- 상태 파일 관리 (`/tmp/harvest_state.json`, 환경변수 `HARVEST_STATE_FILE`로 재정의 가능)
- VLA API와 통신 (`POST /predict`)
- Teleop API와 통신 (`/move`, `/gripper`)
- 로봇 상태 모니터링 (TCP pose, 관절 각도, 그리퍼)
- 수확 로그 기록

**주요 엔드포인트**:
```
GET  /                          웹 UI 페이지
GET  /camera-info               카메라 정보
GET  /camera/0                  Base 카메라 스냅샷
GET  /camera/1                  Wrist 카메라 스냅샷
POST /api/vla/predict           VLA 추론 요청
POST /api/joint-command         관절 각도 직접 제어
POST /api/tcp-command           TCP pose 직접 제어
POST /api/gripper-command       그리퍼 제어
POST /api/teleop                텔레오퍼레이션 명령
POST /api/set-target            수확 목표 설정
GET  /api/sw-stages             수확 단계 조회
POST /api/sw-stages             수확 단계 저장
POST /api/set-planned-duration  예상 소요 시간 설정
GET  /api/sensor-data           센서 데이터 조회
GET  /api/snapshot              카메라 스냅샷
GET  /api/snapshot/0            Base 카메라 스냅샷
GET  /api/snapshot/1            Wrist 카메라 스냅샷
GET  /api/report                수확 보고서 다운로드
WS   /ws                        WebSocket 실시간 업데이트
```

**호출하는 파일**:
- `ros2_bridge.py` → 상태 파일 읽기
- `teleop_api_server.py` → 로봇 동작 실행
- VLA API 서버 (기본: `http://192.168.50.79:18003`) → 추론 요청

**환경변수**:
```
VLA_API_URL          VLA 서버 주소 (기본: http://192.168.50.79:18003)
TELEOP_API_PORT      Teleop API 포트 (기본: 8767)
HARVEST_STATE_FILE   상태 파일 경로 (기본: /tmp/harvest_state.json)
```

**사용 방법**:
```bash
python3 src/dashboard/harvest_dashboard.py [--demo] [--no-camera] [--port 8765]
```

---

### 2. **ros2_bridge.py** (17KB)
**역할**: ROS2 ↔ 대시보드 브리지

**주요 기능**:
- ROS2 토픽 구독 (Joint States, TCP Pose, 카메라)
- MJPEG 스트림 서버 (포트 8766)
- 상태 파일 실시간 업데이트
- 카메라 이미지 캐싱

**구독하는 ROS2 토픽**:
```
/dsr01/joint_states              관절 각도
/dsr01/system/get_current_pose   TCP pose
/camera/camera/color/image_raw   Base 카메라 (YOLO용)
/camera2/camera2/color/image_raw Wrist 카메라 (파지점 인식)
/gripper/position                그리퍼 위치
```

**퍼블리시하는 서비스**:
- `http://localhost:8766/stream?camera=0` → Base 카메라 MJPEG
- `http://localhost:8766/stream?camera=1` → Wrist 카메라 MJPEG

**상태 파일**:
- 기본 경로: `/data/harvest_state.json` (환경변수 `HARVEST_STATE_FILE`로 재정의 가능)
- `harvest_dashboard.py`와 경로를 맞추려면 `HARVEST_STATE_FILE` 환경변수를 동일하게 설정해야 함

**사용 방법**:
```bash
python3 src/dashboard/ros2_bridge.py
```

---

### 3. **teleop_api_server.py** (29KB)
**역할**: 로봇 제어 REST API 서버

**주요 기능**:
- 로봇 위치 제어 (상대 이동: dx, dy, dz, drx, dry, drz)
- 스플라인 이동 (waypoint 기반)
- 그리퍼 제어 (position 0-740)
- ROS2 bag 녹화 시작/중지
- 데이터셋 변환 트리거
- 안전성 검증 (Joint limit, IK 검증)
- 동작 로깅

**제공하는 엔드포인트**:
```
GET  /status          로봇 상태 조회 (변환 진행률 포함)
POST /move            상대 이동 명령 (dx, dy, dz, drx, dry, drz)
POST /spline          스플라인 이동 (waypoints 배열)
POST /gripper         그리퍼 제어 (position)
POST /home            홈 포즈 복귀
POST /record/start    ROS2 bag 녹화 시작
POST /record/stop     ROS2 bag 녹화 중지
POST /convert         bag → LeRobot 데이터셋 변환
GET  /health          서버 상태 확인
```

**요청 예시**:
```json
POST /move
{
  "dx": 50.0,        // mm (±200mm 범위)
  "dy": 0.0,
  "dz": -30.0,
  "drx": 0.0,        // deg (±30deg 범위)
  "dry": 0.0,
  "drz": 0.0
}
```

**호출하는 파일**:
- `harvest_dashboard.py` → VLA 추론 후 로봇 동작 실행

**사용 방법**:
```bash
python3 src/teleop_api_server.py
```

---

### 4. **teleop_record_and_convert_eef.py** (28KB)
**역할**: 원격 제어를 통한 데이터 수집 및 자동 변환

**주요 기능**:
- ROS2 bag 파일 녹화
- 실시간 YOLO 딸기 검출
- EEF (End-Effector) 기반 delta action 계산
- 자동 데이터셋 변환

**프로세스 흐름**:
1. ROS2 bag 녹화 시작
2. 사용자 원격 제어 (키보드: 화살표키, WASD, 그리퍼: o/c)
3. 카메라, TCP pose, 그리퍼 위치 기록
4. ROS2 bag 저장
5. `bag_to_lerobot_eef.py` 자동 호출 → 데이터셋 변환

**저장되는 ROS2 토픽**:
```
/dsr01/joint_states
/dsr01/tcp_pose
/camera/camera/color/image_raw
/camera2/camera2/color/image_raw
/gripper/position
```

**생성되는 데이터**:
- Raw: `/home/user/robot_workspace/vla_ws/data/raw/final_project/episode_XXX/`
- Mid: `/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.X/`

**사용 방법**:
```bash
python3 src/teleop_record_and_convert_eef.py --task "Grasp the strawberry stem and pick it."
```

---

### 5. **bag_to_lerobot_eef.py** (35KB)
**역할**: ROS2 bag 파일 → LeRobot v3.0 데이터셋 변환

**주요 기능**:
- CDR 포맷 ROS2 메시지 파싱
- 이미지 디코딩 (JPEG → 224×224 RGB)
- TCP pose 정규화 (mm/deg → m/rad)
- EEF delta action 계산
- Parquet 형식으로 저장

**입력**:
- ROS2 bag 파일 (`/home/user/robot_workspace/vla_ws/data/raw/final_project/episode_XXX/`)

**출력**:
- Parquet 데이터셋
  ```
  /home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.X/
  ├── data/chunk-000/file-000.parquet
  ├── data/chunk-001/file-000.parquet
  ├── ...
  ├── videos/{video_key}/chunk-000/file-000.mp4
  ├── meta/
  │   ├── info.json (데이터셋 메타정보)
  │   ├── stats.json (정규화 통계)
  │   ├── tasks.parquet (task 목록)
  │   ├── episodes/ (에피소드별 메타데이터)
  │   └── videos.json
  └── README.md
  ```

**Parquet 스키마**:
```
observation.state (13-dim):
  [TCP_x_m, TCP_y_m, TCP_z_m, Rx_rad, Ry_rad, Rz_rad, 
   J1_rad, J2_rad, J3_rad, J4_rad, J5_rad, J6_rad, gripper]

action (7-dim):
  [delta_x_m, delta_y_m, delta_z_m, 
   delta_rx_rad, delta_ry_rad, delta_rz_rad, 
   grip_next]
```

**사용 방법**:
```bash
python3 src/bag_to_lerobot_eef.py --task "Grasp the strawberry stem and pick it."
```

---

## 통신 흐름

### 1. VLA 추론 요청 흐름
```
User (Web UI)
   ↓ (WebSocket)
harvest_dashboard.py
   ↓ (POST /api/vla/predict)
→ VLA API Server (port 18003)
   ↓ (반환 action)
harvest_dashboard.py
   ├─ IK/Joint limit 검증
   └─ Teleop API로 로봇 제어
      ↓ (POST /move, /gripper)
teleop_api_server.py
   ↓ (ROS2 publish)
로봇 (Doosan DSR01)
```

### 2. 상태 업데이트 흐름
```
로봇 (Doosan DSR01)
   ↓ (ROS2 publish)
ros2_bridge.py
   ├─ /dsr01/joint_states
   ├─ /dsr01/tcp_pose
   ├─ /camera/color/image_raw (MJPEG)
   └─ /gripper/position
   ↓ (파일 업데이트)
harvest_state.json  ← HARVEST_STATE_FILE 환경변수로 경로 지정
   ↓ (파일 읽기)
harvest_dashboard.py
   ↓ (WebSocket)
Web UI (실시간 표시)
```

### 3. 데이터 수집 흐름
```
teleop_record_and_convert_eef.py
   ├─ ROS2 bag 녹화 시작
   ├─ 사용자 원격 제어 (TCP pose, gripper 변경)
   └─ ROS2 bag 저장
   ↓
bag_to_lerobot_eef.py
   ├─ bag 파싱
   ├─ 이미지 디코딩
   ├─ state/action 정규화
   └─ Parquet 저장
   ↓
/home/user/robot_workspace/vla_ws/data/mid/
```

---

## 포트 설정

| 포트 | 서비스 | 역할 |
|------|--------|------|
| **8765** | harvest_dashboard.py | 웹 UI + WebSocket |
| **8766** | ros2_bridge.py | MJPEG 카메라 스트림|
| **8767** | teleop_api_server.py | 로봇 제어 REST API |
| **18003** | VLA API 서버 | VLA 추론 API (기본값, `VLA_API_URL`로 재정의 가능) |

---

## 상태 파일 구조

### `harvest_state.json`
기본 경로: `harvest_dashboard.py` → `/tmp/harvest_state.json`, `ros2_bridge.py` → `/data/harvest_state.json`  
→ 두 프로세스가 동일한 파일을 바라보도록 `HARVEST_STATE_FILE` 환경변수를 통일해야 함

```json
{
  "session_start": "2026-06-08T15:30:00.000000",
  "total_attempts": 32,
  "success_count": 24,
  "damage_count": 2,
  "status": "idle",                    // idle|approaching|grasping|returning|error
  "robot_ready": true,
  "joint_angles": [0.0, 0.0, ..., 0.0],  // 6-dim
  "tcp_pose": [300.0, 280.0, 880.0, 90.0, 86.0, -90.0],  // mm/deg
  "gripper": {
    "position": 100.0,                 // 0-100 (%)
    "state": "open",                   // open|close
    "force": 30.0                      // N
  },
  "target_count": 15,
  "detected_count": 12,
  "messages": [
    {
      "time": "15:30:45",
      "level": "info",
      "text": "수확 시작"
    }
  ],
  "last_updated": "2026-06-08T15:30:45.123456"
}
```

---

## 실행 순서 (초기 설정)

### 1단계: ROS2 브릿지 시작
```bash
HARVEST_STATE_FILE=/tmp/harvest_state.json python3 src/dashboard/ros2_bridge.py
```
→ 포트 8766에서 MJPEG 스트림 시작

### 2단계: Teleop API 서버 시작
```bash
python3 src/teleop_api_server.py
```
→ 포트 8767에서 로봇 제어 API 시작

### 3단계: 대시보드 시작
```bash
python3 src/dashboard/harvest_dashboard.py
```
→ 포트 8765에서 웹 UI 시작

### 4단계: 브라우저 접속
```
http://localhost:8765
```

---

## 데이터 수집 과정

### 원격 제어 (Teleop) 데이터 수집
```bash
# 1. 데이터 수집 스크립트 실행
python3 src/teleop_record_and_convert_eef.py \
  --task "Grasp the strawberry stem and pick it." \
  --episode 001

# 2. 사용자가 원격 제어로 수확 시뮬레이션 수행
# (키보드: 화살표키 = 이동, W/A/S/D = 회전, O = 그리퍼 열기, C = 닫기)

# 3. ROS2 bag 저장 및 자동 변환
# bag → parquet 변환 완료
```

### 저장된 데이터 확인
```bash
# 현재 데이터셋 정보 조회
python3 src/view_parquet.py
```

---

## 주요 클래스 및 함수

### harvest_dashboard.py
```python
def _load() -> dict:
    """상태 파일 로드"""

def _save(s: dict) -> None:
    """상태 파일 저장"""

async def vla_predict(request):
    """VLA 추론 요청 처리
    - 카메라 이미지 캡처
    - 상태 벡터 구성
    - VLA API 호출
    - 로봇 동작 실행
    - 로그 저장
    """

async def tcp_cmd(request):
    """TCP pose 직접 제어"""

async def grip_cmd(request):
    """그리퍼 직접 제어"""

async def ws_endpoint(ws: WebSocket):
    """WebSocket 실시간 통신"""
```

### ros2_bridge.py
```python
class ROS2Bridge(Node):
    """ROS2 토픽 구독 및 상태 파일 업데이트"""

class MJPEGHandler(http.server.BaseHTTPRequestHandler):
    """MJPEG 스트림 제공"""
```

### teleop_api_server.py
```python
@app.get('/status')
async def get_status():
    """로봇 상태 조회 (변환 진행률 포함)"""

@app.post('/move')
async def move_delta(request):
    """상대 이동 명령"""

@app.post('/spline')
async def api_spline(request):
    """스플라인 이동"""

@app.post('/gripper')
async def control_gripper(request):
    """그리퍼 제어"""

@app.post('/record/start')
@app.post('/record/stop')
async def record_control():
    """ROS2 bag 녹화 제어"""

@app.post('/convert')
async def api_convert():
    """bag → LeRobot 데이터셋 변환"""
```

---

## 문제 해결

### 대시보드가 로봇 상태를 읽지 못함
- ros2_bridge.py 실행 확인
- `HARVEST_STATE_FILE` 환경변수가 두 프로세스에서 동일한지 확인
- ROS2 토픽 구독 확인: `ros2 topic echo /dsr01/joint_states`

### 카메라 스트림이 안 보임
- ros2_bridge.py 포트 8766 접근 확인
- `http://localhost:8766/stream?camera=0` 접근 테스트
- 카메라 연결 상태 확인: `ros2 device list`

### VLA 추론 실패
- VLA API 서버 실행 확인 (기본 포트 18003, `VLA_API_URL` 환경변수 확인)
- `curl http://192.168.50.79:18003/predict` 테스트
- 카메라 이미지 224×224 리사이즈 확인

### 로봇 제어가 안 됨
- teleop_api_server.py 실행 확인
- `curl http://localhost:8767/health` 테스트
- 로봇 연결 상태 확인: `ros2 node list`

---

## 관련 문서

- [VLA 수확 파이프라인](./VLA_HARVESTING_PIPELINE.md)
- [데이터셋 파이프라인](./dataset_pipeline_guide.md)
- [로봇 작업 공간 개요](./robot_workspace_overview.md)
