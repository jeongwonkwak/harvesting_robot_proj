"""
에피소드 데이터 수집 launch 파일

사전 조건:
  1. ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py mode:=real host:=<IP>
  2. SmolVLA 서버 실행 중
  (realsense2_camera는 이 launch에서 자동 시작됨)

실행:
  ros2 launch grasp_vla collect_episode.launch.py episode:=001
  ros2 launch grasp_vla collect_episode.launch.py episode:=002 bag_save_path:=/data/bags
"""

import os
import yaml
from datetime import datetime

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction, RegisterEventHandler, Shutdown
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.event_handlers import OnProcessExit


# config/params.yaml 에서 bag_save_path 읽기
_PARAMS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "config", "params.yaml"
)
_DEFAULT_BAG_PATH = "/home/user/robot_workspace/vla_ws/data/raw"

try:
    with open(_PARAMS_FILE) as f:
        _cfg = yaml.safe_load(f)
    _DEFAULT_BAG_PATH = (
        _cfg.get("data_collection", {})
            .get("ros__parameters", {})
            .get("bag_save_path", _DEFAULT_BAG_PATH)
    )
except Exception:
    pass

# 같은 episode 번호로 재실행 시 충돌 방지: 타임스탬프 suffix
_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_launch_description():
    episode_arg = DeclareLaunchArgument(
        "episode",
        default_value="001",
        description="에피소드 번호",
    )
    bag_path_arg = DeclareLaunchArgument(
        "bag_save_path",
        default_value=_DEFAULT_BAG_PATH,
        description="bag 파일 저장 루트 경로 (config/params.yaml의 bag_save_path)",
    )
    instruction_arg = DeclareLaunchArgument(
        "instruction",
        default_value="grasp the green stem above the red strawberry and pick it",
    )

    # ── RealSense 카메라 ──────────────────────────────────────────────────
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

    # ── /gripper/position 퍼블리셔 ────────────────────────────────────────
    gripper_pub = Node(
        package="grasp_vla",
        executable="gripper_state_publisher_node",
        name="gripper_state_publisher",
        output="screen",
    )

    # ── ros2 bag record ───────────────────────────────────────────────────
    # 폴더명: episode_001_20260518_195715  (재실행 시 덮어쓰지 않도록 타임스탬프 추가)
    # --qos-profile-overrides-path: VOLATILE 강제 지정으로 QoS 불일치 방지
    _qos_file = os.path.join(os.path.dirname(__file__), "..", "config", "bag_qos_overrides.yaml")
    bag_record = ExecuteProcess(
        cmd=[
            "ros2", "bag", "record",
            "--qos-profile-overrides-path", _qos_file,
            "-o", PythonExpression([
                '"', LaunchConfiguration("bag_save_path"),
                '/episode_', LaunchConfiguration("episode"),
                '_', _TIMESTAMP, '"'
            ]),
            "/dsr01/joint_states",
            "/camera/camera/color/image_raw",
            "/gripper/position",
        ],
        output="screen",
    )

    # ── grasp_pipeline (카메라 + bag이 올라온 뒤 4초 후 시작) ─────────────
    # realsense2_camera는 __ns:=/camera __node:=camera 로 실행 → 실제 토픽: /camera/camera/color/image_raw
    grasp_node = Node(
        package="grasp_vla",
        executable="grasp_pipeline_node",
        name="grasp_pipeline",
        output="screen",
        parameters=[{
            "instruction": ParameterValue(LaunchConfiguration("instruction"), value_type=str),
            "camera_topic": "/camera/camera/color/image_raw",
        }],
    )
    grasp = TimerAction(period=4.0, actions=[grasp_node])

    # ── grasp_pipeline 종료 시 launch 전체 자동 종료 ──────────────────────
    auto_shutdown = RegisterEventHandler(
        OnProcessExit(
            target_action=grasp_node,
            on_exit=[Shutdown()],
        )
    )

    return LaunchDescription([
        episode_arg,
        bag_path_arg,
        instruction_arg,
        realsense,
        gripper_pub,
        bag_record,
        grasp,
        auto_shutdown,
    ])
