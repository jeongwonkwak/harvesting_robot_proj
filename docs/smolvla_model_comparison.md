# SmolVLA 모델 비교 및 Doosan 로봇 적용 가이드

---

## 1. 모델 교체 이유

| | SmolVLA-base | SmolVLA-libero |
|--|-------------|----------------|
| 기반 로봇 DOF | **6관절** (그리퍼 미포함) | **7관절** (6 EEF + 그리퍼) |
| action 차원 | 6-dim | **7-dim** `[Δx,Δy,Δz,Δrx,Δry,Δrz,grip]` |

Doosan M1013은 **6관절 팔 + 그리퍼 = 7-dim 제어**로, SmolVLA-libero의 action 공간과 일치한다.  
SmolVLA-base는 그리퍼를 포함하지 않는 6-dim 구조라 그리퍼 제어가 불가능하거나 별도 처리가 필요했다.

---

## 2. 모델 상세 비교

| 항목 | SmolVLA-base | SmolVLA-libero |
|------|-------------|----------------|
| HuggingFace ID | `lerobot/smolvla_base` | `lerobot/smolvla_libero` |
| 파라미터 수 | ~450M | ~450M (base와 동일 아키텍처) |
| 모델 파일 크기 | 907 MB (`model.safetensors`) | 907 MB (`model.safetensors`) |
| 학습 데이터 | 범용 로봇 조작 데이터 (다양한 6-DOF 로봇) | LIBERO 데이터셋 (Franka Panda 7-DOF, 탁상 조작) |
| 기반 로봇 DOF | 6 | 7 (Franka 7관절) |
| state 입력 차원 | 7-dim `[x,y,z,rx,ry,rz,gripper]` | **6-dim** `[x,y,z,rx,ry,rz]` (그리퍼 state 없음) |
| state 단위 | mm / deg | **m / rad** |
| action 출력 차원 | 6-dim EEF delta | **7-dim** `[Δx,Δy,Δz,Δrx,Δry,Δrz,grip]` |
| action 단위 | rad 계열 (raw) | 정규화된 OSC 제어 신호 `[-1, 1]` |
| 카메라 키 | `image_top` | `camera1`, `camera2`, `camera3` |
| 서버 역정규화 | 직접 처리 필요 (버그 있었음) | 서버 postprocessor가 자동 처리 |

---

## 3. Doosan M1013 로봇 입출력

### 로봇 → 파이프라인 (읽기)

| 데이터 | 형식 | ROS2 토픽 / 방법 |
|--------|------|----------------|
| EEF 위치·자세 | `[x, y, z]` mm, `[rx, ry, rz]` deg (ZYZ Euler) | `/dsr01/msg/current_posx` |
| 관절 각도 | `[J1~J6]` deg | `/dsr01/msg/current_posj` |
| 그리퍼 위치 | 0 (open) ~ 740 (close), raw count | serial `/dev/ttyUSB0` |

### 파이프라인 → 로봇 (쓰기)

| 명령 | 형식 | 설명 |
|------|------|------|
| `move_line(target, vel, acc)` | `[x,y,z,rx,ry,rz]` mm/deg | Cartesian 직선 이동 (현재 사용) |
| `move_joint(joints, vel, acc)` | `[J1~J6]` deg | 관절 각도 이동 |
| `gripper.set_ratio(ratio)` | `0.0` (open) ~ `1.0` (close) | 0~740 raw 로 변환 후 시리얼 전송 |

### 홈포즈 (기준)

```
관절: J = [0°, 0°, 90°, 0°, 90°, 0°]
EEF:  x=373mm  y=0mm   z=245mm
      rx=130°  ry=-180°  rz=130°
```

> ⚠️ ry=-180° → ZYZ Euler **gimbal lock** 영역. rx/rz가 인접 스텝 간 크게 점프.  
> J5를 85° 등으로 조정해 ry를 ±180°에서 멀리 두는 것을 권장.

---

## 4. 학습 환경 (LIBERO)

SmolVLA-libero는 [LIBERO 데이터셋](https://libero-project.github.io/)으로 학습됐다.

- **로봇**: Franka Emika Panda (7-DOF 팔 + 그리퍼)
- **작업**: 탁상 위 물체 집기·밀기·정렬 등 테이블 조작 시나리오
- **EEF 좌표계** (Franka base frame 기준)

  | 방향 | LIBERO Franka | Doosan M1013 (홈포즈 기준) |
  |------|--------------|--------------------------|
  | 앞쪽 (물체 접근) | **−x** | +y |
  | 좌우 | ±y | ±x |
  | 상하 | ±z | ±z |

- **action 단위**: OSC(Operational Space Control) 정규화 신호
  - 서버 `policy_postprocessor.json`의 `unnormalizer_processor`가 역정규화 후 반환
  - 직접 m/rad가 아님 → `max_pos_delta_mm`, `max_rot_delta_deg`로 스케일 적용

```
LIBERO action.max 참고값:
  [0.9375, 0.9375, 0.9375, 0.356, 0.375, 0.375, 1.0]
  (위치 3축, 회전 3축, 그리퍼)
```

---

## 5. Doosan 적용 시 필요한 변환

### Step 1: 단위 변환 (mm/deg → m/rad)
```python
state_mrad[:3] = eef[:3] / 1000.0        # mm → m
state_mrad[3:6] = np.radians(eef[3:6])   # deg → rad
```

### Step 2: State 분포 캘리브레이션 (out-of-distribution 방지)
```python
state = _LIBERO_STATE_MEAN + (state_mrad - _OUR_STATE_MEAN) / _OUR_STATE_STD * _LIBERO_STATE_STD
```

```python
# LIBERO 학습 데이터 분포 (policy_preprocessor safetensors에서 추출)
_LIBERO_STATE_MEAN = [-0.04652,  0.03441,  0.76455,  2.97221, -0.22047, -0.12558]
_LIBERO_STATE_STD  = [ 0.10494,  0.15177,  0.37852,  0.34427,  0.90695,  0.32539]

# Doosan 홈포즈 [0,0,90,0,90,0]° 기준 분포 (m/rad)
_OUR_STATE_MEAN    = [ 0.30,     0.00,     0.15,     2.25,    -3.14,     2.25   ]
_OUR_STATE_STD     = [ 0.08,     0.05,     0.10,     0.20,     0.20,     0.20   ]
```

### Step 3: Action 좌표계 remapping (LIBERO Franka → Doosan)

Franka의 접근 방향(−x)이 Doosan의 앞방향(+y)에 대응하므로 축 교환 + 부호 반전.

```python
pos_raw = action[:3] * max_pos_mm

pos_delta = np.array([
     pos_raw[1],   # LIBERO  y → Doosan  x (횡방향)
    -pos_raw[0],   # LIBERO -x → Doosan +y (앞방향, 부호 반전)
     pos_raw[2],   # LIBERO  z → Doosan  z (상하, 동일)
])

rot_raw = action[3:6] * max_rot_deg

rot_delta = np.array([
     rot_raw[1],   # LIBERO ry → Doosan rx
    -rot_raw[0],   # LIBERO rx → Doosan ry (부호 반전)
     rot_raw[2],   # LIBERO rz → Doosan rz (동일)
])
```

### Step 4: 역정규화 (서버 자동 처리)

클라이언트가 별도로 역정규화하지 않는다.  
서버 `unnormalizer_processor`가 action chunk 반환 전 자동 적용.

> **주의**: 이전 `grasp_pipeline.py`(SmolVLA-base)에서는 클라이언트가 stats를 로드해  
> 직접 역정규화하는 **이중 역정규화 버그**가 있었다. 현재 수정됨.

---

## 6. 현재 알려진 한계

| 문제 | 원인 | 상태 |
|------|------|------|
| 로봇이 −x 방향으로 이동 | LIBERO 접근 방향(−x)이 Doosan에 그대로 적용됨 | remapping으로 수정 |
| 수직 하강(−z) 상대적으로 약함 | action[2] 크기가 x,y보다 작음 | 스케일 조정 필요 |
| Gimbal lock (ry≈±180°) | 홈포즈 J5=90° → EEF ry=−180° | J5 각도 조정으로 완화 가능 |
| 이미지 도메인 불일치 | LIBERO(Franka 환경) vs 우리 카메라 뷰 | fine-tuning 필요 |
| State 분포 잔류 오차 | affine 캘리브레이션의 std 추정값이 대략적 | 실제 데이터로 재추정 필요 |

---

## 7. 향후 계획

1. **Fine-tuning 데이터 재녹화**  
   `teleop_record_and_convert_eef.py`로 Doosan 환경에서 에피소드 재녹화.  
   저장 단위: m/rad (LIBERO 포맷 일치).

2. **smolvla_libero fine-tuning**  
   `lerobot-train`으로 Doosan 데이터셋(`smolvla_dataset_v2.0`) 기반 fine-tuning.

3. **홈포즈 조정**  
   J5를 85° 등으로 변경해 EEF ry를 ±180°에서 멀어지게 설정.

---

## 8. 관련 파일

| 파일 | 역할 |
|------|------|
| `grasp_vla/grasp_pipeline_eef.py` | EEF delta 방식 VLA 실행 메인 파이프라인 (현재 사용) |
| `grasp_vla/grasp_pipeline.py` | SmolVLA-base용 파이프라인 (joint delta, 이전) |
| `src/bag_to_lerobot_eef.py` | rosbag → LeRobot 데이터셋 변환 (m/rad 단위) |
| `src/move_to_pose.py` | 홈포즈 이동 유틸리티 |
| `docs/libero_doosan_frame_remapping.md` | 좌표계 remapping 상세 설명 |
