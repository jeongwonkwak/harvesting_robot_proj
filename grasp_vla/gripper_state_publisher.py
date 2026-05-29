"""
Gripper state publisher node.

Reads the current position of the RH-P12-RN-DF gripper via Dynamixel SDK
and publishes it as a ROS2 topic so it can be captured by ros2 bag record.

Published topic:
  /gripper/position  (std_msgs/Float32)  0.0 = fully open, 1.0 = fully closed

Run:
  ros2 run grasp_vla gripper_state_publisher_node
  ros2 run grasp_vla gripper_state_publisher_node --ros-args -p port:=/dev/ttyUSB1 -p rate_hz:=30.0
"""

from __future__ import annotations

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

from grasp_vla.gripper_controller import GripperController


class GripperStatePublisher(Node):
    def __init__(self):
        super().__init__("gripper_state_publisher")

        self.declare_parameter("port",     "/dev/ttyUSB0")
        self.declare_parameter("rate_hz",  10.0)

        port    = self.get_parameter("port").get_parameter_value().string_value
        rate_hz = self.get_parameter("rate_hz").get_parameter_value().double_value

        self._gripper = GripperController(port=port)
        self._pub     = self.create_publisher(Float32, "/gripper/position", 10)
        self._timer   = self.create_timer(1.0 / rate_hz, self._publish)

        self.get_logger().info(
            f"Gripper state publisher started  port={port}  rate={rate_hz:.0f}Hz  "
            f"→ /gripper/position"
        )

    def _publish(self) -> None:
        pos = self._gripper.get_position()  # float [0.0, 1.0]
        msg = Float32()
        msg.data = float(pos)
        self._pub.publish(msg)


def main():
    rclpy.init()
    node = GripperStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
