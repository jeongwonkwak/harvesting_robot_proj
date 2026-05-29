"""
GraspPipelineNode – main ROS2 node that drives the full grasp sequence.

Flow per episode
----------------
1. health-check SmolVLA server
2. open gripper
3. (optional) move to a user-defined pre-grasp home pose
4. VLA control loop  ←  repeats for max_steps
     a. capture RGB frame from D455
     b. read joint positions from Doosan e0509
     c. POST to SmolVLA server  →  6-DoF action
     d. execute action on robot
     e. if close_trigger_step reached → close gripper → done
5. report success / failure

Run
---
  ros2 run grasp_vla grasp_pipeline_node
or
  ros2 launch grasp_vla grasp.launch.py instruction:="pick up the silver connector"
"""

from __future__ import annotations

import time
from typing import Optional

import numpy as np
import rclpy
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node

from grasp_vla.camera_node import CameraNode
from grasp_vla.gripper_controller import GripperController
from grasp_vla.robot_controller import DoosanController
from grasp_vla.smolvla_client import SmolVLAClient


class GraspPipelineNode(Node):
    def __init__(self):
        super().__init__("grasp_pipeline")

        # ----------------------------------------------------------------
        # Declare ROS2 parameters (overridable from launch / yaml)
        # ----------------------------------------------------------------
        self._declare("smolvla_url",     "http://192.168.50.79:16003")
        self._declare("instruction",     "pick up the silver cylindrical connector")
        self._declare("action_mode",     "cartesian")   # "cartesian" | "joint"
        self._declare("max_steps",       50)
        self._declare("close_at_step",   35)            # close gripper after this many steps
        self._declare("step_hz",         5.0)           # control frequency
        self._declare("gripper_port",    "/dev/ttyUSB0")
        self._declare("robot_id",        "dsr01")
        self._declare("home_pose",       [])            # [] = skip home move
        self._declare("retreat_delta",   [-150.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # ----------------------------------------------------------------
        # Instantiate sub-components
        # ----------------------------------------------------------------
        url       = self.get_parameter("smolvla_url").value
        gport     = self.get_parameter("gripper_port").value
        robot_id  = self.get_parameter("robot_id").value
        act_mode  = self.get_parameter("action_mode").value

        self._vla     = SmolVLAClient(base_url=url)
        self._camera  = CameraNode()
        self._robot   = DoosanController(self, robot_id=robot_id, action_mode=act_mode)
        self._gripper = GripperController(port=gport)

        self.get_logger().info("GraspPipelineNode initialised. Call execute_grasp() to start.")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def execute_grasp(self, instruction: Optional[str] = None) -> bool:
        """
        Run a full grasp episode.
        Returns True if the episode completed without error.
        """
        instruction = instruction or self.get_parameter("instruction").value
        max_steps   = self.get_parameter("max_steps").value
        close_step  = self.get_parameter("close_at_step").value
        step_period = 1.0 / self.get_parameter("step_hz").value

        # 1. Health check
        if not self._vla.health():
            self.get_logger().error(f"SmolVLA server not reachable: {self._vla.base_url}")
            return False
        self.get_logger().info(f'SmolVLA OK. Instruction: "{instruction}"')

        # 2. Wait for first camera frame
        self.get_logger().info("Waiting for camera frames …")
        deadline = time.time() + 10.0
        while not self._camera.ready:
            self._camera.grab()
            if time.time() > deadline:
                self.get_logger().error("Camera timeout – check camera (device 6).")
                return False
        self.get_logger().info("Camera ready.")

        # 3. Open gripper
        self.get_logger().info("Opening gripper …")
        self._gripper.open()

        # 4. Optional: move to pre-grasp home pose
        home = self.get_parameter("home_pose").value
        if home:
            self.get_logger().info(f"Moving to home pose: {home}")
            self._robot.move_joint(list(home), velocity=30.0, acceleration=60.0)

        # 5. VLA control loop
        self.get_logger().info("Starting VLA control loop …")
        reset = True
        grasped = False

        for step in range(max_steps):
            t0 = time.time()

            # 5a. Get camera image
            self._camera.grab()
            rgb, _ = self._camera.get_images()
            if rgb is None:
                self.get_logger().warn(f"Step {step}: no camera frame, skipping.")
                continue

            # 5b. Get robot state (joint positions → radians)
            joint_state = self._robot.get_joint_state()
            if joint_state is None:
                self.get_logger().warn(f"Step {step}: no joint state, using zeros.")
                joint_state = np.zeros(6, dtype=np.float64)
            state6 = joint_state[:6].astype(np.float32)

            # 5c. Call SmolVLA
            try:
                result = self._vla.predict(
                    state=state6,
                    image_top=rgb,
                    instruction=instruction,
                    reset_episode=reset,
                )
                reset = False
                action = result.action  # shape (6,)
                self.get_logger().info(
                    f"Step {step:02d}  action={np.round(action, 4).tolist()}"
                    f"  latency={result.latency_ms:.1f}ms"
                )
            except Exception as e:
                self.get_logger().error(f"Step {step}: VLA call failed: {e}")
                break

            # 5d. Execute action
            self._robot.execute_action(action)

            # 5e. Close gripper at the designated step → then retreat
            if step >= close_step and not grasped:
                self.get_logger().info(f"Step {step}: closing gripper.")
                self._gripper.close()
                grasped = True
                self.get_logger().info("Grasp complete. Retreating …")
                self._retreat()
                break

            # Rate limiting
            elapsed = time.time() - t0
            sleep_t = step_period - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

        return grasped

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _retreat(self) -> None:
        delta = list(self.get_parameter("retreat_delta").value)
        if not any(delta):
            return
        current = self._robot.get_eef_pose()
        if current is None:
            self.get_logger().error("Cannot get EEF pose for retreat.")
            return
        target = (np.array(current) + np.array(delta)).tolist()
        self.get_logger().info(f"Retreat delta: {delta}")
        self._robot.move_line(target, velocity=30.0, acceleration=60.0)
        self.get_logger().info("Retreat complete.")

    def _declare(self, name: str, default) -> None:
        self.declare_parameter(
            name, default, ParameterDescriptor(description=name))


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = GraspPipelineNode()

    import threading

    def run():
        success = node.execute_grasp()
        node.get_logger().info(f"Episode finished. Success={success}")
        rclpy.shutdown()

    t = threading.Thread(target=run, daemon=True)
    t.start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._camera.release()
        node.destroy_node()


if __name__ == "__main__":
    main()
