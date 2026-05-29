#!/bin/bash
# ROS2 + Gazebo 완전 재시작 스크립트

echo "[1/4] 프로세스 종료..."
pkill -9 -f "ros2_control_node|robot_state_publisher|rviz2|gazebo_bridge|gripper_joint_publisher|gripper_service_node|spawner|ign_gazebo|gz_sim|grasp_pipeline|realsense" 2>/dev/null
pkill -9 -f "ign_gazebo_server|ign_gazebo_gui|ruby" 2>/dev/null
sleep 1

echo "[2/4] FastDDS 공유 메모리 정리..."
rm -f /dev/shm/fastrtps_* 2>/dev/null

echo "[3/4] ROS2 daemon 재시작..."
ros2 daemon stop
sleep 1
ros2 daemon start
sleep 2

echo "[4/4] Launch 시작..."
source /opt/ros/humble/setup.bash
source /home/user/robot_workspace/doosan_ws/install/setup.bash
ros2 launch e0509_gripper_description bringup_real_gazebo.launch.py mode:=real host:=${1:-110.120.1.66}
