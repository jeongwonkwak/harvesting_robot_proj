# E0509 두산 로봇 + Gazebo 시뮬레이션 셋업 메뉴얼

> 대상 환경: **Ubuntu 22.04 LTS** | **ROS2 Humble** | **Gazebo Fortress(Ignition)**

---

## 목차

1. [사전 준비](#1-사전-준비)
2. [Anaconda 설치](#2-anaconda-설치)
3. [Conda 가상환경 생성](#3-conda-가상환경-생성)
4. [ROS2 Humble 설치](#4-ros2-humble-설치)
5. [워크스페이스 생성 및 패키지 클론](#5-워크스페이스-생성-및-패키지-클론)
6. [커스텀 인터페이스 패키지 생성](#6-커스텀-인터페이스-패키지-생성)
7. [의존성 설치 및 빌드](#7-의존성-설치-및-빌드)
8. [환경 변수 설정](#8-환경-변수-설정)
9. [Gazebo 시뮬레이션 실행](#9-gazebo-시뮬레이션-실행)
10. [동작 확인](#10-동작-확인)
11. [프로세스 종료 및 재시작](#11-프로세스-종료-및-재시작)
12. [트러블슈팅](#12-트러블슈팅)

---

## 1. 사전 준비

### 시스템 패키지 업데이트

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget build-essential
```

### GPU 드라이버 확인 (선택사항 — cuRobo 사용 시 필요)

```bash
nvidia-smi
```

---

## 2. Anaconda 설치

> 이미 설치되어 있으면 이 단계를 건너뛰세요.

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
bash Anaconda3-2024.02-1-Linux-x86_64.sh
```

설치 후 터미널 재시작 또는:

```bash
source ~/.bashrc
```

---

## 3. Conda 가상환경 생성

```bash
conda create -n robot_env python=3.10 -y
conda activate robot_env
```

필요 패키지 설치:

```bash
pip install colcon-common-extensions catkin-pkg empy lark
pip install ultralytics          # YOLO (비전 기능 사용 시)
pip install PyQt5 matplotlib     # 모니터링 GUI 사용 시
```

> **주의**: 이후 모든 작업은 `(robot_env)` 가상환경 활성화 상태에서 진행합니다.

---

## 4. ROS2 Humble 설치

> 이미 설치되어 있으면 이 단계를 건너뛰세요.

### ROS2 apt 저장소 등록

```bash
sudo apt update
sudo apt update && sudo apt install curl gnupg2 lsb-release -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### rosdep 설치

```bash
sudo apt update
sudo apt install python3-rosdep -y
```

### colcon 설치

```bash
# 패키지 목록 업데이트
sudo apt update
iss
# colcon 및 관련 확장 도구 설치
sudo apt install python3-colcon-common-extensions -y
```

### ROS2 Humble 설치

```bash
sudo apt install -y ros-humble-desktop ros-dev-tools
source /opt/ros/humble/setup.bash
```

### rosdep 초기화

```bash
sudo rosdep init
rosdep update
```

### Gazebo Fortress 설치

```bash
sudo apt install -y ignition-fortress
```

### ROS2-Gazebo 브릿지 설치

```bash
sudo apt install -y ros-humble-ros-ign-bridge \
                    ros-humble-ros-gz-bridge \
                    ros-humble-joint-state-publisher \
                    ros-humble-joint-state-publisher-gui \
                    ros-humble-robot-state-publisher \
                    ros-humble-xacro \
                    ros-humble-ros2-controllers \
                    ros-humble-ros2-control \
                    ros-humble-ign-ros2-control
```

---

## 5. 워크스페이스 생성 및 패키지 클론

### 워크스페이스 생성

```bash
mkdir -p ~/robot_workspace/doosan_ws/src
cd ~/robot_workspace/doosan_ws/src
```

### 패키지 클론

```bash
# 1. 두산 로봇 패키지 (gripper 제어 기능이 포함된 포크 버전)
git clone -b humble https://github.com/fhekwn549/doosan-robot2.git

# 2. ROBOTIS RH-P12-RN-A 그리퍼
git clone https://github.com/ROBOTIS-GIT/RH-P12-RN-A.git

# 3. E0509 + 그리퍼 통합 패키지
git clone https://github.com/fhekwn549/e0509_gripper_description.git
```

> **중요**: 공식 두산 패키지(`doosan-robot`) 대신 위 포크 버전을 사용해야 합니다.
> 포크 버전에는 Flange Serial 기반 그리퍼 제어 서비스가 포함되어 있습니다.

클론 후 구조:

```
~/robot_workspace/doosan_ws/src/
├── doosan-robot2/
├── RH-P12-RN-A/
└── e0509_gripper_description/
```

---

## 6. 커스텀 인터페이스 패키지 생성

ROS2에서 직접 만든 메시지(`.msg`), 서비스(`.srv`), 액션(`.action`)을 사용하려면 전용 패키지를 만들어야 합니다.

### 패키지 구조

```
my_robot_interfaces/
├── CMakeLists.txt       # 빌드 설정 (가장 중요!)
├── package.xml          # 의존성 관리
├── msg/                 # 데이터 구조 (.msg) 폴더
│   └── TurtleStatus.msg
├── srv/                 # 서비스 규격 (.srv) 폴더
│   └── SetTurtleMode.srv
└── action/              # 액션 규격 (.action) 폴더
    └── MoveRobot.action
```

---

### Step 1. 패키지 생성

```bash
cd ~/robot_workspace/doosan_ws/src
ros2 pkg create --build-type ament_cmake my_robot_interfaces
cd my_robot_interfaces
```

**패키지 작명 가이드라인**

| 규칙 | 예시 |
|------|------|
| 소문자만 사용 | `my_robot` (O) &nbsp; `My_Robot` (X) |
| 단어 구분은 언더바(`_`) | snake_case (O) &nbsp; camelCase (X) |
| 숫자로 시작 불가 | `robot1` (O) &nbsp; `1robot` (X) |
| 하이픈·공백·마침표 불가 | `my_robot` (O) &nbsp; `my-robot` (X) |

**역할별 패키지 이름 관례**

| 역할 | 권장 이름 | 설명 |
|------|-----------|------|
| 인터페이스 전용 | `[이름]_interfaces` | `.msg` `.srv` `.action` 파일만 모음 |
| 메인 로직/노드 | `[이름]_py` / `[이름]_cpp` | 실제 알고리즘·노드 구현 |
| 실행 설정 | `[이름]_bringup` | 여러 노드를 한 번에 실행하는 launch 파일 모음 |
| 로봇 모델 | `[이름]_description` | URDF, Mesh 등 외형 정보 |

---

### Step 2. 디렉토리 생성

```bash
mkdir msg srv action
```

---

### Step 3. 인터페이스 파일 생성

```bash
touch msg/TurtleStatus.msg
touch srv/SetTurtleMode.srv
```

**msg/TurtleStatus.msg** 내용 작성:

```bash
nano msg/TurtleStatus.msg
```

```
float64 distance_to_wall    # 벽까지의 남은 거리
string  current_state       # 로봇의 상태 (예: NORMAL, WARN, STOP)
bool    is_moving           # 이동 중 여부
```

---

### Step 4. package.xml 수정

`<buildtool_depend>ament_cmake</buildtool_depend>` 아래에 추가:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

| 태그 | 역할 |
|------|------|
| `rosidl_default_generators` | `.msg` `.srv` 파일을 C++/Python 코드로 변환하는 빌드 타임 도구 |
| `rosidl_default_runtime` | 생성된 메시지를 노드 실행 중에 주고받을 수 있게 하는 런타임 라이브러리 |
| `rosidl_interface_packages` | 이 패키지를 인터페이스 그룹으로 등록해 빌드 시스템이 우선 스캔 |

---

### Step 5. CMakeLists.txt 수정

전체 내용을 아래로 교체합니다:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. 필수 빌드 도구 불러오기
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 2. 메시지/서비스 파일 등록
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TurtleStatus.msg"
  "srv/SetTurtleMode.srv"
  # 추가 파일이 있으면 여기에 계속 추가
)

# 3. 패키지 내보내기 (항상 마지막에 위치)
ament_package()
```

> **주의**: `ament_package()`는 반드시 파일의 가장 마지막에 있어야 합니다.

---

### Step 6. 빌드 및 확인

```bash
cd ~/robot_workspace/doosan_ws
colcon build --packages-select my_robot_interfaces
source install/setup.bash

# 메시지가 정상 등록됐는지 확인
ros2 interface show my_robot_interfaces/msg/TurtleStatus
```

정상 출력 예시:

```
float64 distance_to_wall
string current_state
bool is_moving
```

---

## 7. 의존성 설치 및 빌드

```bash
cd ~/robot_workspace/doosan_ws

# ROS2 의존성 자동 설치
rosdep install --from-paths src --ignore-src -r -y

# 빌드
colcon build --symlink-install
```

> 빌드 시간: 약 3~10분 (PC 사양에 따라 다름)

빌드 성공 확인:

```bash
# 아래와 같이 출력되면 정상
# Summary: X packages finished [X min Xs]
```

---

## 8. 환경 변수 설정

`~/.bashrc` 파일에 아래 내용을 추가합니다:

```bash
# ROS2 Humble
export ROS_DISTRO='humble'
source /opt/ros/humble/setup.bash

# 워크스페이스
source ~/robot_workspace/doosan_ws/install/setup.bash

# Gazebo 리소스 경로
export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:\
~/robot_workspace/doosan_ws/install/rh_p12_rn_a_description/share:\
~/robot_workspace/doosan_ws/install/dsr_description2/share

# ROS 도메인 ID (같은 네트워크의 다른 ROS 노드와 충돌 방지)
export ROS_DOMAIN_ID=99
```

설정 적용:

```bash
source ~/.bashrc
```

---

## 9. Gazebo 시뮬레이션 실행

### 가상 로봇 모드 (권장 — 실제 로봇 없이 시뮬레이션)

```bash
conda activate robot_env
ros2 launch e0509_gripper_description bringup.launch.py mode:=virtual
```

### 실제 로봇 연결 모드

```bash
ros2 launch e0509_gripper_description bringup.launch.py mode:=real host:=<로봇_IP주소>
```

### RViz 시각화만 보기

```bash
ros2 launch e0509_gripper_description display.launch.py
```

---

## 10. 동작 확인

### 서비스 목록 확인

```bash
ros2 service list | grep dsr01
```

아래 서비스들이 보이면 정상:

```
/dsr01/motion/move_joint
/dsr01/motion/move_line
/dsr01/motion/move_circle
/dsr01/motion/fkin
/dsr01/gripper/open
/dsr01/gripper/close
```

### 토픽 확인

```bash
ros2 topic list | grep dsr01
```

### 그리퍼 테스트

```bash
# 그리퍼 열기
ros2 service call /dsr01/gripper/open std_srvs/srv/Trigger

# 그리퍼 닫기
ros2 service call /dsr01/gripper/close std_srvs/srv/Trigger

# 위치 제어 (0=열림, 700=닫힘)
ros2 topic pub --once /dsr01/gripper/position_cmd std_msgs/msg/Int32 "{data: 350}"
```

### 로봇 제어 스크립트 실행

```bash
cd ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src
python3 robot_move3_gazebo.py
```

---

## 11. 프로세스 종료 및 재시작

Gazebo나 ROS2 노드가 비정상 종료되거나 재시작이 필요할 때 사용합니다.

아래 스크립트 한 번으로 프로세스 종료 → FastDDS 공유 메모리 정리 → daemon 재시작 → launch 까지 자동 처리됩니다.

```bash
cd ~/robot_workspace/doosan_ws
./restart.sh              # 기본 IP (110.120.1.66)
./restart.sh 192.168.x.x  # 다른 IP 지정 시
```

**스크립트 내용** (`restart.sh`):

```bash
#!/bin/bash
# 1. 모든 관련 프로세스 종료
pkill -9 -f "ros2_control_node|robot_state_publisher|rviz2|gazebo_bridge|gripper_joint_publisher|gripper_service_node|spawner|ign_gazebo|gz_sim|grasp_pipeline|realsense" 2>/dev/null
pkill -9 -f "ign_gazebo_server|ign_gazebo_gui|ruby" 2>/dev/null
sleep 1

# 2. FastDDS 공유 메모리 정리 (재시작 후 open_and_lock_file failed 오류 방지)
rm -f /dev/shm/fastrtps_* 2>/dev/null

# 3. ROS2 daemon 재시작
ros2 daemon stop
sleep 1
ros2 daemon start
sleep 2

# 4. launch 시작
source /opt/ros/humble/setup.bash
source ~/robot_workspace/doosan_ws/install/setup.bash
ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py mode:=real host:=${1:-110.120.1.66}
```

---

## 12. 트러블슈팅

### 빌드 실패 — 의존성 없음

```bash
# 누락된 패키지 확인 후 개별 설치
sudo apt install ros-humble-<패키지명>
```

### Gazebo 실행 시 화면이 안 뜸

```bash
# IGN_GAZEBO_RESOURCE_PATH 확인
echo $IGN_GAZEBO_RESOURCE_PATH

# 경로가 비어 있으면 환경변수 재설정 후 재시작
source ~/.bashrc
```

### 서비스가 안 뜸 (`ros2 service list`에 없음)

```bash
# launch가 정상 실행 중인지 확인
ros2 node list

# 노드가 없으면 mode:=virtual 옵션 확인 후 재실행
ros2 launch e0509_gripper_description bringup.launch.py mode:=virtual
```

### `colcon build` 후 패키지 못 찾음

```bash
# install/setup.bash 재소싱
source ~/robot_workspace/doosan_ws/install/setup.bash
```

### conda 환경과 ROS2 충돌

```bash
# robot_env 활성화 상태인지 확인
conda activate robot_env

# ROS2가 제대로 소싱됐는지 확인
echo $ROS_DISTRO   # humble 이 출력되어야 함
```

---

## 참고 레포지토리

| 패키지 | 주소 |
|--------|------|
| e0509_gripper_description | https://github.com/fhekwn549/e0509_gripper_description |
| doosan-robot2 (포크) | https://github.com/fhekwn549/doosan-robot2 |
| RH-P12-RN-A | https://github.com/ROBOTIS-GIT/RH-P12-RN-A |
