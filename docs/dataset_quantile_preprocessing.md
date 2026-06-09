# 학습 데이터셋 Quantile Stats 전처리 과정

## 개요

LeRobot PI05는 action/state 정규화에 **quantile 통계**를 사용한다.  
`mid/` 단계에서 수집된 raw 데이터셋을 `fin/`으로 복사하고, quantile stats를 `stats.json`에 추가하는 것이 전처리의 핵심이다.

---

## 전체 흐름

```
data/vla/mid/vla_dataset_vX.X.X/   →   data/vla/fin/vla_dataset_vX.X.X/
        (raw 수집 데이터)                    (학습용, quantile stats 포함)
```

**실행 스크립트**: `src/prepare_fin_dataset.py`

```bash
# 호스트에서 실행
python3 src/prepare_fin_dataset.py

# 경로 직접 지정
python3 src/prepare_fin_dataset.py \
    --src ../data/vla/mid/vla_dataset_v0.4.0 \
    --dst ../data/vla/fin/vla_dataset_v0.4.0
```

---

## Step 1: 데이터셋 복사

`mid/` → `fin/`으로 디렉토리를 통째로 복사한다.  
`fin/`이 이미 존재하면 건너뜀.

```
fin/vla_dataset_vX.X.X/
├── data/chunk-000/file-000.parquet   # state, action, index 등
├── videos/                           # camera1, camera2 MP4
└── meta/
    ├── info.json
    ├── episodes/
    ├── tasks.parquet
    └── stats.json                    ← 이 파일에 quantile stats 추가
```

---

## Step 2: Quantile Stats 계산

`lerobot.scripts.augment_dataset_quantile_stats`를 사용한다.

### 실행 위치에 따른 분기

| 환경 | 동작 |
|------|------|
| 호스트 (docker 있음) | `docker exec vla-train python -c ...` 로 컨테이너에 위임 |
| 컨테이너 내부 (docker 없음) | Python 코드 직접 실행 |

### 계산 순서

1. `LeRobotDataset` 로드 (repo_id + root 경로)
2. `has_quantile_stats()` 로 이미 존재하는지 확인 → 있으면 skip
3. 에피소드별 통계 수집:
   - 비디오 있음 → **순차 처리** (thread-safe 문제로 병렬 불가)
   - 비디오 없음 → **병렬 처리** (ThreadPoolExecutor, max 16 workers)
4. 에피소드별 stats → `aggregate_stats()` 로 전체 합산
5. `write_stats()` 로 `meta/stats.json` 업데이트

### 계산되는 통계량

feature별 (action, observation.state, 이미지 등)로 아래 값들이 저장된다:

| 키 | 설명 |
|----|------|
| `min` / `max` | 최솟값 / 최댓값 |
| `mean` / `std` | 평균 / 표준편차 |
| `q01` | 1% 분위수 |
| `q10` | 10% 분위수 |
| `q50` | 50% 분위수 (중앙값) |
| `q90` | 90% 분위수 |
| `q99` | 99% 분위수 |

`DEFAULT_QUANTILES = [0.01, 0.10, 0.50, 0.90, 0.99]`

### feature 타입별 axis 처리

| dtype | axis | 의미 |
|-------|------|------|
| `video` / `image` | `(0, 2, 3)` | 채널별 통계 (batch, **C**, H, W) |
| `float32` 벡터 | `0` | 차원별 통계 (samples, **features**) |

---

## 정규화에서의 활용

학습 시 PI05 preprocessor는 `stats.json`의 quantile 값으로 action/state를 정규화한다.  
구체적으로 `q01` ~ `q99` 범위를 기준으로 클리핑 + 스케일링하여 outlier에 강건한 정규화를 수행한다.

---

## 버전별 경로 정리

| 버전 | mid (raw) | fin (학습용) |
|------|-----------|-------------|
| v0.4.0 | `data/vla/mid/vla_dataset_v0.4.0` | `data/vla/fin/vla_dataset_v0.4.0` |
| v0.2.0 | `data/vla/mid/vla_dataset_v0.2.0` | `data/vla/fin/vla_dataset_v0.2.0` |

> `src/prepare_fin_dataset.py` 상단의 `DEFAULT_SRC` / `DEFAULT_DST` / `REPO_ID` 를 수정해서 버전 변경 가능.
