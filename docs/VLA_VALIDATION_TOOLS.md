# VLA 검증 도구 — 데이터 품질 검토 앱 & 추론 테스트 앱

> **관련 문서**: `VLA_ISSUES_SUMMARY.md` (이슈 정리표), `VLA_DAILY_ISSUES.md` (상세 기록)
> **마지막 업데이트**: 2026-06-10

LeRobot 데이터셋은 **parquet(수치) + MP4(영상) + stats.json(통계)** 형식이라 텍스트 에디터나 일반 뷰어로는 내용을 확인할 수 없다. 이슈 추적 과정에서 데이터를 직접 눈으로 확인하고, 추론 서버 출력을 학습 데이터와 비교하기 위해 두 개의 Streamlit 앱을 직접 만들어 사용했다.

| 앱 | 파일 | 용도 |
| --- | --- | --- |
| VLA Viewer (데이터 품질 검토) | `src/visualize_simple.py` | parquet/MP4/stats.json을 프레임 단위로 열람하고 데이터셋 통계를 시각화 |
| VLA 추론 테스트 | `src/vla_inference_mock_test.py` | 추론 서버(`serve_pi05.py`)에 데이터셋 프레임을 보내 모델 출력을 정답과 비교 |

---

## 1. VLA Viewer — 데이터 품질 검토용 앱 (`visualize_simple.py`)

### 만든 이유

- 학습 데이터(`vla_dataset_v0.4.3`)가 parquet 형식이라 값 분포·이상치를 쉽게 볼 수 없음
- "그리퍼가 0.001로 고정", "action이 뾰족뾰족함" 같은 현상을 **수치 표와 그래프로 직접 확인**할 필요
- stats.json(학습 정규화에 쓰이는 통계)을 사람이 읽을 수 있는 형태로 보여줄 도구 필요

실행: `streamlit run src/visualize_simple.py` (데이터: `mid/vla_dataset_v0.4.3`, 통계: `fin/vla_dataset_v0.4.3/meta/stats.json`)

### 주요 기능

| 기능 | 내용 |
| --- | --- |
| 에피소드/프레임 탐색 | 에피소드 선택 드롭다운 + 프레임 슬라이더 + 이전/다음 버튼으로 임의 프레임 이동 |
| 에피소드 통계 | 총 에피소드 수, 총 프레임 수, 에피소드당 평균 프레임, 총/평균 길이(초) 메트릭 + 에피소드별 프레임 수 바 차트 (현재 에피소드·평균선 표시) |
| 카메라 프레임 뷰 | MP4에서 현재 프레임을 디코드해 카메라 1/2 동시 표시 → 영상-parquet 프레임 동기화를 눈으로 확인 |
| 현재 프레임 데이터 표 | TCP Pose(6축), Joint State(6축), Action(7차원)의 현재 프레임 값을 표로 표시 |
| 타임라인 그래프 | 에피소드 전체의 TCP Pose / Action(EEF) / Gripper / Joint Angles 시계열 그래프 |
| Dataset Statistics | stats.json의 Mean/Std/Min/Max를 모달리티별 표로 표시 — TCP Pose(6축), Gripper(ratio+% 병기), Joint(rad+deg 병기), Action(위치는 mm, 회전은 rad/deg 병기) |
| Quantiles | state 6축·action 7차원의 Q1/Q10/Q50/Q90/Q99 표 + 바 차트 → QUANTILES 정규화 분모(q99−q01) 크기를 직접 확인 가능 |
| 역기구학 유틸 | e0509 DH 파라미터 기반 수치 역기구학(TCP→Joint) — Joint 데이터 정합성 검증 보조 |

(스크린샷: 에피소드 통계 + 프레임 뷰)

(스크린샷: Dataset Statistics / Quantiles)

### 이 앱으로 확인한 통계와 발견 (이슈 연결)

| 확인한 통계/그래프 | 발견 내용 | 연결 이슈 (`VLA_ISSUES_SUMMARY.md` 기준) |
| --- | --- | --- |
| Gripper State 통계 (Min/Max/Std) | state 그리퍼가 0.001 고정 (Min≈Max≈0.001, action 0.81~1.0과 불일치) | #1 → #4 (raw/740² 스케일 버그) |
| Joint State 통계 (Std) | 6축 전부 Std=0 (고정값) → 토픽 수집 오류 | #2 |
| TCP/Action 타임라인 | 에피소드 내 -X 방향 이동 경향 확인 (추론 +X와 반대) | #3 |
| Gripper Quantiles | q99−q01 ≈ 0.00026 → QUANTILES 정규화 분모 폭발의 직접 증거. v0.4.3 보정 후 0.189로 정상화 확인 | #4 |
| Action 통계 (Min/Max) | ΔX 범위 -21.85~+86.52mm 비대칭 → 정규화 0의 물리값이 +33mm가 되는 원인 | #7, #10 |
| Action(EEF) 타임라인 | 0↔20mm를 오가는 뾰족한 계단 패턴, 정지(near-zero) 프레임이 약 75% | #10 (버튼 스텝 한계) |
| 카메라 프레임 ↔ parquet 대조 | 영상-수치 동기화 정상 (프레임 수 일치) 확인 | #9 (검증) |

---

## 2. VLA 추론 테스트 앱 (`vla_inference_mock_test.py`)

### 만든 이유

- 실로봇을 연결하지 않고도 **추론 서버 출력이 학습 데이터(정답)와 맞는지** 확인할 도구 필요
- 처음에는 목업(mock) 추론으로 클라이언트 파이프라인을 검증했고, 이후 실제 API(`serve_pi05.py /predict`) 호출로 확장
- 데이터셋의 실제 프레임(이미지+state)을 그대로 서버에 보내므로, "학습 때 본 입력 → 어떤 출력이 나와야 하는지"를 프레임 단위로 비교 가능

실행: `streamlit run src/vla_inference_mock_test.py`

### 주요 기능

| 기능 | 내용 |
| --- | --- |
| 에피소드/프레임 선택 | 에피소드 number_input(0~31) + 프레임 슬라이더. 에피소드 변경 시 슬라이더 자동 리셋 |
| 액션 타임라인 차트 | 에피소드 전체 ΔX/ΔY/ΔZ/Grip 시계열(plotly), 현재 프레임 세로선, 파지 시점 마커, 차트 데이터 포인트 클릭으로 해당 프레임 이동 |
| 카메라 프리뷰 | 카메라 1(base) / 카메라 2(left_wrist) 현재 프레임 표시 (해상도 병기) |
| 현재 로봇 상태 | TCP 위치(mm)/회전(deg), 그리퍼 raw(0~740)+ratio, 파지 전/시점/후 단계 표시 |
| 추론 실행 | 현재 프레임의 이미지+state를 서버로 전송 → 응답 레이턴시, 에피소드 리셋 여부 표시 |
| 모델 출력 vs 정답 비교 | 모델이 출력한 action(7차원)과 데이터셋의 GT action을 나란히 비교 |
| raw_action 표시 | **역정규화 전 정규화 공간 값 [-1,1]**을 별도 행으로 표시 → 모델이 "0 근처 무난한 값"을 내는지 직접 관찰 가능 |
| 계산된 목표 포즈 | 현재 TCP에 모델 delta를 적용한 목표 포즈 계산 결과 표시 |
| 전체 벡터 표 | 전송한 state 벡터, 수신한 action/raw_action 전체 차원을 표로 확인 |

(스크린샷: 액션 타임라인 + 추론 결과 비교)

### 이 앱으로 확인한 것 (이슈 연결)

| 확인 내용 | 발견/검증 | 연결 이슈 |
| --- | --- | --- |
| 모델 출력 범위 | 출력이 [-1,1] 그대로 반환됨 → 역정규화 누락의 직접 증거 | #7 |
| X축 방향 | 학습 -X 구간에서 모델이 +X 예측하는 현상 재현 | #3 |
| 수정 후 회귀 확인 | 정규화(#5)/역정규화(#7)/레터박스(#8) 서버 수정 후 출력 변화를 같은 프레임으로 전후 비교 | #5, #7, #8 |
| raw_action 관찰 | raw_action ≈ 0.014 (노이즈 평균 근처) → 역정규화 후 +33mm가 되는 메커니즘 실측 확인 | #10 |
| 파이프라인 동작 검증 | 데이터셋 프레임 입력 시 전체 추론 경로(인코딩→서버→응답) 정상 동작 확인 | #9 |

---

## 보조 도구

| 도구 | 파일 | 용도 |
| --- | --- | --- |
| Bag Monitor | `src/bag_monitor.py` | 수집 중인 ROS 2 bag의 토픽 값(Joint/TCP/Gripper/카메라)을 실시간 그래프로 모니터링 — 수집 단계에서 토픽 이상(고정값 등)을 조기 발견하는 용도 |
| 통합 대시보드 | `src/integrated_dashboard.py`, `src/monitoring.py` | harvest_dashboard(제어) + bag_monitor(모니터링)를 한 화면에서 실행/열람 |
