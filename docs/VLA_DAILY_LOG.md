# VLA 개발 데일리 로그

**모델**: pi05 | **로봇**: Doosan | **태스크**: Occlusion 딸기 줄기 파지  
**이전 이슈 요약**: `VLA_DAILY_ISSUES_SUMMARY.md`

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
