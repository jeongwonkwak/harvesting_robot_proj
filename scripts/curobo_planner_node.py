#!/usr/bin/env python3
"""
cuRobo Motion Planner Node for Doosan E0509

Subscribes to target pose, plans collision-free trajectory using cuRobo,
and executes via Doosan MoveSplineJoint service.

Usage:
    ros2 run e0509_gripper_description curobo_planner_node.py

Test:
    ros2 topic pub --once /dsr01/curobo/target_pose geometry_msgs/msg/PoseStamped \
        "{header: {frame_id: 'base_link'}, pose: {position: {x: 0.3, y: 0.2, z: 0.3}, \
        orientation: {x: 0.0, y: 0.7071, z: 0.0, w: 0.7071}}}"
"""

import os
import time
import threading
import torch
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64MultiArray
from std_srvs.srv import Trigger
from dsr_msgs2.srv import MoveSplineJoint, MoveJoint, MoveLine

from curobo.types.base import TensorDeviceType
from curobo.types.robot import JointState as CuroboJointState, RobotConfig
from curobo.types.math import Pose
from curobo.wrap.reacher.motion_gen import MotionGen, MotionGenConfig
from curobo.geom.types import WorldConfig, Cuboid
from std_msgs.msg import String
import json

# ===== 상수 =====
HOME_JOINTS_DEG = [-3.12, 41.11, -107.67, 97.45, 23.47, -20.53]  # 스캔 포즈 (실측 2026-05-12)
TWIST_DEG   = 40.0
GRASP_HEIGHT = 0.03   # target 위 3cm (줄기 잡기)
MAX_GRASP_Z  = 0.70   # 's' 키가 0.65m 성공 → 0.70m까지 허용
# ================


def _wait_motion(deg_start, deg_end, vel_deg_s, margin=1.5, min_sec=0.5):
    """관절 최대 이동각 / 속도 * margin 으로 대기 시간 산출."""
    max_delta = float(np.max(np.abs(np.array(deg_end) - np.array(deg_start))))
    return max(max_delta / vel_deg_s * margin, min_sec)


class CuroboPlanner(Node):
    JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]

    def __init__(self):
        super().__init__("curobo_planner_node")

        self.service_cb_group = rclpy.callback_groups.ReentrantCallbackGroup()

        self.get_logger().info("Initializing cuRobo planner...")

        self.current_joints = None
        self._pick_lock = threading.Lock()   # 중복 픽 방지

        config_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config", "curobo"
        )
        if not os.path.exists(config_dir):
            from ament_index_python.packages import get_package_share_directory
            config_dir = os.path.join(
                get_package_share_directory("e0509_gripper_description"),
                "config", "curobo"
            )

        self.get_logger().info(f"Config dir: {config_dir}")

        tensor_args = TensorDeviceType(device=torch.device("cuda:0"))

        robot_cfg = RobotConfig.from_basic(
            urdf_path=os.path.join(config_dir, "e0509_gripper.urdf"),
            base_link="base_link",
            ee_link="gripper_rh_p12_rn_base",
            tensor_args=tensor_args,
        )

        world_cfg = WorldConfig(
            cuboid=[
                Cuboid(name="table", pose=[0.0, 0.0, -0.02, 1, 0, 0, 0], dims=[1.2, 1.2, 0.04]),
            ]
        )

        motion_gen_cfg = MotionGenConfig.load_from_robot_config(
            robot_cfg,
            world_cfg,
            tensor_args=tensor_args,
            num_trajopt_seeds=12,
            num_graph_seeds=12,
            collision_cache={"obb": 30, "mesh": 10},
        )
        self.motion_gen = MotionGen(motion_gen_cfg)
        self.motion_gen.warmup(warmup_js_trajopt=False)
        self.get_logger().info("cuRobo MotionGen warmed up!")

        self.tensor_args = tensor_args
        self.robot_cfg = robot_cfg

        # ROS2 인터페이스
        self.joint_sub = self.create_subscription(
            JointState, "/dsr01/joint_states", self.joint_state_cb, 10)

        self.target_sub = self.create_subscription(
            PoseStamped, "/dsr01/curobo/target_pose", self.target_pose_cb, 10)

        self.pick_sub = self.create_subscription(
            PoseStamped, "/dsr01/curobo/pick_pose", self.pick_pose_cb, 10)

        self.obstacles_sub = self.create_subscription(
            String, "/dsr01/curobo/obstacles", self.obstacles_cb, 10)

        # Doosan 서비스
        self.cli_spline = self.create_client(
            MoveSplineJoint, "/dsr01/motion/move_spline_joint",
            callback_group=self.service_cb_group)
        self.cli_movej = self.create_client(
            MoveJoint, "/dsr01/motion/move_joint",
            callback_group=self.service_cb_group)
        self.cli_movel = self.create_client(
            MoveLine, "/dsr01/motion/move_line",
            callback_group=self.service_cb_group)
        self.cli_gripper_open = self.create_client(
            Trigger, "/dsr01/gripper/open",
            callback_group=self.service_cb_group)
        self.cli_gripper_close = self.create_client(
            Trigger, "/dsr01/gripper/close",
            callback_group=self.service_cb_group)

        self.get_logger().info("========================================")
        self.get_logger().info("cuRobo Planner Ready!")
        self.get_logger().info("  /dsr01/curobo/target_pose  → move (s key)")
        self.get_logger().info("  /dsr01/curobo/pick_pose    → full pick (p key)")
        self.get_logger().info("========================================")

        # 시작 시 자동 스캔 포즈 이동 (3초 후)
        self._init_timer = self.create_timer(3.0, self._init_scan_pose)

    # ──────────────────────────────────────────────────────────────────────────
    # 초기화
    # ──────────────────────────────────────────────────────────────────────────

    def _init_scan_pose(self):
        """One-shot: 시작 시 스캔 포즈로 이동."""
        self._init_timer.cancel()
        self.get_logger().info("Auto-moving to scan pose...")
        self.move_joint(HOME_JOINTS_DEG, vel=15.0)
        self.get_logger().info("Scan pose ready - waiting for targets")

    # ──────────────────────────────────────────────────────────────────────────
    # 콜백
    # ──────────────────────────────────────────────────────────────────────────

    def obstacles_cb(self, msg: String):
        try:
            obstacles_data = json.loads(msg.data)
            cuboids = [
                Cuboid(name="table", pose=[0.0, 0.0, -0.02, 1, 0, 0, 0], dims=[1.2, 1.2, 0.04])
            ]
            for obj in obstacles_data:
                cuboids.append(Cuboid(
                    name=obj["name"],
                    pose=[obj["pos"][0], obj["pos"][1], obj["pos"][2], 1, 0, 0, 0],
                    dims=obj.get("dims", [0.05, 0.05, 0.05])
                ))
            self.motion_gen.update_world(WorldConfig(cuboid=cuboids))
            self.get_logger().info(f"World updated: {len(obstacles_data)} objects + table")
        except Exception as e:
            self.get_logger().error(f"Failed to update obstacles: {e}")

    def joint_state_cb(self, msg: JointState):
        joint_map = {}
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                joint_map[name] = msg.position[i]
        joints = []
        for name in self.JOINT_NAMES:
            if name in joint_map:
                joints.append(joint_map[name])
            else:
                return
        self.current_joints = joints

    def target_pose_cb(self, msg: PoseStamped):
        """'s' 키 → 목표 위치로 이동 (cuRobo IK + MoveJoint).
        msg orientation → scan_quat → down_quat 순서로 폴백."""
        if self.current_joints is None:
            self.get_logger().warn("No joint state received yet")
            return

        pos = msg.pose.position
        ori = msg.pose.orientation
        home_rad = [np.deg2rad(j) for j in HOME_JOINTS_DEG]
        scan_quat = self.get_ee_quat_wxyz(home_rad)
        down_quat = [0.0, 0.7071, 0.7071, 0.0]

        # 메시지에 유효한 orientation이 있으면 첫 번째로 시도
        msg_quat = [ori.w, ori.x, ori.y, ori.z]
        quat_norm = sum(v**2 for v in msg_quat) ** 0.5
        candidates = []
        if quat_norm > 0.99:
            candidates.append(("msg_quat", msg_quat))
        candidates += [("scan_quat", scan_quat), ("down_quat", down_quat)]

        self.get_logger().info(
            f"Target: pos=[{pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f}]")

        for label, quat in candidates:
            traj = self.plan(self.current_joints, [pos.x, pos.y, pos.z], quat)
            if traj is not None:
                self.get_logger().info(f"Planning SUCCESS with {label}")
                self.execute_movej(traj)
                return
            self.get_logger().warn(f"Planning failed with {label}, trying next...")

        self.get_logger().error("Planning failed with all orientations!")

    def pick_pose_cb(self, msg: PoseStamped):
        """'p' 키 → 딸기 픽 시퀀스 (중복 실행 방지)."""
        if not self._pick_lock.acquire(blocking=False):
            self.get_logger().warn("Pick already in progress, ignoring")
            return
        try:
            self._pick_sequence(msg)
        finally:
            self._pick_lock.release()

    # ──────────────────────────────────────────────────────────────────────────
    # 픽 시퀀스
    # ──────────────────────────────────────────────────────────────────────────

    def _pick_sequence(self, msg: PoseStamped):
        pos = msg.pose.position

        target_z = max(pos.z, 0.02)
        grasp_z   = min(target_z + GRASP_HEIGHT, MAX_GRASP_Z)  # workspace 상한 클램핑

        self.get_logger().info(
            f"=== PICK START: target=({pos.x:.3f},{pos.y:.3f},{target_z:.3f})m "
            f"grasp_z={grasp_z*1000:.0f}mm ===")

        # Step 0 : 스캔 포즈로 귀환 (완료까지 대기)
        self.get_logger().info("=== Step 0/5: Homing to scan pose ===")
        if not self.move_joint(HOME_JOINTS_DEG, vel=20.0):
            self.get_logger().error("Pick failed: homing failed")
            return
        time.sleep(0.5)  # joint_states 갱신 대기

        # Step 1 : 그리퍼 열기
        self.get_logger().info("=== Step 1/5: Open gripper ===")
        self.call_trigger(self.cli_gripper_open)
        time.sleep(1.5)

        # Step 2 : cuRobo로 grasp_z 위치까지 이동 (scan pose → grasp)
        self.get_logger().info(f"=== Step 2/5: Descend to Z={grasp_z*1000:.0f}mm ===")
        home_rad = [np.deg2rad(j) for j in HOME_JOINTS_DEG]
        scan_quat = self.get_ee_quat_wxyz(home_rad)
        down_quat = [0.0, 0.7071, 0.7071, 0.0]  # 그리퍼 수직 하향 폴백

        traj = None
        for label, quat in [("scan_quat", scan_quat), ("down_quat", down_quat)]:
            traj = self.plan(home_rad, [pos.x, pos.y, grasp_z], quat)
            if traj is not None:
                self.get_logger().info(f"  Descend planning SUCCESS with {label}")
                break
            self.get_logger().warn(f"  Descend planning failed with {label}, trying next...")

        if traj is None:
            self.get_logger().error("Pick failed: descend planning failed")
            return
        self.execute_movej(traj)

        # Step 3 : 그리퍼 닫기
        self.get_logger().info("=== Step 3/5: Close gripper ===")
        self.call_trigger(self.cli_gripper_close)
        time.sleep(1.0)

        # Step 4 : 꼭지 분리 (J6 회전 twist — MoveLine 대신 joint space 사용)
        # J6은 ±360° 제한이므로 어떤 pose에서도 안전
        self.get_logger().info("=== Step 4/5: Twist (J6 rotation) ===")
        if self.current_joints is not None:
            cur_deg = np.rad2deg(self.current_joints).tolist()
            twist_fwd = cur_deg.copy()
            twist_fwd[5] += TWIST_DEG
            twist_bwd = cur_deg.copy()
            twist_bwd[5] -= TWIST_DEG
            self.move_joint(twist_fwd, vel=40.0)
            time.sleep(0.3)
            self.move_joint(twist_bwd, vel=40.0)
        else:
            self.get_logger().warn("current_joints None, skipping twist")

        # Step 5 : 스캔 포즈로 복귀 (관절 한계 안전)
        self.get_logger().info("=== Step 5/5: Retreat to scan pose ===")
        self.move_joint(HOME_JOINTS_DEG, vel=15.0)

        self.get_logger().info("=== PICK COMPLETE ===")

    # ──────────────────────────────────────────────────────────────────────────
    # cuRobo
    # ──────────────────────────────────────────────────────────────────────────

    def get_ee_quat_wxyz(self, joint_positions_rad):
        """FK로 현재 EE 쿼터니언 반환 (wxyz)."""
        js = CuroboJointState.from_position(
            position=torch.tensor([joint_positions_rad], device="cuda:0", dtype=torch.float32),
            joint_names=self.JOINT_NAMES,
        )
        state = self.motion_gen.kinematics.get_state(js.position)
        return state.ee_pose.quaternion[0].cpu().tolist()  # [w, x, y, z]

    def plan(self, start_joints, target_pos, target_quat_wxyz):
        """cuRobo MotionGen으로 경로 계획. 성공 시 numpy array (N,6) rad 반환."""
        t0 = time.time()

        start_state = CuroboJointState.from_position(
            position=torch.tensor([start_joints], device="cuda:0", dtype=torch.float32),
            joint_names=self.JOINT_NAMES,
        )
        target_pose = Pose(
            position=torch.tensor([target_pos], device="cuda:0", dtype=torch.float32),
            quaternion=torch.tensor([target_quat_wxyz], device="cuda:0", dtype=torch.float32),
        )

        result = self.motion_gen.plan_single(start_state, target_pose)
        plan_time = (time.time() - t0) * 1000

        if result.success.item():
            traj = result.get_interpolated_plan()
            positions = traj.position.cpu().numpy()
            self.get_logger().info(f"Planning SUCCESS: {plan_time:.1f}ms, {positions.shape[0]} pts")
            return positions
        else:
            self.get_logger().error(f"Planning FAILED: {plan_time:.1f}ms")
            return None

    # ──────────────────────────────────────────────────────────────────────────
    # 모션 실행 (모두 시간 기반 대기)
    # ──────────────────────────────────────────────────────────────────────────

    def execute_spline(self, traj_rad) -> bool:
        """MoveSplineJoint로 궤적 실행. 완료까지 시간 기반 대기."""
        if not self.cli_spline.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("MoveSplineJoint service not available")
            return False

        traj_deg = np.rad2deg(traj_rad)
        n = traj_deg.shape[0]

        # 최대 8 포인트로 서브샘플 (포인트 많으면 DSR이 극도로 느림)
        if n > 8:
            indices = np.linspace(0, n - 1, 8, dtype=int)
            traj_deg = traj_deg[indices]
            n = 8

        req = MoveSplineJoint.Request()
        req.pos_cnt = n
        for row in traj_deg:
            pt = Float64MultiArray()
            pt.data = row.tolist()
            req.pos.append(pt)
        req.vel  = [30.0] * 6
        req.acc  = [60.0] * 6
        req.time = 0.0
        req.mode = 0
        req.sync_type = 1  # ASYNC (DSR sync_type=0도 즉시 반환하는 것으로 확인됨)

        # 이동 예상 시간: start→end 직선 거리가 아닌 전체 경로 합산 (spline은 중간 포인트 경유)
        total_path_deg = sum(
            float(np.max(np.abs(traj_deg[i + 1] - traj_deg[i])))
            for i in range(n - 1)
        )
        wait_sec = max(total_path_deg / 30.0 * 1.5, 3.0)

        self.get_logger().info(
            f"Spline {n}pts  start={[f'{v:.1f}' for v in traj_deg[0]]}  "
            f"end={[f'{v:.1f}' for v in traj_deg[-1]]}  est={wait_sec:.1f}s")

        future = self.cli_spline.call_async(req)
        call_start = time.time()
        while not future.done() and (time.time() - call_start) < 5.0:
            time.sleep(0.05)

        if not (future.done() and future.result() and future.result().success):
            self.get_logger().error("Spline service call failed")
            return False

        # 실제 모션 완료 대기
        self.get_logger().info(f"  waiting {wait_sec:.1f}s for spline motion...")
        time.sleep(wait_sec)
        self.get_logger().info("  spline motion done")
        return True

    def execute_movej(self, traj_rad):
        """궤적 마지막 포즈로 MoveJoint 이동 ('s' 키용)."""
        if not self.cli_movej.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("MoveJoint service not available")
            return

        final_deg = np.rad2deg(traj_rad[-1]).tolist()
        self.get_logger().info(f"MoveJoint → {[f'{v:.1f}' for v in final_deg]}")

        req = MoveJoint.Request()
        req.pos       = final_deg
        req.vel       = 30.0
        req.acc       = 60.0
        req.time      = 0.0
        req.radius    = 0.0
        req.mode      = 0
        req.blend_type = 0
        req.sync_type  = 1  # ASYNC

        # 이동 예상 시간
        current_deg = np.rad2deg(self.current_joints).tolist() if self.current_joints else final_deg
        wait_sec = _wait_motion(current_deg, final_deg, vel_deg_s=30.0, margin=1.5, min_sec=0.5)

        future = self.cli_movej.call_async(req)
        call_start = time.time()
        while not future.done() and (time.time() - call_start) < 5.0:
            time.sleep(0.05)

        if future.done() and future.result() and future.result().success:
            self.get_logger().info(f"  waiting {wait_sec:.1f}s for joint motion...")
            time.sleep(wait_sec)
            self.get_logger().info("  joint motion done")
        else:
            self.get_logger().error("MoveJoint call failed")

    def move_joint(self, joints_deg: list, vel=20.0) -> bool:
        """관절 이동 + 완료 대기. 픽 시퀀스 내부용."""
        if not self.cli_movej.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("MoveJoint service not available")
            return False

        current_deg = np.rad2deg(self.current_joints).tolist() if self.current_joints else joints_deg
        wait_sec = _wait_motion(current_deg, joints_deg, vel_deg_s=vel, margin=1.5, min_sec=0.5)

        req = MoveJoint.Request()
        req.pos       = [float(j) for j in joints_deg]
        req.vel       = float(vel)
        req.acc       = float(vel * 2)
        req.time      = 0.0
        req.sync_type = 1  # ASYNC

        future = self.cli_movej.call_async(req)
        call_start = time.time()
        while not future.done() and (time.time() - call_start) < 5.0:
            time.sleep(0.05)

        if not (future.done() and future.result() and future.result().success):
            self.get_logger().error("move_joint service call failed")
            return False

        self.get_logger().info(f"  waiting {wait_sec:.1f}s for joint motion...")
        time.sleep(wait_sec)
        return True

    def move_linear(self, x, y, z, vel=100.0, rz=0.0):
        """TCP 직선 이동 + 완료 대기 (twist용)."""
        if not self.cli_movel.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("MoveLine service not available")
            return

        req = MoveLine.Request()
        req.pos        = [x * 1000, y * 1000, z * 1000, 0.0, 180.0, rz]
        req.vel        = [vel, 30.0]
        req.acc        = [vel, 30.0]
        req.time       = 0.0
        req.ref        = 0
        req.mode       = 0
        req.blend_type = 0
        req.sync_type  = 1  # ASYNC

        # twist는 짧은 회전이므로 1.5s 고정
        future = self.cli_movel.call_async(req)
        call_start = time.time()
        while not future.done() and (time.time() - call_start) < 5.0:
            time.sleep(0.05)

        if future.done() and future.result() and future.result().success:
            self.get_logger().info(f"MoveLine Z={z*1000:.0f}mm rz={rz:.0f}°  waiting 1.5s...")
            time.sleep(1.5)
        else:
            self.get_logger().error("MoveLine call failed")

    def call_trigger(self, client):
        """Trigger 서비스 호출 (그리퍼)."""
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("Trigger service not available")
            return
        future = client.call_async(Trigger.Request())
        start = time.time()
        while not future.done() and (time.time() - start) < 10.0:
            time.sleep(0.1)
        if future.done() and future.result():
            self.get_logger().info(f"Trigger: {future.result().message}")


def main():
    rclpy.init()
    node = CuroboPlanner()
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
