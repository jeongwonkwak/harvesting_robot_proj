"""
RealSense D455 ROS2 subscriber.

Subscribes to:
  /camera/color/image_raw          sensor_msgs/Image  (RGB8)
  /camera/depth/image_rect_raw     sensor_msgs/Image  (16UC1, mm)
  /camera/color/camera_info        sensor_msgs/CameraInfo
"""

import threading
from typing import Optional, Tuple

import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class CameraNode(Node):
    def __init__(self):
        super().__init__("camera_node")
        self._bridge = CvBridge()
        self._lock = threading.Lock()

        self._rgb: Optional[np.ndarray] = None    # (H, W, 3) uint8 RGB
        self._depth: Optional[np.ndarray] = None  # (H, W)    uint16 mm
        self._K: Optional[np.ndarray] = None      # 3×3 intrinsics

        qos = rclpy.qos.QoSPresetProfiles.SENSOR_DATA.value

        self.create_subscription(Image,      "/camera/color/image_raw",
                                 self._rgb_cb,   qos)
        self.create_subscription(Image,      "/camera/depth/image_rect_raw",
                                 self._depth_cb, qos)
        self.create_subscription(CameraInfo, "/camera/color/camera_info",
                                 self._info_cb,  10)

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _rgb_cb(self, msg: Image) -> None:
        with self._lock:
            self._rgb = self._bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")

    def _depth_cb(self, msg: Image) -> None:
        with self._lock:
            self._depth = self._bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

    def _info_cb(self, msg: CameraInfo) -> None:
        # Only need to set this once
        if self._K is None:
            self._K = np.array(msg.k, dtype=np.float64).reshape(3, 3)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_rgb(self) -> Optional[np.ndarray]:
        with self._lock:
            return None if self._rgb is None else self._rgb.copy()

    def get_depth(self) -> Optional[np.ndarray]:
        with self._lock:
            return None if self._depth is None else self._depth.copy()

    def get_images(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        with self._lock:
            rgb = None if self._rgb is None else self._rgb.copy()
            dep = None if self._depth is None else self._depth.copy()
        return rgb, dep

    @property
    def ready(self) -> bool:
        return self._rgb is not None and self._depth is not None

    def pixel_to_3d(self, u: int, v: int) -> Optional[np.ndarray]:
        """
        Back-project pixel (u, v) to 3-D point in camera frame (metres).
        Returns None if depth is zero or camera not initialised.
        """
        if self._K is None or self._depth is None:
            return None

        with self._lock:
            depth_mm = float(self._depth[v, u])

        if depth_mm <= 0:
            return None

        z = depth_mm / 1000.0
        fx, fy = self._K[0, 0], self._K[1, 1]
        cx, cy = self._K[0, 2], self._K[1, 2]

        return np.array([(u - cx) * z / fx,
                         (v - cy) * z / fy,
                         z], dtype=np.float64)
