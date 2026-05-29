# 딸기 수확 VLA 데이터 수집 가이드

## 환경

| 장비 | 모델 |
|---|---|
| 로봇 팔 | Doosan E0509 |
| 카메라 | Intel RealSense D455 |
| 그리퍼 | Robotis RH-P12-RN-DF (Dynamixel) |

---

## 수집 데이터

| 토픽 | 타입 | Hz | 내용 |
|---|---|---|---|
| `/dsr01/joint_states` | `sensor_msgs/JointState` | ~100 | 관절 각도 6개 (라디안) |
| `/camera/camera/color/image_raw` | `sensor_msgs/Image` | 30 | RGB 영상 (1280×720) |
| `/gripper/position` | `std_msgs/Float32` | 10 | 그리퍼 개폐 비율 (0.0=열림, 1.0=닫힘) |

---

## 저장 경로 설정

`config/params.yaml` 에서 bag 파일 저장 위치를 지정합니다.

```yaml
data_collection:
  ros__parameters:
    bag_save_path: "/home/user/robot_workspace/vla_ws/data"  # ← 여기 수정
```

저장 결과 구조 (타임스탬프로 덮어쓰기 방지):

```
bag_save_path/
├── episode_001_20260518_195715/
│   ├── episode_001_20260518_195715_0.db3
│   └── metadata.yaml
├── episode_002_20260518_201030/
│   ├── episode_002_20260518_201030_0.db3
│   └── metadata.yaml
└── ...
```

---

## 실행 순서

### 터미널 1 — 로봇 실행

```bash
ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py \
  mode:=real \
  host:=110.120.1.66
```

### 터미널 2 — 에피소드 수집 (카메라 + 그리퍼 퍼블리셔 + bag record + grasp_pipeline 자동 시작)

```bash
source ~/robot_workspace/vla_ws/install/setup.bash

ros2 launch grasp_vla collect_episode.launch.py episode:=001
```

에피소드마다 번호를 증가시켜 반복합니다.

```bash
ros2 launch grasp_vla collect_episode.launch.py episode:=002
ros2 launch grasp_vla collect_episode.launch.py episode:=003
```

저장 경로를 즉석에서 바꾸고 싶을 때는 인수로 넘길 수 있습니다.

```bash
ros2 launch grasp_vla collect_episode.launch.py episode:=001 bag_save_path:=/data/strawberry
```

> **주의**: RealSense 카메라는 collect_episode.launch.py 내부에서 자동으로 시작됩니다. 별도로 켤 필요 없습니다.

---

## 그리퍼 동작

SmolVLA 베이스 모델은 6차원 액션(EEF Cartesian 또는 관절 delta)만 출력합니다.  
그리퍼는 `close_at_step` 파라미터에 지정된 스텝에서 고정값으로 닫힙니다.

```yaml
grasp_pipeline:
  ros__parameters:
    close_at_step: 35   # 이 스텝에서 그리퍼 close
    max_steps: 50       # 전체 루프 최대 스텝
    min_grasp_step: 15  # 이 스텝 이전에는 close 무시
```

---

## 권장 수집량

| 단계 | 에피소드 수 | 시나리오 |
|---|---|---|
| Phase 1 | 100 | 잎 가림 없는 딸기 (단독/군집, 다양한 높이·각도) |
| Phase 2 | 200 | 잎 25/50/75% 가림, 다른 딸기에 가려진 경우 |
| Phase 3 | 200+ | 조명 다양화, 다양한 접근 각도, 실패→재시도 케이스 |

> 수량보다 **일관된 그립 전략**이 중요합니다. 매 에피소드 동일한 방식으로 시연하세요.

---

## 다음 단계

수집된 bag 파일은 `sroi_rosbag_utilities/lerobot/sroi_to_lerobot.py`로 LeRobot v3.0 포맷으로 변환한 뒤 SmolVLA fine-tuning에 사용합니다.
