# robot_workspace 구조 정리

> `sim2real`, `vla_ws` 먼저 정리. 나머지 패키지는 추후 추가 예정.

---

## sim2real

Isaac Lab(시뮬레이션)에서 학습된 강화학습 Policy를 실제 Doosan E0509 로봇에서 실행하는 Sim-to-Real 전이 패키지.  
**ROS2 없이 DRFL(Doosan Robot Framework Library)로 직접 로봇 제어.**

```
sim2real/
├── README.md                              # 프로젝트 개요 및 사용법
├── create_presentation.py                 # 발표 자료(pptx) 자동 생성 스크립트
├── pen_grasp_sim2real_presentation.pptx   # 생성된 발표 자료
│
└── sim2real/                              # 메인 Python 패키지
    │
    ├── [실행 진입점]
    ├── run_sim2real.py                    # V7 실행 진입점 — IK 모드 전용
    │                                      #   YOLO 펜 감지 → 27차원 obs → Policy → Δ[x,y,z] → IK → 관절 명령
    ├── run_sim2real_unified.py            # 통합 실행 진입점 — IK / OSC 모드 선택 가능
    │
    ├── [핵심 모듈]
    ├── robot_interface.py                 # DRFL 기반 Doosan E0509 로봇 인터페이스
    │                                      #   connect/disconnect, 관절/TCP 읽기, MoveJoint/MoveLinear
    ├── jacobian_ik.py                     # Jacobian 기반 Differential IK (DLS 방식)
    │                                      #   URDF 로드 → Jacobian 계산 → Δq 산출
    ├── osc_controller.py                  # Operational Space Controller (토크 제어)
    │                                      #   Isaac Lab OSC 구현을 실제 로봇용으로 포팅
    ├── pen_detector_yolo.py               # YOLOv8-seg 기반 펜 감지기
    │                                      #   세그멘테이션 마스크로 펜 끝점(캡/팁) 3D 위치 추출
    ├── policy_loader.py                   # Isaac Lab 학습 Policy (.pt) 로더
    │                                      #   target_tracking / e0509_reach 환경 지원
    ├── gripper_interface.py               # DRFL 기반 RH-P12-RN-A 그리퍼 제어
    │                                      #   Tool Flange Serial → Modbus RTU 통신
    │
    ├── [테스트 스크립트]
    ├── test_osc_control.py                # OSC 컨트롤러 단독 테스트
    ├── test_pen_detection_calibrated.py   # 캘리브레이션 적용 후 펜 감지 검증
    ├── test_torque_control.py             # 토크 제어 직접 테스트
    │
    ├── calibration/                       # 카메라-로봇 캘리브레이션 스크립트
    │   ├── calibrate_eye_in_hand.py       # Eye-in-Hand 수동 캘리브레이션 (T_cam→gripper)
    │   ├── calibrate_eye_to_hand.py       # Eye-to-Hand 캘리브레이션 (T_cam→base)
    │   ├── calibrate_eye_to_hand_org.py   # Eye-to-Hand 원본 버전 (참고용)
    │   ├── calibrate_z_offset.py          # Z축 오프셋 보정 (펜 감지 vs 실제 TCP 비교)
    │   └── eye_in_hand_auto.py            # Eye-in-Hand 자동 캘리브레이션
    │                                      #   사전 정의 포즈 순회 → 자동 샘플 수집 → 저장
    │
    ├── config/
    │   └── pen_workspace.py               # 펜 작업 공간 파라미터 (sim + real 공유)
    │                                      #   펜 위치/각도 유효 범위 정의
    │
    ├── calib_images/                      # 캘리브레이션 수집 데이터
    │   └── YYYYMMDD_HHMMSS/
    │       ├── positions.csv              # 수집 시 로봇 관절 위치 기록
    │       └── sample_NN.png              # ArUco 마커 이미지 샘플
    │
    ├── Screenshots/                       # 실험 결과 스크린샷 (날짜별 폴더)
    │   ├── 260506/                        # robot_poses.txt 포함
    │   └── 260514/
    │
    └── deprecated/                        # 구버전 / 실험 중단 스크립트 (참고용)
        ├── action_processor.py            # 액션 후처리 (구버전)
        ├── auto_hand_eye_calibration.py   # 자동 Hand-Eye 캘리브레이션 구버전
        ├── generate_checkerboard.py       # 체커보드 패턴 이미지 생성
        ├── hand_eye_calibration.py        # Hand-Eye 캘리브레이션 구버전
        ├── manual_hand_eye_calibration.py # 수동 Hand-Eye 캘리브레이션 구버전
        ├── pen_detector.py                # YOLO 이전 펜 감지기
        ├── pen_grasp_controller.py        # 펜 파지 컨트롤러 구버전
        ├── robot_observation.py           # 로봇 상태 관찰 구버전
        ├── run_pen_tracking.py            # 펜 추적 실행 구버전
        ├── sim2real_bridge.py             # Sim2Real 브릿지 구버전
        ├── test_ik_move.py                # IK 이동 테스트 구버전
        ├── test_observation.py            # 관찰 테스트 구버전
        └── verify_calibration.py          # 캘리브레이션 검증 구버전
```

---

## vla_ws

SmolVLA(Vision-Language-Action) 모델을 활용한 로봇 파지 파이프라인.  
**ROS2(Humble) 기반. 카메라 → VLA 추론 → Doosan e0509 제어.**  
에피소드 데이터 수집 → LeRobot 포맷 변환 → 모델 파인튜닝까지의 전체 흐름 포함.

```
vla_ws/
├── package.xml                            # ROS2 패키지 메타데이터
├── setup.py                               # Python 패키지 설치 설정
│
├── grasp_vla/                             # 메인 ROS2 패키지 소스
│   ├── grasp_pipeline.py                  # 전체 파지 시퀀스 ROS2 노드 (핵심)
│   │                                      #   그리퍼 열기 → VLA 루프(이미지+관절→SmolVLA→액션 실행) → 닫기
│   ├── camera_node.py                     # RealSense D455 카메라 인터페이스
│   │                                      #   pyrealsense2 직접 사용 / ROS 토픽 fallback
│   ├── robot_controller.py                # Doosan e0509 ROS2 제어
│   │                                      #   dsr_ros2 기반, cartesian/joint 모드 지원
│   ├── smolvla_client.py                  # SmolVLA HTTP API 클라이언트
│   │                                      #   POST /predict → 6-DoF 액션 수신
│   ├── gripper_controller.py              # RH-P12-RN-DF 그리퍼 제어 (Dynamixel SDK)
│   │                                      #   /dev/ttyUSB0, Protocol 2.0
│   └── gripper_state_publisher.py         # 그리퍼 위치 ROS2 토픽 퍼블리셔
│                                          #   /gripper/position (Float32) → bag 기록용
│
├── launch/                                # ROS2 launch 파일
│   ├── grasp.launch.py                    # 파지 파이프라인 실행
│   │                                      #   instruction / action_mode / close_at_step 파라미터 지정
│   ├── collect_episode.launch.py          # 에피소드 데이터 수집
│   │                                      #   RealSense 노드 + bag record 자동 시작
│   └── strawberry_harvest.launch.py       # 딸기 수확 VLA 데모 (가상 환경용)
│
├── config/
│   ├── params.yaml                        # 전체 노드 파라미터
│   │                                      #   SmolVLA URL, instruction, max_steps,
│   │                                      #   action_mode, gripper_port, retreat_delta 등
│   └── bag_qos_overrides.yaml             # ros2 bag record QoS 오버라이드 설정
│
├── src/                                   # 데이터 변환 스크립트
│   ├── bag_to_lerobot.py                  # ROS2 bag(SQLite3) → LeRobot v3.0 데이터셋 변환
│   │                                      #   출력: parquet + mp4 + meta/info.json
│   └── make_sample_dataset.py             # SmolVLA SFT용 더미 샘플 데이터셋 생성
│
├── data/                                  # 학습 데이터 저장소
│   ├── raw/                               # ROS2 bag 원본 에피소드
│   │   └── episode_NNN_YYYYMMDD_HHMMSS/
│   │       ├── *.db3                      # ROS2 bag 데이터
│   │       └── metadata.yaml
│   ├── mid/                               # 중간 처리 단계 데이터
│   └── fin/                               # 최종 LeRobot 포맷 데이터셋
│       └── lerobot_dataset_v1.0.0/
│           ├── data/                      # parquet 파일
│           ├── videos/                    # mp4 영상
│           └── meta/                      # info.json
│
├── sroi_rosbag_utilities/                 # ROS bag 전처리 유틸리티 모음 (외부)
│   ├── README.md                          # 사용법 설명
│   ├── rosbag_segment.py                  # /upi/status/is_action 기준 bag 구간 분리
│   ├── extract_images_interactive.py      # bag에서 이미지 인터랙티브 추출
│   ├── extract_stereo_rosbags.py          # 스테레오 카메라 bag 추출
│   ├── gripper_estimation_april_tag.py    # AprilTag 기반 그리퍼 위치 추정
│   ├── transform_trajectory.py            # 궤적 좌표계 변환
│   ├── create_orb_slam_yaml.py            # ORB-SLAM 카메라 YAML 설정 생성
│   ├── orb_slam_yaml/                     # ORB-SLAM YAML 예시 (RealSense D435i, OAK-D)
│   └── extract_rgbd/                      # RGBD 데이터 추출 스크립트 모음
│       ├── extract_rgbd.py                # 기본 RGBD 추출
│       ├── extract_realsense_color.py     # RealSense 컬러 이미지 추출
│       ├── extract_rgb_lr.py              # 좌/우 RGB 추출
│       ├── extract_rgb_rec_compress_lr.py # 압축 저장 버전
│       ├── extract_endpose_ros1.py        # ROS1 bag에서 End-pose 추출
│       ├── extract_stereo_ros1.py         # ROS1 스테레오 추출
│       ├── extract_stereo_ros1_rs.py      # ROS1 RealSense 스테레오 추출
│       ├── extract_stereo_rosbags.py      # ROS2 스테레오 추출
│       ├── gripper_detection.py           # 그리퍼 검출 유틸
│       ├── color_seg_utils.py             # 색상 세그멘테이션 유틸
│       ├── msgReaders.py                  # ROS 메시지 파서
│       ├── batch_compare_traj_and_gt.py   # 궤적 vs GT 배치 비교
│       ├── batch_evo_metrics.py           # evo 라이브러리 메트릭 배치 계산
│       ├── rename_evo.py                  # evo 결과 파일 리네임
│       ├── README.md
│       └── README_rosbags.md
│
├── lerobot/                               # HuggingFace LeRobot 서브모듈 (원본 레포)
│                                          #   SmolVLA 모델 학습/서빙 코드 포함
│
├── build/                                 # colcon 빌드 아티팩트 (자동 생성, 무시)
└── install/                               # colcon 설치 결과 (자동 생성, 무시)
```

---

## 전체 데이터 흐름 요약

```
[실제 로봇 작업]
collect_episode.launch.py
  → RealSense D455 영상 + 관절값 → ros2 bag (data/raw/)

[데이터 변환]
src/bag_to_lerobot.py
  → data/raw/ → data/fin/ (LeRobot v3.0 포맷)

[모델 파인튜닝]
data/fin/ → lerobot/ SmolVLA SFT 학습

[추론 서버]
SmolVLA 서버 (http://192.168.50.79:16003)
  ← smolvla_client.py POST /predict

[로봇 제어]
grasp.launch.py
  → grasp_pipeline.py (카메라→VLA→로봇→그리퍼)
```
