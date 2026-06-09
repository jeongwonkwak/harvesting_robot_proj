# VLA 데이터 검증 - 일일 이슈 리스트

**작성일**: 2026-06-08  
**상태**: 진행 중

---

## 🟡 **발견 1: 그리퍼 토픽 데이터 오류**

### 뭐가 일어났냐

```
VLA 명령 내림        ✅ action[6] = 0.81~1.0 (잘 기록됨)
        ↓
로봇 실제 움직임     ✅ Timeline에 0→1로 올라감 (동작함)
        ↓
토픽 데이터         ❌ state[12] = 0.001 (고정값)
```

### 현황 분석

| 항목 | 상태 | 값 |
|------|------|-----|
| **명령 (action[6])** | ✅ 정상 | 0.81~1.0 |
| **실제 동작** | ✅ 정상 | Timeline에서 확인 |
| **토픽 데이터 (state[12])** | ⚠️ 오류 | 0.001 고정 |

### 원인
- `/gripper/position` 토픽이 고정값만 기록됨
- 센서 미연결, 토픽 노드 오류, 또는 데이터 수집 오류

### 학습에 미치는 영향
- ⚠️ **학습에 영향 없을 가능성**: VLA 모델이 EEF만 입력받으면 문제 없음
- 🔍 **확인 필요**: 실제 학습 시 state[12] 사용 여부

### 현 상황에서의 대응
- ❓ state[12] 사용 여부 확인 후 판단
- ✅ action[6]은 정상 (학습 가능)
- 📝 새 데이터 수집 시 토픽 확인 필수

---

## 🔴 **발견 4: X축 방향 반대 (주의: 실제 문제)**

### 현황
| 항목 | 값 |
|------|-----|
| **학습 데이터셋** | -X 방향으로 기록 |
| **Mock 추론 테스트** | +X 방향으로 예측 |
| **결론** | ❌ 로봇이 반대 방향으로 움직일 수 있음 |

### 데이터 확인
- [ ] Timeline에서 -X 방향 확인됨 ✅
- [ ] 다른 축(Y, Z)은 방향이 맞는지 확인
- [ ] 전체 에피소드에서 일관되게 -X인지 확인

### 코드 확인
- [ ] ROS 2 bag의 원본 데이터에서 좌표축이 어떻게 정의되어 있는지
- [ ] bag_to_lerobot_eef.py의 좌표 변환 로직
  - [ ] _eef_delta_m_rad() 함수에서 부호 처리
  - [ ] 어디서 축이 반전되는지
- [ ] 로봇 URDF의 좌표계 정의
- [ ] vla_inference_mock_test.py에서 Action 해석 방식

---

## 🟡 **발견 2: Joint State 토픽 데이터 오류**

### 뭐가 일어났냐

Joint State (state[6:11])도 그리퍼처럼 **고정값**으로 기록됨:

| Joint | Min | Max | Std |
|-------|-----|-----|-----|
| J1 | 0.430 | 0.430 | **0.0** |
| J2 | 0.092 | 0.092 | **0.0** |
| J3 | 1.256 | 1.256 | **0.0** |
| J4 | 1.263 | 1.263 | **0.0** |
| J5 | 0.552 | 0.552 | **0.0** |
| J6 | 4.108 | 4.108 | **0.0** |

### 원인
- `/dsr01/joint_states` 토픽이 고정값만 기록됨
- 토픽 수집 오류 또는 데이터 저장 오류

### 학습에 미치는 영향
- ⚠️ **학습에 영향 없을 가능성**: VLA 모델이 EEF만 입력받으면 문제 없음
- 🔍 **확인 필요**: 실제 학습 시 state[6:11] 사용 여부

---

## 🟡 **발견 3: State vs Action의 그리퍼 값 불일치**

### 현황
| 항목 | 범위 | 고유값 |
|------|------|--------|
| **State[12]** | 0.001096 ~ 0.001351 | 2개 |
| **Action[6]** | 0.81 ~ 1.0 | ? |
| **상태** | ❓ 뭐가 일어났는지 불명 |

### 추측
- A) grips 값이 실제로는 0.81~1.0 범위?
- B) action을 저장할 때 다시 정규화?
- C) 다른 처리가 추가됨?

### 확인 필요
- [ ] bag_to_lerobot_eef.py [DEBUG] 출력 → grips 실제값 확인
- [ ] action[6]이 0.81~1.0인 이유 파악
  - [ ] grips가 실제로 0.81~1.0?
  - [ ] action 저장 시 정규화?
  - [ ] 코드 어디서 처리?

---

## 📋 **기타 확인 사항**

### 정규화
- [ ] State[0~5] (TCP): mm/deg → m/rad (코드 확인됨 ✅)
- [ ] State[6~11] (Joint): 이미 rad 형태 (확인됨 ✅)
- [ ] Action[0~5] (EEF delta): m/rad 범위 확인
- [ ] Action[6] (grip_next): 실제 저장 범위 확인

### Joint State
- [ ] 학습 데이터의 Joint State가 실제 로봇 센서값과 일치?
- [ ] 기대값 vs 실제값 오차 분석 필요?

### 카메라 & 동기화
- [ ] 카메라 이미지는 정상? (문서에서 OK)
- [ ] 타임스탬프 동기화 제대로 됐나?
- [ ] 5Hz 샘플링 맞나? (프레임 누락 없나?)

### Dataset 구조
- [ ] State가 정말 13-dim? (EEF 6 + Joint 6 + Gripper 1)
- [ ] Action이 정말 7-dim? (EEF delta 6 + Grip 1)
- [ ] 다른 에피소드도 같은 구조?

---

## 🔥 **우선순위**

### 긴급 (오늘)
1. bag_to_lerobot_eef.py [DEBUG] 출력 → grips 실제값 확인
2. Action[6] = 0.81~1.0인 이유 파악

### 중요 (이번 주)
3. X축 방향 원인 파악 (좌표계 확인)
4. ROS 2 bag 원본 데이터 확인

### 나중 (필요시)
5. 정규화, 타임스탬프, 구조 확인

---

---

## 💥 **현 상황 정리: 토픽 데이터 오류 vs 학습 영향**

### 발견된 토픽 데이터 오류

```
state[t] = [TCP Pose, Joint State, Gripper]
           ✅ 정상   ⚠️ 고정값   ⚠️ 고정값

상세:
- state[0:5]:   TCP Pose (X, Y, Z, Rx, Ry, Rz)    ✅ 정상
- state[6:11]:  Joint State (J1~J6)               ⚠️ 토픽 오류 (고정값)
- state[12]:    Gripper                           ⚠️ 토픽 오류 (0.001)
```

### 실제 학습에 영향이 있는지는 **아직 미확인**

| 항목 | 상태 | 문제 | 학습 영향 |
|------|------|------|---------|
| **TCP Pose** | ✅ 정상 | 없음 | O (사용됨) |
| **Action EEF** | ✅ 정상 | 없음 | O (사용됨) |
| **Joint State** | ⚠️ 오류 | 고정값 | ? (미확인) |
| **Gripper State** | ⚠️ 오류 | 고정값 | ? (미확인) |

### 다음 단계

**중요**: 
- VLA 모델이 **EEF만 입력받으면** 문제 없음
- VLA 모델이 **Joint/Gripper를 입력받으면** 영향 있음
- **어느 쪽인지 확인이 필수**

**현재 상황**:
- 토픽 데이터 오류는 확정
- 학습에 영향을 주는지는 불명
- 새 데이터 수집 필요 여부도 확인 후 판단

---

## 🔍 **우선순위 1: 학습 데이터 입력 흐름 확인 (가장 중요)**

### 핵심 질문
**VLA 모델이 실제로 어떤 state 데이터를 입력으로 사용하나?**
- state[0:5] (EEF)만 사용? → 토픽 오류가 학습에 영향 없음
- state[0:13] 전부 사용? → 토픽 오류가 학습에 영향 있을 수 있음

확인이 필수인 이유:
- 토픽 오류의 실제 영향을 알아야 함
- 새 데이터 수집이 필요한지 판단해야 함

### 1단계: 데이터셋이 어떻게 기록되었는지
```bash
# state가 몇 차원으로 저장되는지 확인
grep -r "observation.state" /home/user/robot_workspace --include="*.py" | grep -E "shape|dim|append"
```
- [ ] state 저장 차원 확인 (6-dim vs 13-dim)
- [ ] 어디서 저장되는지 확인

### 2단계: 데이터 로더가 어떻게 입력받는지
```bash
# 학습 시 state를 어떻게 슬라이싱하는지
grep -r "state\|observation" /home/user/robot_workspace --include="*.py" | grep -E "load|batch|\[:\]"
```
- [ ] 데이터 로더가 전체 state를 받는지, 일부만 받는지
- [ ] state 슬라이싱 여부 확인 (state[:6] vs state[:13])

### 3단계: 모델이 몇 차원을 기대하는지
```bash
# 모델 입력 정의
grep -r "input_size\|state_dim\|observation.*shape" /home/user/robot_workspace --include="*.py"
```
- [ ] 모델 입력 차원 확인
- [ ] 모델 설정에서 state 사용 범위 확인

### 4단계: 실제 학습 코드 찾기
```bash
# 학습 스크립트 위치
find /home/user/robot_workspace -name "*train*.py" -o -name "*learning*.py" -o -name "*main*.py" | head -20

# 파일 구조 파악
find /home/user/robot_workspace/vla_ws -type f -name "*.py" | grep -E "vla|model|train|data" | head -20
```
- [ ] 학습 스크립트 위치 파악
- [ ] 모델 forward() 함수에서 state 사용 범위 확인

### 최종 확인 항목
- [ ] 학습 데이터의 실제 입력 차원 (6-dim? 13-dim?)
- [ ] VLA 모델이 사용하는 state의 범위 명확히
- [ ] 토픽 오류가 실제 학습에 영향을 주는지 판단
- [ ] 토픽 오류의 심각도 재평가 (학습 영향 기반)

---

## 📝 **진행 상황**

| 발견 사항 | 상태 | 진행도 |
|---------|------|--------|
| 그리퍼 토픽 오류 | ✅ 확인됨 | 100% |
| Joint State 토픽 오류 | ✅ 확인됨 | 100% |
| 학습 입력 데이터 확인 | 🔄 **우선순위 1** | 0% |
| X축 방향 문제 | 🔄 진행중 | 30% |

---

**마지막 업데이트**: 2026-06-08  
**현 상황**: 토픽 데이터 오류 확인, 학습 영향 여부 미확인 → 우선 학습 입력 흐름 파악 필수

---
---

# 📅 2026-06-09 — 정규화·추론 입력 파이프라인 정밀 점검

**대상**: `vla_dataset_v0.4.3` (신규 생성) / pi05 학습·추론 파이프라인

## ✅ 결론 한눈에 보기 (발견 이슈 5건)

| # | 이슈 | 구분 | 영향 | 해결 | 적용 위치 |
|---|------|------|------|------|-----------|
| 1 | 입력 **State QUANTILES 정규화 누락** | 추론 | 🔴 치명 (state 토큰 전 차원 어긋남) | ✅ | `serve_pi05.py` (q01/q99 인라인) |
| 2 | **right_wrist 카메라** 빈 슬롯 처리 불일치 | 추론 | 🟠 높음 (학습=더미/추론=base복제) | ✅ | `serve_pi05.py` (빈 슬롯 키 제외) |
| 3 | **그리퍼 state 스케일** 버그 (raw/740²) | 데이터 | 🔴 치명 (정규화 분모≈0 폭발) | ✅ | `fin/vla_dataset_v0.4.3` (×740) |
| 4 | 출력 **Action MIN_MAX 역정규화 누락** | 추론 | 🔴 치명 (출력 [-1,1] 그대로 반환) | ✅ | `serve_pi05.py` (inverse MIN_MAX) |
| 5 | **이미지 리사이즈 불일치** (학습=레터박스 / 추론=정사각 왜곡) | 추론 | 🔴 높음 (딸기 세로로 늘어남→방향 예측 교란) | ❌ | `serve_pi05.py`+클라이언트 (정사각 리사이즈 제거) |

**상태**: 정규화/역정규화 4건은 해결. **#5 이미지 리사이즈 불일치 미해결** — 추론 결과 X/Y 방향 이상의 유력 원인. 실측 추론에서 모델 출력이 학습 궤적과 어긋나는 현상 조사 중.

> ℹ️ 검증 완료(문제없음): 카메라 슬롯 매핑(base/left_wrist), action=EEF delta 일관성, 프레임/영상 동기화, 이미지 정규화, **delta 적용 프레임(수집·추론 둘 다 DR_BASE 일치 → 좌표프레임 원인 기각)**.
> 🟡 데이터 한계(버그 아님, 재수집 필요): 그리퍼·회전축 저분산, 단일 태스크.

---

## 🟢 발견 #1 — [추론] State 정규화(QUANTILES) 누락 (해결 완료)

### 문제 정의
pi05는 state를 **텍스트 프롬프트에 256-bin 이산화**해서 넣는다. 학습은 **QUANTILES 정규화 → 이산화** 순서인데, **추론 서버는 정규화를 건너뛰고 raw 값을 그대로 이산화**한다. → 같은 자세인데 학습/추론의 state 토큰이 완전히 달라짐.

### 증거 (코드)
- 학습 정식 순서 (`lerobot/.../pi05/processor_pi05.py:139-150`):
  ```
  raw → NormalizerProcessorStep(STATE=QUANTILES, stats.json q01/q99) → [-1,1]
      → Pi05PrepareStateTokenizerProcessorStep (256-bin 이산화 → 프롬프트)
  ```
  주석 L74/L143: *"State should already be normalized to [-1,1] ... NormalizerProcessorStep MUST come before the tokenizer step."*
- 추론 서버 (`serve_pi05.py` predict):
  ```python
  state_np = np.clip(req.state, -1, 1)     # ❌ QUANTILES 정규화 없음
  np.digitize(linspace(-1,1,257)[:-1])     # 이산화 식만 동일
  ```
- 클라이언트(`harvest_dashboard.py:2529`, `grasp_pipeline_pi05.py:297`)는 **raw 물리값**(m/rad/ratio)을 전송.

### 영향 (수치, v0.4.3 stats 기준, 동일 자세)
| dim | raw | 학습 bin (정규화O) | 서버 bin (정규화X) | 차이 |
|-----|-----|------|------|------|
| x_m | 0.20 | 113 | 153 | 40 |
| y_m | 0.40 | 134 | 179 | 45 |
| z_m | 0.87 | 143 | 239 | 96 |
| rx_rad | 1.5699 | 169 | 255(saturate) | 86 |
| ry_rad | 1.5068 | 139 | 255 | 116 |
| rz_rad | -1.5642 | 131 | 0 | 131 |
| gripper | 0.811 | 0 | 231 | 231 |

→ **전 차원이 어긋남.** 회전축은 raw≈1.5라 전부 ±1.0으로 saturate. 모델이 "전혀 다른 상태"로 인식 → 추론 품질 저하 직결.

### 해결방법
**원인**: 추론 경로에서 QUANTILES 정규화 단계가 빠짐. **둘 중 하나로 수정.**

- **(권장) 서버가 정식 프로세서를 쓰도록 리팩터링**: 프롬프트를 수동 조립하지 말고, `obs["observation.state"]=raw` + `task=instruction`을 넣어 `policy.select_action`이 `make_pi05_pre_post_processors` 파이프라인(정규화→이산화)을 그대로 타게 한다. → 학습과 100% 동일 보장.
- **(빠른 우회) 서버 수동 정규화 추가**: 이산화 직전에 stats.json의 state `q01/q99`로 QUANTILES 정규화:
  ```python
  norm = 2*(state - q01)/(q99 - q01) - 1   # 7개 실차원, 나머지 패딩 0
  state_np = np.clip(norm, -1, 1)
  ```
  단, stats.json(`fin/vla_dataset_v0.4.3`)을 서버가 로드해야 함. 모델별 stats 일치 필수.

### 상태
🟢 **해결 (2026-06-09, 서버 적용)** — `serve_pi05.py`에 빠른 우회(수동 QUANTILES) 적용.
- 체크포인트의 `policy_preprocessor_step_2_normalizer_processor.safetensors`에서 `observation.state.q01/q99` 로드 (확인 결과 **N=7**).
- `predict()`에서 `req.state[:7]`에 QUANTILES 정규화(`2*(x-q01)/(q99-q01)-1`) 후 256-bin 이산화 → 학습 프롬프트(7토큰)와 동일 구조.
- 클라이언트는 **raw(m/rad) 전송** (서버가 정규화). 현 클라이언트(dashboard·grasp_pipeline)는 이미 raw 전송이라 호환.

---

## 🟢 발견 #2 — [추론] right_wrist 카메라 처리 불일치 (해결 완료)

### 문제 정의
학습은 카메라 2대(`camera1→base_0_rgb`, `camera2→left_wrist_0_rgb`)만 쓰고, 없는 `right_wrist_0_rgb`는 **더미(-1) + attention mask=0(무시)**로 채운다. 그런데 추론 서버는 빈 슬롯을 **base 이미지 복제 + mask=1(사용)**로 채운다.

### 증거
- 학습 (`modeling_pi05.py` empty-camera 로직): `img = -1` 더미, `mask = 0` → 모델이 무시.
- 추론 (`serve_pi05.py`): `right_img = base_img.clone()` 후 obs에 항상 포함 → 키가 존재하므로 mask=1로 **모델이 attention**.
- 학습 `rename_map`: `{camera1: base_0_rgb, camera2: left_wrist_0_rgb}` (right 없음).

### 영향
학습은 "right_wrist 없음"으로 배웠는데, 추론은 그 슬롯에 base 화면을 넣어 모델이 보게 됨 → 학습에 없던 입력 패턴 → 추론 교란.

### 해결방법
**서버에서 빈 wrist 슬롯을 base로 복제하지 말고 obs에서 키를 제외**한다. 그러면 `modeling_pi05`가 학습과 동일하게 더미(-1)+mask=0으로 채운다:
```python
obs = {base_0_rgb, left_wrist_0_rgb, language...}      # 항상
if req.right_wrist_image:
    obs["observation.images.right_wrist_0_rgb"] = right_img   # 있을 때만
```

### 상태
🟢 **해결 (2026-06-09, 서버 적용)** — `serve_pi05.py`에서 `base_img.clone()` fallback 제거.
- 이미지가 None이면 obs에 키를 넣지 않음 → `modeling_pi05`가 학습과 동일하게 더미(-1)+mask=0으로 처리.
- left_wrist도 동일 처리 (현재는 camera2가 항상 들어옴).

---

## 🟢 발견 #4 — [추론] 출력 Action 역정규화(MIN_MAX) 누락 (해결 완료)

### 문제 정의
학습은 ACTION을 **MIN_MAX 정규화**해서 모델이 **정규화된 action([-1,1])**을 출력하도록 배운다. 추론에서 모델 출력을 **raw(m/rad/ratio)로 역정규화**해야 로봇이 올바로 움직이는데, 서버가 이 단계를 빠뜨리고 **정규화값을 그대로 반환**한다.

### 증거 (코드)
- `modeling_pi05.py:1226-1241` `predict_action_chunk`: `model.sample_actions(...)` → 정규화공간 출력 → 차원 슬라이스만 하고 **역정규화 없이 반환**.
  ```python
  actions = self.predict_action_chunk(batch)[:, : self.config.n_action_steps]
  # 여기까지가 모델 출력 → 정규화([-1,1]) 값
  ```
- 역정규화 `UnnormalizerProcessorStep`는 **별도 postprocessor**(`processor_pi05.py:160-166`, 체크포인트의 `policy_postprocessor.json`)에 정의돼 있으나, **서빙 코드가 postprocessor를 호출하지 않음**.
- 서버 `serve_pi05.py`: `action = policy.select_action(obs)` 결과를 그대로 응답 → **postprocessor 미적용**.
- 클라이언트(`harvest_dashboard.py`)는 `action[:3]`을 raw m로 보고 `×1000`(mm) 변환 → 정규화값에 적용 시 **명령 왜곡**.

### 영향
- 학습 데이터 action 범위: 예) `dx_m ∈ [-0.022, 0.087]`, `grip_next ∈ [0.81, 1.0]`.
- 클라이언트가 받는 값: **[-1, 1] 정규화 값 (잘못된 범위)**.
- 로봇에 그대로 명령 시 **의도치 않은 큰 움직임 / 잘못된 그리퍼 명령**.
- State 정규화(#1)와 함께 추론 동작에 치명적.
- 🔎 참고: 이 버그 때문에 **이전 버전(~v0.4.1) 데모가 어떻게 동작했는지 의아한 수준** — 당시 동작 경위(별도 역정규화 경로 존재 여부 등) 확인 필요.

### 해결방법
모델 출력에 **MIN_MAX 역정규화** 적용: `raw = (norm+1)/2 * (max-min) + min`
- **(빠른 우회)** `action.min`/`action.max`를 동일 `normalizer.safetensors`에서 로드해 위 식 적용 (state q01/q99 로드와 동일 패턴).
- **(권장)** 체크포인트의 **postprocessor(`UnnormalizerProcessorStep`)를 로드해 적용** → MIN_MAX/QUANTILES 모드 무관하게 학습과 일치.

### 그리퍼(action dim6) 주의
ACTION은 feature 단위라 **그리퍼도 동일하게 MIN_MAX**다. 역정규화하면 `grip_next`는 학습 범위 **[0.81, 1.0]의 연속값**으로 복원된다(0/1 아님). 로봇이 binary 그리퍼 명령(0=open/1=close)을 기대하면 **클라이언트에서 임계값 처리** 필요: 예) `grip = 1 if action[6] > 0.9 else 0`.

### 상태
🟢 **해결 (2026-06-09, 서버 적용)** — `serve_pi05.py`에서 모델 출력에 inverse MIN_MAX 인라인 적용: `(norm+1)*(max-min)/2 + min` (`action.min`/`action.max`를 동일 `normalizer.safetensors`에서 로드). 체크포인트 config로 `ACTION=MIN_MAX` 재확인.

---

## 🔴 발견 #5 — [추론] 이미지 리사이즈 방식 불일치 (미해결)

### 문제 정의
학습은 이미지를 **resize_with_pad(비율 유지 + 검은 패딩 = 레터박스)**로 224×224 만들고, 추론 서버/클라이언트는 **정사각 강제 리사이즈(왜곡)**로 224×224를 만든다. → 모델이 학습 때와 **다른 모양의 이미지**를 보게 됨.

### 핵심 메커니즘 (`modeling_pi05.py:1178`)
모델 `_preprocess_images`는 **학습·추론 공용**이고, 이미지가 224가 아닐 때만 패딩한다:
```python
if img.shape[1:3] != (224, 224):
    img = resize_with_pad_torch(img, 224, 224)   # 레터박스
img = img * 2.0 - 1.0
```
- **학습**: 데이터로더가 원본 480×640 그대로 줌 → ≠224 → **resize_with_pad 적용** ✅
- **추론**: 서버 `_decode_image`가 미리 224×224로 욱여넣음 → ==224 → **resize_with_pad 스킵** → 왜곡 그대로 ❌

### 변환 과정 (학습 vs 추론)
```
[학습 = resize_with_pad]
  640×480 (4:3)
     ↓ 비율 그대로 1/2.857 축소
  224×168  (딸기 비율 정상)
     ↓ 상/하 28px 검은 패딩
  224×224  ← 위아래 검은띠, 딸기 모양 정상

[추론 = 정사각 resize]
  640×480
     ↓ 가로 ×0.350 / 세로 ×0.467 (배율 다름)
  224×224  ← 검은띠 없음, 딸기 세로로 1.33배 늘어남(왜곡)
```

| | 모델에 도달 크기 | resize_with_pad | 최종 모델 입력 |
|---|------------------|------------------|----------------|
| 학습 | 480×640 (원본) | ✅ 적용 | 레터박스(비율 정상) |
| 추론 | 224×224 (사전 왜곡) | ❌ 스킵 | 세로로 늘어난 왜곡 |

### 영향
모델이 "레터박스 정상비율 딸기"로 학습했는데 추론은 "세로로 늘어난 딸기 + 띠 없음"을 봄 → **물체 위치/형태 인식 어긋남 → 방향 예측 교란**. 실측에서 모델 X/Y 출력이 학습 궤적과 어긋나는 현상의 유력 원인(단, flip이 아닌 stretch라 단독으로 "정확한 반전"을 설명하진 않음).

### 해결방법
추론도 학습과 동일하게 **resize_with_pad(레터박스)**가 적용되게:
- **서버** `_decode_image`: 정사각 `.resize((224,224))` **제거** → 원본 비율로 모델에 전달 → 모델 내부 resize_with_pad가 학습과 동일 레터박스 생성.
- **클라이언트**(dashboard/mock/grasp): 정사각 리사이즈 제거, **원본 비율로 base64 전송**.

> 참고 이미지: `docs/img_resize_compare/` (A=학습 레터박스, B=추론 왜곡, compare=나란히)

### 상태
🔴 **미해결** — 서버(원격) + 클라이언트(로컬) 모두 정사각 리사이즈 제거 필요.

### (확인 권장)
"학습 데이터로더가 480×640 원본을 그대로 모델에 넣는다"의 최종 확정은 학습 환경에서 **image_transforms에 resize가 없는지** 1회 확인. (동일 `_preprocess_images` 사용 + config에 resize 없음 + LeRobot 기본 원본해상도 → 거의 확실)

---

## 🟢 발견 #3 — [데이터] 그리퍼 state 스케일 버그 (해결 완료)

> 6/8자 발견 1·3("그리퍼 state 0.001 고정 / action과 불일치")의 **근본 원인 규명 + 해결**.

### 문제 정의
`observation.state[6]`(그리퍼)이 `raw/740²`(≈0.001)로 잘못 스케일됨. action `grip_next`는 변환 시 `×740` 덕에 우연히 정상 ratio(0.811/1.0)였음.

### 원인
녹화 시점 `/gripper/position`이 `raw/740²`(≈0.001)로 publish됨 (당시 `get_position()`이 740으로 한 번 더 나눔). 변환 스크립트(`bag_to_lerobot_eef.py`)는 정상 — 그 값을 그대로 state로, `×740`해서 action으로 저장. (git이 단일 squash 커밋이라 버그 커밋 추적 불가, 현재 코드는 이미 수정됨.)

### 영향
state 그리퍼 QUANTILES 분모 `q99-q01 ≈ 0.00026` → 추론 시 그리퍼(0~1)가 정규화 후 **수천 배 폭발**.

### 해결방법 (적용 완료)
1. `mid/vla_dataset_v0.4.2` → `v0.4.3` 복사
2. 모든 parquet에서 `observation.state[6] *= 740` (그리퍼만; action·타 차원·비디오 불변)
   - `0.00109569 → 0.810811`(raw 600), `0.00135135 → 1.000000`(raw 740)
3. `fin/vla_dataset_v0.4.3` 생성 + stats.json 재계산 → 분모 `0.00026 → 0.189` (폭발 해소, 추론 스케일 일치)

### 상태
🟢 **해결** — `fin/vla_dataset_v0.4.3`가 권장 학습 데이터. (상세: `dataset_versions.md`)

---

## ℹ️ 검증 완료 — 문제 없음으로 확인된 항목

| 항목 | 결과 |
|------|------|
| 카메라 슬롯 매핑 (base/left_wrist) | ✅ 학습 `rename_map`과 일치. 4개 클라이언트 모두 `camera2→left_wrist_image` 정상 (잘못 바꾼 대시보드 원복함) |
| action = EEF delta 일관성 | ✅ state 전이와 오차 ~1e-16 |
| 프레임 연속성 / timestamp 단조 / index | ✅ |
| 비디오 ↔ parquet 동기화 | ✅ camera1/2 모두 7650 = parquet |
| NaN/Inf | ✅ 없음 |
| 이미지 정규화 (이중정규화 의심) | ✅ `/255`→`*2-1` 고정 직렬변환, VISUAL=IDENTITY라 stats 미사용. 문제없음 |

> **참고 — 카메라 슬롯 교훈**: 물리적 위치(오른쪽/팔)와 무관하게, 모델은 **학습 때 붙인 슬롯 이름**(`left_wrist_0_rgb`)만 안다. 추론도 같은 슬롯으로 보내야 하며, "물리적으로 right니까 right로" 바꾸는 건 학습-추론 불일치를 만든다. (재학습 불필요)

---

## 🟡 알려진 한계 (버그 아님, 재수집으로만 개선)

| 채널 | 현상 | 의미 |
|------|------|------|
| gripper | 값 2개(600→740 단일전환) | "언제 잡을지(완전히 닫을지)" 타이밍만 학습. 여는/놓는·미세폭 제어 불가 |
| rx/ry/rz | ≈90° 거의 고정 (분모 0.0008~0.003) | 회전 학습 신호 거의 없음. 추론 자세가 학습 범위 벗어나면 민감 |
| task_index | 전부 0 | 단일 태스크. 멀티태스크 불가 |

→ 값·스케일은 정상이나 **분산이 작다**. 새 자세/동작/태스크는 학습 불가 → 다양성 있는 재수집 필요.

---

## 🔥 액션 아이템 (2026-06-09 기준)

| # | 항목 | 담당/위치 | 우선순위 | 상태 |
|---|------|-----------|----------|------|
| 1 | 추론 서버 State QUANTILES 정규화 추가 | `serve_pi05.py` (원격) | 🔴 최우선 | ✅ 해결 |
| 2 | 추론 서버 right_wrist 빈 슬롯 처리 (키 제외) | `serve_pi05.py` (원격) | 🟠 높음 | ✅ 해결 |
| 3 | 그리퍼 스케일 수정 + v0.4.3 생성 | 로컬 데이터 | 🟢 완료 | ✅ |
| 4 | 추론 서버 출력 Action MIN_MAX 역정규화 추가 | `serve_pi05.py` (원격) | 🔴 최우선 | ✅ 해결 |
| 5 | **이미지 리사이즈 정사각 제거(레터박스 일치)** | `serve_pi05.py`(원격)+클라이언트 | 🔴 높음 | ❌ 미해결 |
| 6 | 추론 실측 검증 (서버 수정 후 동작 확인) + 방향 다중프레임 테스트 | 로봇/서버 | 🔵 다음 | 대기 |
| 7 | (선택) 그리퍼/회전 다양성 재수집 | 데이터 수집 | 🟡 중기 | 보류 |

---

## ⚠️ 잔여 확인사항 (서버 수정은 됐으나 검증 권장)

1. **State 토큰 수(7개) 가정** — "학습 프롬프트=7토큰"은 ① 체크포인트 stats가 7-dim(확실) + ② 로컬 lerobot 코드 읽기(추정)에 근거. **실제 학습은 별도 서버 환경**이라 코드가 다를 수 있음.
   → 서버에서 **정책 자체 프로세서**(`make_pi05_pre_post_processors`)에 샘플을 통과시켜 토큰 수/값이 수동 경로와 일치하는지 1회 대조 권장. (더 안전한 길은 수동 조립 대신 체크포인트 프로세서를 그대로 사용)
2. **정규화 후 클립 차이(경미)** — 서버는 정규화값을 `clip(-1,1)` 후 이산화하나, 학습 토크나이저는 클립하지 않음. **범위 내 값은 동일**, q01 미만(범위 이탈) 값만 bin이 다를 수 있음(서버 0 vs 학습 -1). 영향 작음.
3. **클라이언트 raw 전송 확인** — 서버가 내부 정규화하므로 클라이언트는 raw(m/rad) 전송 필수. dashboard·grasp_pipeline은 이미 raw → OK. 사전 정규화하는 클라이언트가 있으면 제거.

---

**마지막 업데이트**: 2026-06-09
**현 상황**: 정규화/역정규화 4건(#1·#2·#3·#4) 해결. **이미지 리사이즈 불일치(#5) 신규 발견·미해결** — 추론 X/Y 방향 이상의 유력 원인. delta 적용 프레임은 수집·추론 모두 DR_BASE로 일치(좌표프레임 원인 기각). 다음: #5 수정 후 방향 다중프레임 테스트.

### 학습 파이프라인 ↔ 서빙 매핑 (전 단계 점검 완료)
| 학습 단계 | 서빙 처리 | 상태 |
|-----------|-----------|------|
| RenameObservations (camera1→base_0_rgb) | 클라이언트가 해당 키로 전송 | ✅ |
| AddBatchDimension | `.unsqueeze(0)` | ✅ |
| RelativeActions | `use_relative_actions=False` → 스킵 | ✅ |
| Normalize STATE (QUANTILES) | safetensors q01/q99로 인라인 적용 | ✅ |
| Normalize VISUAL (IDENTITY) | 미적용(동일) | ✅ |
| Pi05PrepareStateTokenizer | 256-bin digitize → 7토큰 prompt | ✅ |
| TokenizerProcessor (PaliGemma) | `tokenizer(prompt, ...)` | ✅ |
| DeviceProcessor (→cuda) | `.to(DEVICE)` | ✅ |
| 모델 추론 | `policy.select_action(obs)` | ✅ |
| **Unnormalize ACTION (inverse MIN_MAX)** | `(norm+1)*(max-min)/2+min` 인라인 | ✅ |
| DeviceProcessor (→cpu) | `.cpu().float().numpy()` | ✅ |

> 학습 postprocessor는 `[unnormalizer, device]` 2단계뿐 → 서빙에서 모두 동등 적용. **누락 없음 확인.**

---
---

# 📊 부록 — 데이터 변환 전 과정 (로봇 수집 → 학습 → 추론)

> 같은 데이터가 단계마다 **단위·범위·형식**이 어떻게 바뀌는지 한눈에. (v0.4.3 기준)

## 큰 그림 (3단계)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [A] 수집 → 학습 데이터화                                                 │
│                                                                           │
│  로봇 센서 ──rosbag(raw)──▶ bag_to_lerobot_eef.py ──▶ mid ──▶ fin         │
│  (mm/deg,                  (단위변환 mm→m,deg→rad)   (LeRobot)  (+stats)   │
│   ratio, uint8)            (+EEF delta 계산)                              │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  [B] 학습 (pi05)                                                          │
│                                                                           │
│  fin ──DataLoader──▶ Preprocessor ──▶ 모델(정규화 공간 학습)              │
│   raw값            정규화/이산화/토큰화        손실=정규화된 action 기준   │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  [C] 추론 (서빙)                                                          │
│                                                                           │
│  로봇 ──client(raw)──▶ server(정규화→모델→역정규화) ──▶ client ──▶ 로봇   │
│  (mm/deg)            (학습과 동일 파이프라인 재현)      (raw)     (delta)  │
└─────────────────────────────────────────────────────────────────────────┘
```

핵심 원리: **모델은 항상 "정규화 공간"에서만 동작.** 입력은 들어가기 전 정규화, 출력은 나온 뒤 역정규화. 학습과 추론이 **같은 stats(q01/q99, min/max)**를 써야 일치.

---

## 모달리티별 변환 추적 (값 1개가 끝까지 어떻게 변하나)

### ① TCP 위치 (x) — state 입력
| 단계 | 값/단위 | 처리 |
|------|---------|------|
| 로봇 센서 | `350 mm` | Doosan native |
| mid/fin | `0.350 m` | `÷1000` (mm→m) |
| 학습 정규화 | `[-1,1]` 토큰 | QUANTILES: `[q01,q99]→[-1,1]` → 256bin |
| 추론 client | `0.350 m` | 로봇 mm `÷1000` (raw 전송) |
| 추론 server | `[-1,1]` 토큰 | 동일 QUANTILES (q01/q99 from safetensors) |

### ② TCP 회전 (rx) — state 입력
| 단계 | 값/단위 |
|------|---------|
| 로봇 | `90 deg` |
| mid/fin | `1.5708 rad` (`deg→rad`) |
| 학습/추론 정규화 | QUANTILES → `[-1,1]` (분산 작아 거의 saturate) |

### ③ 그리퍼 — state 입력 & action 출력
| 단계 | state gripper | action grip_next |
|------|---------------|------------------|
| 로봇 | `get_position()` = ratio 0~1 | — |
| mid v0.4.2 | `0.001` ❌ (raw/740² 버그) | `0.811/1.0` ✅ |
| **mid/fin v0.4.3** | **`0.811/1.0`** ✅ (`×740` 수정) | `0.811/1.0` |
| 학습 정규화 | QUANTILES→[-1,1] | MIN_MAX→[-1,1] |
| 추론 server 출력 | — | 역MIN_MAX → `0.811~1.0` (ratio) |
| 추론 client→로봇 | — | `×740` → `0~740 raw` (`harvest_dashboard.py:2576`) |

### ④ Action delta (dx) — 출력
| 단계 | 값/단위 |
|------|---------|
| mid/fin | `dx_m` (Δm, 범위 ±0.087) |
| 학습 | MIN_MAX: `[min,max]→[-1,1]` (target) |
| 추론 모델 출력 | `[-1,1]` (정규화 공간) |
| 추론 server 역정규화 | `(norm+1)/2*(max-min)+min` → `dx_m` (raw) |
| 추론 client→로봇 | `×1000`→mm, **clamp ±200mm**, delta 이동 |

### ⑤ 카메라 — 이미지 입력
| 단계 | 값/형식 |
|------|---------|
| 로봇 | uint8 RGB `480×640` |
| mid/fin | MP4 (uint8) |
| 학습 로딩 | 영상 decode → `÷255` → `[0,1]` |
| 학습 모델 | resize `224`, `×2−1` → `[-1,1]` (SigLIP) |
| 키 매핑 | `camera1→base_0_rgb`, `camera2→left_wrist_0_rgb` |
| right_wrist | 학습=더미(-1)+mask0 / 추론=키 제외(동일 처리) |
| 추론 client | RGB→resize224→base64 |
| 추론 server | decode→`÷255`→`[0,1]`→모델 `×2−1` |

---

## 단위 요약 (어디서 무슨 단위인가)

| 모달리티 | 로봇/센서 | 학습 데이터(parquet) | 모델 내부 | 추론 출력→로봇 |
|----------|-----------|----------------------|-----------|----------------|
| 위치 | mm | m | 정규화 [-1,1] | (state 전용) |
| 회전 | deg | rad | 정규화 [-1,1] | (state 전용) |
| 그리퍼 | ratio 0~1 | ratio 0.811~1.0 | 정규화 [-1,1] | ratio→`×740`→0~740 |
| action 위치 | — | Δm | 정규화 [-1,1] | Δm→`×1000`→mm |
| action 회전 | — | Δrad | 정규화 [-1,1] | Δrad→`×57.3`→deg |
| 이미지 | uint8 0~255 | MP4 uint8 | [-1,1] | — |

---

## 핵심 규칙 3가지 (직관)

1. **단위 변환과 정규화는 다른 것.** mm→m, deg→rad는 "단위 변환"(데이터화 단계). [-1,1]로 펴는 건 "정규화"(학습/추론 런타임). 정규화는 데이터에 저장하지 않고 stats로 매번 적용.
2. **모델은 정규화 공간에서만 산다.** 입력=정규화 후 투입, 출력=역정규화 후 사용. 학습·추론이 같은 stats를 써야 함 (state=QUANTILES q01/q99, action=MIN_MAX min/max).
3. **클라이언트는 raw(m/rad/ratio)만 다룬다.** 정규화는 서버가, 단위 변환(×1000, ×57.3, ×740)은 클라이언트가. 클라이언트에서 사전 정규화하면 이중 정규화 → 금지.
