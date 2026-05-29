import threading
from typing import Optional, Tuple

import cv2
import numpy as np

try:
    import pyrealsense2 as rs
    _RS_AVAILABLE = True
except ImportError:
    _RS_AVAILABLE = False


class CameraNode:
    def __init__(self, width: int = 640, height: int = 480, fps: int = 30,
                 ros_image_topic: Optional[str] = None, ros_node=None,
                 ros_depth_topic: Optional[str] = None,
                 use_realsense: bool = True,
                 camera_index: int = 4):
        self._lock = threading.Lock()
        self._rgb:   Optional[np.ndarray] = None
        self._depth: Optional[np.ndarray] = None
        self._mode = "dummy"

        # 0순위: ROS2 토픽 (Gazebo bridge 등)
        if ros_image_topic and ros_node:
            try:
                from sensor_msgs.msg import Image as RosImage
                from rclpy.qos import qos_profile_sensor_data
                # realsense2_camera는 BEST_EFFORT로 퍼블리시 → 구독도 맞춰야 메시지 수신 가능
                ros_node.create_subscription(RosImage, ros_image_topic, self._ros_image_cb, qos_profile_sensor_data)
                if ros_depth_topic:
                    ros_node.create_subscription(RosImage, ros_depth_topic, self._ros_depth_cb, qos_profile_sensor_data)
                    print(f"[CameraNode] ROS2 depth 토픽 구독: {ros_depth_topic}")
                self._mode = "ros"
                print(f"[CameraNode] ROS2 토픽 구독: {ros_image_topic}")
                return
            except Exception as e:
                print(f"[CameraNode] ROS2 토픽 설정 실패 ({e}), 폴백")

        # 1순위: RealSense
        if _RS_AVAILABLE and use_realsense:
            try:
                pipeline = rs.pipeline()
                cfg = rs.config()
                cfg.enable_stream(rs.stream.color, width, height, rs.format.rgb8, fps)
                cfg.enable_stream(rs.stream.depth, width, height, rs.format.z16,  fps)
                pipeline.start(cfg)
                self._pipeline = pipeline
                self._align    = rs.align(rs.stream.color)
                self._mode     = "realsense"
                print("[CameraNode] RealSense 연결 성공")
            except Exception as e:
                print(f"[CameraNode] RealSense 없음 ({e}), VideoCapture 시도...")

        # 2순위: VideoCapture — RealSense color stream은 /dev/video4
        if self._mode == "dummy":
            cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
            if cap.isOpened():
                # YUYV 포맷 + 해상도/FPS 명시 (RealSense V4L2 select() timeout 방지)
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
                cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                cap.set(cv2.CAP_PROP_FPS, fps)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self._cap  = cap
                self._mode = "opencv"
                print(f"[CameraNode] VideoCapture({camera_index}) 연결 성공")
            else:
                cap.release()
                print("[CameraNode] 카메라 없음 → 더미 프레임 사용 (시뮬레이션 모드)")

    def _ros_image_cb(self, msg) -> None:
        enc = msg.encoding.lower()
        ch = 3 if enc in ('rgb8', 'bgr8') else None
        if ch is None:
            return
        arr = np.frombuffer(bytes(msg.data), dtype=np.uint8).reshape(msg.height, msg.width, ch)
        if 'bgr' in enc:
            arr = arr[:, :, ::-1].copy()
        with self._lock:
            self._rgb = arr

    def _ros_depth_cb(self, msg) -> None:
        enc = msg.encoding.lower()
        if enc == '16uc1':
            arr = np.frombuffer(bytes(msg.data), dtype=np.uint16).reshape(msg.height, msg.width)
        elif enc == '32fc1':
            arr = (np.frombuffer(bytes(msg.data), dtype=np.float32).reshape(msg.height, msg.width) * 1000).astype(np.uint16)
        else:
            return
        with self._lock:
            self._depth = arr

    def grab(self) -> bool:
        if self._mode == "ros":
            return self._rgb is not None  # 콜백에서 자동 업데이트됨

        if self._mode == "realsense":
            try:
                frames  = self._pipeline.wait_for_frames(timeout_ms=1000)
                aligned = self._align.process(frames)
                color   = aligned.get_color_frame()
                depth   = aligned.get_depth_frame()
                if not color or not depth:
                    return False
                with self._lock:
                    self._rgb   = np.asanyarray(color.get_data())
                    self._depth = np.asanyarray(depth.get_data())
                return True
            except Exception:
                return False

        if self._mode == "opencv":
            ret, frame = self._cap.read()
            if not ret:
                return False
            with self._lock:
                self._rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return True

        # dummy: 검정 프레임 반환
        with self._lock:
            self._rgb   = np.zeros((480, 640, 3), dtype=np.uint8)
            self._depth = np.zeros((480, 640),    dtype=np.uint16)
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
        return self._rgb is not None

    def release(self):
        if self._mode == "realsense":
            self._pipeline.stop()
        elif self._mode == "opencv":
            self._cap.release()
