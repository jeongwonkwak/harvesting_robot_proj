"""
collect_curobo.launch.py

cuRobo 자동 파지 파이프라인을 실행하면서 LeRobot 학습용 데이터를 수집합니다.
strawberry_yolo_node의 Auto 모드(키: a)를 켜면 연속으로 파지 데이터를 수집합니다.

사전 조건:
  로봇 bringup 실행 중 (dsr01, RealSense 제외)

실행:
  ros2 launch /home/user/robot_workspace/vla_ws/src/collect_curobo.launch.py
  ros2 launch /home/user/robot_workspace/vla_ws/src/collect_curobo.launch.py session:=session_001

녹화 토픽:
  /dsr01/joint_states             → 로봇 관절 상태
  /camera/camera/color/image_raw  → RGB 카메라
  /gripper/position               → 그리퍼 개폐 비율 (0.0~1.0)
  /dsr01/curobo/pick_complete     → 에피소드 경계 마커

변환 (수집 완료 후):
  python3 src/bag_to_lerobot.py
"""

import os
from datetime import datetime

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    TimerAction,
)
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare


_TIMESTAMP   = datetime.now().strftime("%Y%m%d_%H%M%S")
_VLA_WS      = os.path.join(os.path.dirname(__file__), "..")
_DEFAULT_BAG = os.path.join(_VLA_WS, "data", "raw")
_QOS_FILE    = os.path.join(_VLA_WS, "config", "bag_qos_overrides.yaml")
_SCRIPTS_DIR = os.path.expanduser(
    "~/robot_workspace/harvesting_robot_miniproj/scripts"
)
_VLA_SETUP   = os.path.join(_VLA_WS, "install", "setup.bash")

# cuRobo 스크립트 실행용 shell prefix
def _bash(script_path: str, extra_env: str = "") -> str:
    lines = []
    if os.path.exists(_VLA_SETUP):
        lines.append(f"source {_VLA_SETUP}")
    else:
        lines.append("source /opt/ros/humble/setup.bash")
    if extra_env:
        lines.append(extra_env)
    lines.append(f"python3 {script_path}")
    return " && ".join(lines)


def generate_launch_description():
    session_arg = DeclareLaunchArgument(
        "session",
        default_value=f"curobo_{_TIMESTAMP}",
        description="세션 이름 (bag 폴더 suffix)",
    )
    bag_path_arg = DeclareLaunchArgument(
        "bag_save_path",
        default_value=_DEFAULT_BAG,
        description="bag 저장 루트 경로",
    )

    # ── RealSense ─────────────────────────────────────────────────────────────
    realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("realsense2_camera"), "/launch/rs_launch.py"
        ]),
        launch_arguments={
            "enable_color": "true",
            "enable_depth": "false",
            "rgb_camera.color_profile": "640x480x30",
        }.items(),
    )

    # ── 그리퍼 상태 퍼블리셔 (/gripper/position) ───────────────────────────────
    gripper_pub = Node(
        package="grasp_vla",
        executable="gripper_state_publisher_node",
        name="gripper_state_publisher",
        output="screen",
    )

    # ── bag recorder ──────────────────────────────────────────────────────────
    # 폴더: data/raw/<session>/
    bag_record = ExecuteProcess(
        cmd=[
            "ros2", "bag", "record",
            "--qos-profile-overrides-path", _QOS_FILE,
            "-o", PythonExpression([
                '"', LaunchConfiguration("bag_save_path"),
                '/', LaunchConfiguration("session"), '"'
            ]),
            "/dsr01/joint_states",
            "/camera/camera/color/image_raw",
            "/gripper/position",
            "/dsr01/curobo/pick_complete",   # 에피소드 경계 마커
        ],
        output="screen",
    )

    # ── cuRobo planner (즉시 시작, JIT 컴파일 ~30초 소요) ─────────────────────
    curobo_planner = ExecuteProcess(
        cmd=[
            "bash", "-c",
            _bash(
                os.path.join(_SCRIPTS_DIR, "curobo_planner_node.py"),
                extra_env="export CUDA_HOME=/usr/local/cuda-12.8",
            ),
        ],
        output="screen",
    )

    # ── strawberry YOLO (30초 후 시작 – cuRobo JIT 대기) ─────────────────────
    # 화면에서 'a' 키를 누르면 Auto 모드 → pick_complete 마다 다음 파지 자동 진행
    yolo_node = TimerAction(
        period=30.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    "bash", "-c",
                    _bash(
                        os.path.join(_SCRIPTS_DIR, "strawberry_yolo_node.py"),
                        extra_env="export CUDA_HOME=/usr/local/cuda-12.8",
                    ),
                ],
                output="screen",
            )
        ],
    )

    return LaunchDescription([
        session_arg,
        bag_path_arg,
        realsense,
        gripper_pub,
        bag_record,
        curobo_planner,
        yolo_node,
    ])
