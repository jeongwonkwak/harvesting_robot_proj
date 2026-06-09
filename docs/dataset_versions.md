# VLA 데이터셋 버전 정리 (vla_dataset)

> 대상 정책: Pi0.5 (pi05) · 태스크: `"Grasp the strawberry stem and pick it."`
> 정규화 상세는 [`normalization_guide.md`](./normalization_guide.md) 참고.

이 문서는 `vla_dataset` 버전별 차이·특징을 기본 통계와 함께 정리한다.

---

## 0. 버전 계보 (lineage)

```
raw/final_project/vla_dataset_v0.4.0   (rosbag 원본 녹화)
        │  teleop_convert_eef.sh → bag_to_lerobot_eef.py  (단위변환 mm→m, deg→rad)
        ▼
mid/vla_dataset_v0.4.2                  (LeRobot 변환본, 비정규화 원본)
        │  prepare_fin_dataset.py        (복사 + quantile stats 계산)
        ▼
fin/vla_dataset_v0.4.2                  (학습용, quantile stats 포함)  ※ 현재 삭제됨
        │
        │  ── 그리퍼 스케일 버그 발견 → state[6] ×740 수정 ──
        ▼
mid/vla_dataset_v0.4.3                  (mid 4.2 복사 + gripper ×740)
        │  stats.json 강제 재계산
        ▼
fin/vla_dataset_v0.4.3                  (★ 현재 권장 학습 데이터)
```

### 현재 디스크 상태 (2026-06-09 기준)

| 경로 | 존재 | 용량 | 비고 |
|------|------|------|------|
| `raw/final_project/vla_dataset_v0.4.0` | ✅ | — | rosbag 원본 |
| `mid/vla_dataset_v0.4.2` | ✅ | 323M | 비정규화 원본 (보존) |
| `mid/vla_dataset_v0.4.3` | ✅ | 323M | 그리퍼 수정본 |
| `fin/vla_dataset_v0.4.2` | ❌ 삭제됨 | — | 사용자가 삭제 (mid 4.2로 재생성 가능) |
| `fin/vla_dataset_v0.4.3` | ✅ | 323M | **권장 학습 데이터** |

> 버전 번호가 0.4.0(raw) → 0.4.2(mid/fin)로 건너뛴다. 0.4.1은 이 워크스페이스에 없다.

---

## 1. 공통 특징 (전 버전 동일)

| 항목 | 값 |
|------|-----|
| 로봇 | Doosan `dsr01` |
| 에피소드 수 | **32** |
| 총 프레임 | **7,650** |
| fps | **5** |
| 태스크 수 | **1** (단일) — `"Grasp the strawberry stem and pick it."` |
| 카메라 | 2대 (`camera1`, `camera2`), 각 `3×480×640`, uint8 MP4 |
| state | 7-dim `[x_m, y_m, z_m, rx_rad, ry_rad, rz_rad, gripper]` |
| action | 7-dim `[dx_m, dy_m, dz_m, drx_rad, dry_rad, drz_rad, grip_next]` (EEF delta) |
| codebase_version | LeRobot v3.0 |
| 용량 | ~323M (비디오 322M + parquet 0.6M) |

- **action은 절대좌표가 아니라 프레임간 delta** (1/5초당 변위).
- **task_index 전부 0** → 단일 태스크. 텍스트 인스트럭션은 `meta/tasks.parquet`에 저장.

---

## 2. 버전별 차이 요약

| | mid 4.2 | fin 4.2 (삭제) | mid 4.3 | **fin 4.3 (권장)** |
|---|---|---|---|---|
| 데이터 값 | 원본 | 원본 | gripper ×740 수정 | gripper ×740 수정 |
| gripper state 범위 | 0.0011~0.00135 ❌ | 0.0011~0.00135 ❌ | **0.811~1.0** ✅ | **0.811~1.0** ✅ |
| quantile stats(q01..q99) | 없음 (1.7KB) | 있음 (13.8KB) | 없음 (1.7KB) | **있음 (13.8KB)** ✅ |
| 학습 사용 가능 | △(stats 없음) | △(gripper 버그) | △(stats 없음) | **✅ 권장** |

> mid는 항상 quantile 없는 짧은 stats.json(1.7KB), fin은 quantile 포함(13.8KB). 학습엔 fin을 쓴다.

---

## 3. v0.4.3 핵심 변경 — 그리퍼 스케일 버그 수정

### 문제 (v0.4.2)
녹화 시점 `/gripper/position`이 `raw/740²`(≈0.001)로 잘못 publish되어, **state 그리퍼만** 비정상 스케일(≈0.001)이었다. (action `grip_next`는 변환 시 `×740` 덕에 우연히 정상 0~1로 복구됨.)

- 영향: state 그리퍼 정규화(QUANTILES) 분모 `q99-q01 ≈ 0.00026` → 추론 시 그리퍼 입력(0~1)이 정규화 후 **수천 배로 폭발**, train/serve 스케일 불일치.

### 수정 (v0.4.3)
- `observation.state[6] × 740` (그리퍼만). action·다른 6개 차원·비디오는 **불변**.
- `0.00109569 → 0.810811` (raw 600), `0.00135135 → 1.000000` (raw 740).
- stats.json 재계산 → 분모 `0.00026 → 0.189` (폭발 해소, 추론 스케일 일치).

### 그리퍼 동작 패턴 (전 버전 공통, 참고)
- **방향 정의** (`gripper_controller.py:39-42`): `0 = 완전 열림`, `740 = 완전 닫힘`.
  - 600 → ratio **0.811 = 거의 닫힘**(접근 폭), 740 → ratio **1.0 = 완전 닫힘**(꽉 쥠).
- 고유값 **2개뿐**: 600(거의 닫힘, 5002 프레임) / 740(완전 닫힘, 2648 프레임).
- **32개 에피소드 전부** `600→740` **단일 전환 = "줄기를 잡는(완전히 닫는) 순간"**.
  - 시작 600(접근) → 잡는 순간 740(완전 닫힘) → 740 유지하며 들어올림 → 740으로 종료.
  - 에피소드 리셋 시 그리퍼를 HOME=600으로 고정(`teleop_record_and_convert_eef.py:328`)해 모두 600에서 시작.
- **학습 가능**: 언제 완전히 닫을지(잡을지) 타이밍.
- **학습 불가**: 여는/놓는 동작(데이터에 없음), 미세 폭 제어(값 2개뿐 binary), 완전 열림(0)에서의 접근.

---

## 4. 기본 통계 (fin/v0.4.3 기준, 수정 후)

### observation.state (7-dim)

| idx | 이름 | 단위 | min | max | q01 | q99 | 정규화 모드 |
|-----|------|------|-----|-----|-----|-----|-------------|
| 0 | x_m | m | 0.0952 | 0.3132 | 0.1107 | 0.3127 | QUANTILES |
| 1 | y_m | m | 0.2788 | 0.5279 | 0.2789 | 0.5092 | QUANTILES |
| 2 | z_m | m | 0.8030 | 0.9302 | 0.8386 | 0.8947 | QUANTILES |
| 3 | rx_rad | rad | 1.5686 | 1.5729 | 1.5687 | 1.5705 | QUANTILES |
| 4 | ry_rad | rad | 1.5038 | 1.5138 | 1.5050 | 1.5083 | QUANTILES |
| 5 | rz_rad | rad | -1.5655 | -1.5632 | -1.5646 | -1.5638 | QUANTILES |
| 6 | **gripper** | ratio | **0.8108** | **1.0000** | **0.8108** | **1.0000** | QUANTILES |

### action (7-dim)

| idx | 이름 | 단위 | min | max | q01 | q99 | 정규화 모드 |
|-----|------|------|-----|-----|-----|-----|-------------|
| 0 | dx_m | Δm | -0.0219 | 0.0865 | -0.0132 | 0.0177 | MIN_MAX* |
| 1 | dy_m | Δm | -0.0555 | 0.0277 | -0.0156 | 0.0140 | MIN_MAX* |
| 2 | dz_m | Δm | -0.0197 | 0.0148 | -0.0091 | 0.0047 | MIN_MAX* |
| 3 | drx_rad | Δrad | -0.00075 | 0.00065 | -0.00029 | 0.00033 | MIN_MAX* |
| 4 | dry_rad | Δrad | -0.00194 | 0.00178 | -0.00067 | 0.00066 | MIN_MAX* |
| 5 | drz_rad | Δrad | -0.00080 | 0.00068 | -0.00034 | 0.00028 | MIN_MAX* |
| 6 | grip_next | ratio | 0.8108 | 1.0000 | 0.8108 | 1.0000 | MIN_MAX* |

\* **실제 학습 환경 기준 `ACTION=MIN_MAX`** (min/max 사용). 로컬 LeRobot 소스 기본값은 `QUANTILES`이므로 환경별 차이 주의. 자세한 내용은 [`normalization_guide.md`](./normalization_guide.md) §4.

### 이미지 (camera1/2)

| | min | max | mean(≈) | 정규화 모드 |
|---|-----|-----|---------|-------------|
| camera1 | 0.0 | 1.0 | 0.225 | IDENTITY (stats 미사용) |
| camera2 | 0.0 | 1.0 | 0.228 | IDENTITY (stats 미사용) |

> 이미지는 `/255`(로딩) → `*2-1`(pi05) 고정 변환만. stats.json 이미지 통계는 IDENTITY라 학습에 미사용.

---

## 5. 알려진 한계 (v0.4.3에도 남음)

스케일·단위 버그는 v0.4.3에서 모두 해결됐으나, **데이터 커버리지(분산) 한계**는 재수집으로만 해결 가능하다.

| 채널 | 현상 | q99-q01(분모) | 의미 |
|------|------|---------------|------|
| gripper | 값 2개(0.811/1.0)뿐 | 0.189 | "언제 잡을지(완전히 닫을지)" 타이밍만 학습. 여는/놓는·미세 폭 제어 불가 |
| rx_rad | ≈90° 거의 고정 | 0.0019 | 회전 학습 신호 거의 없음 |
| ry_rad | 〃 | 0.0033 | 〃 |
| rz_rad | ≈-90° 거의 고정 | 0.0008 | 〃 (분모 작아 추론 민감) |

- **회전축(rx/ry/rz)은 분모가 매우 작다.** 값은 물리적으로 정상(top-down 자세)이지만, 추론 시 로봇 자세가 학습 범위(±0.1°)를 벗어나면 정규화 값이 크게 튄다. top-down 자세를 유지하는 한 정상 동작한다.
- 새로운 자세/그리퍼 동작을 배우려면 **다양성 있는 재수집**이 필요하다.

---

## 6. 권장 사용

- **학습 데이터: `fin/vla_dataset_v0.4.3`** (그리퍼 수정 + quantile stats 포함).
- `fin/vla_dataset_v0.4.2`는 그리퍼 버그가 있으므로 사용하지 말 것 (현재 삭제됨).
- `mid/*`는 quantile stats가 없어 직접 학습 불가 — 항상 `fin`을 통해 사용.

### 재현 방법 (v0.4.3 생성 절차)
```bash
# 1) mid 4.2 → 4.3 복사
cp -r data/mid/vla_dataset_v0.4.2 data/mid/vla_dataset_v0.4.3
# 2) parquet observation.state[6] *= 740  (그리퍼만; action/타 차원 불변)
#    (1회성 파이썬 스크립트로 적용)
# 3) fin 4.3 생성 + stats.json 강제 재계산
python3 src/prepare_fin_dataset.py \
    --src data/mid/vla_dataset_v0.4.3 \
    --dst data/fin/vla_dataset_v0.4.3
#    ※ 복사본에 기존 quantile이 남아있으면 stats 재계산이 skip되므로,
#      compute_quantile_stats_for_dataset를 강제 호출해 덮어쓸 것.
```

---

## 7. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-06-09 | v0.4.3 | state 그리퍼 ×740 스케일 버그 수정, stats.json 재계산, fin 생성 |
| (이전) | v0.4.2 | raw v0.4.0 → LeRobot 변환, quantile stats 추가 |
