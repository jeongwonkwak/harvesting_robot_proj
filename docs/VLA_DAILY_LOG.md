# VLA 개발 데일리 로그

**모델**: pi05 | **로봇**: Doosan | **태스크**: Occlusion 딸기 줄기 파지  
**이전 이슈 요약**: `VLA_DAILY_ISSUES_SUMMARY.md`

---

# 2026-06-19

## vla_dataset_v0.4.4 보간 분석 및 v0.4.5 생성

### 발견: v0.4.4는 nearest 동기화로 생성된 비보간 데이터

`meta/tasks.parquet` 확인 결과 인스트럭션은 단 1개:
```
Grasp the strawberry stem and pick it.
```

`teleop_convert_eef.sh` 16번 줄 주석에서 버전별 동기화 방식 확인:
- v0.4.4 / v0.5.0: **nearest** 동기화 → 동일 raw 샘플이 연속 2회 이상 선택되는 중복 프레임 발생
- v0.6.0: **선형 보간** (`bag_to_lerobot_eef.py` 발견 #8 해결)

실측: v0.4.4에서 완전히 동일한 연속 프레임 쌍 **472 / 7618 (6.2%)**

### v0.4.5 생성: 후처리 선형 보간

raw bag이 없으므로 parquet에 직접 후처리 적용 (`src/make_v045_interp.py`):
- 완전히 동일한 연속 프레임을 앞뒤 keyframe 사이 선형 보간값으로 대체
- action(delta)을 보간된 state 기반으로 재계산
- videos/ 는 심볼릭 링크 (321 MB 절약)
- 결과: 중복 프레임 6.2% → **0.09%** (7쌍 잔존 — 에피소드 마지막 프레임 직전)

### 발견: 보간이 근본적으로 효과 없는 이유 (버튼식 텔레오퍼레이션 구조)

v0.4.5 데이터를 분석한 결과, 선형 보간으로도 학습 품질이 개선되지 않는 구조적 원인 확인.

**데이터 특성 (ep0 기준)**

| 항목 | 값 |
|------|-----|
| 정지 프레임 비율 | **50.2%** (zero-action) |
| 이동 burst 수 | 24회 |
| burst당 총 이동량 | ~20mm (버튼 1회) 또는 ~40mm (2회) |
| 이동 방향 | 거의 완전한 축 정렬 (`[-1,0,0]`, `[0,1,0]`, `[0,0,-1]`) |

**시퀀스 패턴**
```
STILL(10) → MOVE(3) → STILL(2) → MOVE(5) → STILL(2) → MOVE(3) → ...
```

**보간이 효과 없는 이유**

1. **이중 분포 (bimodal action)**: action이 0mm(정지) 또는 ~6mm(이동) 중 하나. 중간값이 거의 없어 VLA 모델이 평균값으로 수렴하려는 경향.
2. **불연속 전환**: 정지→이동이 계단식. 선형 보간은 앞뒤 state만 수정하며 이 구조 자체는 건드리지 못함.
3. **보간 대상 오류**: nearest 중복(6.2%)은 이미 이동 중인 burst 내에서 발생 — 해결해도 전체 구조(50% 정지)는 그대로.
4. **이산 이벤트 특성**: 버튼식 제어는 20mm 고정 스텝의 이산 이벤트 기반. 상태공간 보간으로 연속 궤적을 만들 수 없음.

**향후 검토 방향**
- 정지 프레임 제거/다운샘플 (zero-action 비율 줄이기)
- action chunking으로 버튼 1회 = 단일 액션으로 묶기
- 학습 시 zero-action 프레임 가중치 감소

---

## 버튼식 텔레오퍼레이션의 한계

### 구조적 문제

| 문제 | 내용 |
|------|------|
| zero-action 과다 | 전체 프레임의 50%가 action=0 (버튼 미입력 대기) |
| 이산 이벤트 | 20mm 고정 스텝 단위로만 이동 — 연속적인 속도 프로파일 없음 |
| 깔짝 미세조정 | 위치 보정 시 20~50mm 소규모 비축방향 burst 발생. 에피소드마다 방향·위치가 달라 모델에겐 노이즈 |

### 깔짝 구간이 학습 불가한 이유

같은 시각적 상태에서 에피소드마다 다른 액션이 나오는 inconsistency가 핵심.
오퍼레이터가 느낀 "살짝 틀렸다"는 감각은 카메라 이미지에 거의 반영되지 않기 때문에
모델은 이 액션을 예측할 근거가 없다.

### 보간으로 해결 가능한 것 / 불가능한 것

- 해결됨: nearest 아티팩트 중복 프레임 (v0.4.5, 6.2% → 0.09%)
- 부분 해결: 같은 방향 연속 버튼 사이 STILL 보간 (v0.4.6, zero-action 50% → 48%)
- 해결 불가: 깔짝 미세조정 구간의 에피소드 간 inconsistency — 보간이 아닌 수집 방식 개선 필요

---

# 2026-06-18

## vla_dataset_v0.7.0 Instruction 확정

```
Grasp the leftmost ripe strawberry stem.
```

### 결정 배경

군집 내 익은 딸기와 미숙 딸기가 혼재하는 환경에서 모델이 어떤 딸기를 타겟으로 삼을지 결정할 수 없다는 문제에서 출발.

- **에피소드당 타겟 하나**: 한 에피소드에서 딸기를 모두 따는 구조는 순서 결정 ambiguity 및 시퀀스 복잡도가 높아 imitation learning에 부적합
- **공간 기준 명시**: "leftmost"를 instruction에 포함해 시연자 선택 기준을 명문화 → 같은 장면에서 항상 동일한 타겟 선택 보장
- **색 기준 명시**: "ripe"로 익은 것(빨간색)만 타겟으로 지정 → 미숙 딸기는 negative example로 자연스럽게 활용
- **번역**: 줄기 = stem (peduncle보다 모델 언어 분포에 적합)

### 수집 시 준수 사항

- 시연자는 반드시 **카메라 화면 기준 가장 왼쪽에 있는 익은 딸기**를 타겟으로 선택
- 카메라 마운트 위치 고정 (image 기준 좌우 방향 일관성 유지)
- 에피소드 종료: 해당 딸기 파지 + 1~2초 정지 후 종료

---

## 베이스 모델(pi0.5-base) 추론 파이프라인 분석

### serve_pi05.py 처리 흐름 파악

`http://192.168.50.79:19003/predict` 서버(`serve_pi05.py`)의 전체 파이프라인:

```
[1] state[:N_STATE_REAL] → QUANTILES 정규화 → 256-bin 이산화 → 텍스트 프롬프트
[2] 모델 추론 → normalized action [-1, 1]
[3] raw_action = action.copy()   ← 역정규화 전 저장 (디버그용)
[4] inverse QUANTILES → 원본 단위(m/rad)로 역정규화  (stats 있을 때)
[5] CONVERT_ABS_TO_DELTA=true 시: action[:6] -= req.state[:6]
```

- `raw_action`: 역정규화 전 모델 직출력 (normalized, 디버그용)
- `action`: 역정규화 + delta 변환 완료된 값 (실제 사용)

### 베이스 모델 stats 부재 확인

`pi05_base` 체크포인트에는 `policy_preprocessor_step_2_normalizer_processor.safetensors`가 없음. `model.safetensors` 내부에도 q01/q99 키 없음.

- 베이스 모델은 stats 없이 배포됨 (Physical Intelligence 내부 학습 stats 미공개)
- `policy_preprocessor.json`에 `STATE: QUANTILES, ACTION: QUANTILES`로 명시되어 있으나 실제 수치 미포함
- fine-tuning 시 사용자 데이터셋 stats가 체크포인트에 포함되는 구조

**현재 상태**: `STATS_PATH=/models/stats-model`이 베이스 모델과 동일 경로를 가리키므로 stats 로드 실패 → 역정규화 identity → `action == raw_action`

### CONVERT_ABS_TO_DELTA 활성화

`docker-compose.yml` 기본값 `false` → `true` 변경 후 `--force-recreate`로 재시작.

- 활성화 후: `action[:6] = raw_normalized[:6] - state[:6]`
- 단, stats 미로드 상태이므로 단위 불일치 (normalized값 - m) → 의미 있는 delta 아님

### 베이스 모델 좌표계 불일치 확인

에피소드 0에서 10프레임 샘플 추론 결과:

| | dx | dy | dz |
|--|--|--|--|
| 모델 delta (mm) | -267 ± 69 | -140 ± 85 | -233 ± 18 |
| GT delta (mm) | 2.5 ± 7.5 | -0.9 ± 8.1 | 0.5 ± 2.0 |

- 우리 로봇 state: x≈0.184m, y≈0.377m, z≈0.866m
- 모델 raw output: x≈-0.083, y≈+0.238, z≈+0.633 (다른 좌표계)
- raw_action std가 0이 아님 → 모델이 입력에 완전히 무반응하지는 않음
- dx가 에피소드 진행에 따라 단조 감소 (-0.005 → -0.130) → 시퀀스 인식은 하나 자기 좌표계 기준

### 결론

베이스 모델로는 의미 있는 delta 출력 검증 불가:
1. stats 미공개 → 역정규화 불가
2. 우리 dataset stats를 억지로 적용해도 좌표계가 달라 수치 무의미
3. fine-tuned 모델 준비 후 동일 파이프라인으로 검증 필요

---

# 📅 2026-06-16

## 수정 — 단계별 웨이포인트 명칭 및 의미 정의 (harvest_dashboard.py)

수확 동작을 7단계로 세분화. 각 단계의 의미는 아래와 같다.

| 단계 | 의미 |
|------|------|
| `APPROACH` | 딸기 위치로 초기 접근 |
| `SEARCH` | 파지점(줄기) 탐색 |
| `REPOSITION` | 탐색한 파지점에 다가가기 위한 위치 재조정 |
| `ALIGN` | 줄기를 정확히 집을 수 있도록 그리퍼 방향·위치 정렬 |
| `GRASP` | 줄기 파지 (그리퍼 닫기) |
| `PULL_DOWN` | 아래로 당겨 수확 |
| `HOME` | 홈 포즈 복귀 |

```
APPROACH → SEARCH → REPOSITION → ALIGN → GRASP → PULL_DOWN → HOME
```

- localStorage 키 `sw_stages_v3` → `sw_stages_v4` → `sw_stages_v5` 순차 마이그레이션 적용
- 기존 저장 데이터는 자동 이름 변환 후 v5로 재저장

## 수정 — Action Chunking + Doosan Spline Blending (harvest_dashboard.py)

VLA 추론 결과로 로봇이 덜컹거리며 이동하는 문제를 해결하기 위해 두 가지 기법을 동시 적용.

### Action Chunking (추론-실행 분리)

| 항목 | 이전 | 이후 |
|------|------|------|
| `VLA_CHUNK_SIZE` | 50 | 10 |
| `reset_episode=True` 처리 | VLA 1회 호출 → `/move` 1개 delta 전송 | VLA 10회 호출 → 누적 waypoint 10개 생성 → `/spline` 일괄 전송 |
| `reset_episode=False` 처리 | VLA 1회 호출 → `/move` | 즉시 `{"ok":true,"queued":true}` 반환 (spline 실행 중) |

JS 루프(200ms)에서 매 10번 중 첫 번째 호출에서만 추론·전송. 나머지 9번은 즉시 반환하여 스플라인 실행 시간을 확보.

### Doosan Spline Blending (실행 측 보간)

- `/spline` 엔드포인트 → `move_spline_task(waypoints, velocity=50.0)` 호출
- Doosan 컨트롤러가 waypoints 사이를 스플라인으로 보간하며 이동 → 꺾이는 구간 없이 부드러운 궤적
- 0.5mm 미만 이동 waypoint는 중복으로 제거하여 전송

### 두 기법의 역할 구분

| 기법 | 위치 | 효과 |
|------|------|------|
| Action Chunking | 추론-실행 사이 | 추론 횟수를 줄이고 연속 동작 흐름 확보 |
| Spline Blending | 실행 측 (Doosan 컨트롤러) | waypoint 간 스플라인 보간으로 부드러운 궤적 |

---

## 수정 — YOLO 딸기 인식 모델 교체 (ros2_bridge.py, docker-compose.yml)

기존 단일 detection 모델 → seg + pose 듀얼 모델로 교체.

| 항목 | 이전 | 이후 |
|------|------|------|
| 모델 | `strawberry_yolo26m_unified/weights/last.pt` (단일) | `share_yolo/strawberry_seg_best.pt` + `share_yolo/strawberry_pose_best.pt` |
| 출력 | 바운딩 박스만 | 세그 마스크 + 줄기 키포인트 + 수확 후보 표시 |
| conf 임계값 | 0.3 | 0.15 (unripe 감지 누락 이슈로 완화) |

시각화:
- **세그**: ripe(빨강) / unripe(초록) / sick(노랑) 반투명 마스크 + 바운딩 박스
- **포즈**: 줄기 3키포인트 (stem_base 주황 → stem_mid 빨강 → stem_tip 초록)
- **수확 후보**: 포즈 박스 중심이 ripe 마스크 안에 있을 때 `HARVEST` 레이블 + 노란 박스

---

# 📅 2026-06-15

## Instruction 확정

```
Find the path to the strawberry stem and grasp it.
```

- "scan left to right" 같은 구현 수단은 제외 — 모델이 경로 전략을 스스로 학습하도록
- 줄기가 보이면 바로 접근, 가려지면 탐색 후 접근 — 두 경우 모두 포함
- 학습·추론 instruction 반드시 동일하게 유지 (발견 #13 교훈)

적용:
```json
// meta/info.json
{ "tasks": ["Find the path to the strawberry stem and grasp it."] }
```

## 수정 — VLA 추론 실행 주기 (harvest_dashboard.py:2392)

```js
// 수정 전
const VLA_LOOP_INTERVAL_MS = 1000;
// 수정 후
const VLA_LOOP_INTERVAL_MS = 200;  // 학습 데이터 수집 주파수(5Hz)와 일치
```

학습은 5Hz(200ms 간격)로 수집됐는데 추론은 1Hz로 실행 → 로봇이 1/5 속도로 동작하던 문제.  
Docker 재시작 후 반영 필요.

> **확인 필요**: `move_delta`가 명령을 즉시 실행하는지, 시간 보간으로 실행하는지에 따라 실제 속도 체감이 다를 수 있음. 실로봇에서 확인.

## 다음 작업

- [ ] 대시보드 키보드 버그 수정
- [ ] Occlusion 수집 환경 세팅
- [ ] 수집 시작 (목표 50~100 에피소드)

수집 시 필수:
- 파지(그리퍼 닫기) + 정지 1~2초 포함 (발견 #9)
- grip 스케일 ratio 확인, 보간 변환 스크립트 적용 확인 (발견 #8)
- 딸기 위치 에피소드마다 다양화 (발견 #11)

---

## Occlusion 데이터셋 수집 전략

### 핵심 목표
단순 Pick-and-Place가 아닌 **"탐색 → 판단 → 접근 → 파지"** 전체를 학습.  
모델이 "왜 왼쪽으로 갔는지"를 이미지에서 추론할 수 있어야 함.

### Trajectory 구조

```
SEARCH  →  ALIGN  →  APPROACH  →  GRASP
(줄기 탐색)  (줄기 정렬)  (접근)      (파지+정지)
```

### Instruction 전략 — 두 버전 병행 수집 권장

| 버전 | Instruction | 특징 |
|------|-------------|------|
| A. 단일 | `Find the path to the strawberry stem and grasp it.` | 구현 단순, pi05 표준 |
| B. 단계별 | `Find the grasp point.` / `Align with the stem.` / `Approach the stem.` / `Grasp the strawberry.` | 모델이 현재 단계 명시적 인식 |

같은 trajectory를 A/B 두 형식으로 저장 → occlusion 상황 일반화 비교 실험 가능.

### 수집 필수 조건

- **줄기 안 보이는 상태로 시작** 에피소드를 전체의 50% 이상 확보 ← 핵심
- 시작 각도 다양화: 정면 / 좌20° / 좌40° / 우20° / 위아래
- `stem invisible → move left/right` 탐색 행동 데이터 충분히 포함
- 에피소드 종료: 파지 + 정지 1~2초 필수 (발견 #13)
- 실패 데이터 선택 포함: `miss → retry`, `leaf blocking → move` 등

### 메타데이터 저장 권장

```json
{
  "stem_visible_at_start": false,
  "occlusion_level": "high",
  "stage_transitions": [
    {"frame": 0,  "stage": "SEARCH"},
    {"frame": 18, "stage": "ALIGN"},
    {"frame": 28, "stage": "APPROACH"},
    {"frame": 38, "stage": "GRASP"}
  ]
}
```

### 목표 수량

| 항목 | 목표 |
|------|------|
| 전체 에피소드 | 80~120개 |
| 줄기 비가시 시작 | 50% 이상 |
| 시작 각도 종류 | 6방향 이상 |

---
