# LeRobot 데이터셋 포맷 (SmolVLA 기준)

---

## 용어 정리

| 용어 | 설명 |
|---|---|
| **FPS** | Frames Per Second. 초당 프레임 수 = 로봇 제어 주기. 30fps면 33ms마다 state 읽고 action 전송 |
| **Frame** | 하나의 시간 단위. 이미지 1장 + state 1개 + action 1개 묶음 |
| **Episode** | 하나의 작업 시도 전체. 시작부터 끝까지 녹화된 프레임 묶음 |
| **Task** | 자연어 지시문. 에피소드에 붙이는 레이블. "Pick up the red cube." |
| **State** | 현재 로봇 관절이 실제로 있는 위치 (센서에서 읽어오는 값) |
| **Action** | 그 순간 로봇에게 보낸 명령값 (목표 관절 위치) |
| **ACTION_DIM** | 제어하는 관절 수. 관절 6개 + 그리퍼 1개 = 7 |
| **STATE_DIM** | 읽어오는 관절 수. 보통 ACTION_DIM과 동일 |
| **N_FRAMES** | 에피소드 하나의 총 프레임 수. 30초 × 30fps = 900 |
| **Chunk** | 파일 분할 단위. 에피소드 1000개마다 chunk-000, chunk-001 ... 으로 나뉨 |
| **Action Chunking** | 모델이 action을 50개씩 한 번에 예측하고 1개씩 꺼내 실행하는 방식 |

---

## 디렉토리 구조

```
my_dataset/
├── meta/
│   ├── info.json                               ← 데이터셋 전체 메타정보 (features 정의)
│   ├── tasks.parquet                           ← task 텍스트 목록 (자연어 instruction)
│   ├── stats.json                              ← state/action 정규화 통계
│   └── episodes/
│       └── chunk-000/file-000.parquet          ← 에피소드별 메타정보
├── data/
│   └── chunk-000/file-000.parquet              ← 프레임별 state/action/timestamp 등
└── videos/
    └── observation.images.<cam_key>/
        └── chunk-000/file-000.mp4
```

### chunk 분할 기준

`chunks_size=1000` (info.json) 기준으로 에피소드가 1000개를 넘으면 자동으로 다음 chunk로 넘어갑니다.

```
chunk-000/file-000.parquet  ← 에피소드 0~999
chunk-001/file-000.parquet  ← 에피소드 1000~1999
```

---

## 각 파일 설명

### meta/info.json

```json
{
  "codebase_version": "v3.0",
  "fps": 30,
  "robot_type": "so100_follower",
  "total_episodes": 50,
  "total_frames": 45000,
  "total_tasks": 1,
  "features": {
    "observation.images.cam_wrist": {
      "dtype": "video",
      "shape": [3, 720, 1280],
      "names": ["channels", "height", "width"]
    },
    "observation.state": {
      "dtype": "float32",
      "shape": [7],
      "names": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "gripper"]
    },
    "action": {
      "dtype": "float32",
      "shape": [7],
      "names": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "gripper"]
    },
    "timestamp":     {"dtype": "float32", "shape": [1]},
    "frame_index":   {"dtype": "int64",   "shape": [1]},
    "episode_index": {"dtype": "int64",   "shape": [1]},
    "index":         {"dtype": "int64",   "shape": [1]},
    "task_index":    {"dtype": "int64",   "shape": [1]}
  }
}
```

### meta/tasks.parquet

| task_index | task |
|---|---|
| 0 | Pull off the silver connector from the strawberry. |
| 1 | Pick up the red cube and place it in the box. |

- task = language instruction (영어 권장)
- 에피소드 전체에 하나의 task가 붙음
- 각 프레임의 `task_index`가 이 테이블을 참조

### data/chunk-000/file-000.parquet (프레임별)

| index | episode_index | frame_index | timestamp | task_index | observation.state | action |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.000 | 0 | [0.12, -0.45, ...] | [0.15, -0.42, ...] |
| 1 | 0 | 1 | 0.033 | 0 | [0.15, -0.42, ...] | [0.18, -0.39, ...] |

---

## 각 필드 상세 설명

### 인덱스 3종

| 필드 | 의미 |
|---|---|
| `index` | 전체 데이터셋 통틀어 프레임의 고유 번호. 에피소드가 달라도 계속 증가 |
| `episode_index` | 이 프레임이 몇 번째 에피소드에 속하는지 |
| `frame_index` | 에피소드 내에서 몇 번째 프레임인지. 새 에피소드 시작 시 0으로 리셋 |

### timestamp

- 에피소드 시작 기준 경과 시간(초)
- `frame_index / fps` 로 자동 계산
- 예: 30fps → 0.000, 0.033, 0.066, ...

### task_index

- `tasks.parquet`의 task 문자열과 연결되는 인덱스
- SmolVLA는 이 텍스트를 VLM tokenizer에 넣어 language conditioning 수행
- 에피소드 내 모든 프레임이 동일한 task_index 공유

### observation.state

- 로봇의 **현재 관절 위치** (센서에서 읽어오는 실제값)
- shape: `(7,)` — 관절 6개 + 그리퍼 1개

### observation.images.\<cam_key\>

- 카메라 RGB 이미지
- shape: `(3, H, W)`
- 파일 저장: `videos/observation.images.<cam_key>/chunk-000/file-000.mp4`
- SmolVLA 내부에서 512×512로 리사이즈됨

### action

- 그 프레임에서 로봇에게 **보낸 명령값** (목표 관절 위치)
- shape: `(7,)` — observation.state와 동일한 차원

```
t=0: state=[현재 위치]            action=[다음에 가야 할 위치]
t=1: state=[action이 실행된 결과]  action=[또 다음 위치]
t=2: state=[action이 실행된 결과]  action=[또 다음 위치]
...
```

- `state` → 로봇 모터에서 **읽어오는 값** (encoder 값)
- `action` → 조종기로 **보내는 값** (motor command)
- 둘은 비슷하지만 완전히 같지 않음 (모터가 명령을 받아도 물리적으로 즉시 도달하지 못함)

---

## Episode vs Task

- **Task** = "무엇을 해라"는 목표 지시문 (변하지 않는 개념)
- **Episode** = 그 task를 수행한 하나의 시도/궤적 (데이터 수집 단위)

```
Task 0: "Pull off the silver connector from the strawberry."
  ├── Episode 0: 성공한 시도 (900 프레임, 30초)
  ├── Episode 1: 다른 위치에서 같은 task (870 프레임)
  └── Episode 2: 또 다른 시도 (950 프레임)
```

SmolVLA 논문 권장: **task당 50 에피소드 이상**

---

## Action Chunking

SmolVLA는 한 번에 50개의 action을 예측하고, 로봇에는 1개씩 꺼내서 실행합니다.

```
t=0:  큐 비어있음 → 모델 추론 (50개 생성) → 큐: [a0, a1, ..., a49]
        → 로봇에 a0 전송
t=1:  큐에서 a1 꺼냄 → 로봇에 a1 전송  (추론 없음)
...
t=49: 큐에서 a49 꺼냄 → 로봇에 a49 전송
t=50: 큐 비어있음 → 다시 모델 추론 → 반복
```

모델 추론은 50 스텝에 1번만 일어나고, 로봇 제어는 매 스텝 1개씩 나갑니다.

---

## 데이터 수집 시 필요한 것

| 데이터 | 단위 | 설명 |
|---|---|---|
| 카메라 이미지 | 프레임별 | 각 순간의 RGB 이미지 → mp4로 저장 |
| 관절 각도 (state) | 프레임별 | 현재 로봇 자세 (encoder 값) |
| 관절 명령 (action) | 프레임별 | 그 순간 로봇에 보낸 명령값 |
| 지시문 (task) | 에피소드별 | 자연어 instruction (영어 권장) |

### 권장 설정

| 항목 | 값 |
|---|---|
| FPS | 30 |
| 카메라 | RealSense D455 (1280×720) |
| ACTION_DIM / STATE_DIM | 7 (관절 6개 + 그리퍼 1개) |
| 에피소드 수 | task당 50개 이상 |
| task 언어 | 영어 |

---

## 학습 데이터셋 구성 핵심 규칙

### FPS 규칙

- **데이터셋 내부**: 모든 에피소드가 동일한 FPS여야 함 (`info.json`에 하나만 존재)
- **데이터셋 간**: 서로 달라도 무관
- **학습 FPS = 추론 FPS** 반드시 일치해야 함 (다르면 action timing 어긋남)

### N_FRAMES (에피소드 길이)

- 에피소드마다 달라도 무관
- 각 에피소드 메타에 `length` 필드로 개별 기록됨

```
데이터셋 A (fps=30)
  ├── episode 0: 900 프레임 (30초)   ← OK
  ├── episode 1: 750 프레임 (25초)   ← OK
  └── episode 2: 1050 프레임 (35초)  ← OK
```

### 학습 방식

시퀀셜 데이터를 넣으면 SmolVLA가 스스로 학습합니다. 별도 레이블링 불필요.

```
입력:  카메라 이미지 + state + task 문자열
출력:  action[t], action[t+1], ..., action[t+49]  (50개 한번에 예측)
```

모델이 배우는 것: "이 이미지 + 이 관절 상태 + 이 지시 → 앞으로 50스텝 동안 이렇게 움직여라"

### 시뮬레이터 데이터 수집 (Isaac Sim / CuRobo)

로그 파싱보다 시뮬 루프 안에서 직접 기록하는 방식 권장:

```python
for step in simulation:
    frame = {
        "observation.state": robot.get_joint_positions(),
        "action":            controller.get_action(),
        "task":              "Pull off the silver connector...",
    }
    image = camera.get_rgb()
    dataset_writer.add_frame(frame, image)
```
