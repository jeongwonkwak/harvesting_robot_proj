"""
Doosan e0509 controller via dsr_ros2 (ROS2 Humble).

Required packages (on robot PC):
  ros-humble-dsr-msgs2
  ros-humble-dsr-bringup2   (or equivalent Doosan ROS2 driver)

Topic / service names follow the default dsr_ros2 convention with robot_id=dsr01.

State convention used here:
  joint_state  – [J1..J6]  in radians  (from /dsr01/joint_states)
  EEF pose     – [X, Y, Z, Rx, Ry, Rz] in mm / degrees (Doosan task-space)

Action convention from SmolVLA (6-DoF, normalised MEAN_STD):
  Interpreted as *delta* EEF pose by default (action_mode='cartesian').
  Set action_mode='joint' to interpret as *delta* joint positions.
"""

from __future__ import annotations

import math
import time
from typing import List, Optional

import numpy as np
import rclpy
from builtin_interfaces.msg import Duration
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

# Doosan message types – graceful fallback so the module still imports
# even when dsr_msgs2 is not installed (useful for unit tests / dry runs).
try:
    from dsr_msgs2.srv import MoveJoint, MoveLine, GetCurrentPose, JogMulti, MoveStop, MoveSplineTask
    from std_msgs.msg import Float64MultiArray as _Float64MultiArray
    _DSR_AVAILABLE = True
except ImportError:
    _DSR_AVAILABLE = False

_JOINT_NAMES = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
# Gazebo JointTrajectoryController 토픽 (bringup_gazebo의 /gz/ 브리지 경유)
_TRAJ_TOPIC = '/dsr01/joint_trajectory_controller/joint_trajectory'


# ---------------------------------------------------------------------------
# Scaling factors: SmolVLA raw delta → Doosan command unit
#   Cartesian: model output is typically in metres → convert to mm
#              rotation: model output is typically in radians → convert to deg
#   Joint:     model output in radians → keep as rad, but Doosan uses deg
# ---------------------------------------------------------------------------
_CART_POS_SCALE = 1000.0   # m  → mm
_CART_ROT_SCALE = 57.2958  # rad → deg
_JOINT_SCALE    = 57.2958  # rad → deg

# Safety clamps (per step)
_MAX_CART_DELTA_MM  = 20.0   # mm per step
_MAX_CART_DELTA_DEG = 10.0   # deg per step
_MAX_JOINT_DELTA_DEG = 5.0   # deg per step


class DoosanController:
    """Thin wrapper around dsr_ros2 services for Doosan e0509."""

    def __init__(self, node: Node, robot_id: str = "dsr01",
                 action_mode: str = "cartesian"):
        self._node = node
        self._prefix = f"/{robot_id}"
        self._action_mode = action_mode  # "cartesian" | "joint"
        self._joint_state: Optional[np.ndarray] = None  # radians

        # JointTrajectoryController 폴백 publisher (Doosan 서비스 없을 때 사용)
        self._traj_pub = node.create_publisher(JointTrajectory, _TRAJ_TOPIC, 10)

        # Doosan joint states (primary) + Gazebo joint states (fallback)
        self._js_sub = node.create_subscription(
            JointState, f"{self._prefix}/joint_states", self._joint_state_cb, 10)
        self._gz_js_sub = node.create_subscription(
            JointState, '/gz/joint_states', self._joint_state_cb, 10)

        if _DSR_AVAILABLE:
            self._init_services()
            # 서비스 실제 응답 가능 여부 확인
            self._doosan_available = self._movej_cli.service_is_ready()
            self._sim = False
        else:
            node.get_logger().warn(
                "dsr_msgs2 not found – DoosanController in SIMULATION mode."
            )
            self._sim = True
            self._doosan_available = False

    # ------------------------------------------------------------------
    # ROS2 setup
    # ------------------------------------------------------------------

    def _wait_future(self, future, timeout_sec: float) -> bool:
        """Poll until future is done. Executor runs in a separate thread —
        do NOT call spin_once here; just sleep and let the executor deliver the response."""
        deadline = time.monotonic() + timeout_sec
        while not future.done():
            if time.monotonic() > deadline:
                return False
            time.sleep(0.005)
        return True

    def _init_services(self) -> None:
        self._movej_cli = self._node.create_client(
            MoveJoint, f"{self._prefix}/motion/move_joint")
        self._movel_cli = self._node.create_client(
            MoveLine,  f"{self._prefix}/motion/move_line")
        self._pose_cli  = self._node.create_client(
            GetCurrentPose, f"{self._prefix}/system/get_current_pose")
        self._jogm_cli   = self._node.create_client(
            JogMulti,       f"{self._prefix}/motion/jog_multi")
        self._stop_cli   = self._node.create_client(
            MoveStop,       f"{self._prefix}/motion/move_stop")
        self._spline_cli = self._node.create_client(
            MoveSplineTask, f"{self._prefix}/motion/move_spline_task")

        for cli in (self._movej_cli, self._movel_cli, self._pose_cli):
            if not cli.wait_for_service(timeout_sec=5.0):
                self._node.get_logger().warn(
                    f"Service {cli.srv_name} not available.")

    def _joint_state_cb(self, msg: JointState) -> None:
        # joint_1..joint_6만 추출 (그리퍼 등 추가 관절 제외)
        name_pos = {n: p for n, p in zip(msg.name, msg.position)}
        arm = [name_pos[j] for j in _JOINT_NAMES if j in name_pos]
        if len(arm) == 6:
            self._joint_state = np.array(arm, dtype=np.float64)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_joint_state(self) -> Optional[np.ndarray]:
        """Return current joint positions in radians (6,)."""
        return self._joint_state.copy() if self._joint_state is not None else None

    def get_eef_pose(self) -> Optional[np.ndarray]:
        """Return current EEF pose [X,Y,Z,Rx,Ry,Rz] in mm/deg."""
        if self._sim:
            return np.zeros(6, dtype=np.float64)
        req = GetCurrentPose.Request()
        req.space_type = 1   # task space
        fut = self._pose_cli.call_async(req)
        if not self._wait_future(fut, timeout_sec=2.0):
            return None
        if fut.result() and fut.result().success:
            return np.array(fut.result().pos, dtype=np.float64)
        return None

    def move_joint(
        self,
        positions_deg: List[float],
        velocity: float = 30.0,
        acceleration: float = 60.0,
    ) -> None:
        """Move to absolute joint positions (degrees). Blocking."""
        # Doosan 서비스가 살아있으면 사용, 아니면 JointTrajectoryController 폴백
        if not self._sim and self._movej_cli.service_is_ready():
            self._move_joint_doosan(positions_deg, velocity, acceleration)
        else:
            duration = max(2.0, len(positions_deg) * 0.1 + 2.0)
            self._move_joint_traj(positions_deg, duration_sec=duration)

    def _move_joint_doosan(
        self, positions_deg: List[float],
        velocity: float, acceleration: float,
    ) -> None:
        req = MoveJoint.Request()
        req.pos        = positions_deg
        req.vel        = velocity
        req.acc        = acceleration
        req.time       = 0.0
        req.radius     = 0.0
        req.mode       = 0
        req.blend_type = 0
        req.sync_type  = 1
        fut = self._movej_cli.call_async(req)
        if not self._wait_future(fut, timeout_sec=30.0):
            self._node.get_logger().warn("move_joint service timed out.")
            return
        if fut.result() and not fut.result().success:
            self._node.get_logger().warn("move_joint service returned failure.")

    def _move_joint_traj(
        self, positions_deg: List[float], duration_sec: float = 3.0,
    ) -> None:
        """JointTrajectoryController로 직접 Gazebo 관절 제어."""
        traj = JointTrajectory()
        traj.joint_names = _JOINT_NAMES
        pt = JointTrajectoryPoint()
        pt.positions = [math.radians(d) for d in positions_deg]
        secs = int(duration_sec)
        pt.time_from_start = Duration(sec=secs, nanosec=int((duration_sec - secs) * 1e9))
        traj.points = [pt]
        self._traj_pub.publish(traj)
        self._node.get_logger().info(
            f"[TRAJ] move_joint {np.round(positions_deg, 1)} ({duration_sec:.1f}s)")
        time.sleep(duration_sec + 0.5)

    def move_line(
        self,
        pose_mm_deg: List[float],
        velocity: float = 50.0,
        acceleration: float = 100.0,
        blocking: bool = False,
        timeout_sec: float = 30.0,
    ) -> None:
        """
        Move EEF to absolute Cartesian pose [X,Y,Z,Rx,Ry,Rz] in mm/deg.
        If blocking=False (default), sends command asynchronously without waiting.
        """
        if self._sim:
            self._node.get_logger().info(
                f"[SIM] move_line: {np.round(pose_mm_deg, 2)}")
            return
        req = MoveLine.Request()
        req.pos        = [float(p) for p in pose_mm_deg]
        req.vel        = [float(velocity), float(velocity)]
        req.acc        = [float(acceleration), float(acceleration)]
        req.time       = 0.0
        req.radius     = 0.0
        req.ref        = 0   # world frame (DR_BASE)
        req.mode       = 0   # absolute
        req.blend_type = 0
        req.sync_type  = 1
        fut = self._movel_cli.call_async(req)

        if not blocking:
            return

        if not self._wait_future(fut, timeout_sec=timeout_sec):
            self._node.get_logger().warn("move_line service timed out.")
            return
        result = fut.result()
        if result is None:
            self._node.get_logger().warn("move_line service returned None (server may be down).")
        elif not result.success:
            self._node.get_logger().warn("move_line service returned failure.")

    def move_line_stream(self, pose_mm_deg: List[float],
                         vel_lin: float = 200.0, vel_rot: float = 40.0,
                         acc_lin: float = 800.0, acc_rot: float = 150.0) -> None:
        """Non-blocking move_line (sync_type=0) for jog.
        대형 목표 1회 발사 후 버튼 release 시 move_stop 으로 중단.
        vel_lin: TCP 선속도(mm/s), vel_rot: 각속도(deg/s)."""
        if self._sim:
            return
        req = MoveLine.Request()
        req.pos        = [float(p) for p in pose_mm_deg]
        req.vel        = [float(vel_lin), float(vel_rot)]
        req.acc        = [float(acc_lin), float(acc_rot)]
        req.time       = 0.0
        req.radius     = 0.0
        req.ref        = 0
        req.mode       = 0
        req.blend_type = 0
        req.sync_type  = 0   # Non-blocking: Python 즉시 반환, 로봇은 계속 실행
        self._movel_cli.call_async(req)

    def jog_multi(self, jog_axis: list, speed: float, move_reference: int = 0) -> None:
        """Continuous cartesian jog. jog_axis: 6-float unit vector [Tx,Ty,Tz,Rx,Ry,Rz],
        speed: % of max (0=stop, + forward, - backward). move_reference: 0=BASE, 1=TOOL."""
        if self._sim:
            self._node.get_logger().info(f"[SIM] jog_multi: {jog_axis} speed={speed:.1f}%")
            return
        req = JogMulti.Request()
        req.jog_axis = [float(v) for v in jog_axis]
        req.move_reference = int(move_reference)
        req.speed = float(speed)
        self._jogm_cli.call_async(req)

    def move_stop(self, stop_mode: int = 3) -> None:
        """Stop robot motion. stop_mode: 0=QStop_STO, 1=QStop, 2=SStop, 3=Hold(smooth)."""
        if self._sim:
            self._node.get_logger().info(f"[SIM] move_stop mode={stop_mode}")
            return
        req = MoveStop.Request()
        req.stop_mode = int(stop_mode)
        self._stop_cli.call_async(req)

    def move_spline_task(
        self,
        waypoints: list,
        velocity: float = 50.0,
        acceleration: float = 100.0,
        blocking: bool = True,
        timeout_sec: float = 120.0,
    ) -> None:
        """TCP 스플라인 이동. waypoints: [[X,Y,Z,Rx,Ry,Rz], ...] (mm/deg), max 100개."""
        if self._sim:
            self._node.get_logger().info(f"[SIM] move_spline_task: {len(waypoints)} pts")
            return
        if not waypoints or len(waypoints) < 2:
            self._node.get_logger().warn("move_spline_task: 웨이포인트 2개 이상 필요")
            return
        req = MoveSplineTask.Request()
        pts = []
        for wp in waypoints[:100]:
            pt = _Float64MultiArray()
            pt.data = [float(v) for v in wp]
            pts.append(pt)
        req.pos      = pts
        req.pos_cnt  = len(pts)
        req.vel      = [float(velocity), float(velocity)]
        req.acc      = [float(acceleration), float(acceleration)]
        req.time     = 0.0
        req.ref      = 0  # DR_BASE
        req.mode     = 0  # ABSOLUTE
        req.opt      = 0  # DEFAULT
        req.sync_type = 1
        fut = self._spline_cli.call_async(req)
        if not blocking:
            return
        if not self._wait_future(fut, timeout_sec=timeout_sec):
            self._node.get_logger().warn("move_spline_task timed out.")
            return
        result = fut.result()
        if result is None or not result.success:
            self._node.get_logger().warn("move_spline_task returned failure.")

    def execute_action(self, action: np.ndarray, velocity: float = 20.0, acceleration: float = 40.0) -> None:
        """
        Execute one VLA action step.

        action shape: (6,)
          cartesian mode → [dx, dy, dz, drx, dry, drz]  (model normalised units)
          joint mode     → [dJ1..dJ6]                    (model normalised units)
        """
        if self._action_mode == "cartesian":
            self._execute_cartesian_delta(action, velocity=velocity, acceleration=acceleration)
        else:
            self._execute_joint_delta(action)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _execute_cartesian_delta(self, action: np.ndarray, velocity: float = 20.0, acceleration: float = 40.0) -> None:
        current = self.get_eef_pose()
        if current is None:
            self._node.get_logger().error("Cannot get EEF pose.")
            return

        delta_pos = np.clip(
            action[:3] * _CART_POS_SCALE,
            -_MAX_CART_DELTA_MM,
             _MAX_CART_DELTA_MM,
        )
        # 회전 델타 미적용: 현재 자세 유지 (Doosan 손목 관절 한계 초과 방지)
        target = current + np.concatenate([delta_pos, np.zeros(3)])

        pos_c = np.round(current[:3], 1).tolist()
        pos_t = np.round(target[:3], 1).tolist()
        d     = np.round(delta_pos, 1).tolist()
        self._node.get_logger().info(
            f"  EEF  현재={pos_c}  →  목표={pos_t}  (Δ={d} mm)"
        )
        self.move_line(target.tolist(), velocity=velocity, acceleration=acceleration)

    def _execute_joint_delta(self, action: np.ndarray) -> None:
        current = self.get_joint_state()
        if current is None:
            self._node.get_logger().error("Cannot get joint state.")
            return

        # VLA action은 이미 degree delta – _JOINT_SCALE 곱셈 없이 직접 사용
        delta_deg = np.clip(action, -_MAX_JOINT_DELTA_DEG, _MAX_JOINT_DELTA_DEG)
        current_deg = np.degrees(current)
        target_deg  = current_deg + delta_deg
        self.move_joint(target_deg.tolist(), velocity=20.0, acceleration=40.0)
