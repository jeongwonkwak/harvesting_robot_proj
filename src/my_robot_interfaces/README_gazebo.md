# Gazebo 버전 실행 가이드

## virtual(RViz) vs Gazebo 차이점

| 항목 | virtual / RViz | Gazebo |
|------|---------------|--------|
| 물리 시뮬레이션 | ❌ | ✅ |
| 이동 방식 | Doosan 전용 서비스 | JointTrajectoryController |
| 직선/원호 이동 | ✅ | MoveIt2 필요 |
| 관절 이동 | ✅ | ✅ |
| 그리퍼 제어 | `/dsr01/gripper/position_cmd` | `/dsr01/gripper_controller/commands` |
| 강화학습 | ❌ | ✅ |
| 실행 파일 | `main.py` | `main_gazebo.py` |

---

## 1. Gazebo 실행

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
joint_state_broadcaster   - active
joint_trajectory_controller - active
gripper_controller        - active
```

---

## 2. 파일별 실행 명령어

### main_gazebo.py — Gazebo 통합 메뉴

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/main_gazebo.py
```

| 선택 | 동작 |
|------|------|
| `1` | 관절 제어 (MoveJoint + 그리퍼) |
| `2` | 픽앤플레이스 시뮬레이션 |
| `q` | 종료 |

---

### robot_move3_gazebo.py — Gazebo 관절 제어

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/robot_move3_gazebo.py
```

`JointTrajectoryController`로 관절을 직접 제어. virtual 버전의 `robot_move3.py`와 메뉴 구조 동일.

| 선택 | 동작 |
|------|------|
| `0` | 현재 관절 각도 확인 |
| `1` | MoveJoint — 관절 6개 각도 이동 |
| `4` | 그리퍼 제어 (0=열림 / 700=닫힘) |
| `q` | 종료 |

> MoveLine / MoveCircle은 Gazebo에서 MoveIt2가 필요하여 미지원.

**MoveJoint 입력 예시:**
```
6개 관절 각도 입력 (예: 0 0 90 0 90 0):
이동 시간(초, 기본=3.0): 3
```

**그리퍼 제어:**
```
그리퍼 값 입력 (0~700): 350
```

| 값 | 상태 |
|----|------|
| `0` | 완전 열림 |
| `350` | 절반 |
| `700` | 완전 닫힘 |

---

### pick_and_place_gazebo.py — Gazebo 픽앤플레이스

```bash
python3 ~/robot_workspace/doosan_ws/src/my_robot_interfaces/src/pick_and_place_gazebo.py
```

관절 웨이포인트 기반 픽앤플레이스 시뮬레이션. RViz의 `/object_marker` 토픽으로 물체 시각화.

**실행 전 RViz 설정:**
1. RViz 좌측 `Add` 버튼 클릭
2. `By topic` → `/object_marker` → `Marker` 선택
3. `Fixed Frame`을 `base_link` 로 설정

**동작 순서:**

| 단계 | 동작 |
|------|------|
| 1 | 안전 자세 이동 |
| 2 | 그리퍼 열기 |
| 3~4 | 물체 위 접근 → 하강 |
| 5 | 그리퍼 닫기 → 물체 색상 주황→초록 |
| 6~8 | 들어올리기 → 목표 위치 이동 → 하강 |
| 9 | 그리퍼 열기 → 물체 고정 |
| 10~11 | 후퇴 → 안전 자세 복귀 |

---

## 3. 웨이포인트 교정 (필수)

Gazebo 버전은 Cartesian 좌표 대신 **관절 각도(웨이포인트)** 로 동작합니다.  
`pick_and_place_gazebo.py` 상단의 값을 실제 로봇 위치에 맞게 교정해야 합니다.

### 교정 순서

**1단계: robot_move3_gazebo.py로 위치 탐색**
```bash
python3 robot_move3_gazebo.py
# 옵션 1로 MoveJoint 반복 → 원하는 위치 찾기
# 옵션 0으로 현재 관절각 확인
```

**2단계: pick_and_place_gazebo.py 웨이포인트 수정**

```python
# pick_and_place_gazebo.py 상단에서 수정
SAFE_JOINTS          = [  0.0,   0.0,  90.0,  0.0,  90.0,  0.0]  # 안전 자세
PICK_APPROACH_JOINTS = [  0.0, -20.0,  80.0,  0.0, 110.0,  0.0]  # 물체 위 접근
PICK_JOINTS          = [  0.0, -30.0,  85.0,  0.0, 115.0,  0.0]  # 물체 픽업 위치
PLACE_APPROACH_JOINTS= [ 45.0, -20.0,  80.0,  0.0, 110.0,  0.0]  # 목표 위 접근
PLACE_JOINTS         = [ 45.0, -30.0,  85.0,  0.0, 115.0,  0.0]  # 물체 놓는 위치
```

> 위 기본값은 예시이며 실제 환경에 맞지 않을 수 있습니다.

---

## 4. 컨트롤러 토픽

| 컨트롤러 | 토픽 | 메시지 타입 |
|---------|------|------------|
| 관절 이동 | `/dsr01/joint_trajectory_controller/joint_trajectory` | `trajectory_msgs/JointTrajectory` |
| 그리퍼 | `/dsr01/gripper_controller/commands` | `std_msgs/Float64MultiArray` |
| 관절 상태 | `/dsr01/joint_states` | `sensor_msgs/JointState` |

**관절 이름:** `joint_1` ~ `joint_6`  
**그리퍼 관절:** `gripper_rh_r1`, `gripper_rh_r2`, `gripper_rh_l1`, `gripper_rh_l2`

**수동 명령 예시:**
```bash
# 관절 상태 확인
ros2 topic echo /dsr01/joint_states --once

# 그리퍼 열기 (0.0 rad)
ros2 topic pub /dsr01/gripper_controller/commands std_msgs/msg/Float64MultiArray \
  "{data: [0.0, 0.0, 0.0, 0.0]}" --once

# 그리퍼 닫기 (1.0 rad)
ros2 topic pub /dsr01/gripper_controller/commands std_msgs/msg/Float64MultiArray \
  "{data: [1.0, 1.0, 1.0, 1.0]}" --once
```

---

## 5. Gazebo 트러블슈팅

### 증상: 로봇이 Gazebo에 안 보임

Gazebo가 완전히 뜨기 전에 spawn이 실행된 타이밍 문제.

```bash
pkill -9 -f "gz_sim|ros2_control_node|robot_state_publisher|spawner"
sleep 3
ros2 launch e0509_gripper_description bringup_gazebo.launch.py
```

### 증상: joint_trajectory_controller가 inactive

```bash
ros2 control switch_controllers \
  --activate joint_trajectory_controller \
  --controller-manager /dsr01/controller_manager
```

### 증상: 관절이 목표까지 안 가고 멈춤

`move_joint()` 의 `duration_sec` 값을 늘려주세요.  
기본 3초가 너무 짧으면 도달 전에 타임아웃됩니다.

```python
self._move_joint([0, 0, 90, 0, 90, 0], duration_sec=5.0)
```

### virtual 버전 트러블슈팅

→ 기존 `README.md`의 **2-2. 가상 로봇 트러블슈팅** 참고
