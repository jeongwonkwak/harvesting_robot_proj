# 딸기 수확 로봇 대시보드

실시간 수확 통계 + 카메라 피드 웹 대시보드 (FastAPI + WebSocket + MJPEG).

## 실행

```bash
cd src/dashboard

docker compose up -d          # 백그라운드 시작
docker compose up             # 포그라운드 (로그 확인)
docker compose down           # 중지
docker compose up -d --build  # 코드 수정 후 재빌드
```

브라우저: **http://localhost:8765**

## 카메라 설정 (docker-compose.yml)

| 상황 | 설정 |
|---|---|
| 웹캠 `/dev/video0` | `devices: - /dev/video0:/dev/video0` (기본) |
| RealSense D435 | `- /dev/bus/usb:/dev/bus/usb` + `privileged: true` |
| 카메라 없음 | `devices` 섹션 전체 주석 처리 |

카메라가 없어도 대시보드는 정상 동작 (카메라 패널에 "연결 없음" 표시).

## 상태 업데이트 (호스트 터미널)

```bash
export HARVEST_STATE_FILE=./data/harvest_state.json

python3 harvest_dashboard.py --update start_harvest    # 수확 시작 (타이머 시작)
python3 harvest_dashboard.py --update harvest_success  # 수확 성공
python3 harvest_dashboard.py --update harvest_fail     # 수확 실패
python3 harvest_dashboard.py --update damage           # 손상 감지
python3 harvest_dashboard.py --update reset            # 통계 초기화

python3 harvest_dashboard.py --msg "꼭지 가림 — 방향 변경" --level warning
python3 harvest_dashboard.py --status grasping
```

## 데모 모드 (Docker 없이 로컬 실행)

```bash
HARVEST_STATE_FILE=./data/harvest_state.json \
  python3 harvest_dashboard.py --demo
```

## 파일 구조

```
dashboard/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── README.md
├── harvest_dashboard.py      ← 메인 대시보드 (FastAPI)
├── ros2_bridge.py            ← ROS2 토픽 연결 (상태 동기화)
└── data/                     ← 상태 파일 볼륨 (git 제외)
    └── harvest_state.json
```

## 대시보드 구성

```
┌──────────────────── 🍓 헤더 (세션 정보 + 시계) ──────────────────────┐
│  수확량 │ 성공률 │ 평균파지 │ 현재수확시간 │ 손상률 │ 총시도  (6카드) │
├──────────┬──────────────────────┬─────────────────────────────────────┤
│ 로봇상태  │   실시간 메시지 로그  │        카메라 피드 (MJPEG)          │
│ (펄스)   │   (최신 40개)        │        RealSense / 웹캠             │
└──────────┴──────────────────────┴─────────────────────────────────────┘
```

---

# 🏗️ 시스템 아키텍처

## Docker 컴포넌트 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                    호스트 (ROS2 도메인)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │ harvest-camera   │  │ ros2-bridge      │  │ teleop-api   │   │
│  │ (RealSense)      │  │ (상태 + MJPEG)   │  │ (로봇 제어)  │   │
│  │ ROS2 발행        │  │ ROS2 구독/발행   │  │ ROS2 발행    │   │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘   │
│           │                     │                   │             │
│           └─────────────────────┼───────────────────┘             │
│                                 │ ROS2 토픽                       │
│                                 ↓                                 │
│                            🤖 로봇 제어                          │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         harvest-dashboard (포트 8765)                      │  │
│  │  웹 UI + FastAPI + WebSocket                              │  │
│  │  ├─ harvest_state.json (공유 상태 파일)                   │  │
│  │  ├─ /api/teleop          (방향 조작)                       │  │
│  │  ├─ /api/joint-command   (관절 직접 제어)                  │  │
│  │  ├─ /api/tcp-command     (TCP 좌표 제어)                  │  │
│  │  ├─ /api/vla/predict     (VLA 추론)                       │  │
│  │  └─ /ws                 (WebSocket 실시간 업데이트)        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📡 ROS2 신호 흐름 (전체 시스템)

### 신호 경로 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ROS2 토픽 (HOST)                                 │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  harvest-camera │
│  (RealSense)    │
└────────┬────────┘
         │ 발행 (30Hz)
         ├─ /camera/camera/color/image_raw
         ├─ /camera2/camera2/color/image_raw
         │
         ↓

┌──────────────────────────┐      ┌──────────────────────────┐
│   로봇 드라이버          │      │   Teleop API             │
│   (Doosan Robot)         │      │   (teleop_api_server)    │
├──────────────────────────┤      ├──────────────────────────┤
│ 발행 (~100Hz):           │      │ 발행 (20Hz):              │
│ /dsr01/joint_states ────┼──────┤ ├─ /dsr01/tcp_pose       │
│ (관절각도)               │      │ └─ /gripper/position     │
│                          │      │                          │
│ /dsr01/system/...        │      │ 기능:                    │
│ (TCP 포즈 서비스)        │      │ - HTTP /move 처리        │
│                          │      │ - DoosanController 제어  │
└──────────────┬───────────┘      └──────────┬───────────────┘
               │ 구독                         │ 구독
               │                              │
               └────────────┬─────────────────┘
                            │ 모두 구독

            ┌──────────────────────────────┐
            │   ROS2 Bridge                │
            │   (ros2_bridge.py, 8766)     │
            ├──────────────────────────────┤
            │ 구독 (ROS2 토픽):             │
            │ ├─ /dsr01/joint_states       │
            │ ├─ /dsr01/tcp_pose           │
            │ ├─ /gripper/position         │
            │ └─ 카메라 토픽들             │
            │                              │
            │ 처리:                        │
            │ ├─ 상태 파싱                 │
            │ ├─ YOLO 추론                 │
            │ └─ MJPEG 인코딩              │
            │                              │
            │ 발행:                        │
            │ └─ MJPEG 스트림 (포트 8766)  │
            └────────────┬─────────────────┘
                         │ 업데이트
            ┌────────────↓──────────────────┐
            │  harvest_state.json (공유)    │
            │  ├─ joint_angles              │
            │  ├─ tcp_pose                  │
            │  ├─ gripper                   │
            │  ├─ pending_teleop_command    │
            │  ├─ pending_joint_command     │
            │  ├─ pending_tcp_command       │
            │  ├─ messages                  │
            │  └─ camera_fps                │
            └────────────┬───────────────────┘
                         │ 읽기
        ┌────────────────┼────────────────┐
        │                │                │
        ↓                ↓                ↓

   ┌────────────────┐  ┌───────────────┐
   │  Harvest       │  │  Teleop API   │
   │  Dashboard     │  │  (폴링?)      │
   │  (포트 8765)   │  │               │
   └────────────────┘  └───────────────┘
        │                      │
        │ WebSocket            │ 읽기
        ├──────────────────────┘
        │
        ↓
   📱 웹 브라우저
   ├─ 상태 실시간 업데이트
   ├─ MJPEG 카메라 피드 (포트 8766)
   └─ VLA 결과 표시
```

### 신호 종류별 정리

| 신호 | 출처 | 목적지 | 주기 | 내용 | 용도 |
|-----|------|--------|------|------|------|
| `/dsr01/joint_states` | 🤖 로봇 드라이버 | ROS2 Bridge | ~100Hz | [rad, rad, ...] | 관절각도 |
| `/dsr01/tcp_pose` | ⚙️ **Teleop API** | ROS2 Bridge | 20Hz | [x, y, z, rx, ry, rz] | TCP 좌표 |
| `/gripper/position` | ⚙️ **Teleop API** | ROS2 Bridge | 20Hz | 0.0~1.0 | 그리퍼 위치 |
| `/camera/.../image_raw` | 📷 harvest-camera | ROS2 Bridge | 30Hz | 이미지 프레임 | 카메라 |
| `harvest_state.json` | ROS2 Bridge | 대시보드 | 10Hz | JSON 상태 | 상태 저장 |
| WebSocket `/ws` | 🌐 대시보드 | 브라우저 | 400ms | 실시간 상태 | UI 업데이트 |
| MJPEG (포트 8766) | ROS2 Bridge | 브라우저 | ~10fps | JPEG 스트림 | 카메라 피드 |

---

### 신호 흐름 요약 (경로별)

#### **경로 1: 센서 상태 → 화면 (읽기만)**

```
🤖 로봇 드라이버
  ├─ /dsr01/joint_states
  │   ↓ 구독
  └─ ROS2 Bridge
      ├─ 파싱
      ├─ harvest_state.json 업데이트
      │   ↓ 읽기
      └─ 🌐 대시보드
          ├─ WebSocket 전송
          └─ 📱 브라우저 화면
```

#### **경로 2: Teleop API 상태 발행 (20Hz 동기화)**

```
⚙️ Teleop API (DoosanController)
  ├─ /dsr01/tcp_pose (TCP 좌표)
  ├─ /gripper/position (그리퍼)
  │   ↓ 구독
  └─ ROS2 Bridge
      ├─ 수신 (20Hz)
      ├─ harvest_state.json 업데이트
      │   ↓ 읽기
      └─ 🌐 대시보드
          ├─ WebSocket 전송 (10Hz)
          └─ 📱 화면에 표시
```

#### **경로 3: 카메라 피드 (실시간 스트림)**

```
📷 RealSense 카메라
  ├─ /camera/.../image_raw (30Hz)
  │   ↓ 구독 + YOLO 추론
  └─ ROS2 Bridge
      ├─ MJPEG 인코딩
      └─ HTTP 스트림 (포트 8766)
          ↓
      📱 브라우저
          └─ <img src="..."> 표시
```

---

### 명령 흐름 (명확함 vs 불명확함)

#### **✅ 명확한 명령: VLA 추론**

```
🌐 대시보드
  ├─ 카메라 읽음
  ├─ harvest_state.json 읽음 (현재 상태)
  ├─ VLA API 호출
  │   ↓
  └─ VLA 결과 (delta 값)
      ├─ Joint Limit 검증
      ├─ POST http://localhost:8767/move (6회)
      ├─ POST http://localhost:8767/gripper
      │   ↓
      └─ ⚙️ Teleop API
          ├─ DoosanController.move_delta()
          └─ 🤖 로봇 제어
```

#### **⚠️ 불명확한 명령: 방향 버튼**

```
🌐 대시보드
  ├─ POST /api/teleop
  │
  └─ harvest_state.json
      {pending_teleop_command: "forward"}
      │
      ↓ ❓ 누가 처리?
      
  가능성 1: ⚙️ Teleop API가 주기적으로 폴링
  가능성 2: 📊 ROS2 Bridge가 처리 (코드상 ❌ 확인됨)
  
      ↓ (추정)
  ⚙️ Teleop API
      └─ DoosanController.move_delta()
          └─ 🤖 로봇 제어
              └─ /dsr01/tcp_pose 발행
                  └─ (이후 정상 흐름)
```

---

## 신호 흐름 (데이터 경로)

### 1️⃣ 방향 조작 (화살표 버튼 ↑↓←→)

**간접 경로 (비동기, 상태 기반)**

```
사용자 클릭 (↑ 버튼)
        ↓
JavaScript: sendTeleop('forward')
        ↓
HTTP POST /api/teleop
Body: {"command": "forward", "speed": 0.2}
        ↓
harvest_state.json
{
  "pending_teleop_command": {
    "command": "forward",
    "speed": 0.2,
    "sent_at": "2026-06-04T..."
  }
}
        ↓ ⚠️ 누가 처리?
가능성 1: Teleop API가 주기적으로 폴링해서 처리
가능성 2: 다른 메커니즘 (코드 확인 필요)
        ↓
DoosanController.move_delta() 실행
        ↓
ROS2 토픽으로 로봇에 전송
        ↓
🤖 로봇 동작
```

**특징:**
- ⏱️ 약간의 지연 있음 (폴링 주기)
- 📝 명령어 기반 ("forward" 등)
- 🔄 상태 파일을 통한 간접 통신
- ⚠️ **주의: pending_teleop_command 처리 메커니즘 불명확**
  - ROS2 Bridge는 이를 처리하지 않음 (코드 확인됨)
  - Teleop API가 처리할 가능성 높음 (정확한 메커니즘은 확인 필요)

---

### 2️⃣ VLA 단일 추론

**직접 경로 (동기, 이벤트 기반)**

```
사용자 클릭 (▶ 단일 추론)
        ↓
JavaScript: runVlaOnce()
        ↓
HTTP POST /api/vla/predict
Body: {
  "instruction": "Grasp the strawberry stem and pick it.",
  "reset_episode": false
}
        ↓
harvest_dashboard.py의 vla_predict() 엔드포인트
        ↓
1. 카메라 이미지 캡처 (JPEG)
2. 현재 상태 벡터 구성 (TCP pose, gripper)
        ↓
HTTP POST http://192.168.50.79:18003/predict
(외부 VLA 모델 서버)
        ↓
VLA API 응답:
{
  "action": [0.1, 0.05, -0.02, 0.01, 0.0, -0.01, 0.5]
  (delta_x, delta_y, delta_z, delta_rx, delta_ry, delta_rz, gripper)
}
        ↓
✅ Joint Limit 검증
   (최종 target_pose를 IK로 변환 후 범위 확인)
        ↓
2️⃣ 회전 조작: HTTP POST http://localhost:8767/move
   6번 반복: dx, dy, dz, drx, dry, drz
        ↓
3️⃣ 그리퍼 조작: HTTP POST http://localhost:8767/gripper
   Body: {"position": 450}
        ↓
teleop-api가 처리
        ↓
ROS2 토픽으로 로봇에 전송
        ↓
🤖 로봇 동작
```

**특징:**
- ⚡ 즉시 반응 (동기)
- 🔢 정확한 delta 값
- 🛡️ Joint Limit 검증 포함

---

### 3️⃣ 회전 직접 조작 (Rx+, Ry+ 등)

**직접 경로 (동기)**

```
사용자 클릭 (Rx+ 버튼)
        ↓
JavaScript: teleopMove('rx_plus')
        ↓
HTTP POST http://localhost:8767/move
Body: {"command": "rx_plus", "angle_scale": 1.0}
        ↓
teleop-api가 즉시 처리
        ↓
ROS2 토픽으로 로봇에 전송
        ↓
🤖 로봇 동작
```

---

### 4️⃣ 그리퍼 직접 조작

**직접 경로 (동기)**

```
사용자 클릭 (열기/파지)
        ↓
JavaScript: teleopGripper(position)
        ↓
HTTP POST http://localhost:8767/gripper
Body: {"position": 600}
        ↓
teleop-api가 처리
        ↓
ROS2 토픽으로 로봇에 전송
        ↓
🤖 그리퍼 동작
```

---

## API 엔드포인트 정리

### 대시보드 내부 API (harvest_dashboard.py)

| 엔드포인트 | 메서드 | 목적 | 로봇 제어 | Joint Limit 검증 |
|-----------|--------|------|---------|-----------------|
| `/api/teleop` | POST | 방향 조작 명령 저장 | ❌ (상태만) | ❌ |
| `/api/joint-command` | POST | 관절각도 직접 명령 | ❌ (Teleop API로) | ✅ |
| `/api/tcp-command` | POST | TCP 좌표 명령 (IK) | ❌ (Teleop API로) | ✅ |
| `/api/vla/predict` | POST | VLA 추론 + 로봇 제어 | ✅ (직접) | ✅ |
| `/api/snapshot/0`, `/1` | GET | 카메라 스냅샷 | - | - |
| `/ws` | WebSocket | 실시간 상태 업데이트 | - | - |

### Teleop API (teleop-api 컨테이너, 포트 8767)

| 엔드포인트 | 메서드 | 목적 | 출처 |
|-----------|--------|------|------|
| `/move` | POST | 로봇 이동 명령 | 대시보드 또는 VLA |
| `/gripper` | POST | 그리퍼 제어 | 대시보드 또는 VLA |
| `/home` | POST | 홈 위치 복귀 | 대시보드 |
| `/record/start`, `/stop` | POST | 데이터 녹화 | 대시보드 |

---

## 상태 파일 (harvest_state.json)

```json
{
  "joint_angles": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
  "tcp_pose": [310.81, 278.6, 874.33, 89.86, 86.22, -167.92],
  
  "pending_teleop_command": {
    "command": "forward",
    "speed": 0.2,
    "sent_at": "2026-06-04T12:34:56.789"
  },
  
  "pending_joint_command": {
    "angles": [0, 0, 155, -58, 0, 0],
    "velocity": 10,
    "sent_at": "2026-06-04T12:34:56.789"
  },
  
  "gripper": {
    "position": 100.0,
    "state": "open",
    "force": 30.0
  },
  
  "messages": [
    {"time": "12:34:56", "level": "info", "text": "✅ Joint command 수락"},
    {"time": "12:35:00", "level": "error", "text": "🚫 Joint limit 초과"}
  ],
  
  "status": "idle|approaching|grasping|returning|error",
  "robot_ready": true,
  "robot_error": ""
}
```

**주요 필드:**
- `pending_*_command`: 대기 중인 명령 (Teleop API가 처리, ros2-bridge는 읽지 않음)
- `joint_angles`, `tcp_pose`: 현재 로봇 상태 (ros2-bridge가 ROS2 토픽에서 읽어 업데이트)
- `messages`: UI에 표시할 메시지 로그

---

## 컴포넌트별 책임

### harvest-dashboard (포트 8765)
- ✅ 웹 UI 제공
- ✅ 사용자 입력 처리
- ✅ 상태 파일 읽기/쓰기
- ✅ **Joint Limit 검증** (VLA, Joint command, TCP command)
- ✅ VLA API 호출 및 결과 로봇 전송
- ✅ MJPEG 스트림 제공

### ros2-bridge (포트 8766) — "상태 배달원" 🚚

**역할:** 로봇 상태를 수집해서 대시보드로 전달 (읽기만!)

**✅ 하는 것:**
- ROS2 토픽 **구독** (create_subscription):
  - `/dsr01/joint_states` (로봇 드라이버 → 관절각도)
  - `/dsr01/tcp_pose` (Teleop API → TCP 좌표)
  - `/gripper/position` (Teleop API → 그리퍼 위치)
  - 카메라 토픽들 (화상 데이터)
- 상태 파싱 및 harvest_state.json 업데이트 (10Hz)
- MJPEG 스트림 생성 (카메라 + YOLO 추론)
- WebSocket으로 대시보드에 상태 전송

**❌ 안 하는 것 (중요!):**
- ❌ `create_publisher` 없음 — 발행하지 않음
- ❌ `DoosanController` 없음 — 로봇 제어 안 함
- ❌ `move_delta()`, `move_line()` 없음 — 명령 미전송
- ❌ `pending_teleop_command` 처리 안 함
- ❌ 로봇에 명령 신호 발행 안 함

**코드 증거:**
```python
# ros2_bridge.py에 있는 것:
self.create_subscription(JointState, "/dsr01/joint_states", ...)    # 구독만
self.create_subscription(Float32MultiArray, "/dsr01/tcp_pose", ...) # 구독만
self.create_subscription(Float32, "/gripper/position", ...)         # 구독만

# ros2_bridge.py에 없는 것:
# ❌ create_publisher (발행 없음)
# ❌ DoosanController (제어 안 함)
# ❌ move_line, move_delta (명령 미전송)
```

---

### teleop-api (포트 8767) — "로봇 제어 담당" 🎮

**역할:** 명령을 받아서 로봇을 직접 제어

**✅ 하는 것:**
- HTTP API 엔드포인트 제공:
  - `/move` - 로봇 이동 (DoosanController.move_delta() 호출)
  - `/gripper` - 그리퍼 제어
  - `/home` - 홈 위치 복귀
- **DoosanController로 로봇 직접 제어:**
  - `move_line()` - 직선 이동
  - `move_joint()` - 관절 이동
  - `gripper.move_to()` - 그리퍼 제어
- 20Hz로 현재 상태 **발행** (create_publisher):
  - `/dsr01/tcp_pose` (TCP 좌표)
  - `/gripper/position` (그리퍼 위치)
  - ROS2 Bridge가 이를 구독해서 대시보드로 전달
- 데이터 녹화 관리 (bag 레코딩)

**코드 증거:**
```python
# teleop_api_server.py에 있는 것:
self._gripper_pub = create_publisher(Float32, '/gripper/position')    # 발행!
self._eef_pub = create_publisher(Float32MultiArray, '/dsr01/tcp_pose') # 발행!
self._robot = DoosanController(...)  # 로봇 제어 객체
self._robot.move_line(target, velocity=...)  # 직접 제어!

# teleop_api_server.py의 명령 처리:
def move_delta(self, dx=0, dy=0, ...):
    self._robot.move_line(target, ...)  # 로봇 제어 ← 여기!
```

**❌ 안 하는 것:**
- ❌ HTML/웹 UI 제공 안 함 (FastAPI API만)
- ❌ 대시보드와 직접 통신 안 함 (JSON 파일만 공유)

---

### 🔑 **핵심: 역할 분담**

```
ROS2 Bridge                          Teleop API
──────────────────────────────────────────────────────
"상태 읽기 + 대시보드 전달"          "명령 받기 + 로봇 제어"

구독:                                 발행:
✅ joint_states (로봇)                ✅ tcp_pose (로봇에)
✅ tcp_pose (Teleop API)              ✅ gripper_position
✅ gripper_position                  
✅ 카메라                             제어:
                                      ✅ DoosanController
저장:                                 ✅ move_line()
✅ harvest_state.json                ✅ move_joint()
                                      ✅ gripper.move_to()
발행:
❌ 없음!                               명령 처리:
                                      ✅ /move (HTTP)
                                      ✅ /gripper (HTTP)
```

---

### harvest-camera
- ✅ RealSense 카메라에서 프레임 캡처
- ✅ ROS2 토픽으로 발행
  - `/camera/camera/color/image_raw`
  - `/camera2/camera2/color/image_raw`

### harvest-camera
- ✅ RealSense 카메라에서 프레임 캡처
- ✅ ROS2 토픽으로 발행

---

## Joint Limit 검증 (신규 기능)

**목적:** 로봇의 관절이 물리적 한계에 도달하기 전에 명령 거부

**Safety Margin:** 실제 limit의 90% 까지만 허용
- 예: Joint 3: ±155° → ±139.5°로 제한

**검증 대상:**
1. ✅ `/api/joint-command` - 관절각도 명령
2. ✅ `/api/tcp-command` - TCP 좌표 명령 (IK로 변환 후)
3. ✅ `/api/vla/predict` - VLA 결과 (target_pose 검증)
4. ❌ `/api/teleop` - 방향 조작 (미검증)

**동작:**
- 범위 초과 시: 에러 메시지 반환, 로봇 명령 거부
- 메시지 로그에 기록: "🚫 Joint limit 초과: joint_3=160° (범위: -139.5~139.5°)"
