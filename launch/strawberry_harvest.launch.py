"""
딸기 수확 VLA 데모 launch 파일

사전 조건:
  1. ros2 launch e0509_gripper_description bringup_gazebo.launch.py mode:=virtual
  2. VLA 서버가 smolvla_url 주소에서 실행 중

실행:
  ros2 launch grasp_vla strawberry_harvest.launch.py
  ros2 launch grasp_vla strawberry_harvest.launch.py smolvla_url:=http://192.168.50.79:16003

홈 포즈 (home_pose):
  J1=90°  : +Y 방향(딸기 벽)으로 회전
  J2=-30° : 어깨 들어올림
  J3=100° : 팔꿈치 전방 굽힘
  J4=0°   : 손목 중립
  J5=-70° : 손목 수평 방향
  J6=0°   : 롤 중립
  → 실제 로봇/시뮬 결과에 따라 조정 필요

리트릿 (retreat_delta):
  Y=-200mm (벽에서 멀어지는 방향), Z=+60mm (위로 살짝)
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "smolvla_url",
            default_value="http://192.168.50.79:16003",
        ),
        DeclareLaunchArgument(
            "instruction",
            default_value="grasp the green stem above the red strawberry and pick it",
        ),
        DeclareLaunchArgument(
            "action_mode",
            default_value="joint",
            description="cartesian | joint",
        ),
        DeclareLaunchArgument(
            "max_steps",
            default_value="60",
        ),
        DeclareLaunchArgument(
            "close_at_step",
            default_value="45",
            description="그리퍼를 닫는 최대 스텝 (VLA가 더 일찍 닫으면 무시됨)",
        ),
        DeclareLaunchArgument(
            "step_hz",
            default_value="3.0",
            description="VLA 제어 주파수 (Hz). 낮출수록 각 액션이 완료될 시간을 줌",
        ),
        DeclareLaunchArgument(
            "robot_id",
            default_value="dsr01",
        ),
        DeclareLaunchArgument(
            "gripper_port",
            default_value="/dev/ttyUSB0",
        ),
        # 딸기 벽을 바라보는 홈 포즈 (degrees)
        DeclareLaunchArgument(
            "home_pose",
            default_value="190.0,-30.0,100.0,0.0,-70.0,0.0",
            description="J1~J6 (degrees), 쉼표 구분. 비워두면 홈 이동 스킵",
        ),
        # 줄기를 잡은 후 벽에서 당겨내는 델타 (Doosan 태스크 공간: mm/deg)
        DeclareLaunchArgument(
            "retreat_delta",
            default_value="[0.0, -200.0, 60.0, 0.0, 0.0, 0.0]",
            description="파지 후 후퇴 델타: -Y 방향으로 당김, +Z 위로",
        ),
        # Gazebo 카메라 ROS2 토픽 (bringup_gazebo가 브리지해 줌)
        DeclareLaunchArgument(
            "min_grasp_step",
            default_value="20",
            description="이 스텝 이전에는 그리퍼 close 신호 무시 (VLA 조기 close 방지)",
        ),
        DeclareLaunchArgument(
            "camera_topic",
            default_value="/dsr01/wrist_camera/image",
            description="Gazebo 브리지 카메라 토픽. 실물 카메라 시 비워둠",
        ),

        Node(
            package="grasp_vla",
            executable="grasp_pipeline_node",
            name="grasp_pipeline",
            output="screen",
            parameters=[{
                "smolvla_url":   LaunchConfiguration("smolvla_url"),
                "instruction":   LaunchConfiguration("instruction"),
                "action_mode":   LaunchConfiguration("action_mode"),
                "max_steps":     LaunchConfiguration("max_steps"),
                "close_at_step": LaunchConfiguration("close_at_step"),
                "step_hz":       LaunchConfiguration("step_hz"),
                "robot_id":      LaunchConfiguration("robot_id"),
                "gripper_port":  LaunchConfiguration("gripper_port"),
                "home_pose":     LaunchConfiguration("home_pose"),
                "retreat_delta": LaunchConfiguration("retreat_delta"),
                "min_grasp_step": LaunchConfiguration("min_grasp_step"),
                "camera_topic":  LaunchConfiguration("camera_topic"),
            }],
        ),
    ])
