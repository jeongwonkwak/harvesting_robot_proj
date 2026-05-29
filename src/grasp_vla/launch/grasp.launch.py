"""
ROS2 launch file for the VLA grasp pipeline.

Usage:
  ros2 launch grasp_vla grasp.launch.py
  ros2 launch grasp_vla grasp.launch.py instruction:="pick up the silver connector"
  ros2 launch grasp_vla grasp.launch.py action_mode:=joint close_at_step:=30
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # ------------------------------------------------------------------
        # Launch arguments (all map 1-to-1 to ROS2 parameters)
        # ------------------------------------------------------------------
        DeclareLaunchArgument("smolvla_url",  default_value="http://192.168.50.79:16003"),
        DeclareLaunchArgument("instruction",  default_value="pick up the silver cylindrical connector"),
        DeclareLaunchArgument("action_mode",  default_value="cartesian"),
        DeclareLaunchArgument("max_steps",    default_value="50"),
        DeclareLaunchArgument("close_at_step",default_value="35"),
        DeclareLaunchArgument("step_hz",      default_value="5.0"),
        DeclareLaunchArgument("gripper_port", default_value="/dev/ttyUSB0"),
        DeclareLaunchArgument("robot_id",     default_value="dsr01"),

        # ------------------------------------------------------------------
        # Grasp pipeline node
        # ------------------------------------------------------------------
        Node(
            package="grasp_vla",
            executable="grasp_pipeline_node",
            name="grasp_pipeline",
            output="screen",
            parameters=[{
                "smolvla_url":  LaunchConfiguration("smolvla_url"),
                "instruction":  LaunchConfiguration("instruction"),
                "action_mode":  LaunchConfiguration("action_mode"),
                "max_steps":    LaunchConfiguration("max_steps"),
                "close_at_step":LaunchConfiguration("close_at_step"),
                "step_hz":      LaunchConfiguration("step_hz"),
                "gripper_port": LaunchConfiguration("gripper_port"),
                "robot_id":     LaunchConfiguration("robot_id"),
            }],
        ),
    ])
