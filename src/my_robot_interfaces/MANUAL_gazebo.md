# E0509 Gazebo 제어 매뉴얼

## 목차

1. [시스템 개요](#1-시스템-개요)
2. [환경 준비](#2-환경-준비)
3. [빌드](#3-빌드)
4. [실행 모드](#4-실행-모드)
   - [모드 A: Gazebo 단독 (시뮬레이션만)](#모드-a-gazebo-단독-시뮬레이션만)
   - [모드 B: 실제 로봇 + Gazebo 디지털 트윈](#모드-b-실제-로봇--gazebo-디지털-트윈)
5. [제어 프로그램 실행](#5-제어-프로그램-실행)
6. [메뉴 기능 설명](#6-메뉴-기능-설명)
7. [픽앤플레이스 웨이포인트 교정](#7-픽앤플레이스-웨이포인트-교정)
8. [트러블슈팅](#8-트러블슈팅)
9. [토픽 · 서비스 레퍼런스](#9-토픽--서비스-레퍼런스)

---

## 1. 시스템 개요

### 모드 비교

| 항목 | Gazebo 단독 (모드 A) | 실제 로봇 + Gazebo (모드 B) |
|------|---------------------|---------------------------|
| 실제 로봇 연결 | 불필요 | 필요 (IP 지정) |
| 물리 시뮬레이션 | Gazebo | Gazebo (미러링) |
| MoveJoint | JointTrajectoryController | Doosan 서비스 |
| MoveLine / MoveCircle | 미지원 | Doosan 서비스 |
| 그리퍼 제어 토픽 | `/dsr01/gripper_controller/commands` | `/dsr01/gripper/position_cmd` |
| 그리퍼 Gazebo 미러링 | 직접 | `gazebo_bridge.py` 자동 처리 |
| 관절 제어 방식 | 토픽 publish | 서비스 호출 |
| 용도 | 알고리즘 테스트 | 실 작업 + 시각화 |

### 파일 구성

```
src/my_robot_interfaces/src/
├── main_gazebo.py            # 통합 메뉴 진입점
├── robot_move3_gazebo.py     # 관절/직선/원호 제어 (메뉴)
├── pick_and_place_gazebo.py  # 픽앤플레이스 시퀀스
└── object_detect.py          # 카메라 물체 인식

src/e0509_gripper_description/
├── launch/
│   ├── bringup_gazebo.launch.py        # Gazebo 단독
│   └── bringup_real_gazebo.launch.py   # 실제 로봇 + Gazebo
└── scripts/
    ├── gripper_joint_publisher.py
    ├── gripper_service_node.py
    └── gazebo_bridge.py
```

---

## 2. 환경 준비

### 필수 패키지 확인

```bash
# ROS2 Humble 환경 활성화
source /opt/ros/humble/setup.bash
source ~/robot_workspace/doosan_ws/install/setup.bash

# 또는 conda 환경 사용 시
conda activate robot_env
```

### 실제 로봇 네트워크 확인 (모드 B만 해당)

```bash
ping -c 3 <로봇_IP>   # 예: ping -c 3 110.120.1.66
```

응답 없으면 네트워크 설정 확인 후 진행.

---

## 3. 빌드

### 최초 1회 또는 소스 변경 후 실행

```bash
cd ~/robot_workspace/doosan_ws
colcon build --packages-select e0509_gripper_description
source install/setup.bash
```

> **주의:** `CMakeLists.txt`의 `install(PROGRAMS ...)` 에 Python 스크립트가 모두 등록되어 있어야 합니다.  
> 누락된 스크립트가 있으면 `executable '<name>.py' not found` 오류가 발생합니다.  
> 현재 등록된 스크립트 목록은 `src/e0509_gripper_description/CMakeLists.txt`에서 확인하세요.

---

## 4. 실행 모드

### 모드 A: Gazebo 단독 (시뮬레이션만)

실제 로봇 없이 Gazebo 물리 시뮬레이션만 실행합니다.

```bash
ros2 launch e0509_gripper_description bringup_gazebo.launch.py
```

약 10초 후 Gazebo 창에 E0509 로봇이 표시되면 정상.

**컨트롤러 활성화 확인:**

```bash
ros2 control list_controllers --controller-manager /dsr01/controller_manager
```

아래 3개가 `active` 상태이면 준비 완료:

```
joint_state_broadcaster     - active
joint_trajectory_controller - active
gripper_controller          - active
```

**이 모드의 제한:**
- MoveJoint만 가능 (JointTrajectoryController 방식)
- MoveLine, MoveCircle, Fkin 서비스 없음
- 메뉴에서 2, 3, 5번 옵션이 `[비활성]`으로 표시됨

---

### 모드 B: 실제 로봇 + Gazebo 디지털 트윈

실제 로봇을 Doosan 서비스로 제어하고, 동일한 움직임을 Gazebo에서 시각화합니다.

```bash
ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py host:=<로봇_IP>
```

예시:

```bash
ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py host:=110.120.1.66
```

**정상 기동 로그 확인 포인트:**

```
[dsr_hw_interface2]: ROBOT_STATE : STATE_STANDBY      ← 로봇 대기 상태 확인
[dsr_hw_interface2]: Real Robot Mode                  ← 실제 로봇 연결 확인
[dsr_hw_interface2]: Connected RT control stream      ← RT 스트림 연결 확인
```

**기동 완료 후 서비스 확인:**

```bash
ros2 service list | grep "dsr01/motion"
```

아래 서비스들이 보이면 정상:

```
/dsr01/motion/move_joint
/dsr01/motion/move_line
/dsr01/motion/move_circle
/dsr01/motion/fkin
```

> Doosan 서비스가 보이지 않으면 `dsr_controller2` 가 기동되지 않은 것입니다.  
> 트러블슈팅 섹션을 참고하세요.

---

## 5. 제어 프로그램 실행

**새 터미널**에서 실행합니다 (launch는 별도 터미널에서 실행 중이어야 함).

### 통합 메뉴 (권장)

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/main_gazebo.py
```

```
  1: 관절 제어 (MoveJoint + 그리퍼)
  2: 픽앤플레이스 시뮬레이션
  q: 종료
```

### 관절 제어만

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/robot_move3_gazebo.py
```

### 픽앤플레이스만

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/pick_and_place_gazebo.py
```

---

## 6. 메뉴 기능 설명

`robot_move3_gazebo.py` 실행 시 표시되는 메뉴:

```
  0: 현재 위치 확인 (관절 + TCP)
  1: MoveJoint  - 관절 각도 이동
  2: MoveLine   - 직선 이동          ← 모드 B 전용
  3: MoveCircle - 원호 이동          ← 모드 B 전용
  4: 그리퍼 제어 (0=열림 / 700=닫힘)
  5: MoveCircle 자동 (끝점만 입력)   ← 모드 B 전용
```

모드 A(Gazebo 단독)에서는 2, 3, 5번이 `[비활성]` 표시됩니다.

---

### 옵션 0: 현재 위치 확인

엔터를 누르면 현재 관절 각도(도)와 TCP 위치(X/Y/Z/RX/RY/RZ, mm)를 출력합니다.

---

### 옵션 1: MoveJoint

6개 관절 각도를 입력해 이동합니다.

```
6개 관절 각도 입력 (예: 0 0 90 0 90 0): 0 0 90 0 90 0
이동 시간(초, 기본=3.0): 5
```

| 항목 | 설명 |
|------|------|
| 입력 형식 | 공백으로 구분된 6개 실수 (단위: 도) |
| 이동 시간 | 생략 시 3.0초 (느린 이동은 5~10초 권장) |
| 모드 A | JointTrajectoryController 사용 |
| 모드 B | Doosan `/dsr01/motion/move_joint` 서비스 사용 |

**안전 자세 예시:**

```
0 0 90 0 90 0
```

---

### 옵션 2: MoveLine (모드 B 전용)

현재 자세를 유지하면서 목표 XYZ 좌표로 직선 이동합니다.

```
목표 위치 입력 (X Y Z, 자세 유지): 400 0 300
```

또는 자세까지 지정:

```
목표 위치 입력 (X Y Z, 자세 유지): 400 0 300 45 180 45
```

| 항목 | 설명 |
|------|------|
| 단위 | mm (XYZ), 도 (RX/RY/RZ) |
| 3개 입력 | 현재 자세(RX/RY/RZ) 유지 |
| 6개 입력 | 자세까지 지정 |

**작업 공간 (E0509 기준):**

| 축 | 안전 범위 |
|----|---------|
| X | 200 ~ 600 mm |
| Y | -300 ~ 300 mm |
| Z | 150 ~ 700 mm |

> 홈 자세(모든 관절 0°)에서 직선/원호 이동 시 특이점(Singularity) 오류가 발생합니다.  
> 반드시 `0 0 90 0 90 0` 안전 자세로 이동 후 Cartesian 제어를 시작하세요.

---

### 옵션 3: MoveCircle (모드 B 전용)

경유점과 끝점을 입력해 원호 이동합니다.

```
경유점 입력 (X Y Z, 자세 유지): 400 100 300
끝점 입력  (X Y Z, 자세 유지): 400 -100 300
```

---

### 옵션 4: 그리퍼 제어

```
그리퍼 값 입력 (0~700): 350
```

| 값 | 상태 |
|----|------|
| `0` | 완전 열림 |
| `350` | 절반 |
| `700` | 완전 닫힘 |

**모드별 동작 방식:**

모드 B (실제 로봇 + Gazebo):
```
set_gripper(350)
  → /dsr01/gripper/position_cmd (Int32: 350)
  → gripper_service_node.py → 실제 로봇 Modbus RTU
  → /dsr01/gripper/stroke 발행
  → gripper_joint_publisher.py → /dsr01/joint_states 업데이트 (RViz)
  → gazebo_bridge.py → /gz/gripper_controller/commands (Gazebo 미러링)
```

모드 A (Gazebo 단독):
```
set_gripper(350)
  → /dsr01/gripper_controller/commands (Float64MultiArray: [0.5, 0.5, 0.5, 0.5])
```

---

### 옵션 5: MoveCircle 자동 (모드 B 전용)

끝점만 입력하면 현재 위치에서 자동으로 경유점을 계산해 원호 이동합니다.

```
끝점 입력 (X Y Z): 500 200 300
```

---

## 7. 픽앤플레이스 웨이포인트 교정

`pick_and_place_gazebo.py`는 관절 각도 웨이포인트 기반으로 동작합니다.  
실제 환경에 맞게 반드시 교정이 필요합니다.

### 웨이포인트 위치

`pick_and_place_gazebo.py` 상단 클래스 변수:

```python
SAFE_JOINTS           = [  0.0,   0.0,  90.0,  0.0,  90.0,  0.0]  # 안전 자세
PICK_APPROACH_JOINTS  = [  0.0, -20.0,  80.0,  0.0, 110.0,  0.0]  # 물체 위 접근
PICK_JOINTS           = [  0.0, -30.0,  85.0,  0.0, 115.0,  0.0]  # 물체 픽업
PLACE_APPROACH_JOINTS = [ 45.0, -20.0,  80.0,  0.0, 110.0,  0.0]  # 목표 위 접근
PLACE_JOINTS          = [ 45.0, -30.0,  85.0,  0.0, 115.0,  0.0]  # 물체 놓기
```

> 위 기본값은 예시이며 실제 로봇/환경에 맞지 않을 수 있습니다.

### 교정 순서

**1단계 — 원하는 위치 탐색:**

```bash
python3 robot_move3_gazebo.py
# 옵션 1로 MoveJoint 반복하며 원하는 위치 탐색
# 옵션 0으로 현재 관절 각도 확인
```

**2단계 — 웨이포인트 수정:**

확인한 관절 각도를 `pick_and_place_gazebo.py`의 각 변수에 입력합니다.

**3단계 — 물체/목표 위치 수정 (RViz 마커용):**

```python
OBJECT_POS = [400.0,   0.0,  0.0]   # 물체 위치 (mm)
PLACE_POS  = [300.0, 200.0,  0.0]   # 목표 위치 (mm)
```

### 픽앤플레이스 시퀀스

| 단계 | 동작 |
|------|------|
| 1 | 안전 자세 이동 |
| 2 | 그리퍼 열기 |
| 3 | 물체 위 접근 |
| 4 | 물체로 하강 |
| 5 | 그리퍼 닫기 → 마커 주황→초록 |
| 6 | 들어올리기 |
| 7 | 목표 위치로 이동 |
| 8 | 물체 내려놓기 |
| 9 | 그리퍼 열기 → 마커 초록→주황 |
| 10 | 후퇴 |
| 11 | 안전 자세 복귀 |

---

## 8. 트러블슈팅

### executable '<name>.py' not found

**증상:**
```
[ERROR]: executable 'gripper_service_node.py' not found on the libexec directory
```

**원인:** `CMakeLists.txt`의 `install(PROGRAMS ...)` 목록에 해당 스크립트 누락.

**해결:**
```cmake
# CMakeLists.txt
install(PROGRAMS
  scripts/gripper.py
  scripts/gripper_joint_publisher.py
  scripts/gripper_service_node.py
  scripts/gazebo_bridge.py
  scripts/digital_twin_bridge.py
  scripts/robot_slider_control.py
  scripts/curobo_planner_node.py
  scripts/marker_tracking_node.py
  scripts/object_tracking_node.py
  DESTINATION lib/${PROJECT_NAME}
)
```

```bash
colcon build --packages-select e0509_gripper_description
source install/setup.bash
```

---

### Doosan 서비스가 없음 (MoveLine/MoveCircle 비활성)

**증상:** 메뉴에서 2, 3, 5번이 `[비활성]`으로 표시됨.

**확인:**
```bash
ros2 service list | grep "dsr01/motion"
```

아무것도 안 나오면 `dsr_controller2`가 미실행 상태.

**원인 및 해결:**

| 원인 | 해결 |
|------|------|
| 모드 A로 실행 중 | 모드 B(`bringup_real_gazebo.launch.py`)로 재실행 |
| 실제 로봇 연결 실패 | `ping <로봇_IP>` 확인, 네트워크 점검 |
| 기동 시간 부족 | launch 후 20~30초 대기 후 재확인 |

---

### joint_states 수신 실패

**증상:** 옵션 0 실행 시 `[현재 위치] joint_states 수신 실패`

**확인:**
```bash
ros2 topic echo /dsr01/joint_states --once
```

**원인 및 해결:**

| 원인 | 해결 |
|------|------|
| 로봇이 에러 상태 | 아래 프로세스 전체 재시작 |
| launch 아직 기동 중 | 30초 대기 후 재시도 |

---

### 로봇 에러 상태 완전 초기화

관절이 움직이지 않거나, joint_states가 0으로만 나오거나, 로봇이 보호 정지(띡 소리)된 경우:

**1단계 — 모든 ROS 프로세스 종료**

```bash
pkill -9 -f "ros2_control_node|run_emulator|robot_state_publisher|rviz2|spawner|gripper"
pkill -9 -f "gz_sim|gazebo_bridge|dsr"
sleep 5
```

**2단계 — 티치 펜던트(TP) 에러 해제**

TP 화면에서 에러 코드 확인 → `확인 / Reset` 버튼으로 클리어 → `STANDBY` 상태 복귀 확인.

**3단계 — 재시작**

```bash
ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py host:=<로봇_IP>
```

> `ros2 daemon stop/start`로는 해결되지 않습니다. 반드시 `pkill`로 프로세스를 종료하세요.

---

### joint_trajectory_controller가 inactive

```bash
ros2 control switch_controllers \
  --activate joint_trajectory_controller \
  --controller-manager /dsr01/controller_manager
```

---

### MoveJoint가 타임아웃

`duration_sec` 값이 너무 짧은 경우. 큰 각도 이동 시 5~10초 권장.

---

### 로봇이 갑자기 꺼짐 (보호 정지)

**증상:** 이동 중 "띡" 소리와 함께 로봇 전원이 꺼짐. Gazebo 재시작 시 "딱딱딱딱" 소리.

**원인:** MoveJoint는 현재 관절 각도에서 목표 각도까지 관절 공간에서 직선 보간합니다. 중간 경로가 자기 충돌 또는 관절 한계를 통과하면 로봇이 보호 정지합니다.

**대표적인 위험 패턴:**

| 상황 | 위험 이유 |
|------|---------|
| Cartesian 이동 후 MoveJoint로 안전 자세 복귀 | 직전 관절 상태에 따라 경로 중간에 충돌 발생 가능 |
| 홈 자세(0 0 0 0 0 0)에서 Cartesian 이동 | 특이점(Singularity) 오류 |
| 이동 시간이 너무 짧아 고속 이동 | 충돌 감지 트리거 |

**안전한 안전 자세 복귀 방법:**

한 번에 이동하지 않고 중간 자세를 거쳐 이동하세요.

```
현재 위치 → [0 0 45 0 90 0] → [0 0 90 0 90 0]
```

또는 이동 시간을 충분히 길게 설정하세요:

```
이동 시간(초, 기본=3.0): 8
```

---

## 9. 토픽 · 서비스 레퍼런스

### 토픽 — 공통

| 토픽 | 타입 | 용도 |
|------|------|------|
| `/dsr01/joint_states` | `sensor_msgs/JointState` | 현재 관절 각도 수신 |
| `/object_marker` | `visualization_msgs/Marker` | RViz 물체 마커 |

**관절 이름:** `joint_1` ~ `joint_6`  
**그리퍼 관절:** `gripper_rh_r1`, `gripper_rh_r2`, `gripper_rh_l1`, `gripper_rh_l2`

### 토픽 — 모드 A (Gazebo 단독)

| 토픽 | 타입 | 용도 |
|------|------|------|
| `/dsr01/joint_trajectory_controller/joint_trajectory` | `trajectory_msgs/JointTrajectory` | 관절 이동 명령 |
| `/dsr01/gripper_controller/commands` | `std_msgs/Float64MultiArray` | 그리퍼 (0.0~1.0 rad, 4개 값) |

### 토픽 — 모드 B (실제 로봇 + Gazebo)

| 토픽 | 타입 | 용도 |
|------|------|------|
| `/dsr01/gripper/position_cmd` | `std_msgs/Int32` | 그리퍼 위치 명령 (0~700) |
| `/dsr01/gripper/stroke` | `std_msgs/Int32` | 현재 그리퍼 stroke (gripper_service_node 발행) |
| `/gz/joint_trajectory_controller/joint_trajectory` | `trajectory_msgs/JointTrajectory` | Gazebo 팔 미러링 (gazebo_bridge 발행) |
| `/gz/gripper_controller/commands` | `std_msgs/Float64MultiArray` | Gazebo 그리퍼 미러링 (gazebo_bridge 발행) |

### Doosan 서비스 (모드 B 전용)

| 서비스 | 타입 | 용도 |
|--------|------|------|
| `/dsr01/motion/move_joint` | `dsr_msgs2/MoveJoint` | 관절 각도 이동 |
| `/dsr01/motion/move_line` | `dsr_msgs2/MoveLine` | 직선 이동 |
| `/dsr01/motion/move_circle` | `dsr_msgs2/MoveCircle` | 원호 이동 |
| `/dsr01/motion/fkin` | `dsr_msgs2/Fkin` | 순기구학 (관절→TCP) |
| `/dsr01/gripper/open` | `std_srvs/Trigger` | 그리퍼 열기 |
| `/dsr01/gripper/close` | `std_srvs/Trigger` | 그리퍼 닫기 |

### 수동 명령 예시

```bash
# 관절 상태 확인
ros2 topic echo /dsr01/joint_states --once

# 그리퍼 열기 (모드 A)
ros2 topic pub /dsr01/gripper_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0]}" --once

# 그리퍼 닫기 (모드 A)
ros2 topic pub /dsr01/gripper_controller/commands \
  std_msgs/msg/Float64MultiArray "{data: [1.0, 1.0, 1.0, 1.0]}" --once

# 그리퍼 위치 명령 (모드 B - 0~700)
ros2 topic pub /dsr01/gripper/position_cmd std_msgs/msg/Int32 "{data: 350}" --once

# 그리퍼 열기 서비스 (모드 B)
ros2 service call /dsr01/gripper/open std_srvs/srv/Trigger

# 그리퍼 닫기 서비스 (모드 B)
ros2 service call /dsr01/gripper/close std_srvs/srv/Trigger

# 컨트롤러 목록 확인
ros2 control list_controllers --controller-manager /dsr01/controller_manager
```
