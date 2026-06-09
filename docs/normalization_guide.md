# VLA 데이터 정규화 가이드 (Normalization Guide)

> 대상 데이터셋: `vla_dataset_v0.4.2`
> 대상 정책(policy): **Pi0.5 (pi05)**
> 작성 기준: LeRobot 로컬 소스 (`vla_ws/lerobot/src/lerobot`)

이 문서는 우리 VLA 파이프라인에서 **정규화(normalization)가 정확히 어디서, 어떻게, 무엇을 기준으로** 일어나는지를 정리한다. "데이터를 미리 정규화해서 저장했나?", "이중 정규화 아닌가?" 같은 질문에 대한 명확한 답을 담는다.

---

## 0. 한 줄 요약

- **저장되는 데이터 파일은 정규화하지 않는다 (원본 그대로 저장).**
- **정규화는 학습/추론 런타임에 `stats.json`을 읽어서 수행한다.**
- `prepare_fin_dataset.py`는 **정규화 스크립트가 아니라**, 정규화에 쓸 **통계(stats.json)를 계산해 추가**하는 스크립트다.
- 통계는 **모델이 정규화 시점에 보는 데이터 표현과 동일한 경로**(`LeRobotDataset` 로딩)를 통과시켜 계산되므로, 항상 학습과 일관된다.

---

## 1. 데이터 3단계 파이프라인

```
raw (rosbag)
  └─ teleop_convert_eef.sh → bag_to_lerobot_eef.py
       ↓  (정규화 안 함, 단위 변환만: mm→m, deg→rad)
mid/vla_dataset_v0.4.2          ← 원본(비정규화) LeRobot 데이터셋
  └─ prepare_fin_dataset.py
       ↓  (복사 + stats.json 계산. 데이터 값은 그대로)
fin/vla_dataset_v0.4.2          ← 원본 데이터 + quantile 통계 포함
  └─ lerobot-train / 추론 서버
       ↓  (런타임에 stats.json으로 정규화)
모델 입력
```

### 각 단계가 데이터를 변형하는가?

| 단계 | 스크립트 | 데이터 값 변형 | 비고 |
|------|----------|----------------|------|
| raw → mid | `bag_to_lerobot_eef.py` | **단위 변환만** (mm→m, deg→rad, gripper ratio→raw) | 정규화 아님 |
| mid → fin | `prepare_fin_dataset.py` | **없음** (`shutil.copytree`로 그대로 복사) | stats.json만 추가 |
| fin → 모델 | 학습/추론 런타임 | **정규화 적용** | `NormalizerProcessorStep` |

> **핵심:** mid도 fin도 **데이터 파일 자체는 비정규화 원본**이다. fin은 mid에 `stats.json`(quantile 포함)만 더한 것이다.

---

## 2. `prepare_fin_dataset.py`는 정규화 코드가 아니다

`src/prepare_fin_dataset.py`가 하는 일은 딱 2가지다.

```python
# (1) 복사 — 데이터 값 변형 없음
shutil.copytree(src, dst)

# (2) Quantile 통계 계산 → stats.json 기록
dataset   = LeRobotDataset(repo_id=REPO_ID, root=dst_path)
new_stats = compute_quantile_stats_for_dataset(dataset)
write_stats(new_stats, dataset.meta.root)
```

| 질문 | 답 |
|------|-----|
| 데이터 값을 정규화해서 저장하는가? | ❌ 아니오 |
| 정규화에 쓸 통계를 계산해 저장하는가? | ✅ 예 (`stats.json`) |

즉 이 스크립트의 산출물은 **"정규화된 데이터"가 아니라 "정규화에 쓸 참조 통계"**다. 실제 정규화는 나중에 런타임의 `NormalizerProcessorStep`이 이 통계를 읽어서 수행한다.

---

## 3. 정규화 모드 (NormalizationMode)

정의: `lerobot/src/lerobot/configs/types.py`
적용 로직: `lerobot/src/lerobot/processor/normalize_processor.py` (`_apply_transform`)

| 모드 | 필요한 통계 | 정규화 식 | 역정규화 식 | 결과 범위 |
|------|-------------|-----------|-------------|-----------|
| `IDENTITY` | (없음) | `x` (그대로) | `x` | 변화 없음 |
| `MEAN_STD` | `mean`, `std` | `(x - mean) / (std + eps)` | `x * std + mean` | 평균0/분산1 |
| `MIN_MAX` | `min`, `max` | `2*(x - min)/(max - min) - 1` | `(x+1)/2*(max-min)+min` | `[-1, 1]` |
| `QUANTILES` | `q01`, `q99` | `2*(x - q01)/(q99 - q01) - 1` | `(x+1)*(q99-q01)/2 + q01` | `[-1, 1]`* |
| `QUANTILE10` | `q10`, `q90` | `2*(x - q10)/(q90 - q10) - 1` | `(x+1)*(q90-q10)/2 + q10` | `[-1, 1]`* |

\* QUANTILES/QUANTILE10은 분위수 바깥의 outlier가 `[-1, 1]` 범위를 벗어날 수 있다. 대신 극단값에 둔감해 더 안정적이다.

> **모드별로 필요한 통계가 다르다.** 그래서 `stats.json`에는 `min/max/mean/std`뿐 아니라 `q01/q10/q50/q90/q99`까지 모두 들어 있어야 한다. `prepare_fin_dataset.py`(정확히는 `augment_dataset_quantile_stats.py`)가 quantile을 추가하는 이유가 이것이다.

---

## 4. Pi0.5 (pi05)의 정규화 매핑

> ⚠️ **중요 — 실제 학습 환경 기준:**
> 실제 학습은 **별도 학습 환경**에서 수행되며, 그곳의 pi05 설정은 다음과 같다.
> 이 문서는 **실제 학습 환경 기준**으로 작성한다.

```python
# 실제 학습 환경의 pi05 normalization_mapping
normalization_mapping: dict[str, NormalizationMode] = field(
    default_factory=lambda: {
        "VISUAL": NormalizationMode.IDENTITY,    # 이미지: stats 미사용
        "STATE":  NormalizationMode.QUANTILES,   # 상태: q01/q99 필요
        "ACTION": NormalizationMode.MIN_MAX,     # 액션: min/max 필요  ← 실제 학습 환경
    }
)
```

### feature 타입별로 어떤 통계가 필요한가

| feature 타입 | 우리 데이터 키 | pi05 모드 | 필요한 통계 | 비고 |
|--------------|----------------|-----------|-------------|------|
| `VISUAL` | `observation.images.camera1/2` | `IDENTITY` | **없음** | stats.json의 이미지 통계는 **사용 안 됨** |
| `STATE` | `observation.state` (7-dim) | `QUANTILES` | `q01`, `q99` | TCP 위치 + gripper |
| `ACTION` | `action` (7-dim) | `MIN_MAX` | `min`, `max` | EEF delta + grip_next |

> ⚠️ **환경 간 차이 — ACTION 모드 (반드시 인지):**
> ACTION 정규화 모드가 환경에 따라 다르므로 주의한다.
>
> | 환경 | ACTION 모드 | 필요 통계 | 정규화 식 |
> |------|-------------|-----------|-----------|
> | **실제 학습 환경 (이 문서 기준)** | **`MIN_MAX`** | `min`, `max` | `2*(x-min)/(max-min) - 1` |
> | 로컬 저장소 pi05 기본값 (`configuration_pi05.py:76`) | `QUANTILES` | `q01`, `q99` | `2*(x-q01)/(q99-q01) - 1` |
>
> - **실제 학습은 `MIN_MAX`를 쓴다.** 따라서 ACTION은 `stats.json`의 `min`/`max`로 정규화된다.
> - 로컬 LeRobot 소스를 그대로 학습에 쓰면 기본값이 `QUANTILES`라 **결과가 달라질 수 있으니** 반드시 학습 환경 config를 확인할 것.
> - 다행히 `stats.json`에는 `min/max`와 `q01/q99`가 **모두** 들어 있어 어느 모드든 통계 누락 없이 동작한다.
>
> **STATE/ACTION이 모드가 다른 이유:** STATE(절대 위치)는 outlier에 강건한 분위수(QUANTILES)가 유리하고, ACTION(델타)은 실제 동작 한계를 `[-1,1]`에 정확히 매핑하는 MIN_MAX가 유리하다는 판단으로 보인다.

---

## 5. 정규화가 "실제로" 일어나는 시점

### 5.1 이미지 (VISUAL) — 2단계 고정 변환 (stats 무관)

이미지는 `IDENTITY`라 `stats.json`을 쓰지 않는다. 대신 **고정된** 2단계 변환을 거친다.

```
저장: uint8 MP4 [0, 255]
  │
  │ ① 데이터 로딩 시 (video_utils.py:190, 330)
  │    closest_frames = frames.type(torch.float32) / 255
  ▼
[0, 1] float32
  │
  │ (NormalizerProcessorStep: VISUAL = IDENTITY → 아무것도 안 함)
  │
  │ ② 모델 입력 직전 (modeling_pi05.py:1182)
  │    img = img * 2.0 - 1.0          # PaliGemma/SigLIP는 [-1,1] 요구
  ▼
[-1, 1]
```

- 근거: `modeling_pi05.py:1140-1141` 주석 — *"Images from LeRobot are typically normalized to [0,1]. PaliGemma expects [-1,1]."*
- 이 `/255`와 `*2-1`은 **dataset 통계와 무관한 고정 식**이다. 따라서 stats.json의 이미지 값이 `[0,255]`든 `[0,1]`든 학습 결과에 영향이 없다.
- **이것은 이중 정규화가 아니다.** 두 단계는 서로 다른 목적의 직렬 변환(`uint8→[0,1]→[-1,1]`)이며, 학습과 추론에서 **동일하게** 적용된다.

### 5.2 상태/액션 (STATE/ACTION) — stats.json 기반 정규화

```
저장: parquet 원본값 (변환 없음)
  │
  │ 로딩 시 parquet은 그대로 (/255 같은 변환 없음 — 영상에만 적용)
  ▼
원본값
  │
  │ NormalizerProcessorStep
  │    state  (QUANTILES): 2*(x - q01)/(q99 - q01) - 1
  │    action (MIN_MAX):   2*(x - min)/(max - min) - 1
  ▼
정규화값  →  모델
```

추론 후에는 `UnnormalizerProcessorStep`이 동일 통계로 **역정규화**해 로봇 명령으로 되돌린다.

---

## 6. 학습 vs 추론: 정규화 횟수

| 데이터 | 학습 시 | 추론 시 |
|--------|---------|---------|
| 이미지 | `/255` + `*2-1` (고정 2단계) | `/255` + `*2-1` (동일) |
| 상태 (STATE) | QUANTILES 정규화 1회 | QUANTILES 1회 + 출력 역정규화 |
| 액션 (ACTION) | MIN_MAX 정규화 1회 | MIN_MAX 1회 + 출력 역정규화 |

> 학습과 추론에서 **동일한 변환 경로**를 사용하므로 train/serve 불일치가 없다. 이것이 "통계를 학습 로딩 경로로 계산해야 하는" 핵심 이유다 (§7).

---

## 7. "통계는 원본 기준으로 내야 하는 것 아닌가?" — 핵심 원칙

> **황금률: 통계는 추상적 '원본'이 아니라, 모델이 정규화하는 그 순간에 보는 데이터 표현을 기준으로 계산해야 한다.**

`prepare_fin_dataset.py`는 통계를 낼 때 **학습과 똑같은 `LeRobotDataset` 로딩 경로**를 통과시킨다. 그래서 자동으로 일관성이 보장된다.

### 상태/액션 — 이미 "원본 기준"이 맞다
- parquet은 로딩 시 **아무 변환도 없다** (`/255`는 영상 전용).
- 따라서 `저장 parquet 원본값 == NormalizerProcessorStep이 보는 값 == stats.json`.
- 검증: 이 데이터셋에서 parquet 실측 범위 = stats.json의 min/max가 일치함.
  - `action` 범위 `[-0.0555, 0.0865]` = stats.json action min/max ✅
  - `state` 범위 `[-1.5655, 1.5729]` = stats.json state min/max ✅

### 이미지 — "원본=[0,255]" 기준은 오히려 틀리다
- 이미지는 로딩 시 `/255`가 적용되어 모델은 항상 `[0,1]`부터 본다.
- 그래서 통계도 `[0,1]` 기준이어야 학습 로딩 범위와 일치한다.
- 만약 통계를 `[0,255]` 원본으로 내면, 학습은 `[0,1]`로 로드하는데 통계만 `[0,255]`라 **불일치(틀림)**가 된다.
- 게다가 pi05는 VISUAL이 `IDENTITY`라 **이미지 통계는 애초에 사용되지 않는다.**

| 통계 기준 | 상태/액션 | 이미지 |
|-----------|-----------|--------|
| 학습 로딩 경로와 동일 (현재 방식) | ✅ 원본 = 로딩값, 일치 | ✅ `[0,1]`, 일치 (단 IDENTITY라 미사용) |
| 추상적 "원본"(`[0,255]`) 강제 | (상태/액션엔 의미 동일) | ❌ 학습 범위와 불일치 |

**결론:** 핵심은 "원본이냐"가 아니라 **"학습이 보는 표현과 같은 경로로 계산했냐"**다. 현재 `prepare_fin_dataset.py`는 동일 `LeRobotDataset`을 통과시키므로 통계가 올바르다.

---

## 8. 우리 데이터셋(`vla_dataset_v0.4.2`) 검증 결과

`meta/stats.json` 및 원본 파일 실측 기준:

| feature | shape | 저장 형식 | stats.json 범위 | 정규화 상태 |
|---------|-------|-----------|-----------------|-------------|
| `observation.images.camera1/2` | (3,480,640) | uint8 MP4 `[0,255]` | min `[0,0,0]`, max `[1,1,1]` (`/255` 후) | 원본 저장, 통계는 `[0,1]` 기준 |
| `observation.state` | (7,) | float parquet | x≈`[0.095,0.313]`m … | 원본(비정규화) |
| `action` | (7,) | float parquet | delta≈`[-0.055,0.087]`, grip≈`[0.81,1.0]` | 원본(비정규화) |
| `task_index` | (1,) | int | min/max/mean = 0 | **단일 태스크** (아래 참고) |

- **task_index가 전부 0**: 이 데이터셋은 태스크가 1개뿐이라는 뜻. 텍스트 인스트럭션은 `meta/tasks.parquet`에 저장됨 → `"Grasp the strawberry stem and pick it."`
- state 7-dim: `[x_m, y_m, z_m, rx_rad, ry_rad, rz_rad, gripper]`
- action 7-dim: `[dx_m, dy_m, dz_m, drx_rad, dry_rad, drz_rad, grip_next]`

**판정:** mid/fin 모두 데이터 값은 **비정규화 원본**이며, 정규화는 학습/추론 런타임에서 stats.json으로 수행된다. 이중 정규화 문제 없음.

---

## 8.1 단위 (Units) — parquet / stats.json

`observation.state`와 `action`은 parquet을 **변환 없이** 통계 내므로 **parquet과 stats.json의 단위가 동일**하다. 이미지만 영상은 `uint8 [0,255]`, stats.json은 `/255` 후 `[0,1]` 무차원이다.

### observation.state (7-dim)

| idx | 이름 | 단위 | 실측 범위 |
|-----|------|------|-----------|
| 0 | `x_m` | 미터 (m) | 0.095 ~ 0.313 |
| 1 | `y_m` | 미터 (m) | 0.279 ~ 0.528 |
| 2 | `z_m` | 미터 (m) | 0.803 ~ 0.930 |
| 3 | `rx_rad` | 라디안 (rad) | 1.569 ~ 1.573 (≈90°) |
| 4 | `ry_rad` | 라디안 (rad) | 1.504 ~ 1.514 |
| 5 | `rz_rad` | 라디안 (rad) | -1.566 ~ -1.563 |
| 6 | `gripper` | ⚠️ 불명확 (≈0.001) | 0.00110 ~ 0.00135 |

### action (7-dim)

| idx | 이름 | 단위 | 실측 범위 |
|-----|------|------|-----------|
| 0 | `dx_m` | 미터/frame (Δm) | -0.0219 ~ 0.0865 |
| 1 | `dy_m` | 미터/frame (Δm) | -0.0555 ~ 0.0277 |
| 2 | `dz_m` | 미터/frame (Δm) | -0.0197 ~ 0.0148 |
| 3 | `drx_rad` | 라디안/frame (Δrad) | -0.00075 ~ 0.00065 |
| 4 | `dry_rad` | 라디안/frame (Δrad) | -0.00194 ~ 0.00178 |
| 5 | `drz_rad` | 라디안/frame (Δrad) | -0.00080 ~ 0.00068 |
| 6 | `grip_next` | 비율 (0~1) | 0.8108 ~ 1.0000 |

### 이미지

| | 단위/형식 |
|---|---|
| 영상 파일 (MP4) | `uint8 [0, 255]` |
| stats.json 이미지 통계 | `/255` 후 `[0, 1]` 무차원 (단, VISUAL=IDENTITY라 미사용) |

> fps = 5 이므로 action의 delta는 **1/5초당 변위**(Δm per frame, Δrad per frame)다.

### ⚠️ 단위 관련 주의 2가지

1. **state `gripper`(≈0.001) vs action `grip_next`(0.81~1.0) 스케일 불일치**
   - 같은 그리퍼인데 단위계가 서로 다르다. state gripper는 값이 너무 작아(≈0.001) 단위가 불명확하다(개폐 폭 m? 센서 비율?). 학습/추론 시 의미 해석에 주의.

2. **변환 코드 주석과 실제 데이터 불일치 (grip_next)**
   - `bag_to_lerobot_eef.py`에는 `grip_next = grips[t+1] * 740.0` (즉 0~740 raw)로 적혀 있으나, **실제 parquet의 `grip_next`는 0.81~1.0 (비율)** 이다.
   - 즉 데이터 생성 시점의 변환 코드가 현재 스크립트와 달랐을 가능성이 크다. 재변환 시 grip_next 스케일이 바뀔 수 있으니 반드시 확인할 것.

---

## 9. 자주 하는 질문 (FAQ)

**Q. `prepare_fin_dataset.py`로 만들었는데 비정규화 데이터일 수 있나?**
A. 그렇다. 이 스크립트는 데이터 값을 바꾸지 않고 통계만 추가한다. 데이터는 비정규화 원본이고, 정규화는 런타임에 일어난다.

**Q. 이미지가 `/255`와 `*2-1`로 두 번 변환되는데 이중 정규화 아닌가?**
A. 아니다. `uint8 → [0,1] → [-1,1]`로 이어지는 단일 직렬 변환이며 stats와 무관한 고정 식이다. 학습/추론에서 동일하게 적용된다.

**Q. 카메라 통계가 `[0,1]`인데 원본 `[0,255]` 통계여야 하지 않나?**
A. 아니다(§7). 학습이 `[0,1]`로 로드하므로 통계도 `[0,1]` 기준이 맞다. 더구나 pi05는 VISUAL=IDENTITY라 이미지 통계 자체를 쓰지 않는다.

**Q. ACTION은 MIN_MAX인가 QUANTILES인가?**
A. **실제 학습 환경은 `MIN_MAX`**를 쓴다 → ACTION은 `min/max`로 정규화된다. 단, 로컬 저장소 pi05 기본값은 `QUANTILES`(`configuration_pi05.py:76`)라 다르므로, 로컬 소스를 그대로 학습에 쓰면 안 되고 학습 환경 config를 따라야 한다. stats.json엔 `min/max`와 `q01/q99`가 모두 있어 어느 쪽이든 통계 누락은 없다.

---

## 10. 관련 코드 위치 (Reference)

| 내용 | 파일:라인 |
|------|-----------|
| 정규화 모드 정의 | `lerobot/src/lerobot/configs/types.py` (`NormalizationMode`) |
| 정규화 적용 로직 | `lerobot/src/lerobot/processor/normalize_processor.py:302-421` (`_apply_transform`) |
| pi05 정규화 매핑 (로컬 기본값 = ACTION:QUANTILES) | `lerobot/src/lerobot/policies/pi05/configuration_pi05.py:72-78` |
| ⚠️ 실제 학습 매핑 (ACTION:MIN_MAX) | **별도 학습 환경** — 로컬과 다름, §4 참고 |
| pi05 이미지 `*2-1` | `lerobot/src/lerobot/policies/pi05/modeling_pi05.py:1182` |
| 영상 `/255` | `lerobot/src/lerobot/datasets/video_utils.py:190, 330` |
| 통계 계산 스크립트 | `src/prepare_fin_dataset.py` + `lerobot/.../scripts/augment_dataset_quantile_stats.py` |
| raw→mid 변환 | `src/bag_to_lerobot_eef.py` |
