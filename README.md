# 딸기 수확 Motion Pipeline

Doosan E0509 6축 로봇팔, ROBOTIS RH-P12-RN(A) 그리퍼, Intel RealSense eye-in-hand 카메라, YOLO 딸기 검출, cuRobo 모션 플래닝을 연결한 벽면 딸기 pick & place 프로토타입입니다.

이 브랜치는 팀 Git Flow 기준 `feature/motion` 브랜치이며, 딸기 수확 시스템 중 **로봇 팔 motion / gripper / place 티칭** 쪽 기능을 담당합니다.

## 전체 흐름

```text
strawberry_yolo_node.py
  RealSense color/depth 수신
  YOLO 딸기 검출
  ripe 후보 필터링
  camera 좌표 -> base_link 좌표 변환
        |
        v
/dsr01/curobo/pick_pose
        |
        v
curobo_planner_node.py
  gripper open
  cuRobo approach
  cuRobo grasp
  soft close gripper
  cuRobo retreat
  bin/place transfer
  place slot above/release
  gripper open
  home
```

## 주요 노드

| 파일 | 역할 |
| --- | --- |
| `scripts/curobo_planner_node.py` | cuRobo 기반 pick & place 시퀀스 실행 |
| `scripts/strawberry_yolo_node.py` | RealSense + YOLO 딸기 검출, ripe 필터링, pick target 발행 |
| `scripts/joint_jog_control.py` | DART 없이 조인트를 step 각도로 미세 이동하는 티칭 보조 노드 |
| `scripts/teach_place_slots.py` | Doosan TCP(posx)와 joint 값을 읽어 계란판 slot pose 저장 |
| `scripts/gripper_service_node.py` | Python 그리퍼 서비스 노드 |
| `src/gripper_service_node.cpp` | C++ 그리퍼 서비스 노드 |

## Git에 포함하지 않는 로컬 파일

아래 파일은 장비별/실험별로 달라지거나 용량이 커서 Git에 포함하지 않습니다.

```text
models/best.pt
config/calibration_eye_in_hand_1.npz
```

- `models/best.pt`: YOLO 딸기 검출 모델
- `config/calibration_eye_in_hand_1.npz`: RealSense eye-in-hand 캘리브레이션 결과
- `logs/`: pick attempt 이미지/JSONL 로그. 실험 산출물이므로 Git 제외

각자 로컬 환경에서 위 경로에 파일을 배치해야 실제 딸기 인식과 좌표 변환이 동작합니다.

## 현재 현장 파라미터

모형 딸기 몸통 중심 파지 기준으로 현재 사용 중인 값입니다.

```python
GRASP_OFFSET = -0.035
GRASP_Z_BIAS = -0.030
GRIPPER_HARVEST_POS = 500
```

soft close 프로파일:

```python
GRIPPER_PRE_CLOSE_POS = 300
GRIPPER_CONTACT_POS = 400
GRIPPER_HARVEST_POS = 500
```

주의:

- 줄기 직접 파지는 아직 안정화되지 않았습니다.
- `position_cmd=1000`까지 들어가는 실행본도 확인했지만, 줄기는 gripper finger tip 형상/마찰/최소 간격 문제로 안정 파지가 어려웠습니다.
- 현재는 딸기 몸통 중심을 약하게 잡는 방식으로 운용합니다.
- `/dsr01/gripper/stroke`는 현재 실행 노드에 따라 실제 피드백이 아니라 명령값처럼 동작할 수 있으므로, 아직 force feedback으로 신뢰하면 안 됩니다.

## 빌드

```bash
cd ~/doosan_ws
colcon build --packages-select e0509_gripper_description
source install/setup.bash
```

## 실제 로봇 실행 순서

### 1. Doosan 로봇 및 그리퍼 bringup

```bash
ros2 launch e0509_gripper_description bringup.launch.py mode:=real host:=<robot_ip>
```

### 2. cuRobo planner 실행

```bash
ros2 run e0509_gripper_description curobo_planner_node.py
```

planner 시작 시 다음 로그를 확인합니다.

```text
cuRobo Planner Ready!
place slots loaded: .../config/place_slots.yaml
```

### 3. YOLO 딸기 인식 노드 실행

```bash
ros2 run e0509_gripper_description strawberry_yolo_node.py
```

YOLO 창 키 조작:

| 키 | 동작 |
| --- | --- |
| `1~9` | 후보 딸기 lock |
| `s` | lock/선택된 딸기 pick target 전송 |
| `a` | auto mode on/off |
| `u` | unlock |
| `h` | home 이동 |
| `y/n/d/m` | 수동 결과 라벨 저장: success/fail/dropped/missed |
| `q` | 종료 |

## ripe 후보 필터

`strawberry_yolo_node.py`는 YOLO class와 bbox 내부 red ratio를 함께 사용합니다.

```python
RIPE_RED_RATIO_MIN = 0.35
RIPE_STABLE_FRAMES = 6
```

현재 정책:

- class가 `unripe`, `green`, `immature`이면 skip
- class가 `ripe`, `mature`, unknown, 단일 `strawberry`여도 `red_ratio >= 0.35`를 만족해야 pick 후보
- 6프레임 연속 통과해야 최종 후보로 표시

## 계란판 place slot 티칭

계란판 place pose는 다음 파일에 저장됩니다.

```text
config/place_slots.yaml
```

각 slot은 두 자세를 가집니다.

- `above`: 계란판 구멍 위 안전 자세
- `release`: gripper를 열어 딸기를 놓는 낮은 자세

현재는 `slot0`만 저장되어 있습니다. 전체 계란판은 5x3 배열, 총 15개 slot이므로 추후 15개 slot 전체를 티칭해야 합니다.

현재 place 흐름:

```text
retreat
-> bin transfer / home 경유
-> slot0 above
-> slot0 release
-> gripper open
-> slot0 above retreat
-> home
```

## 조인트 티칭 도구

DART 없이 조인트를 조금씩 움직일 때 사용합니다.

```bash
ros2 run e0509_gripper_description joint_jog_control.py
```

키 조작:

| 키 | 동작 |
| --- | --- |
| `1~6` | 조인트 선택 |
| `w/s` 또는 방향키 위/아래 | 선택 조인트를 step 각도만큼 이동 |
| `a/d` 또는 방향키 좌/우 | step 각도 감소/증가 |
| `g` | 조인트 6개 직접 입력 후 이동 |
| `p` | 현재 조인트 출력 |
| `q` | 종료 |

현재 방식은 연속 jog가 아니라 **step 각도 기반 MoveJoint**입니다. 티칭용으로 더 안전하고, 원하는 관절 자세를 정확히 맞추기 쉽습니다.

## place slot 저장 도구

현재 로봇 자세를 계란판 slot pose로 저장합니다.

```bash
ros2 run e0509_gripper_description teach_place_slots.py
```

키 조작:

| 키 | 동작 |
| --- | --- |
| `a` | 현재 자세를 `slot_i.above`로 저장 |
| `r` | 현재 자세를 `slot_i.release`로 저장 |
| `n` | 다음 slot |
| `b` | 이전 slot |
| `p` | 현재 joint deg와 Doosan TCP(posx) 출력 |
| `w` | YAML 저장 |
| `q` | 종료 |

`a`, `r`을 누르면 YAML도 자동 저장됩니다.

## TCP 확인과 planner의 관계

`teach_place_slots.py`는 아래 Doosan 서비스를 사용합니다.

```text
/dsr01/aux_control/get_current_posx
```

서비스 타입:

```text
dsr_msgs2/srv/GetCurrentPosx
```

이 서비스로 읽은 TCP(posx)는 DART 티치펜던트 TCP 값과 여러 자세에서 비교했을 때 약 0.1mm 수준으로 일치했습니다.

역할 구분:

- `teach_place_slots.py`: 현재 자세의 joint 값과 Doosan TCP(posx)를 기록하는 티칭 도구
- `curobo_planner_node.py`: `place_slots.yaml`의 `joints_deg`를 읽어 실제 place 동작 실행
- `posx`: 검증/기록용
- `joints_deg`: 실제 place 실행용

즉 TCP 확인 노드는 planner가 직접 motion planning에 쓰는 노드가 아니라, 계란판 pose를 정확히 저장하기 위한 보조 도구입니다.

## 현재 한계 / TODO

- 현재 place는 고정 joint pose 기반 실험 구조입니다.
- 계란판 위치가 바뀌면 다시 티칭해야 합니다.
- 산업용 구조로 가려면 ArUco, tray corner detection, fixture 등을 이용해 tray frame을 자동 추정해야 합니다.
- 현재는 `slot0`만 티칭되어 있습니다.
- 이미 놓은 딸기를 다음 place 때 피하는 occupied slot collision 관리는 아직 없습니다.
- 벽 collision은 cuRobo world에 완전히 반영하지 않았습니다.
- `retreat -> bin/place` 직행은 벽 충돌 위험이 있어 검증 전 사용하면 안 됩니다.
- 일부 물리적으로 닿는 딸기도 고정 wall orientation 때문에 cuRobo IK_FAIL이 날 수 있습니다.
- 실제 딸기 force/pressure 기반 파지 성공 판정은 아직 구현되지 않았습니다.

## Git 관리 주의

Git에 올리지 않는 것:

```text
logs/
models/*.pt
*.npz
*.npy
config/calibration/
.env
```

모델 파일, 캘리브레이션 결과, 실험 로그, API key가 들어간 `.env`는 Git에 올리지 않습니다.
