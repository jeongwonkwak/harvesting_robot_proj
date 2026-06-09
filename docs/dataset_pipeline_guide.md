# 로봇 데이터셋 파이프라인 가이드

## 목차
0. [0단계: 실제 데이터 구조 이해](#0단계-실제-데이터-구조-이해) ⭐
1. [개요](#개요)
2. [1-2단계: 데이터 수집](#1-2단계-데이터-수집)
3. [3단계: 데이터 전처리](#3단계-데이터-전처리)
4. [4단계: 정규화 및 동기화](#4단계-정규화-및-동기화)
5. [5단계: 학습 데이터셋 포맷화](#5단계-학습-데이터셋-포맷화)
6. [5.5단계: Quantile Stats](#55단계-quantile-stats)
7. [5.6단계: 저장 구조](#56단계-저장-구조)
8. [6단계: 품질 검증](#6단계-품질-검증)
9. [7단계: 추론(Inference)](#7단계-추론inference)
10. [트러블슈팅](#트러블슈팅)

---

## 0단계: 실제 데이터 구조 이해

당신의 프로젝트 데이터는 다음 경로에 저장된다:

```
/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.4.0/
├── episode_001_20260602_033711_eef/
│   ├── episode_001_20260602_033711_eef_0.db3  (ROS bag, 3GB)
│   └── metadata.yaml
├── episode_002_... / ...
└── ... (총 49개 에피소드)
```

### ROS Bag 파일 (db3)

**파일 구조**: SQLite3 데이터베이스

```
episode_001_20260602_033711_eef_0.db3 (3.0 GB)
  ↓ SQLite3 DB
  ├── schema 테이블
  ├── metadata 테이블
  ├── topics 테이블
  ├── messages 테이블 ← 실제 센서 데이터
  └── (인덱스)
```

**내부 테이블 구조:**

| 테이블 | 칼럼 | 설명 |
|--------|------|------|
| **topics** | id, name, type | 5개 ROS 토픽 메타데이터 |
| **messages** | id, topic_id, timestamp, data | 14,263개 메시지 (BLOB 형식) |
| **metadata** | (시스템용) | 시간 범위, 버전 등 |
| **schema** | (시스템용) | 저장소 스키마 |

**messages 테이블 상세:**

```
각 행 = 1개 ROS 메시지

칼럼:
  - id (INTEGER): 메시지 번호 (1-14263)
  - topic_id (INTEGER): 어느 토픽인지 (1=조인트, 2=카메라2, ...)
  - timestamp (INTEGER): 나노초 단위 시간
  - data (BLOB): ROS 메시지 직렬화 바이너리 데이터

예시:
  id: 1
  topic_id: 2  → /camera2/camera2/color/image_raw
  timestamp: 1780371435407209289  → ~1780371435.4s
  data: <바이너리 이미지 데이터>
```

**topics 테이블 내용 (episode_001):**

| ID | 토픽명 | 타입 | 메시지 수 |
|----|--------|------|----------|
| 1 | `/dsr01/joint_states` | sensor_msgs/msg/JointState | 8,090 |
| 2 | `/camera2/camera2/color/image_raw` | sensor_msgs/msg/Image | 2,251 |
| 3 | `/camera/camera/color/image_raw` | sensor_msgs/msg/Image | 1,132 |
| 4 | `/dsr01/tcp_pose` | std_msgs/msg/Float32MultiArray | 1,395 |
| 5 | `/gripper/position` | std_msgs/msg/Float32 | 1,395 |

**메시지 직렬화 형식:**

```
data (BLOB) 열:
  이미지 메시지:
    → sensor_msgs/Image CDR 직렬화 형식
    → 높이, 너비, 채널, 픽셀 데이터 등 포함

  조인트 상태 메시지:
    → JointState CDR 직렬화 형식
    → 7개 조인트의 각도, 속도, 토크 값 포함

  Float32 메시지:
    → 단일 float 값 (그리퍼, TCP 포즈)

이 BLOB 데이터를 ROS 라이브러리로 역직렬화해야 읽을 수 있음
```

**파일 크기:**

```
episode_001_20260602_033711_eef_0.db3: 3.0 GB
  ├── 14,263개 메시지
  ├── 이미지 메시지가 대부분 용량 차지 (1,132 + 2,251 = 3,383개)
  └── 각 이미지: ~700-900 KB (640x480 RGB)

metadata.yaml: 3.0 KB
  → 이 db3 파일에 대한 정보 요약 (앞서 본 메타데이터)
```

**실제 예시 - episode_001 통계:**

```
지속 시간: 83.8초
총 메시지: 14,263개

토픽별 메시지 수:
  /dsr01/joint_states: 8,090개 (약 97 FPS)
  /camera2/camera2/color/image_raw: 2,251개 (약 27 FPS)
  /gripper/position: 1,395개 (약 17 FPS)
  /dsr01/tcp_pose: 1,395개 (약 17 FPS)
  /camera/camera/color/image_raw: 1,132개 (약 14 FPS)
```

**db3의 역할:**

```
db3 파일:
  - 센서별로 따로따로 저장됨 (메시지 개수 다름)
  - 타임스탐프로만 연결 가능
  - 아직 5 FPS 동기화 안 됨

  ↓ (bag_to_lerobot_eef.py로 Convert)

Parquet + MP4:
  - 5 FPS로 동기화됨 (프레임 개수 동일)
  - 메타데이터와 이미지 분리 저장
  - 바로 학습에 사용 가능
```

### 메시지(Message) vs 프레임(Frame)

**"메시지"는 센서가 보낸 개별 데이터 패킷이고, "프레임"은 모든 센서가 동기화된 시점의 데이터입니다.**

```
ROS bag (Convert 전):
  카메라1: 1,132개 메시지 (약 14 FPS)
  조인트: 8,090개 메시지 (약 97 FPS)
  그리퍼: 1,395개 메시지 (약 17 FPS)
  ↑ 각 센서의 발행 빈도가 다름!

Convert (5 FPS로 재샘플링):
  모든 센서를 200ms 간격 시간축에 정렬
  
최종 (Convert 후):
  419개 프레임
  (각 프레임 = [이미지, 조인트, 그리퍼] 완벽 동기화)
```

### 5 FPS 재샘플링 상세

```
시간축 생성: 200ms 마다 프레임 1개
  t=0ms:    프레임 0
  t=200ms:  프레임 1
  t=400ms:  프레임 2
  ...
  t=83,800ms: 프레임 419

각 프레임 구성 (예: 프레임 0):
  이미지: 1,132개 메시지 중 t=0ms에 가장 가까운 것 선택
  조인트: 8,090개 메시지 중 t=0ms 값 (보간)
  그리퍼: 1,395개 메시지 중 t=0ms 값 (보간)
```

### 최종 저장 형태

Convert 후 Parquet + MP4로 분리 저장:

**Parquet (메타데이터):**
```
data/vla/fin/vla_dataset_v0.4.0/data/chunk-000/file-000.parquet

각 행 = 1 프레임:
  frame_0:
    joint_states: [0.52, -1.23, 0.89, ...]  ← 조인트
    gripper: 0.75                            ← 그리퍼
    image_file: "episode_001__camera1.mp4"  ← 이미지 참조
  frame_1:
    joint_states: [0.54, -1.20, 0.91, ...]
    gripper: 0.76
    image_file: "episode_001__camera1.mp4"
```

**MP4 (이미지 데이터):**
```
videos/episode_001__camera1.mp4
  t=0ms:    프레임 0 이미지 (640x480)
  t=200ms:  프레임 1 이미지
  t=400ms:  프레임 2 이미지
  ... (419개 프레임)
```

**학습 시:**
```
Parquet → 메타데이터 로드 (조인트, 그리퍼, 파일명)
MP4 → 해당 프레임의 이미지 추출
결과 → [이미지, 조인트, 그리퍼] 완전한 쌍
```

### 데이터 저장 위치별 파일 정리

#### db3 파일 (/data/raw/final_project/)

| 파일 | 크기 | 데이터 내용 |
|------|------|----------|
| `episode_001_20260602_033711_eef_0.db3` | 3.0 GB | SQLite3 DB: 14,263개 센서 메시지 (이미지, 조인트, 그리퍼) |
| `metadata.yaml` | 3.0 KB | db3 파일의 정보 요약 (메시지 수, 토픽, 지속시간) |

**db3 내부:**
- `messages` 테이블: 14,263개 행 (센서 데이터 BLOB)
- `topics` 테이블: 5개 토픽 (카메라, 조인트, 그리퍼 등)

---

### Convert 후 저장 구조 (mid/)

Convert 완료 후 데이터는 다음과 같이 저장됩니다:

#### mid/ 폴더 파일 정리

| 파일 | 크기 | 데이터 내용 |
|------|------|----------|
| `data/chunk-000/file-000.parquet` | 1.1 MB | 16,792개 프레임의 메타데이터 (조인트, 액션) |
| `videos/observation.images.camera1/.../*.mp4` | ~50 GB | 카메라1 RGB 비디오 (640x480, 5 FPS) |
| `videos/observation.images.camera2/.../*.mp4` | ~60 GB | 카메라2 RGB 비디오 (640x480, 5 FPS) |
| `meta/info.json` | ~2 KB | 데이터셋 정보 (버전, fps, 에피소드 수 등) |
| `meta/stats.json` | ~5 KB | Quantile 정규화 통계 (최소/최대/분위수) |
| `meta/tasks.parquet` | ~2 KB | 작업 정보 (작업명, 설명, 에피소드 수) |
| `meta/episodes/episodes.parquet` | ~5 KB | 에피소드 인덱싱 (시작/끝 행, 길이) |

**각 파일 상세:**

**1. Parquet (메타데이터)**
```
16,792개 행, 7개 칼럼:
  - episode_index: 에피소드 번호 (0-48)
  - frame_index: 에피소드 내 프레임 번호
  - timestamp: 초 단위 시간
  - observation.state: 정규화된 조인트 각도 6개
  - action: 정규화된 액션 7개

예: frame 0
  episode_index: 0
  observation.state: [0.244, 0.280, 0.886, 1.569, 1.506, -1.564]
  action: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0011]
```

**2. MP4 비디오 (카메라1, 2)**
```
각 에피소드마다 MP4 파일
- 해상도: 640x480
- 프레임레이트: 5 FPS
- 색상: RGB

Parquet의 frame_index로 해당 프레임 추출
```

**3. info.json (데이터셋 스펙)**
```
- 버전: 0.4.0
- fps: 5
- action 차원: 7
- state 차원: 6
- 이미지: 480x640x3
- 총 에피소드: 49
- 총 프레임: 16,792
```

**4. stats.json (정규화 통계)**
```
각 feature별:
  - min, max: 범위
  - q01, q10, q50, q90, q99: 분위수
  (학습 시 이 값으로 데이터 정규화)
```

**5. tasks.parquet (작업 정보)**
```
작업명, 설명, 에피소드 수, 총 프레임 수
```

**6. episodes.parquet (인덱싱)**
```
각 에피소드별:
  - frame_start, frame_end: Parquet 행 인덱스
  - length: 프레임 수 (약 400개/에피소드)
```

#### fin/ 폴더 (최종 학습용)

| 파일 | 데이터 내용 |
|------|----------|
| `data/chunk-000/file-000.parquet` | mid/와 동일 (메타데이터) |
| `videos/.../*.mp4` | mid/와 동일 (비디오) |
| `meta/info.json` | mid/와 동일 |
| `meta/stats.json` | mid/와 동일 + Quantile 통계 포함 |
| `meta/tasks.parquet` | mid/와 동일 |
| `meta/episodes/episodes.parquet` | mid/와 동일 |

**mid/와의 차이**:
- 내용은 동일
- stats.json에 Quantile 통계가 이미 포함되어 있음 (학습에 바로 사용 가능)

---

### 데이터 로드 방식 (mid/ 또는 fin/)

**쌍으로 저장된 방식:**
```
Parquet의 각 행 (1 프레임) → MP4의 1개 프레임과 연결

Parquet row:
  episode_index: 0
  frame_index: 0
  observation.state: [0.244, 0.280, ...]  ← 로봇 상태
  action: [0.0, 0.0, 0.0, ...]            ← 로봇 액션

MP4 (카메라1):
  frame 0 → RGB 이미지 (640x480)

MP4 (카메라2):
  frame 0 → RGB 이미지 (640x480)
```

**파이썬 로드 예시:**
```python
import pandas as pd
import cv2

# 1. Parquet 읽기
df = pd.read_parquet('data/chunk-000/file-000.parquet')
row = df.iloc[0]  # 첫 번째 프레임

# 2. 메타데이터 추출
joint_state = row['observation.state']  # [0.244, 0.280, ...]
action = row['action']                   # [0.0, 0.0, ..., 0.0011]

# 3. 비디오에서 이미지 추출
cap = cv2.VideoCapture('videos/observation.images.camera1/.../file-000.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, row['frame_index'])
ret, image = cap.read()  # RGB (640x480x3)

# 4. 완벽한 쌍 완성!
sample = {
    'image': image,           # (640x480x3) uint8
    'joint_state': joint_state,  # (6,) float32
    'action': action          # (7,) float32
}
```

---

## 정리: 각 폴더의 핵심

```
raw/
  └── db3 파일
      = 센서 원본 메시지 (14,263개, 따로따로)

mid/
  ├── Parquet (1.1 MB): 16,792개 프레임의 메타데이터
  ├── MP4: 이미지 데이터 (110 GB)
  └── meta/: 정보 파일들
  = Convert 완료 (5 FPS 동기화, 쌍으로 정리됨)

fin/
  = mid/와 동일
  = stats.json에 Quantile 통계 추가
  = 학습 바로 가능
```

---

## 개요

VLA 모델 학습을 위한 데이터 파이프라인:

```
ROS bag 수집 (db3)
    ↓
전처리 & 정규화
    ↓
Parquet + MP4 포맷 변환
    ↓
Quantile Stats 추가
    ↓
최종 학습 데이터셋
```

**핵심 개념:**
- **멀티모달**: 이미지 + 로봇 상태 + 액션 동시 수집
- **정규화**: [-1, 1] 범위로 통일 (모델 학습 안정화)
- **Quantile Stats**: Outlier에 강건한 정규화 파라미터

---

## 1-2단계: 데이터 수집

### 당신의 프로젝트
- 이미 ROS bag 파일로 저장됨 (`/data/raw/final_project/`)
- 49개 에피소드 수집 완료

### 수집되는 센서
- RGB 이미지 (카메라1, 2)
- 조인트 상태: 각도, 속도, 토크
- 그리퍼: 위치, 힘
- 엔드이펙터: XYZ 위치

### 일반적인 문제
- 타임스탐프 불일치: 센서별 시계 차이 (10-50ms)
- 프레임 손상/누락: 네트워크 오류
- 센서 노이즈: 측정값 불안정성

---

## 3단계: 데이터 전처리

### 목표
ROS bag 메시지를 추출하여 구조화하고, 오류/노이즈 제거

### 주요 작업

**1. 손상된 프레임 탐지**
- 완전히 검은/흰 프레임
- 이상한 히스토그램 분포
- 손상된 이미지 헤더

**2. 이상치(Outlier) 탐지**
- Z-score 기반: 평균에서 3σ 이상
- 물리적으로 불가능한 값
- 급격한 점프 (연속 프레임 간 과도한 변화)

**3. 누락 데이터 처리**
- 선형/Cubic 보간으로 채우기
- 너무 많이 누락된 부분은 제거

**결과:** 전처리 보고서 생성 (에피소드마다 상이)
```
예시:
제거된 프레임: 50-300개
탐지된 이상치: 100-200개 (보간됨)
최종 유효 프레임: 원본의 95-99%
```

---

## 4단계: 정규화 및 동기화

### 시간 동기화

ROS bag에서 수집된 메시지들을 재샘플링:

**수집 단계 (ROS bag):**
- 카메라1: 약 14 FPS (USB 2.0 대역폭 제약)
- 카메라2: 약 27 FPS
- 조인트 상태: 약 97 FPS

**Convert 단계 (bag_to_lerobot_eef.py):**
- **FPS = 5로 다운샘플링** (고정)
- 모든 센서를 5 FPS 시간축으로 정렬
- 이미지: 가장 가까운 프레임 선택
- 조인트/상태: 보간으로 채우기

**예:** episode_001 (84초) → 5 FPS로 변환 → 약 420 프레임

### 데이터 정규화

모든 값을 **[-1, 1] 범위**로 변환:

```
원본 범위        →  정규화
조인트: [-π, π]  →  [-1, 1]
그리퍼: [0, 100%] → [-1, 1]
이미지: [0, 255]  → [-1, 1]
```

### 액션 정의
```
action[t] = state[t+1] - state[t]
```
이미 정규화된 상태의 차이이므로 [-1, 1] 범위 내.

---

## 5단계: 학습 데이터셋 포맷화

### 에피소드 개념

500개 프레임을 여러 에피소드로 분할:
- 에피소드 길이: 10-50 타임스텝
- 에피소드 간 오버랩: 일부 겹침으로 데이터 증강
- 각 에피소드: 초기 관측 + 액션 시퀀스 + 메타데이터

### 저장 포맷: Parquet

**Columnar 저장 형식:**
- 효율적 읽기 (필요한 칼럼만 로드)
- 압축 지원 (저장 공간 절약)
- 호환성 높음

**각 행 (타임스텝):**
```
episode_index, frame_index, observation.state, 
observation.image, action, is_first, is_last, ...
```

### 데이터 분할

전체 데이터를 에피소드 단위로 분할:
- **학습**: 70%
- **검증**: 15%
- **테스트**: 15%

---

## 5.5단계: Quantile Stats

### 목표

LeRobot PI05 모델이 사용할 정규화 파라미터 생성

### 과정

1. **데이터셋 복사**: `mid/` → `fin/`
2. **통계 계산**: 각 feature별로 아래 값 계산
   - Min, Max
   - Mean, Std
   - Quantiles: 1%, 10%, 50%, 90%, 99%
3. **저장**: `meta/stats.json`에 저장

### 계산되는 통계

```json
{
  "action": {
    "min": [-0.95, ...],
    "max": [0.92, ...],
    "q01": [-0.85, ...],  // ← 정규화 범위
    "q99": [0.83, ...],    // ← 정규화 범위
    ...
  }
}
```

**중요**: `q01`과 `q99`가 극단값을 제외한 합리적인 정규화 범위 제공

### mid/ vs fin/

| 항목 | mid/ (원본) | fin/ (학습용) |
|------|-----------|-------------|
| Parquet | ✓ | ✓ (동일) |
| 비디오 | ✓ | ✓ (동일) |
| stats.json | ❌ | ✓ quantile stats |

**⚠️ 학습은 반드시 `fin/` 사용해야 함**

---

## 5.6단계: 저장 구조

### 최종 디렉토리 구조

```
data/vla/fin/vla_dataset_v0.4.0/
├── data/
│   └── chunk-000/file-000.parquet  (메타데이터, 액션, 상태)
├── videos/
│   └── episode_000__camera1.mp4    (RGB 이미지 데이터)
└── meta/
    ├── info.json
    ├── episodes.parquet
    ├── tasks.parquet
    └── stats.json                   ← Quantile stats
```

### Parquet 파일 구조

각 행 = 1 타임스텝:

| 칼럼 | 타입 | 설명 |
|------|------|------|
| `episode_index` | int | 에피소드 번호 |
| `observation.state` | float32[7] | 정규화된 조인트 |
| `observation.image` | str | 비디오 파일명 |
| `action` | float32[7] | 정규화된 액션 |

### 비디오 파일

```
episode_000__camera1.mp4
- 해상도: 640x480
- 프레임레이트: 30 FPS
- 코덱: H.264
- 파일 크기: 에피소드당 200-300 MB
```

### 저장 공간 분포

```
총 120 GB
├── data/ (Parquet):  10-20 GB (20%)  - 메타데이터
└── videos/ (MP4):   100-110 GB (80%)  - 이미지 데이터
```

### 학습에 필수인 것

모두 필요:
- `data/` 없으면 → 메타데이터 로드 불가
- `videos/` 없으면 → 이미지 로드 불가
- `stats.json` 없으면 → 정규화 불가

---

## 6단계: 품질 검증

### 검증 항목

**1. 구조**: 필수 파일 존재 확인
**2. 형태**: 모든 데이터의 shape 일관성
**3. 범위**: 정규화 값이 [-1, 1] 내인지
**4. 통계**: 액션/상태 분포 분석
**5. 에피소드**: 길이, 플래그 일관성

### 검증 결과 예시

```
✓ 필수 파일: 모두 존재
✓ Parquet 파일: 손상 없음
✓ 에피소드 수: 150개
✓ 총 타임스텝: 90,000개
✓ 정규화 범위: [-1, 1] 내 99.9%
✓ Quantile stats: 포함됨
→ 학습 준비 완료
```

---

## 7단계: 추론(Inference)

### 실제 모델 사용 흐름

```python
# 로봇에서 이미지와 상태 받기
base_image: np.ndarray (640x480, uint8)  # 원본 크기
state: np.ndarray (7-dim)  # [j1~j6, gripper]

# 전처리
image_b64 = _encode_image(base_image)  # 224x224로 리사이징 후 Base64
state_padded = np.zeros(32)
state_padded[:7] = state  # 32-dim으로 패딩

# 모델에 보내기
response = requests.post(
    "http://192.168.50.79:18003/predict",
    json={
        "state": state_padded.tolist(),
        "base_image": image_b64,
        "instruction": "pick up the red object",
        "reset_episode": False
    }
)

# 응답
action = np.array(response.json()["action"])  # 32-dim
next_joint_angles = action[:6]  # 다음 조인트 각도
next_gripper = action[6]  # 다음 그리퍼 위치
```

### 이미지 전처리 단계

```
원본 이미지 (640x480, uint8)
    ↓ PIL 변환
    ↓ 224x224 리사이징 (bilinear 보간)
    ↓ JPEG 압축 (quality=90)
    ↓ Base64 인코딩
    ↓ JSON 문자열
```

### 모델 입력/출력

**입력:**
- 이미지: Base64 인코딩 (224x224)
- 상태: 32-dim float (앞 7개만 유효)
- 명령어: 텍스트 문자열

**출력:**
- 액션: 32-dim float
- 실제 사용: 앞 7개 (조인트 6 + 그리퍼 1)
- 범위: 원본 범위 ([-π, π] 등, 이미 역정규화됨)

### 학습 데이터셋 vs 추론 입력

| 항목 | 학습 데이터셋 | 추론 입력 |
|------|-------------|---------|
| 이미지 크기 | 원본 (640x480) | 224x224로 리사이징 |
| 이미지 포맷 | MP4/Parquet | JPEG Base64 문자열 |
| 상태 정규화 | [-1, 1] | 원본 범위 |
| 상태 차원 | 7-dim | 32-dim (zero-padded) |
| 저장 형태 | 로컬 파일 | HTTP JSON |

---

## 트러블슈팅

### 데이터 수집 단계

**타임스탐프 오차 > 50ms**
- 원인: 센서 클럭 불동기
- 해결: ROS time sync 설정, 동기화 임계값 조정

**카메라 프레임 드롭**
- 원인: 네트워크 대역폭 부족
- 해결: 해상도 낮추기, ROS 버퍼 크기 증가

### 전처리 단계

**손상된 프레임 너무 많음**
- 원인: 카메라 연결 불안정
- 해결: 카메라 재부팅, 케이블 확인

**정규화 후 값이 범위를 벗어남**
- 원인: Outlier 범위 초과
- 해결: Outlier 임계값 조정, clipping 적용

### Quantile Stats 단계

**계산이 너무 오래 걸림**
- 원인: 대용량 데이터, 비디오 때문에 순차 처리
- 해결: num_workers 증가, 배치 처리

**"quantile_stats 없음" 오류**
- 원인: stats.json은 있지만 키 없음
- 해결: stats.json 재생성

### 학습 단계

**FileNotFoundError - videos/ 없음**
- 해결: mid/에서 fin/으로 다시 복사

**KeyError - 칼럼 누락**
- 해결: 포맷화 재실행

---

## 소요 시간

| 단계 | 150 에피소드 |
|------|-----------|
| 텔레오퍼레이션 | 1-2시간 |
| 전처리 | 30분 |
| 정규화 | 1시간 |
| 포맷화 | 1시간 |
| Quantile Stats | 2-3시간 |
| 검증 | 30분 |
| **총합** | **6-8시간** |

---

**최종 문서 버전**: 2.1 (간결화)
