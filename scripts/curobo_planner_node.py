#!/usr/bin/env python3
"""
cuRobo Motion Planner Node for Doosan E0509

Pick sequence:
  open → approach(CuRobo 15cm) → grasp(CuRobo) → close
       → [check] → retreat(CuRobo) → bin → home → pick_complete
"""

import os
import time
import torch
import numpy as np
import json

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64MultiArray, String, Int32, Empty
from std_srvs.srv import Trigger
from dsr_msgs2.srv import MoveSplineJoint, MoveJoint

from curobo.types.base import TensorDeviceType
from curobo.types.robot import JointState as CuroboJointState, RobotConfig
from curobo.types.math import Pose
from curobo.wrap.reacher.motion_gen import MotionGen, MotionGenConfig, MotionGenPlanConfig
from curobo.geom.types import WorldConfig, Cuboid


# ── 딸기 접근 파라미터 ────────────────────────────────────────────────────────
APPROACH_OFFSET  = 0.15    # 딸기 앞 15cm (TCP 기준)
STAGING_EXTRA    = 0.15    # staging 추가 거리: approach보다 15cm 더 뒤
GRASP_OFFSET     = -0.03   # TCP를 딸기 중심보다 벽 방향으로 3cm 더 밀어 넣음
RETREAT_OFFSET   = 0.20    # 딸기 뒤 20cm
PRE_BIN_CLEAR_OFFSET = 0.35 # bin 이동 전 벽에서 충분히 빠지는 clear 지점
GRASP_Z_BIAS     = -0.030  # 검출 중심보다 30mm 낮게 파지
USE_STAGING      = False   # True: 30cm staging → 15cm approach → grasp
USE_PRE_BIN_CLEAR = False  # True: retreat 후 clear 지점을 거쳐 bin transfer
USE_BIN_TRANSFER = True    # True: bin 전 HOME/안전 관절 자세 경유

GRIPPER_LEN      = 0.160   # ee_link → TCP 거리 (m)
WALL_UNIT        = np.array([-0.035, 0.996, -0.084])   # 티치펜던트 실측 (2026-05-18)
WALL_QUAT_WXYZ   = [0.548415, -0.439294, 0.424628, 0.570923]  # ee_link [w,x,y,z] (2026-05-18)

# ── 고정 자세 ─────────────────────────────────────────────────────────────────
HOME_JOINTS_DEG  = [88.0, -80.0, 130.0, 0.0, 20.0, -90.0]
HOME_JOINTS_RAD  = np.deg2rad(HOME_JOINTS_DEG).tolist()
BIN_JOINTS_DEG   = [0.0, 65.0, 25.0, 0.0, 90.0, 0.0]
BIN_TRANSFER_JOINTS_DEG = HOME_JOINTS_DEG  # 벽에서 빠진 뒤 bin으로 가기 전 안전 관절 자세

# ── 파지 성공 판별 ────────────────────────────────────────────────────────────
USE_GRASP_CHECK  = False  # /gripper/stroke는 현재 명령값이라 실제 파지 판정에 쓰지 않음
GRASP_STROKE_MIN = 10   # stroke 이하면 파지 실패 (완전 닫힘)

# ── 그리퍼 soft close ─────────────────────────────────────────────────────────
USE_SOFT_CLOSE    = True
GRIPPER_PRE_CLOSE_POS = 300     # 접촉 전 1차 닫힘
GRIPPER_CONTACT_POS   = 400     # 스퀴지 딸기 표면 접촉 위치
GRIPPER_HARVEST_POS   = 490     # 스퀴지 딸기 수확 가능한 최소 파지 위치
GRIPPER_CLOSE_STEPS = [
    ("pre", GRIPPER_PRE_CLOSE_POS),
    ("contact", GRIPPER_CONTACT_POS),
    ("harvest", GRIPPER_HARVEST_POS),
]
GRIPPER_STEP_DELAY = 1.2               # gripper_service_node가 명령 처리할 시간


class CuroboPlanner(Node):

    JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]

    JOINT_LIMITS = [
        (-6.273185, 6.273185),
        (-1.648063, 1.648063),
        (-2.6953,   2.6953  ),  # J3: ±155°
        (-6.273185, 6.273185),
        (-2.346194, 2.346194),  # J5: ±135°
        (-6.273185, 6.273185),
    ]

    def __init__(self):
        super().__init__("curobo_planner_node")

        self.service_cb_group = rclpy.callback_groups.ReentrantCallbackGroup()
        self.current_joints = None
        self.gripper_stroke = None
        self._pick_busy = False

        # ── cuRobo 초기화 ─────────────────────────────────────────────────────
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

        tensor_args = TensorDeviceType(device=torch.device("cuda:0"))
        robot_cfg = RobotConfig.from_basic(
            urdf_path=os.path.join(config_dir, "e0509_gripper.urdf"),
            base_link="base_link",
            ee_link="gripper_rh_p12_rn_base",
            tensor_args=tensor_args,
        )
        world_cfg = WorldConfig(cuboid=[
            Cuboid(name="table", pose=[0.0, 0.0, -0.02, 1, 0, 0, 0], dims=[1.2, 1.2, 0.04]),
        ])
        motion_gen_cfg = MotionGenConfig.load_from_robot_config(
            robot_cfg, world_cfg, tensor_args=tensor_args,
            num_trajopt_seeds=16, num_graph_seeds=16,
            collision_cache={"obb": 30, "mesh": 10},
            use_cuda_graph=False,
        )
        self.motion_gen = MotionGen(motion_gen_cfg)
        self.motion_gen.warmup(warmup_js_trajopt=False)
        self.get_logger().info("cuRobo MotionGen warmed up!")

        # ── ROS2 인터페이스 ───────────────────────────────────────────────────
        self.create_subscription(JointState, "/dsr01/joint_states", self.joint_state_cb, 10)
        self.create_subscription(PoseStamped, "/dsr01/curobo/target_pose", self.target_pose_cb, 10)
        self.create_subscription(PoseStamped, "/dsr01/curobo/pick_pose", self.pick_pose_cb, 10)
        self.create_subscription(String, "/dsr01/curobo/obstacles", self.obstacles_cb, 10)
        self.create_subscription(Int32, "/dsr01/gripper/stroke", self._stroke_cb, 10)

        self.pick_complete_pub = self.create_publisher(Empty, "/dsr01/curobo/pick_complete", 10)
        self.gripper_pos_pub = self.create_publisher(Int32, "/dsr01/gripper/position_cmd", 10)

        self.cli_spline = self.create_client(
            MoveSplineJoint, "/dsr01/motion/move_spline_joint",
            callback_group=self.service_cb_group)
        self.cli_movej = self.create_client(
            MoveJoint, "/dsr01/motion/move_joint",
            callback_group=self.service_cb_group)
        self.cli_gripper_open = self.create_client(
            Trigger, "/dsr01/gripper/open", callback_group=self.service_cb_group)
        self.cli_gripper_close = self.create_client(
            Trigger, "/dsr01/gripper/close", callback_group=self.service_cb_group)

        self.get_logger().info("cuRobo Planner Ready!")
        self.get_logger().info(f"  GRASP_STROKE_MIN={GRASP_STROKE_MIN}  BIN={BIN_JOINTS_DEG}")

    # ── 콜백 ─────────────────────────────────────────────────────────────────

    def joint_state_cb(self, msg: JointState):
        jmap = {n: p for n, p in zip(msg.name, msg.position)}
        joints = [jmap.get(n) for n in self.JOINT_NAMES]
        if None not in joints:
            self.current_joints = joints

    def _stroke_cb(self, msg: Int32):
        self.gripper_stroke = msg.data

    def target_pose_cb(self, msg: PoseStamped):
        if self.current_joints is None:
            self.get_logger().warn("No joint state yet")
            return
        p, o = msg.pose.position, msg.pose.orientation
        ret = self.plan(self.current_joints, [p.x, p.y, p.z], [o.w, o.x, o.y, o.z])
        if ret is not None:
            self.execute_spline(*ret)

    def obstacles_cb(self, msg: String):
        try:
            data = json.loads(msg.data)
            cuboids = [Cuboid(name="table", pose=[0, 0, -0.02, 1, 0, 0, 0], dims=[1.2, 1.2, 0.04])]
            for obj in data:
                cuboids.append(Cuboid(
                    name=obj["name"],
                    pose=[*obj["pos"], 1, 0, 0, 0],
                    dims=obj.get("dims", [0.05, 0.05, 0.05])
                ))
            self.motion_gen.update_world(WorldConfig(cuboid=cuboids))
            self.get_logger().info(f"World updated: {len(cuboids)} obstacles")
        except Exception as e:
            self.get_logger().error(f"obstacles_cb error: {e}")

    # ── 핵심 메서드 ───────────────────────────────────────────────────────────

    def _clamp_joints(self, joints):
        return [float(np.clip(j, lo, hi)) for j, (lo, hi) in zip(joints, self.JOINT_LIMITS)]

    def _try_ik_with_seed(self, target_pos, target_quat_wxyz, seed_joints_rad, num_seeds=64):
        """캘리브레이션 delta를 seed로 IK 시도 (approach→grasp 예상 변화량). 성공 시 rad 리스트 반환."""
        # 15cm 전진 기준 실측 delta, 18cm(grasp)에 맞게 1.2 스케일
        scale = 1.2
        cal_delta = np.array([0,
                               np.deg2rad(33.58) * scale,
                               np.deg2rad(-41.61) * scale,
                               0,
                               np.deg2rad(9.63) * scale,
                               0])
        cal_seed = [j + d for j, d in zip(seed_joints_rad, cal_delta)]
        seeds = torch.tensor([[cal_seed]], device='cuda:0', dtype=torch.float32)  # (1, 1, 6)
        tpose = Pose(
            position=torch.tensor([target_pos], device='cuda:0', dtype=torch.float32),
            quaternion=torch.tensor([target_quat_wxyz], device='cuda:0', dtype=torch.float32),
        )
        try:
            ik_res = self.motion_gen.ik_solver.solve_single(
                tpose, seed_config=seeds, num_seeds=num_seeds)
            if ik_res.success.item():
                sol = ik_res.solution.cpu().numpy().reshape(-1)[:6]
                return sol.tolist()
        except Exception as e:
            self.get_logger().warn(f"IK-seed error: {e}")
        return None

    def plan(self, start_joints, target_pos, target_quat_wxyz, num_ik_seeds=32):
        """CuRobo plan_single. 성공 시 (traj ndarray, motion_time_sec) 반환, 실패 시 None."""
        t0 = time.time()
        start_joints = self._clamp_joints(start_joints)

        start_state = CuroboJointState.from_position(
            position=torch.tensor([start_joints], device="cuda:0", dtype=torch.float32),
            joint_names=self.JOINT_NAMES,
        )
        target_pose = Pose(
            position=torch.tensor([target_pos], device="cuda:0", dtype=torch.float32),
            quaternion=torch.tensor([target_quat_wxyz], device="cuda:0", dtype=torch.float32),
        )
        result = self.motion_gen.plan_single(
            start_state, target_pose, MotionGenPlanConfig(num_ik_seeds=num_ik_seeds)
        )
        dt = (time.time() - t0) * 1000

        if result.success.item():
            traj = result.get_interpolated_plan().position.cpu().numpy()
            motion_time = float(result.motion_time.item())
            self.get_logger().info(
                f"Plan OK {dt:.0f}ms {traj.shape[0]}pts {motion_time:.2f}s | "
                f"goal={[f'{v*1000:.0f}' for v in target_pos]}mm")
            return traj, motion_time
        else:
            self.get_logger().error(
                f"Plan FAIL {dt:.0f}ms | status={getattr(result,'status','?')} | "
                f"goal={[f'{v*1000:.0f}' for v in target_pos]}mm")
            return None

    def execute_spline(self, traj_rad, motion_time: float) -> bool:
        """CuRobo trajectory(rad)를 MoveSplineJoint로 실행."""
        if not self.cli_spline.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("MoveSplineJoint not available")
            return False

        traj_deg = np.rad2deg(traj_rad)
        n = traj_deg.shape[0]
        if n > 10:
            idx = np.linspace(0, n - 1, 10, dtype=int)
            traj_deg = traj_deg[idx]
            n = 10

        req = MoveSplineJoint.Request()
        req.pos_cnt = n
        for row in traj_deg:
            pt = Float64MultiArray()
            pt.data = row.tolist()
            req.pos.append(pt)
        req.vel = [60.0] * 6
        req.acc = [80.0] * 6
        req.time = motion_time
        req.mode = 0
        req.sync_type = 0

        self.get_logger().info(f"Spline {n}pts {motion_time:.2f}s → end={[f'{v:.1f}' for v in traj_deg[-1]]}°")
        future = self.cli_spline.call_async(req)
        t0 = time.time()
        while not future.done() and (time.time() - t0) < 60.0:
            time.sleep(0.05)

        ok = future.done() and future.result() and future.result().success
        if not ok:
            self.get_logger().error("Spline failed/timeout")
        return ok

    def movej(self, joints_deg, vel=40.0, acc=40.0) -> bool:
        """MoveJoint으로 고정 자세 이동 (bin, home 등)."""
        if not self.cli_movej.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("MoveJoint not available")
            return False
        req = MoveJoint.Request()
        req.pos = joints_deg
        req.vel = vel
        req.acc = acc
        req.time = 0.0
        req.radius = 0.0
        req.mode = 0
        req.blend_type = 0
        req.sync_type = 0
        future = self.cli_movej.call_async(req)
        t0 = time.time()
        while not future.done() and (time.time() - t0) < 60.0:
            time.sleep(0.05)
        ok = future.done() and future.result() and future.result().success
        if not ok:
            self.get_logger().error("MoveJoint failed")
        return ok

    def call_trigger(self, client):
        if not client.wait_for_service(timeout_sec=3.0):
            return
        future = client.call_async(Trigger.Request())
        t0 = time.time()
        while not future.done() and (time.time() - t0) < 10.0:
            time.sleep(0.1)

    def soft_close_gripper(self):
        """Position command로 단계적으로 닫아 실제 딸기 압상을 줄인다."""
        if not USE_SOFT_CLOSE:
            self.call_trigger(self.cli_gripper_close)
            time.sleep(1.5)
            return

        if self.gripper_pos_pub.get_subscription_count() == 0:
            self.get_logger().warn("No /dsr01/gripper/position_cmd subscriber — Trigger close fallback")
            self.call_trigger(self.cli_gripper_close)
            time.sleep(1.5)
            return

        for label, pos in GRIPPER_CLOSE_STEPS:
            msg = Int32()
            msg.data = int(pos)
            self.gripper_pos_pub.publish(msg)
            self.get_logger().info(f"  soft close {label}: position_cmd={pos}")
            time.sleep(GRIPPER_STEP_DELAY)

    def _check_grasp(self) -> bool:
        """그리퍼 stroke로 파지 성공 여부 판별."""
        if not USE_GRASP_CHECK:
            if self.gripper_stroke is None:
                self.get_logger().info("Grasp check skipped: stroke 데이터 없음")
            else:
                self.get_logger().info(
                    f"Grasp check skipped: stroke={self.gripper_stroke} (명령값 기반)")
            return True
        if self.gripper_stroke is None:
            self.get_logger().warn("Stroke 데이터 없음 — 파지 성공으로 가정")
            return True
        ok = self.gripper_stroke > GRASP_STROKE_MIN
        self.get_logger().info(
            f"Grasp check: stroke={self.gripper_stroke} → {'OK' if ok else 'FAIL (fully closed)'}")
        return ok

    # ── Pick 시퀀스 ───────────────────────────────────────────────────────────

    def pick_pose_cb(self, msg: PoseStamped):
        """open → approach → grasp → close → [check] → retreat → bin → home"""
        if self.current_joints is None:
            self.get_logger().warn("No joint state yet")
            return
        if self._pick_busy:
            self.get_logger().warn("Pick already in progress — ignored")
            return
        self._pick_busy = True
        try:
            self._pick(msg)
        finally:
            self._pick_busy = False

    def _pick(self, msg: PoseStamped):
        p = msg.pose.position
        raw_straw = np.array([p.x, p.y, max(p.z, 0.05)])
        straw = raw_straw + np.array([0.0, 0.0, GRASP_Z_BIAS])
        straw[2] = max(straw[2], 0.05)

        # CuRobo ee_link 목표 위치
        ee_s = straw - (APPROACH_OFFSET + STAGING_EXTRA + GRIPPER_LEN) * WALL_UNIT
        ee_a = straw - (APPROACH_OFFSET + GRIPPER_LEN) * WALL_UNIT
        ee_g = straw - (GRASP_OFFSET    + GRIPPER_LEN) * WALL_UNIT
        ee_r = straw - (RETREAT_OFFSET  + GRIPPER_LEN) * WALL_UNIT
        ee_clear = straw - (PRE_BIN_CLEAR_OFFSET + GRIPPER_LEN) * WALL_UNIT

        self.get_logger().info(
            f"=== PICK 딸기 raw=({raw_straw[0]*1000:.0f},{raw_straw[1]*1000:.0f},{raw_straw[2]*1000:.0f})mm "
            f"grasp=({straw[0]*1000:.0f},{straw[1]*1000:.0f},{straw[2]*1000:.0f})mm ===")

        # 1. 그리퍼 열기
        self.get_logger().info("1 open gripper")
        self.call_trigger(self.cli_gripper_open)
        time.sleep(1.5)

        step = 2
        approach_start_joints = self.current_joints

        if USE_STAGING:
            self.get_logger().info(f"{step} staging (CuRobo 30cm)")
            ret = self.plan(self.current_joints, ee_s.tolist(), WALL_QUAT_WXYZ)
            if ret is None:
                self.get_logger().error("ABORT: staging plan failed")
                return
            # J1 branch 체크: 이상한 configuration이면 64-seed retry
            expected_j1 = np.pi / 2 + np.arctan2(-straw[0], straw[1])
            staging_j1 = float(ret[0][-1][0])
            j1_diff = abs(((staging_j1 - expected_j1 + np.pi) % (2 * np.pi)) - np.pi)
            if j1_diff > 2.0:
                self.get_logger().warn(
                    f"Staging J1 bad: {np.rad2deg(staging_j1):.1f}° (exp {np.rad2deg(expected_j1):.1f}°)"
                    f" → 64-seed retry")
                ret2 = self.plan(self.current_joints, ee_s.tolist(), WALL_QUAT_WXYZ, num_ik_seeds=64)
                if ret2 is not None:
                    ret = ret2
            if not self.execute_spline(*ret):
                self.get_logger().error("ABORT: staging exec failed")
                return
            approach_start_joints = ret[0][-1].tolist()
            step += 1

        # CuRobo: current/staging → approach (15cm)
        self.get_logger().info(f"{step} approach (CuRobo 15cm)")
        ret = self.plan(approach_start_joints, ee_a.tolist(), WALL_QUAT_WXYZ)
        if ret is None:
            self.get_logger().error("ABORT: approach plan failed")
            self.movej(HOME_JOINTS_DEG)
            return
        if not self.execute_spline(*ret):
            self.get_logger().error("ABORT: approach exec failed")
            return
        approach_joints = ret[0][-1].tolist()
        step += 1

        # CuRobo: approach → grasp
        self.get_logger().info(f"{step} grasp (CuRobo)")
        ret = self.plan(approach_joints, ee_g.tolist(), WALL_QUAT_WXYZ)
        if ret is not None:
            if not self.execute_spline(*ret):
                self.get_logger().error("ABORT: grasp exec failed")
                return
            grasp_joints = ret[0][-1].tolist()
        else:
            # Fallback: 캘리브레이션 seed IK → MoveJoint
            self.get_logger().warn("grasp CuRobo fail → IK-seed fallback")
            grasp_sol = self._try_ik_with_seed(ee_g.tolist(), WALL_QUAT_WXYZ, approach_joints)
            if grasp_sol is None:
                self.get_logger().error("ABORT: grasp IK_FAIL — workspace 한계")
                ret2 = self.plan(approach_joints, ee_r.tolist(), WALL_QUAT_WXYZ)
                if ret2 is not None:
                    self.execute_spline(*ret2)
                self.movej(HOME_JOINTS_DEG)
                self.pick_complete_pub.publish(Empty())
                return
            grasp_deg = np.rad2deg(grasp_sol).tolist()
            self.get_logger().info(f"IK-seed OK → MoveJoint {[f'{v:.1f}' for v in grasp_deg]}°")
            if not self.movej(grasp_deg, vel=20, acc=20):
                self.get_logger().error("ABORT: grasp MoveJoint failed")
                self.movej(HOME_JOINTS_DEG)
                self.pick_complete_pub.publish(Empty())
                return
            grasp_joints = grasp_sol

        # 5. 그리퍼 닫기
        step += 1
        self.get_logger().info(f"{step} close gripper")
        self.soft_close_gripper()

        # 6. 파지 성공 판별
        grasp_ok = self._check_grasp()

        # 7. Retreat
        step += 1
        self.get_logger().info(f"{step} retreat (CuRobo)")
        ret = self.plan(grasp_joints, ee_r.tolist(), WALL_QUAT_WXYZ)
        if ret is not None:
            self.execute_spline(*ret)
            retreat_joints = ret[0][-1].tolist()
        else:
            self.get_logger().warn("Retreat plan failed — home으로 직행")
            retreat_joints = grasp_joints

        if not grasp_ok:
            self.get_logger().warn("파지 실패 — abort")
            self.call_trigger(self.cli_gripper_open)
            self.movej(HOME_JOINTS_DEG)
            self.pick_complete_pub.publish(Empty())
            return

        # 8. Bin → deposit
        if USE_PRE_BIN_CLEAR:
            step += 1
            self.get_logger().info(f"{step} pre-bin clear (CuRobo)")
            ret = self.plan(retreat_joints, ee_clear.tolist(), WALL_QUAT_WXYZ)
            if ret is not None:
                if not self.execute_spline(*ret):
                    self.get_logger().error("ABORT: pre-bin clear exec failed — gripper 유지")
                    return
            else:
                self.get_logger().warn("Pre-bin clear plan failed — bin 이동 보류")
                return

        if USE_BIN_TRANSFER:
            step += 1
            self.get_logger().info(f"{step} → bin transfer")
            if not self.movej(BIN_TRANSFER_JOINTS_DEG, vel=20.0, acc=20.0):
                self.get_logger().error("ABORT: bin transfer failed — gripper 유지")
                return

        step += 1
        self.get_logger().info(f"{step} → bin")
        if not self.movej(BIN_JOINTS_DEG, vel=20.0, acc=20.0):
            self.get_logger().error("ABORT: bin move failed — gripper 유지")
            return
        time.sleep(0.5)
        self.call_trigger(self.cli_gripper_open)
        time.sleep(1.0)

        # 9. Home 복귀
        step += 1
        self.get_logger().info(f"{step} → home")
        if not self.movej(HOME_JOINTS_DEG):
            self.get_logger().error("Home move failed after deposit")

        # 10. 완료 신호
        self.pick_complete_pub.publish(Empty())
        self.get_logger().info("=== PICK COMPLETE ===")


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
