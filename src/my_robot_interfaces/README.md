# my_robot_interfaces 실행 가이드

## 0. 패키지 처음 만들기

### 0-1. 워크스페이스 및 패키지 생성

```bash
# 워크스페이스 폴더 생성
mkdir -p ~/robot_workspace/doosan_ws/src
cd ~/robot_workspace/doosan_ws/src

# 패키지 생성 (CMake 타입)
ros2 pkg create my_robot_interfaces --build-type ament_cmake
```

---

### 0-2. msg / srv 폴더 및 파일 생성

```bash
cd ~/robot_workspace/doosan_ws/src/my_robot_interfaces
mkdir msg srv src
```

**msg/TurtleStatus.msg** 파일 생성 후 아래 내용 작성:

```
float64 distance_to_wall    # 벽까지의 남은 거리
string current_state        # 로봇의 상태 (예: NORMAL, WARN, STOP)
bool is_moving              # 이동 중 여부
```

**srv/SetTurtleMode.srv** 파일 생성 후 아래 내용 작성:

```
string mode_name
float64 target_speed
---
bool success
string message
```

---

### 0-3. CMakeLists.txt 수정

`cmake_minimum_required` 아래에 아래 내용이 있는지 확인하고 없으면 추가:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TurtleStatus.msg"
  "srv/SetTurtleMode.srv"
)

ament_package()
```

> **주의**: 각 명령어 끝에 닫는 괄호 `)` 빠지지 않도록 주의. nano로 붙여넣기 권장.

---

### 0-4. package.xml 수정

`<buildtool_depend>ament_cmake</buildtool_depend>` 아래에 추가:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

---

### 0-5. 빌드 및 소스

```bash
cd ~/robot_workspace/doosan_ws
colcon build --packages-select my_robot_interfaces
source install/setup.bash
```

빌드 성공 확인:

```bash
ros2 interface list | grep my_robot_interfaces
```

---

## 1. 로봇 엔진 가동

```bash
# 실물 로봇
ros2 launch e0509_gripper_description bringup.launch.py mode:=real host:=110.120.1.39

# 가상 로봇
ros2 launch e0509_gripper_description bringup.launch.py mode:=virtual
```

---

## 1. 빌드

```bash
cd ~/robot_workspace/doosan_ws
colcon build --packages-select my_robot_interfaces
source install/setup.bash
```

---

## 2. 파일별 실행 명령어

### gripper1.py — 그리퍼 단순 제어 (1/2/q 입력)

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/gripper1.py
```

| 입력 | 동작 |
|------|------|
| `1`  | 그리퍼 열기 (값: 0) |
| `2`  | 그리퍼 닫기 (값: 700) |
| `q`  | 종료 |

---

### gripper2.py — 그리퍼 정밀 제어 (0~700 직접 입력)

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/gripper2.py
```

| 입력 | 동작 |
|------|------|
| `0`  | 완전 열림 |
| `700`| 완전 닫힘 |
| 중간값 | 부분 개폐 |
| `q`  | 종료 |

---

### robot_move1.py — 관절 각도 입력 이동

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/robot_move1.py
```

실행 후 6개 관절 각도를 공백으로 구분해서 입력:

```
6개 관절 각도를 입력하세요 (예: 0 0 90 0 90 0):
```

**관절 각도 부호 규칙** (각 관절을 정면에서 봤을 때 기준):

| 부호 | 방향 |
|------|------|
| `+`  | 반시계 방향 |
| `-`  | 시계 방향 |

> 예: `-90` → 해당 관절이 원점(0도) 기준으로 시계 방향 90도 위치로 이동  
> MoveJoint는 **절대 각도** 기준이므로 현재 위치와 무관하게 지정한 각도로 이동함

---

### robot_move2.py — 순차 관절 이동 매니저

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/robot_move2.py
```

| 입력 | 동작 |
|------|------|
| `S`  | 순차 이동 시작 (J5→J6→J4→J3→J2→J1 순서) |
| `1`~`6` | 해당 관절 각도 직접 수정 |
| `R`  | 각도 초기화 (0, 0, 90, 0, 90, 0) |
| `Q`  | 종료 |

---

### robot_move3.py — 통합 로봇 제어 (Joint + Line + Circle + 그리퍼)

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/robot_move3.py
```

하나의 클래스(`E0509RobotController`)에 모든 서비스/토픽을 통합:

| 선택 | 서비스/토픽 | 동작 |
|------|------------|------|
| `1` | `MoveJoint` | 관절 6개 각도로 이동 |
| `2` | `MoveLine` | 직선 이동 (XYZ + RX RY RZ) |
| `3` | `MoveCircle` | 원호 이동 (경유점 + 끝점) |
| `4` | 그리퍼 publisher | 그리퍼 위치 설정 (0~700) |
| `q` | — | 종료 |

**MoveJoint 입력 예시:**
```
6개 관절 각도 입력 (예: 0 0 90 0 90 0):
```

**MoveLine 입력 예시:**
```
목표 위치 입력 (X Y Z RX RY RZ): 500 0 300 0 0 0
```

> RX, RY, RZ는 말단의 자세(회전)를 도(degree) 단위로 지정. 자세 유지 시 시작점과 동일하게 입력.

**MoveCircle 입력 예시:**
```
경유점 입력 (X Y Z RX RY RZ): 400 100 300 0 0 0
끝점 입력  (X Y Z RX RY RZ): 300 0   300 0 0 0
```

> 경유점은 시작~끝 호의 중간 지점. 세 점이 일직선이 되면 원을 정의할 수 없으므로 주의.

**그리퍼 입력 예시:**
```
그리퍼 값 입력 (0~700): 350
```

| 값 | 상태 |
|----|------|
| `0` | 완전 열림 |
| `350` | 절반 |
| `700` | 완전 닫힘 |

---

### pick_and_place.py — 픽앤플레이스 시뮬레이션

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/pick_and_place.py
```

RViz에 물체(주황 큐브)를 표시하고 로봇이 집어서 다른 위치에 옮기는 시뮬레이션.

**실행 전 RViz 설정:**
1. RViz 좌측 `Add` 버튼 클릭
2. `By topic` → `/object_marker` → `Marker` 선택
3. `Fixed Frame`을 `base_link` 로 설정

**동작 순서:**

| 단계 | 동작 |
|------|------|
| 1 | 안전 자세로 이동 (0 0 90 0 90 0) |
| 2 | 그리퍼 열기 |
| 3~4 | 물체 위 접근 후 하강 |
| 5 | 그리퍼 닫기 → 물체 색상 주황→초록 변경 |
| 6~8 | 들어올리기 → 목표 f위치 이동 → 하강 |
| 9 | 그리퍼 열기 → 물체 목표 위치에 고정 |
| 10~11 | 후퇴 후 안전 자세 복귀 |

**파라미터 수정** (`pick_and_place.py` 상단):
```python
OBJECT_POS = [400.0,   0.0, 200.0]   # 물체 초기 위치 (mm)
PLACE_POS  = [300.0, 200.0, 200.0]   # 놓을 목표 위치 (mm)
APPROACH_H = 100.0                    # 접근/후퇴 Z 오프셋 (mm)
ORIENT     = [45.0, 180.0, 45.0]     # TCP 자세 (RX RY RZ)
```

> 좌표는 작업 공간 안내(2-1)의 권장 범위 내에서 설정할 것.

---

## 2-1. E0509 작업 공간 (Workspace) 안내

최대 도달 거리: **900mm** (베이스 원점 기준)

### 권장 좌표 범위

| 축 | 권장 범위 | 비고 |
|----|-----------|------|
| X | 200 ~ 600 mm | 로봇 정면 방향 |
| Y | -300 ~ 300 mm | 좌우 |
| Z | 150 ~ 700 mm | 높이 |
| 원점 거리 | 300 ~ 750 mm | √(X²+Y²+Z²) 기준 |

> 원점 거리 = √(X²+Y²+Z²). 900mm에 가까울수록 도달 불가 가능성 높아짐.

### Cartesian 이동 시 주의사항

- **반드시 MoveJoint로 먼저 안전 자세로 이동 후** MoveLine/MoveCircle 사용
  ```
  권장 시작 자세: MoveJoint → 0 0 90 0 90 0
  이때 TCP 위치: X=373, Y=0, Z=405, RX=45, RY=180, RZ=45
  ```
- 홈 포지션(모든 관절 0도, Z≈1123)에서 Cartesian 이동을 시도하면 **특이점(Singularity)** 문제로 실패함
- `success=True`를 반환해도 실제로 움직이지 않을 수 있음 (좌표 범위 초과 또는 특이점 근처)
- 처음에는 현재 위치에서 50~100mm 이내의 짧은 이동부터 테스트 권장

### 테스트 예시 순서

```
1. 옵션 1 → 0 0 90 0 90 0          (안전 자세로 이동)
2. 옵션 0 → 현재 TCP 위치 확인     (X≈373, Y≈0, Z≈405 확인)
3. 옵션 5 → 450 100 450             (근거리 원호 이동 테스트)
4. 옵션 2 → 430 50 430              (근거리 직선 이동 테스트)
```

---

## 2-2. 가상 로봇 트러블슈팅

### 증상: RViz가 움직이지 않거나 joint_states가 계속 0

**원인**: 충돌 / 관절 한계 초과 에러 발생 시 에뮬레이터 내부 상태가 깨져서 `GetCurrentPose()`가 0을 반환함.

**해결**: 모든 프로세스를 완전히 종료 후 재시작 (단순 Ctrl+C 후 재시작은 불충분)

```bash
# 1. 관련 프로세스 전체 강제 종료
pkill -9 -f "ros2_control_node|run_emulator|robot_state_publisher|rviz2|spawner|gripper"
sleep 3

# 2. 재시작
ros2 launch e0509_gripper_description bringup.launch.py mode:=virtual
```

> `ros2 daemon stop/start`는 discovery 데몬만 재시작하며 로봇 프로세스에 영향 없음.

### joint_state_broadcaster 자동 실행

launch 파일에 `joint_state_broadcaster` 자동 활성화가 포함되어 있어 수동 실행 불필요.  
재시작 후 약 **15초** 대기하면 자동으로 올라옴.

수동으로 확인하려면:
```bash
ros2 control list_controllers --controller-manager /dsr01/controller_manager
```

`joint_state_broadcaster - active` 상태이면 정상.

### 증상: `Failed to configure controller` 에러

에뮬레이터가 완전히 뜨기 전에 controller_manager가 붙으려다 실패하는 타이밍 문제.  
위의 완전 재시작 절차를 따르면 해결됨.

### 증상: `success=True`인데 로봇이 안 움직임

Doosan API는 명령 수신 시점에 `True`를 반환하며, 실제 실패는 컨트롤러 로그의 WARN으로만 나타남.

```bash
# 컨트롤러 로그에서 에러 확인
# [WARN] ... param : [ERR] Pose(...) is NOT REACHABLE  ← 좌표 범위 초과
# [WARN] ... index : 9008  ← 관절 한계 초과
```

---

## 3. 토픽/서비스 확인 명령어

```bash
# 토픽 목록 확인 (gripper_cmd 있는지 확인)
ros2 topic list

# 그리퍼 토픽 신호 모니터링
ros2 topic echo /dsr01/gripper/position_cmd

# 그리퍼 수동 명령 (터미널에서 바로 보내기)
ros2 topic pub /dsr01/gripper/position_cmd std_msgs/msg/Int32 "{data: 350}" --once

# 그리퍼 열기/닫기 서비스 호출
ros2 service call /dsr01/gripper/open std_srvs/srv/Trigger
ros2 service call /dsr01/gripper/close std_srvs/srv/Trigger
```
