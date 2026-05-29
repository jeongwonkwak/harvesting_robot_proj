# VLA 데이터셋 수집 전략

## 배경

규칙 기반(rule-based) 방식으로 딸기 수확을 1차 시도하고,
실패한 경우(잎 폐색, 미성숙 딸기 폐색 등) VLA가 개입하는 구조.

따라서 VLA는 **규칙 기반이 실패하는 어려운 케이스**에 특화되어야 함.

---

## 참고: HarvestFlex 논문 (arXiv 2603.05982) 비교

| | 논문 (HarvestFlex) | 내 데이터 (현재) |
|---|---|---|
| 모델 | pi_0.5 | pi05 |
| 에피소드 수 | 227개 | 20개 |
| fps | 30fps | 5fps |
| 프레임/에피소드 | ~1,764 | ~220 |
| 총 프레임 | ~400,000 | 4,409 |
| 카메라 수 | 3개 (좌/우/손목) | 1개 |
| fine-tune | full + LoRA 비교 | LoRA r=16 |
| 성공률 | **74.0%** (50회 평가) | - |
| 수확 속도 | 32.6초/pick | - |
| 손상률 | 4.1% | - |

---

## 데이터 카테고리 설계

### 필수 카테고리

| 카테고리 | 태그 | 설명 | 목표 에피소드 수 |
|---|---|---|---|
| 기본 (폐색 없음) | `baseline` | 딸기가 명확히 보이는 기본 수확 | 10~15개 |
| 잎 부분 폐색 | `partial_leaf_occlusion` | 잎이 딸기를 30~60% 가림 | 20~30개 |
| 잎 완전 폐색 | `full_leaf_occlusion` | 딸기가 거의 안 보임, 잎 밀어내며 접근 | 20~30개 |
| 미성숙 딸기 폐색 | `unripe_occlusion` | 초록 딸기 뒤에 빨간 딸기 | 15~20개 |
| 딸기 밀집/겹침 | `dense_cluster` | 여러 딸기가 붙어있어 타겟 선택 어려움 | 15~20개 |
| 회복 동작 | `recovery` | 첫 시도 실패 후 재잡기 (실패+재시도 포함) | 10~15개 |

### 보조 카테고리

| 카테고리 | 설명 |
|---|---|
| 역광/저조도 | 조명 조건 변화 |
| 가지 간섭 | 줄기/가지가 접근 경로 방해 |

### 목표 총량

| 카테고리 | 목표 에피소드 수 |
|---|---|
| 기본 (폐색 없음) | 10~15개 |
| 잎 부분 폐색 | 20~30개 |
| 잎 완전 폐색 | 20~30개 |
| 미성숙 딸기 폐색 | 15~20개 |
| 밀집/겹침 | 15~20개 |
| 회복 동작 | 10~15개 |
| **합계** | **90~130개** |

논문(227개)의 절반 수준이지만, VLA가 실패 케이스만 담당하는 좁은 도메인이므로 유의미한 학습 가능.

---

## 커리큘럼 러닝 필요한가?

**지금 당장은 불필요.**

- 데이터가 부족한 상태에서 단계 나누면 카테고리별 샘플 수가 너무 적어짐
- pi05는 대규모 사전학습 모델 → 기본 pick 동작은 이미 내재화됨
- VLA가 실패 케이스만 담당하므로 baseline(폐색 없음) 데이터 비중 낮아도 됨

**커리큘럼이 의미 있는 시점:**
- 카테고리별 30 에피소드 이상 확보 후
- 쉬운 폐색(부분) → 어려운 폐색(완전) 순서로 fine-tune 단계 구성

---

## 수집 시 체크리스트

- [ ] `--category` 인자로 카테고리 명시하여 수집
  ```bash
  python3 src/teleop_record_and_convert_eef.py --category baseline
  python3 src/teleop_record_and_convert_eef.py --category partial_leaf_occlusion
  python3 src/teleop_record_and_convert_eef.py --category full_leaf_occlusion
  python3 src/teleop_record_and_convert_eef.py --category unripe_occlusion
  python3 src/teleop_record_and_convert_eef.py --category dense_cluster
  python3 src/teleop_record_and_convert_eef.py --category recovery
  ```
- [ ] 실패 후 재시도 과정도 에피소드에 포함 (논문: 1.5 average retries/pick)
- [ ] 조명 조건(역광/저조도) 다양하게 수집
- [ ] 평가 프로토콜 사전 정의 (예: 카테고리별 50회 시험)
