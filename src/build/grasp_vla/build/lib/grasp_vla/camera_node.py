import threading
from typing import Optional, Tuple

import numpy as np
import pyrealsense2 as rs


class CameraNode:
    def __init__(self, width: int = 640, height: int = 480, fps: int = 30):
        self._lock = threading.Lock()
        self._rgb:   Optional[np.ndarray] = None   # (H, W, 3) uint8 RGB
        self._depth: Optional[np.ndarray] = None   # (H, W)    uint16 mm

        self._pipeline = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, width, height, rs.format.rgb8,  fps)
        cfg.enable_stream(rs.stream.depth, width, height, rs.format.z16,   fps)
        self._pipeline.start(cfg)
        self._align = rs.align(rs.stream.color)

    def grab(self) -> bool:
        frames = self._pipeline.wait_for_frames(timeout_ms=1000)
        aligned = self._align.process(frames)

        color = aligned.get_color_frame()
        depth = aligned.get_depth_frame()
        if not color or not depth:
            return False

        with self._lock:
            self._rgb   = np.asanyarray(color.get_data())
            self._depth = np.asanyarray(depth.get_data())   # mm, uint16
        return True

    def get_rgb(self) -> Optional[np.ndarray]:
        with self._lock:
            return None if self._rgb is None else self._rgb.copy()

    def get_depth(self) -> Optional[np.ndarray]:
        with self._lock:
            return None if self._depth is None else self._depth.copy()

    def get_images(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        with self._lock:
            rgb   = None if self._rgb   is None else self._rgb.copy()
            depth = None if self._depth is None else self._depth.copy()
        return rgb, depth

    @property
    def ready(self) -> bool:
        return self._rgb is not None and self._depth is not None

    def release(self):
        self._pipeline.stop()
