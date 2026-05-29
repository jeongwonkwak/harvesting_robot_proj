# RealSense D455 ROS2 설정 가이드

## 카메라 실행

### 기본 실행
```bash
ros2 launch realsense2_camera rs_launch.py
```

### JSON 설정 파일 적용 실행
```bash
ros2 launch realsense2_camera rs_launch.py \
  json_file_path:=/home/user/robot_workspace/librealsense/realsense_setting.json
```

## 카메라 영상 확인

### rqt_image_view 사용 (권장)
```bash
conda deactivate  # Anaconda 환경 비활성화 필수
ros2 run rqt_image_view rqt_image_view
```

드롭다운에서 토픽 선택:
- `/camera/camera/color/image_raw` — RGB 컬러 영상
- `/camera/camera/depth/image_rect_raw` — 뎁스 영상

### rviz2 사용
```bash
rviz2
```
Add → By topic → Image 선택

### 토픽 목록 확인
```bash
ros2 topic list | grep image
```

## 설정 적용 확인

노드가 실행 중인 상태에서 확인:

```bash
# JSON 파일 경로 확인
ros2 param get /camera/camera json_file_path

# 레이저 파워 확인 (JSON 설정값: 150)
ros2 param get /camera/camera depth_module.laser_power
```

`150.0` 이 출력되면 JSON 설정이 정상 적용된 것.

## realsense_setting.json 주요 설정값

| 항목 | 값 |
|------|-----|
| 해상도 (Depth) | 848 x 480 @ 30fps |
| 해상도 (Color) | 1280 x 720 @ 30fps |
| 레이저 파워 | 150 |
| 레이저 상태 | ON |
| Depth Gain | 16 |
| 오토 익스포저 | 활성화 |
| Left-Right Threshold | 24 |

JSON 파일 위치: `/home/user/robot_workspace/librealsense/realsense_setting.json`

## 주의사항

- **Anaconda와 ROS2 충돌**: ROS2는 Python 3.10을 사용하는데 Anaconda base 환경(Python 3.13)이 활성화되면 충돌 발생
  - ROS2 명령 실행 전 `conda deactivate` 필수
  - 자동 활성화 비활성화: `conda config --set auto_activate_base false`

- 파라미터 확인은 반드시 노드가 실행 중인 상태에서 해야 함
