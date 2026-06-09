#!/usr/bin/env python3
"""
move_to_pose.py

로봇을 지정한 포즈로 이동시키는 유틸리티 스크립트.

실행:
  python3 src/move_to_pose.py                    # TARGET 변수에 설정된 포즈로 이동
  python3 src/move_to_pose.py --target top_right # CLI로 포즈 지정
"""

import argparse
import math
import sys
import threading
import time

import rclpy
from rclpy.executors import MultiThreadedExecutor

sys.path.insert(0, '/home/user/robot_workspace/vla_ws')
sys.path.insert(0, '/home/user/robot_workspace/vla_ws/grasp_vla')

from grasp_vla.robot_controller import DoosanController
from grasp_vla.gripper_controller import GripperController

# ── 여기만 수정하세요 ────────────────────────────────────────────────────────

# 이동할 포즈 선택 (아래 POSES 딕셔너리의 키 중 하나)
TARGET = 'top_right'

VELOCITY     = 2000
ACCELERATION = 250
GRIPPER_POS  = 600   # 0=열림, 740=완전닫힘

# ── 포즈 정의 ────────────────────────────────────────────────────────────────
#
# joint 포즈: mode='joint', positions=관절 각도(deg) 6개
# tcp 포즈:   mode='tcp',   positions=TCP [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]

POSES = {
    # ── 홈 포즈 4종 (TCP) ── NW=top_left / NE=top_right / SE=bottom_right / SW=bottom_left
    'home':         {'mode': 'tcp', 'positions': [6.35, -0.25, 547.58, 85.67, 66.27, -89.12]},
    'top_left':     {'mode': 'tcp', 'positions': [-225.46, 338.93, 902.31,  88.42, 87.31, -89.88]},  # NW
    'top_right':    {'mode': 'tcp', 'positions': [ 314.90, 279.89, 883.40,  89.90, 86.29, -89.62]},  # NE
    'bottom_left':  {'mode': 'tcp', 'positions': [-247.70, 317.34, 533.88,  87.75, 86.31, -89.49]},  # SW
    'bottom_right': {'mode': 'tcp', 'positions': [ 312.61, 302.83, 529.32,  89.90, 86.29, -89.62]},  # SE

    # ── 기타 포즈 (joint) ──────────────────────────────────────────────────
    'custom_joint': {'mode': 'joint', 'positions': [70, -30, 100, 6.6, 5, -100]},
}

# ─────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', default=None,
                        choices=list(POSES.keys()),
                        help=f'이동할 포즈 (기본값: {TARGET})')
    args = parser.parse_args()

    # ── 초기화 ───────────────────────────────────────────────────────────────
    rclpy.init()
    node     = rclpy.create_node('move_to_pose')
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    robot   = DoosanController(node, robot_id='dsr01', action_mode='cartesian')
    gripper = GripperController(port='/dev/ttyUSB0', ros_node=node, robot_id='dsr01')
    time.sleep(1.0)

    # ── 일반 포즈 이동 ────────────────────────────────────────────────────────
    target_name = args.target or TARGET
    pose        = POSES[target_name]
    mode        = pose['mode']
    positions   = pose['positions']

    # action_mode를 mode에 맞게 재설정
    robot._action_mode = 'joint' if mode == 'joint' else 'cartesian'

    print(f'포즈: {target_name}  mode={mode}')
    print(f'위치: {positions}')
    print(f'그리퍼: {GRIPPER_POS}')
    print('이동 중 ...')

    # ── 서비스 연결 대기 ─────────────────────────────────────────────────────
    time.sleep(1.0)

    svc_name = f'/dsr01/motion/move_{"joint" if mode == "joint" else "line"}'
    cli = robot._movej_cli if mode == 'joint' else robot._movel_cli
    print(f'서비스 연결 확인: {svc_name} ... ', end='', flush=True)
    if not cli.service_is_ready():
        print('NOT READY — Doosan ROS 드라이버가 실행 중인지 확인하세요.')
        executor.shutdown()
        rclpy.shutdown()
        return
    print('OK')

    # ── 이동 전 현재 pose 확인 ───────────────────────────────────────────────
    before = robot.get_eef_pose()
    print(f'현재 EEF pose (이동 전): {before}')

    # ── 이동 (서비스 결과 직접 확인) ─────────────────────────────────────────
    if mode == 'joint':
        req = robot._movej_cli.srv_type.Request()
        req.pos       = [float(v) for v in positions]
        req.vel       = float(VELOCITY)      # MoveJoint: 스칼라 float
        req.acc       = float(ACCELERATION)  # MoveJoint: 스칼라 float
        req.time      = 0.0
        req.radius    = 0.0
        req.mode      = 0
        req.blend_type = 0
        req.sync_type = 0  # 0=비동기(즉시 반환), 1=동작 완료까지 블로킹
        fut = robot._movej_cli.call_async(req)
    else:
        req = robot._movel_cli.srv_type.Request()
        req.pos       = [float(v) for v in positions]
        req.vel       = [float(VELOCITY)] * 2
        req.acc       = [float(ACCELERATION)] * 2
        req.time      = 0.0
        req.radius    = 0.0
        req.ref       = 0      # base frame
        req.mode      = 0      # absolute
        req.blend_type = 0
        req.sync_type = 0  # 0=비동기(즉시 반환), 1=동작 완료까지 블로킹
        fut = robot._movel_cli.call_async(req)

    done = robot._wait_future(fut, timeout_sec=30.0)
    if not done:
        print('[ERROR] 서비스 응답 타임아웃 (30초)')
    else:
        result = fut.result()
        print(f'서비스 응답 → success={result.success}')

    after = robot.get_eef_pose()
    print(f'현재 EEF pose (이동 후): {after}')

    if before is not None and after is not None:
        diff = [round(a - b, 2) for a, b in zip(after, before)]
        print(f'변화량: {diff}')
        if all(abs(d) < 0.1 for d in diff):
            print('[WARNING] 로봇이 실제로 이동하지 않았습니다.')
            print('  → 로봇이 AUTO 모드인지 확인하세요.')
            print('  → E-STOP이 눌려있지 않은지 확인하세요.')
            print('  → 목표 pose가 현재 pose와 동일한지 확인하세요.')

    print(f'move_{"joint" if mode == "joint" else "line"} 완료')

    # ── 그리퍼 ───────────────────────────────────────────────────────────────
    print(f'그리퍼 → {GRIPPER_POS}')
    if GRIPPER_POS <= 0:
        gripper.open()
    elif GRIPPER_POS >= 700:
        gripper.close()
    else:
        gripper.move_to(GRIPPER_POS)

    print('완료.')

    executor.shutdown()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
