"""
collect_vision.launch.py

YOLO 딸기 검출 + 캘리브레이션 기반 규칙 파지로 학습 데이터를 수집합니다.
VLA 서버 없이 동작하며, 에피소드마다 자동으로 bag을 저장합니다.

사전 조건:
  로봇 bringup 실행 중 (dsr01)

실행:
  ros2 launch grasp_vla collect_vision.launch.py episode:=001
"""

import os
import yaml
from datetime import datetime

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, ExecuteProcess, TimerAction,
    RegisterEventHandler, Shutdown,
)
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.event_handlers import OnProcessExit


_PARAMS_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "params.yaml")
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

_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
_QOS_FILE  = os.path.join(os.path.dirname(__file__), "..", "config", "bag_qos_overrides.yaml")


def generate_launch_description():
    episode_arg = DeclareLaunchArgument(
        "episode", default_value="001",
        description="에피소드 번호 (e.g. 001, 002 ...)",
    )
    bag_path_arg = DeclareLaunchArgument(
        "bag_save_path", default_value=_DEFAULT_BAG_PATH,
    )

    # ── RealSense (color + depth 모두 활성화) ─────────────────────────────────
    realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("realsense2_camera"), "/launch/rs_launch.py"
        ]),
        launch_arguments={
            "enable_color": "true",
            "enable_depth": "true",
            "rgb_camera.color_profile": "640x480x30",
            "depth_module.depth_profile": "640x480x30",
            "align_depth.enable": "true",
        }.items(),
    )

    # ── 그리퍼 상태 퍼블리셔 ─────────────────────────────────────────────────
    gripper_pub = Node(
        package="grasp_vla",
        executable="gripper_state_publisher_node",
        name="gripper_state_publisher",
        output="screen",
    )

    # ── bag recorder ─────────────────────────────────────────────────────────
    bag_record = ExecuteProcess(
        cmd=[
            "ros2", "bag", "record",
            "--qos-profile-overrides-path", _QOS_FILE,
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

    # ── vision grasp 노드 (4초 후 시작) ──────────────────────────────────────
    grasp_node = Node(
        package="grasp_vla",
        executable="grasp_pipeline_node",
        name="grasp_pipeline",
        output="screen",
        parameters=[{
            "mode":         "vision",
            "camera_topic": "/camera/camera/color/image_raw",
            "depth_topic":  "/camera/camera/aligned_depth_to_color/image_raw",
        }],
    )
    grasp = TimerAction(period=4.0, actions=[grasp_node])

    auto_shutdown = RegisterEventHandler(
        OnProcessExit(target_action=grasp_node, on_exit=[Shutdown()])
    )

    return LaunchDescription([
        episode_arg,
        bag_path_arg,
        realsense,
        gripper_pub,
        bag_record,
        grasp,
        auto_shutdown,
    ])
