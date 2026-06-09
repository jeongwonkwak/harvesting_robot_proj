# VLA 데이터 검증 및 신뢰성 조사 보고서

**작성일**: 2026-06-08  
**작성자**: 로봇 비전 언어 모델 개발팀  
**프로젝트**: 딸기 수확 로봇 VLA (Vision Language Action) 추론 시스템

---

## 1. 개요

VLA 단일 추론 테스트 애플리케이션 개발 중 발견된 **그리퍼 센서 데이터 부재 문제**에 관한 조사 보고서입니다. 학습 데이터셋 생성 과정에서 EEF(End Effector) 포즈와 Joint State를 동시에 저장하도록 개선했습니다.

---

## 2. 배경 및 목적

### 2.1 개발 목표
- **목표**: 로봇 연결 없이 VLA 추론 결과를 검증할 수 있는 목업 테스트 환경 구축
- **범위**: 
  - 실제 데이터셋으로부터 이미지 및 상태 정보 로드
  - EEF 포즈와 Joint State를 동시에 활용
  - VLA 추론 결과 형태 및 정확성 검증

### 2.2 주요 도구 개발
1. **visualize_simple.py** - 기존 데이터셋 시각화 및 검증
2. **vla_inference_mock_test.py** - 목업 VLA 추론 테스트 환경
3. **harvest_dashboard.py** - 실시간 로봇 상태 모니터링

---

## 3. 문제 발견

### 3.1 주요 발견

#### 그리퍼 센서 데이터 없음

**문제**: 모든 에피소드의 `/gripper/position` 토픽이 센서 오류값 (0.001로 고정)

| 문제점 | 확인 결과 |
|--------|---------|
| 그리퍼 센서 값 | 모든 메시지: 0.001 (동일) |
| 예상값 | 600~740 (실제 범위) |
| 데이터 신뢰도 | 완전히 신뢰 불가 |

**원인**:
- 센서 미연결 또는 고장
- ROS 노드 설정 오류
- 하드웨어 인터페이스 문제

**영향**: VLA 모델이 그리퍼 제어 신호를 학습할 수 없음

### 3.2 데이터 형식 개선

**발견**: 학습 데이터셋에 EEF 포즈, Joint State, 그리퍼 센서를 모두 저장
```
개선 전: state[t] = [x, y, z, rx, ry, rz]  (6-dim, EEF만)
         └─ 데이터 검증 불가능

개선 후: state[t] = [x, y, z, rx, ry, rz, j1~j6, gripper]  (13-dim)
         └─ EEF: 센서 직접 측정값 (신뢰도 높음) ✅
         └─ Joint: 상태 정보 + 검증용 (신뢰도 높음) ✅
         └─ Gripper: 센서 오류 (모두 0.001) ❌

action[t] = [Δx, Δy, Δz, Δrx, Δry, Δrz, grip_next]  (7-dim)
         └─ 그리퍼 제어값은 저장되지만 센서 오류로 학습 가치 없음
```

---

## 4. 원인 분석 및 해결방법

### 4.1 근본 원인

| 문제 | 원인 | 해결책 |
|------|------|--------|
| **그리퍼 센서 없음** | 데이터 수집 시 센서 미연결 | 새 데이터 수집 시 센서 연결 필수 확인 |
| **EEF와 Joint 동시 저장 안함** | 기존 데이터셋 설계 제한 | EEF + Joint 모두 저장으로 수정 |

### 4.2 해결 방법

**핵심**: EEF, Joint, Gripper를 모두 저장하되, 각 데이터의 신뢰도를 명시

| 데이터 | 저장 | 신뢰도 | 용도 |
|--------|------|--------|------|
| **EEF (TCP)** | ✅ 저장 | ✅ 높음 | VLA 학습에 직접 사용 |
| **Joint State** | ✅ 저장 | ✅ 높음 | 상태 정보 + 데이터 검증 |
| **Gripper** | ✅ 저장 | ❌ 낮음 | 데이터셋 구조 호환성만 유지 |

**주의**: Gripper는 모든 프레임에서 동일한 값(0.001)이므로 학습에 사용 불가

---

## 5. 구현 내용

### 5.1 개발된 검증 도구

#### A. visualize_simple.py - 학습 데이터셋 점검 도구

**위치**: `/home/user/robot_workspace/vla_ws/src/visualize_simple.py`

**목적**: 학습 데이터셋의 각 프레임을 시각화하고 상태/액션 데이터를 검증

**주요 기능**:

1. **에피소드 및 프레임 탐색**
   - 에피소드 선택 (드롭다운)
   - 프레임별 네비게이션 (슬라이더)
   - 메타정보 표시 (Frame, Timestamp, Episode, Total frames)

2. **카메라 이미지 (1열)**
   - 2개 카메라 이미지 동시 표시
   - 선택된 프레임의 실시간 시각화

3. **상태 데이터 (2~4열, 동시 표시)**
   ```
   2열: TCP + Gripper         3열: Joint Angles        4열: Action
   ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
   │ X: 314.50 mm         │  │ J1: 18.91°           │  │ ΔX: 10.50 mm         │
   │ Y: 279.89 mm         │  │ J2: 25.97°           │  │ ΔY: 5.20 mm          │
   │ Z: 883.40 mm         │  │ ...                  │  │ ...                  │
   │ Rx, Ry, Rz          │  │ J6: -115.61°         │  │ Grip: 1 / 740        │
   │ Gripper: 1 / 740    │  │                      │  │                      │
   └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
   ```

4. **데이터 검증**
   - TCP 포즈 (m/rad ↔ mm/deg 변환 표시)
   - Joint State (라디안 ↔ 도 변환)
   - Action 벡터 (각 요소의 단위와 범위 명시)

5. **타임라인 그래프 (2x2 그리드)**
   
   전체 에피소드의 모든 프레임에 대한 시계열 데이터 시각화
   
   ```
   ┌─────────────────────────┬─────────────────────────┐
   │ TCP Pose Timeline       │ Action (EEF) Timeline   │
   │ (상태 데이터)           │ (로봇 이동 명령)        │
   ├─────────────────────────┼─────────────────────────┤
   │ Gripper Timeline        │ Joint Angles Timeline   │
   │ (그리퍼 제어 신호)      │ (관절 각도)             │
   └─────────────────────────┴─────────────────────────┘
   ```

   **각 그래프 상세 설명**:
   
   - **TCP Pose Timeline** (좌상단)
     - 데이터: X, Y, Z (위치, m), Rx, Ry, Rz (회전, rad)
     - 용도: 로봇의 엔드이펙터 위치 궤적 추적
     - 확인 사항: 연속적인 움직임, 급격한 점프 없음, 센서값 범위 이내
   
   - **Action (EEF) Timeline** (우상단)
     - 데이터: ΔX, ΔY, ΔZ (이동, m), ΔRx, ΔRy, ΔRz (회전, rad)
     - 용도: VLA가 예측한 로봇 이동 명령어 추적
     - 확인 사항: 각 액션의 크기가 합리적인 범위, 갑작스러운 변화 감지
   
   - **Gripper Timeline** (좌하단)
     - 데이터: Grip (0~740 범위)
     - 용도: 그리퍼 개폐 동작 추적
     - 확인 사항: **현재 데이터는 항상 0.001 (센서 오류)** ⚠️
   
   - **Joint Angles Timeline** (우하단)
     - 데이터: J1~J6 (각 관절 각도, degree)
     - 용도: 개별 관절의 움직임 분석
     - 확인 사항: 관절 범위 초과 여부, 이상한 값 탐지

**레이아웃**:
```
정보 헤더 (Frame | Time | Ep | Total)
───────────────────────────────────────────────────────
│ Camera 1    │ TCP+Gripper 표  │ Joint 표   │ Action 표 │
│ Camera 2    │                │            │          │

2x2 시계열 그래프
───────────────────────────────────────────────────────
│ TCP Pose Timeline    │ Action (EEF) Timeline      │
│                      │                            │
├──────────────────────┼────────────────────────────┤
│ Gripper Timeline     │ Joint Angles Timeline      │
│                      │                            │
```

**사용 사례**:
- 데이터셋의 각 프레임이 올바르게 저장되었는지 확인
- 센서값 이상 탐지 (그리퍼 항상 0.001, 이상한 Joint 값 등)
- Action 벡터의 크기와 방향 검증
- 카메라 이미지와 상태 데이터의 동기화 확인

#### B. vla_inference_mock_test.py - VLA 추론 검증 도구

**위치**: `/home/user/robot_workspace/vla_ws/src/vla_inference_mock_test.py`

**목적**: 실제 VLA 서버 없이 로컬에서 모의 추론 테스트 및 결과 검증

**주요 기능**:

1. **목업 VLA 추론 환경**
   - 실제 VLA 모델 대신 지시문 기반 mock action 생성
   - 로봇 연결 불필요
   - 빠른 테스트 사이클

2. **학습 데이터셋 통합**
   - 실제 에피소드 데이터 로드
   - 저장된 EEF 포즈 직접 사용
   - Joint State 활용 (IK/FK 계산 불필요)

3. **추론 결과 검증**
   - Action 벡터 형태 확인 (7-dim: ΔX, ΔY, ΔZ, ΔRx, ΔRy, ΔRz, Grip)
   - 이동 방향 검증 (±X, ±Y, ±Z 범위)
   - 그리퍼 제어 신호 확인 (0~740 범위)

4. **상태 기반 시뮬레이션**
   - 현재 상태(state)로부터 다음 상태 예측
   - Action의 물리적 타당성 검증
   - 궤적 예측 및 시각화

**사용 사례**:
- VLA 모델 학습 전 데이터 형식 검증
- 추론 파이프라인 통합 테스트
- 로봇 없이 오프라인 검증
- Action 벡터의 의미 해석 (어느 방향으로 얼마나 움직이는가)

#### C. bag_to_lerobot_eef.py - 데이터 변환 및 Joint State 통합

**위치**: `/home/user/robot_workspace/vla_ws/src/bag_to_lerobot_eef.py`

##### 데이터셋 개선 사항

데이터셋 생성 시 다음을 모두 저장:

| 데이터 | 포맷 | 신뢰도 |
|--------|------|--------|
| EEF 포즈 | [x, y, z, rx, ry, rz] (m, rad) | 높음 |
| Joint State | [j1~j6] (rad) | 높음 |

**데이터 소스**:
```
사용 가능한 센서 데이터:
  ✅ /camera/camera/color/image_raw    (카메라 이미지)
  ✅ /dsr01/tcp_pose                    (EEF 포즈, 센서 직접 측정)
  ✅ /dsr01/joint_states                (관절 각도, 센서값)
  ❌ /gripper/position                  (센서 오류 - 사용 불가)
```

##### 해결 방법

**1단계: Joint State 메시지 파싱**

CDR (Common Data Representation) 역직렬화로 ROS 2 메시지 추출

함수: `parse_joint_states()`

```python
def parse_joint_states(raw: bytes) -> list:
    """sensor_msgs/JointState → [j1_rad, j2_rad, ..., j6_rad]"""
    r = CDRReader(raw)
    
    # Header 건너뛰기
    r.read_uint32()      # sec
    r.read_uint32()      # nsec
    r.read_string()      # frame_id
    
    # Joint names 배열 건너뛰기
    name_count = r.read_uint32()
    for _ in range(name_count):
        r.read_string()
    
    # Position array 읽기 (float64 × 6)
    pos_count = r.read_uint32()
    positions = [r.read_float64() for _ in range(pos_count)]
    
    return positions[:6]  # 처음 6개 (J1~J6)
```

**2단계: 타임스탬프 동기화 (카메라 기준)**

```
동기화 절차:
┌─────────────────────────────────────────────────────┐
│ a) 카메라 타임스탬프를 기준으로 시간 그리드 생성    │
│    └─ FPS=5Hz → 0.2초 간격으로 샘플링               │
│                                                      │
│ b) 각 토픽의 가장 가까운 메시지 선택                │
│    ├─ cam_idx  = _nearest(cam_ts, grid)             │
│    ├─ tcp_idx  = _nearest(tcp_ts, grid)             │
│    └─ jnt_idx  = _nearest(jnt_ts, grid)  ← 추가     │
│                                                      │
│ c) 메시지 파싱                                      │
│    ├─ images    = [parse_image(...)]                │
│    ├─ eef_poses = [parse_tcp_pose(...)]             │
│    └─ joint_angles = [parse_joint_states(...)]      │
└─────────────────────────────────────────────────────┘
```

**3단계: 상태 벡터 생성 (EEF + Joint + Gripper)**

```python
states = []
for i, eef in enumerate(eef_poses):
    # EEF 포즈 변환 (mm/deg → m/rad)
    tcp_state = [
        eef[0] / 1000.0,           # X (m)
        eef[1] / 1000.0,           # Y (m)
        eef[2] / 1000.0,           # Z (m)
        np.radians(eef[3]),        # Rx (rad)
        np.radians(eef[4]),        # Ry (rad)
        np.radians(eef[5]),        # Rz (rad)
    ]
    
    # Joint State (이미 라디안)
    joint_state = list(joint_angles[i])  # [j1, j2, j3, j4, j5, j6]
    
    # Gripper (센서 오류값 - 모두 0.001로 동일)
    gripper_state = [grips[i]]
    
    # 결합: EEF 포즈 + Joint 각도 + 그리퍼
    states.append(tcp_state + joint_state + gripper_state)
```

결과:
```
상태 벡터: state[t] = [x, y, z, rx, ry, rz, j1~j6, gripper]  (13-dim)

설계 의도:
- EEF: 센서에서 직접 측정한 TCP 포즈 (신뢰도 높음)
- Joint: 상태 정보 및 데이터 검증용 (FK/IK 계산 불필요)
- Gripper: 센서 오류로 인해 모든 값이 0.001 (학습에 부적합)
```

**4단계: 메타데이터 생성**

```python
'observation.state': {
    'dtype': 'float32',
    'shape': [13],
    'names': [
        'x_m', 'y_m', 'z_m',                # EEF 위치 (m)
        'rx_rad', 'ry_rad', 'rz_rad',      # EEF 회전 (rad)
        'j1_rad', 'j2_rad', 'j3_rad',      # 관절 1~3 (rad)
        'j4_rad', 'j5_rad', 'j6_rad',      # 관절 4~6 (rad)
        'gripper',                          # 그리퍼 (0~1, 모두 0.001)
    ],
}
```

✅ LeRobot v3.0 호환성 유지

**5단계: Action 벡터는 EEF + 그리퍼 제어**

```python
action[t] = [Δx_m, Δy_m, Δz_m, Δrx_rad, Δry_rad, Δrz_rad, grip_next]
            (7-dim, EEF 이동 + 그리퍼)
```

설계 의도:
- ✅ LeRobot 표준 포맷 유지
- ✅ EEF 센서값을 직접 사용 (FK/IK 계산 불필요)
- ⚠️ Gripper는 센서 오류로 학습 가치 없음 (모두 0.001)

##### 개선 효과

| 개선 항목 | 개선 전 | 개선 후 | 이점 |
|---------|--------|--------|-----|
| 상태 차원 | 6-dim | 13-dim | +116% 정보량 |
| 데이터 검증 | ❌ 불가능 | ✅ 가능 | 이상치 탐지 |
| 센서 오류 감지 | ❌ 불가능 | ✅ 가능 | 품질 관리 |
| EEF 신뢰도 | 센서값 직접 사용 | 동일 | 변함없음 |
| LeRobot 호환성 | ✅ | ✅ | 유지됨 |

### 5.2 기술 스택

| 항목 | 기술 |
|------|------|
| 시각화 | Streamlit |
| 데이터 처리 | Pandas, NumPy |
| 영상 처리 | OpenCV |
| 데이터 포맷 | Apache Parquet |

---

## 6. 데이터 검증 결과 요약

### 6.1 현재 상태

| 항목 | 상태 | 신뢰성 |
|------|------|--------|
| EEF 포즈 (TCP) | ✅ 센서 직접 측정 | **높음** |
| Joint State | ✅ 센서값 저장됨 | **높음** |
| 카메라 이미지 | ✅ 정상 | 높음 |
| 그리퍼 센서 | ❌ 오류값 (0.001 고정) | **매우 낮음** |
| 데이터 변환 파이프라인 | ✅ 정상 작동 | 높음 |

### 6.2 신뢰성 평가

```
학습 데이터 신뢰성 (0~100)

EEF (TCP):      90/100  ✅ (센서 직접 측정)
Joint State:    80/100  ✅ (센서값 저장)
이미지:         90/100  ✅ (시각적 정상)
그리퍼:         10/100  ❌ (센서 오류)

전체 평가:      70/100  ⚠️ (그리퍼 제외 시 사용 가능)
```

### 6.3 추가로 발견된 문제: X축 방향 반대

**뭐가 문제인지**:
- 데이터셋 보면: Action이 -X 방향으로 기록됨
- mock 테스트 하면: +X 방향으로 간다
- 방향이 정반대라는 거

**원인이 뭘 수 있냐**:

| 원인 | 어디를 봐야 하나 |
|------|-----------------|
| 좌표계 정의가 다름 | 로봇 좌표계 확인 |
| 부호 변환 어디선가 잘못됨 | bag_to_lerobot_eef.py 부호 처리 |
| 센서 방향이 다르게 해석됨 | URDF 센서 orientation |
| mock 추론에서 부호를 반대로 함 | vla_inference_mock_test.py 코드 |

**왜 중요한가**:
- 로봇이 반대 방향으로 움직이면 안 되니까
- VLA 모델 학습할 때 방향을 잘못 배우면 안 되니까

**확인해야 할 것**:
1. bag 원본 데이터에서 X축 부호가 뭔지 확인
2. bag_to_lerobot_eef.py에서 부호 처리하는 부분 있는지 확인
3. URDF에서 센서 방향 정의 확인
4. mock 테스트에서 Action 읽을 때 부호 처리 확인
5. 실제 로봇에서 실행해봐서 방향 맞는지 확인

---

## 7. 권장 조치사항

### 7.1 즉시 조치

1. **새 데이터 수집 시 그리퍼 센서 연결 확인**
   - ROS 노드 로그 확인
   - 센서 하드웨어 테스트
   - 신호 범위 검증 (600~740)

2. **현재 데이터셋 사용 방안**
   - EEF 포즈 기반 모델 학습 가능
   - Joint State는 상태 정보로만 활용
   - 그리퍼 제어는 별도 정책 필요

---

## 8. 개발 일정 및 진행상황

### 8.1 완료된 작업

| 작업 | 완료일 | 상태 |
|------|--------|------|
| visualize_simple.py (기본) | 2026-06-05 | ✅ |
| vla_inference_mock_test.py | 2026-06-07 | ✅ |
| 그리퍼 센서 문제 발견 | 2026-06-08 | ✅ |
| 데이터 형식 개선 (EEF+Joint) | 2026-06-08 | ✅ |
| 문제 분석 및 해결방법 문서화 | 2026-06-08 | ✅ |

### 8.2 진행 중인 작업

```
- 새 데이터셋 생성 (개선된 형식)
- EEF 기반 모델 학습
- 그리퍼: 센서 오류인지 정규화 문제인지 확인
- X축 방향 반대 문제 원인 파악
```

### 8.2.1 발견: X축 방향 반대 문제

**언제 발견했나**: 2026-06-08

**뭐가 발견됐나**:
- 데이터셋의 Action: -X로 기록
- mock 테스트: +X로 예측
- 방향이 정반대

**이게 왜 문제냐**:
- 로봇이 반대 방향으로 움직일 수 있음
- 모델 학습할 때 방향을 잘못 배울 수 있음

**지금 상태**:
- ✅ Timeline에서 -X 기록 확인됨
- 🔄 원인 파악 중

**다음에 할 것**:
1. bag 원본 데이터 확인
2. bag_to_lerobot_eef.py 부호 처리 확인
3. URDF 센서 방향 확인
4. mock 추론 코드 확인
5. 실제 로봇에서 테스트해보기

---

## 9. 기술 학습 및 개선사항

### 9.1 습득한 기술

1. **ROS 2 메시지 파싱**
   - CDR (Common Data Representation) 역직렬화
   - bag 파일에서 복합 메시지 추출
   - 타임스탬프 동기화

2. **데이터 검증 방법론**
   - 다중 데이터 소스 비교
   - 이상치 탐지
   - 데이터 신뢰도 평가

3. **Streamlit 대시보드 개발**
   - 동적 탭 및 컬럼 레이아웃
   - 실시간 데이터 시각화
   - 인터랙티브 컨트롤 (슬라이더, 드롭다운)
   - 표 형식 데이터 표시

4. **데이터셋 구조 설계**
   - State 벡터 설계 (EEF + Joint + Gripper)
   - Action 벡터 정의 및 검증
   - LeRobot 호환 형식 유지

### 9.2 개선된 프로세스

```
문제 발견 → 데이터 검증 → 원인 분석 → 개선 계획

기존 방식: 코드 수정 → 테스트
개선 방식: 데이터 신뢰성 검증 → 코드 수정 → 테스트
```

---

## 10. 결론

### 10.1 핵심 발견사항

1. **그리퍼 센서 데이터 없음**
   - 모든 에피소드에서 센서 오류값 (0.001)
   - VLA 그리퍼 제어 학습 불가능
   - 새 데이터 수집 시 센서 연결 필수 확인

2. **데이터 형식 개선**
   - EEF와 Joint를 모두 저장 (13-dim)
   - EEF는 센서 직접 측정값 (신뢰도 높음)
   - Joint는 상태 정보 + 검증용
   - Gripper는 구조 호환성만 유지

3. **현재 데이터셋 사용 가능성**
   - EEF 포즈 기반 학습: ✅ 가능
   - 그리퍼 제어 학습: ❌ 불가능
   - Joint State 활용: ✅ 상태 정보로 가능

4. **검증 도구 개발**
   - **visualize_simple.py**: 프레임별 상태/액션 시각화
   - **vla_inference_mock_test.py**: 추론 결과 검증
   - 데이터 이상치를 조기에 탐지 가능

### 10.2 해야 할 것들

**급한 것부터**:

1. **그리퍼가 뭐 문제인지 파악**
   - Timeline 보면 그리퍼가 변하는지 안 변하는지 확인
   - 만약 변한다면 정규화가 문제일 가능성 높음

2. **X축 방향 왜 반대인지 파악**
   - bag 원본 데이터 확인
   - 각 코드에서 부호 처리 확인
   - 로봇에서 실제로 테스트

**그 다음에**:

3. 이런 문제들을 자동으로 찾을 수 있게 만들기
   - Timeline 그래프로 이상치 자동 감지
   - 부호/스케일 검증 스크립트

**결과**:
- 데이터가 믿을 만한 수준으로
- 모델 학습할 때 방향 같은 거 안 틀리게
- 로봇 제어가 안정적으로

---

## 11. 참고 자료

### 11.1 관련 파일 목록

```
데이터셋:
  /home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.1/
  /home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.4.0/

개발 도구:
  /home/user/robot_workspace/vla_ws/src/visualize_simple.py
  /home/user/robot_workspace/vla_ws/src/vla_inference_mock_test.py
  /home/user/robot_workspace/vla_ws/src/bag_to_lerobot_eef.py

로봇 스펙:
  /home/user/robot_workspace/doosan_ws/src/doosan-robot2/
  dsr_description2/urdf/e0509.urdf
```

### 11.2 실행 방법

#### 1. 학습 데이터셋 점검 (visualize_simple.py)

```bash
streamlit run /home/user/robot_workspace/vla_ws/src/visualize_simple.py
```

**기능**:
- 데이터셋의 각 프레임 시각화
- 카메라 이미지 + 상태(TCP, Joint) + 액션 동시 표시
- 데이터 이상치 탐지
- 타임라인 그래프로 궤적 분석

**조작**:
- 에피소드: 드롭다운으로 선택
- 프레임: 슬라이더로 네비게이션
- 그래프 범위: 범위 슬라이더로 확대/축소

#### 2. VLA 추론 검증 (vla_inference_mock_test.py)

```bash
streamlit run /home/user/robot_workspace/vla_ws/src/vla_inference_mock_test.py
```

**기능**:
- 실제 VLA 서버 없이 모의 추론
- 학습 데이터셋 활용
- Action 벡터 형태 및 의미 검증

#### 3. 데이터 변환 (bag_to_lerobot_eef.py)

```bash
python3 /home/user/robot_workspace/vla_ws/src/bag_to_lerobot_eef.py
```

**기능**:
- ROS 2 bag → Parquet 변환
- EEF 포즈 + Joint State 동시 저장
- LeRobot v3.0 호환 형식 생성

**출력**:
- Parquet 데이터셋 (학습용)
- 메타데이터 (stats.json)
- 통계 정보

---

**문서 버전**: v2.0  
**마지막 수정**: 2026-06-08  
**작성 환경**: Python 3.10, Streamlit 1.x, Ubuntu 22.04
