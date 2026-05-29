# LIBERO(Franka) → Doosan 좌표계 remapping

## 배경

smolvla_libero 모델은 **Franka** 팔로 수집된 LIBERO 데이터셋으로 학습됐다.  
우리 로봇은 **Doosan M1013**으로, 두 로봇의 EEF 좌표계(base frame 기준 축 방향)가 다르다.  
remapping 없이 LIBERO action을 그대로 Doosan에 적용하면, 물체에 다가가야 할 동작이 엉뚱한 방향으로 나온다.

---

## 증상

홈포즈 `J=[0,0,90,0,90,0]°`에서 물체를 향해 전진해야 하는데,  
모델이 `action[0] ≈ -0.83 ~ -0.92` (매우 큰 음수) 를 출력해서  
Doosan이 **-x 방향으로 40mm 이상** 이동하는 문제가 반복됐다.

로그 예시:
```
action(m/rad) [-0.828, 0.173, -0.371, ...]
delta(mm/°) Δx=-41.41  Δy=+8.67  Δz=-18.53
```

---

## 원인: 축 방향 불일치

| 방향 | LIBERO Franka | Doosan (홈포즈 기준) |
|------|--------------|---------------------|
| 앞쪽 (물체 접근) | −x | +y |
| 횡방향 (좌우) | +y | +x |
| 상하 | +z | +z |

LIBERO에서 "앞으로 접근" = `action[0]`이 큰 음수 → Doosan에 그대로 적용하면 `-x` 이동.  
Doosan의 앞방향은 `+y`이므로 축 교환 + 부호 반전이 필요하다.

---

## 적용한 remapping

### 위치 (translation)

```python
pos_raw = action[:3] * max_pos_mm   # LIBERO frame (mm)

pos_delta = np.array([
     pos_raw[1],   # LIBERO  y → Doosan x (횡방향)
    -pos_raw[0],   # LIBERO -x → Doosan +y (앞방향, 부호 반전)
     pos_raw[2],   # LIBERO  z → Doosan z (상하, 동일)
], dtype=np.float32)
```

### 자세 (rotation)

위치 축 교환(x↔y)에 맞춰 회전 축도 동일하게 교환한다.

```python
rot_raw = action[3:6] * max_rot_deg   # LIBERO frame (deg)

rot_delta = np.array([
     rot_raw[1],   # LIBERO ry → Doosan rx
    -rot_raw[0],   # LIBERO rx → Doosan ry (부호 반전)
     rot_raw[2],   # LIBERO rz → Doosan rz (동일)
], dtype=np.float32)
```

### gripper

변환 없음. `action[6]` 그대로 사용 (0.0=open, 1.0=close).

---

## remapping 적용 후 기대 동작

| 이전 (remapping 없음) | 이후 (remapping 적용) |
|-----------------------|-----------------------|
| action[0]=-0.83 → Δx=-41mm | action[0]=-0.83 → Δy=+41mm (앞으로) |
| action[1]=+0.17 → Δy=+8mm | action[1]=+0.17 → Δx=+8mm (옆으로) |
| action[2]=-0.37 → Δz=-18mm | action[2]=-0.37 → Δz=-18mm (아래로, 동일) |

---

## 관련 파라미터 (grasp_pipeline_eef.py)

```
max_pos_delta_mm  = 50.0   # action 1.0 → 50mm 이동
max_rot_delta_deg = 10.0   # action 1.0 → 10° 회전
```

범위를 줄이고 싶으면 이 값을 낮춘다.

---

## 한계 및 향후 작업

- 이 remapping은 **Doosan 홈포즈 `[0,0,90,0,90,0]°` 기준**이다.  
  홈포즈가 바뀌면 EEF base frame 방향도 달라지므로 재검토가 필요하다.
- LIBERO 이미지 도메인(Franka + LIBERO 환경)과 우리 환경의 시각적 차이가 크기 때문에,  
  **Doosan 환경으로 fine-tuning**하는 것이 근본적인 해결책이다.
- 회전 remapping의 정확성은 실제 실험으로 추가 검증이 필요하다.

---

## 코드 위치

`/home/user/robot_workspace/vla_ws/grasp_vla/grasp_pipeline_eef.py`  
→ `execute_grasp()` 내 `# 6d. LIBERO 정규화 제어신호 → Doosan delta 변환` 섹션
