#!/usr/bin/env python3
"""
Object Tracking Node (YOLO + RealSense Depth, Eye-in-Hand)

YOLO 모델로 딸기를 감지하고 depth로 3D 위치를 계산하여
cuRobo planner에 목표를 전송합니다.

Eye-in-hand 구성: T_cam_to_base = T_ee_to_base(TF) × T_cam_to_ee
T_cam_to_ee는 캘리브레이션 파일(스캔 포즈 기준)과 TF에서 한 번만 계산합니다.

Keys:
    s: 선택된 물체 위치로 로봇 이동
    p: 선택된 물체 pick
    1-9: 감지된 물체 중 선택 (lock)
    r: 선택 해제 (unlock)
    w/x: grasp angle +/-5°
    q: 종료
"""

import os
import numpy as np
import cv2
import pyrealsense2 as rs
import warnings
warnings.filterwarnings("ignore")

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from rcl_interfaces.msg import ParameterDescriptor
import json

import tf2_ros
from scipy.spatial.transform import Rotation

from ultralytics import YOLO

EE_FRAME   = 'gripper_rh_p12_rn_base'
BASE_FRAME = 'base_link'


def _transform_to_matrix(tf_stamped) -> np.ndarray:
    """TransformStamped → 4×4 numpy 변환 행렬."""
    t = tf_stamped.transform.translation
    r = tf_stamped.transform.rotation
    T = np.eye(4)
    T[:3, :3] = Rotation.from_quat([r.x, r.y, r.z, r.w]).as_matrix()
    T[:3, 3]  = [t.x, t.y, t.z]
    return T


class ObjectTrackingNode(Node):
    def __init__(self):
        super().__init__("object_tracking_node")

        self.declare_parameter("model_path",
            os.path.expanduser("~/Downloads/share_yolo/strawberry_yolo26m_ft_v3/weights/best.pt"),
            ParameterDescriptor(description="Path to YOLO .pt model"))
        self.declare_parameter("calibration_path",
            os.path.expanduser("~/sim2real/sim2real/config/calibration_eye_in_hand.npz"),
            ParameterDescriptor(description="Path to eye-in-hand calibration .npz file"))
        self.declare_parameter("box_threshold", 0.3,
            ParameterDescriptor(description="Detection confidence threshold"))
        self.declare_parameter("detection_interval", 5,
            ParameterDescriptor(description="Run detection every N frames"))
        self.declare_parameter("target_class", "ripe_strawberry",
            ParameterDescriptor(description="Only pick this class (empty = all)"))

        model_path   = self.get_parameter("model_path").value
        calib_path   = self.get_parameter("calibration_path").value
        self.box_threshold      = self.get_parameter("box_threshold").value
        self.detection_interval = self.get_parameter("detection_interval").value
        self.target_class       = self.get_parameter("target_class").value

        # ── 캘리브레이션 (eye-in-hand) ───────────────────────────────────────────
        # T_cam_to_gripper: 카메라→그리퍼 고정 변환 (4×4), 로봇 자세와 무관
        # eye_in_hand 캘리브 파일에서 직접 로드 — TF 역산 불필요
        self.get_logger().info(f"Loading eye-in-hand calibration: {calib_path}")
        calib = np.load(calib_path)
        self.T_cam_to_ee = calib['T_cam_to_gripper']
        self.get_logger().info(
            f"T_cam_to_gripper translation: {self.T_cam_to_ee[:3, 3].round(4)} m")

        # TF2 (per-frame T_ee_to_base 획득용)
        self.tf_buffer   = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # ── YOLO ────────────────────────────────────────────────────────────────
        self.get_logger().info(f"Loading YOLO model: {model_path}")
        self.yolo = YOLO(model_path)
        self.get_logger().info(f"YOLO loaded! Classes: {self.yolo.names}")

        # ── RealSense ───────────────────────────────────────────────────────────
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline.start(config)
        self.align = rs.align(rs.stream.color)
        self.get_logger().info("RealSense started")

        # ── Publishers ──────────────────────────────────────────────────────────
        self.target_pub    = self.create_publisher(PoseStamped, "/dsr01/curobo/target_pose", 10)
        self.pick_pub      = self.create_publisher(PoseStamped, "/dsr01/curobo/pick_pose", 10)
        self.obstacles_pub = self.create_publisher(String, "/dsr01/curobo/obstacles", 10)

        # ── State ───────────────────────────────────────────────────────────────
        self.detections    = []
        self.selected_idx  = 0
        self.frame_count   = 0
        self.locked        = False
        self.locked_target = None   # (phrase, pos_base, grasp_angle_rad)
        self._last_depth_frame = None

        self.timer = self.create_timer(1.0 / 30.0, self.camera_loop)

        self.get_logger().info("=" * 50)
        self.get_logger().info("  Object Tracking Node Ready  (YOLO, eye-in-hand)")
        self.get_logger().info(f"  Target class: {self.target_class or 'all'}")
        self.get_logger().info("  Keys: 's'=move, 'p'=pick, 1-9=lock, 'r'=unlock, w/x=angle, 'q'=quit")
        self.get_logger().info("=" * 50)

    # ── Eye-in-hand TF 보정 ────────────────────────────────────────────────────

    def _current_T_cam_to_base(self) -> np.ndarray | None:
        """현재 EE pose 기반 T_cam_to_base 반환. TF 실패 시 None."""
        try:
            tf = self.tf_buffer.lookup_transform(
                BASE_FRAME, EE_FRAME, rclpy.time.Time())
            T_ee_to_base = _transform_to_matrix(tf)
            return T_ee_to_base @ self.T_cam_to_ee
        except Exception:
            return None

    def _cam_to_base(self, pt3d: np.ndarray) -> np.ndarray | None:
        """카메라 좌표 → base_link 좌표. TF 실패 시 None."""
        T = self._current_T_cam_to_base()
        if T is None:
            return None
        return (T @ np.append(pt3d, 1.0))[:3]

    # ── Camera loop ────────────────────────────────────────────────────────────

    def camera_loop(self):
        frames = self.pipeline.wait_for_frames()
        aligned = self.align.process(frames)
        cf = aligned.get_color_frame()
        df = aligned.get_depth_frame()
        if not cf:
            return

        image = np.asanyarray(cf.get_data())
        display = image.copy()
        self.frame_count += 1
        self._last_depth_frame = df

        if not self.locked and self.frame_count % self.detection_interval == 0:
            self.run_detection(image, df)

        # Draw detections
        h, w = image.shape[:2]
        for i, det in enumerate(self.detections):
            phrase, pos_base, conf, bbox, grasp_angle = det
            x1 = int((bbox[0] - bbox[2] / 2) * w)
            y1 = int((bbox[1] - bbox[3] / 2) * h)
            x2 = int((bbox[0] + bbox[2] / 2) * w)
            y2 = int((bbox[1] + bbox[3] / 2) * h)

            color = (0, 255, 0) if i == self.selected_idx else (150, 150, 150)
            thick = 3 if i == self.selected_idx else 1
            cv2.rectangle(display, (x1, y1), (x2, y2), color, thick)
            label = f"[{i+1}] {phrase} ({conf:.2f}) {np.degrees(grasp_angle):.0f}deg"
            cv2.putText(display, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            if pos_base is not None:
                coord = f"({pos_base[0]*100:.1f},{pos_base[1]*100:.1f},{pos_base[2]*100:.1f})cm"
                cv2.putText(display, coord, (x1, y2 + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, color, 1)

        # Status bar
        tf_ok = "TF OK" if self._current_T_cam_to_base() is not None else "TF MISS"
        if self.locked and self.locked_target:
            phrase, pos, _ = self.locked_target
            cv2.putText(display, f"LOCKED: {phrase} (press 'r' to unlock)",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            if pos is not None:
                cv2.putText(display,
                    f"Target: X={pos[0]*1000:.1f} Y={pos[1]*1000:.1f} Z={pos[2]*1000:.1f}",
                    (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        elif self.detections:
            sel = self.detections[self.selected_idx]
            cv2.putText(display, f"Selected: [{self.selected_idx+1}] {sel[0]}  [{tf_ok}]",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(display, f"Model: {os.path.basename(self.get_parameter('model_path').value)}",
                    (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        cv2.putText(display, "'s'=move 'p'=pick 1-9=lock 'r'=unlock w/x=angle 'q'=quit",
                    (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 0), 1)

        cv2.imshow("Object Tracking", display)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('s'):
            self.send_move()
        elif k == ord('p'):
            self.send_pick()
        elif ord('1') <= k <= ord('9'):
            idx = k - ord('1')
            if idx < len(self.detections):
                self.selected_idx = idx
                det = self.detections[idx]
                self.locked = True
                self.locked_target = (det[0], det[1], det[4])
                self.get_logger().info(
                    f"LOCKED: [{idx+1}] {det[0]} (grasp angle: {np.degrees(det[4]):.1f}°)")
                self.publish_obstacles()
        elif k == ord('r'):
            self.locked = False
            self.locked_target = None
            self.get_logger().info("UNLOCKED: detection resumed")
        elif k == 82 or k == ord('w'):
            if self.locked and self.locked_target:
                phrase, pos, angle = self.locked_target
                angle += np.radians(5)
                self.locked_target = (phrase, pos, angle)
                self.get_logger().info(f"Angle adjusted: {np.degrees(angle):.1f}°")
        elif k == 84 or k == ord('x'):
            if self.locked and self.locked_target:
                phrase, pos, angle = self.locked_target
                angle -= np.radians(5)
                self.locked_target = (phrase, pos, angle)
                self.get_logger().info(f"Angle adjusted: {np.degrees(angle):.1f}°")
        elif k == ord('q'):
            raise SystemExit

    # ── Detection ──────────────────────────────────────────────────────────────

    def run_detection(self, image, depth_frame):
        """Run YOLO detection and compute 3D positions."""
        h, w = image.shape[:2]
        results = self.yolo(image, conf=self.box_threshold, verbose=False)
        self.detections = []

        for r in results:
            for i in range(len(r.boxes)):
                cls    = int(r.boxes.cls[i])
                conf   = float(r.boxes.conf[i])
                phrase = self.yolo.names[cls]

                if self.target_class and phrase != self.target_class:
                    continue

                x1n, y1n, x2n, y2n = r.boxes.xyxyn[i].tolist()
                cx = (x1n + x2n) / 2
                cy = (y1n + y2n) / 2
                bw = x2n - x1n
                bh = y2n - y1n
                bbox = np.array([cx, cy, bw, bh])

                px    = int(cx * w)
                py_px = int(cy * h)
                pos_base = None
                depth_m  = depth_frame.get_distance(px, py_px) if depth_frame else 0

                if depth_m <= 0.1 or depth_m > 5.0:
                    for du in range(-5, 6):
                        for dv in range(-5, 6):
                            pu, pv = px + du, py_px + dv
                            if 0 <= pu < w and 0 <= pv < h:
                                dd = depth_frame.get_distance(pu, pv)
                                if 0.1 < dd < 5.0:
                                    depth_m = dd
                                    break
                        if 0.1 < depth_m < 5.0:
                            break

                if depth_m > 0.1:
                    intr = depth_frame.profile.as_video_stream_profile().intrinsics
                    pt3d = rs.rs2_deproject_pixel_to_point(intr, [px, py_px], depth_m)
                    pos_base = self._cam_to_base(np.array(pt3d))

                grasp_angle = self.compute_grasp_angle(image, bbox, h, w)
                self.detections.append((phrase, pos_base, conf, bbox, grasp_angle))

        # x좌표 기준 정렬 → 프레임마다 감지 순서 일관되게 유지
        self.detections.sort(key=lambda d: d[3][0])

        if self.selected_idx >= len(self.detections):
            self.selected_idx = 0

    # ── Grasp angle ────────────────────────────────────────────────────────────

    def compute_grasp_angle(self, image, box, h, w):
        """PCA on depth point cloud within bbox to compute grasp angle."""
        if self._last_depth_frame is None:
            return 0.0
        df = self._last_depth_frame
        intr = df.profile.as_video_stream_profile().intrinsics

        x1 = max(0, int((box[0] - box[2] / 2) * w))
        y1 = max(0, int((box[1] - box[3] / 2) * h))
        x2 = min(w, int((box[0] + box[2] / 2) * w))
        y2 = min(h, int((box[1] + box[3] / 2) * h))

        if x2 - x1 < 10 or y2 - y1 < 10:
            return 0.0

        center_depth = df.get_distance(int(box[0] * w), int(box[1] * h))
        if center_depth < 0.1:
            return 0.0

        points_robot = []
        for py in range(y1, y2, 2):
            for px in range(x1, x2, 2):
                d = df.get_distance(px, py)
                if d > 0.1 and abs(d - center_depth) < 0.03:
                    pt3d = rs.rs2_deproject_pixel_to_point(intr, [px, py], d)
                    points_robot.append(self._cam_to_base(np.array(pt3d)))

        if len(points_robot) < 20:
            return 0.0

        points = np.array(points_robot)
        xy = points[:, :2]
        center = xy.mean(axis=0)
        centered = xy - center
        cov = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        major = eigenvectors[:, -1]
        robot_angle = np.arctan2(major[1], major[0])
        return robot_angle + np.pi / 2

    # ── Pose helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def make_down_quaternion(grasp_angle_rad):
        """Quaternion: gripper pointing down, rotated by angle around Z."""
        ca = np.cos(grasp_angle_rad / 2)
        sa = np.sin(grasp_angle_rad / 2)
        qz_w, qz_x, qz_y, qz_z = ca, 0.0, 0.0, sa
        qb_w, qb_x, qb_y, qb_z = 0.0, 0.7071, 0.7071, 0.0
        w = qz_w*qb_w - qz_x*qb_x - qz_y*qb_y - qz_z*qb_z
        x = qz_w*qb_x + qz_x*qb_w + qz_y*qb_z - qz_z*qb_y
        y = qz_w*qb_y - qz_x*qb_z + qz_y*qb_w + qz_z*qb_x
        z = qz_w*qb_z + qz_x*qb_y - qz_y*qb_x + qz_z*qb_w
        return [float(x), float(y), float(z), float(w)]

    def _make_pose_msg(self, pos, grasp_angle_rad=0.0):
        quat = self.make_down_quaternion(grasp_angle_rad)
        msg = PoseStamped()
        msg.header.frame_id = BASE_FRAME
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = float(pos[0])
        msg.pose.position.y = float(pos[1])
        msg.pose.position.z = float(pos[2])
        msg.pose.orientation.x = quat[0]
        msg.pose.orientation.y = quat[1]
        msg.pose.orientation.z = quat[2]
        msg.pose.orientation.w = quat[3]
        return msg

    def _get_target(self):
        if self.locked and self.locked_target:
            phrase, pos, angle = self.locked_target
            return phrase, pos, angle
        if self.detections and self.selected_idx < len(self.detections):
            det = self.detections[self.selected_idx]
            return det[0], det[1], det[4]
        return None, None, 0.0

    # ── Commands ───────────────────────────────────────────────────────────────

    def send_move(self):
        phrase, pos, angle = self._get_target()
        if pos is None:
            self.get_logger().warn("No valid object selected")
            return

        sx, sy, sz = float(pos[0]), float(pos[1]), float(pos[2])

        # down_quat = [w=0, x=0.7071, y=0.7071, z=0] → R = [[0,1,0],[1,0,0],[0,0,-1]]
        # 이 orientation이 IK 성공률 가장 높으므로 카메라 오프셋도 이 기준으로 역산
        R_down = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]], dtype=float)
        cam_off = R_down @ self.T_cam_to_ee[:3, 3]  # world 기준 카메라 오프셋

        # EE 위치: down_quat으로 움직였을 때 카메라가 딸기 35cm 위에 위치
        approach_height = 0.35
        ee_pos = np.array([
            sx - cam_off[0],
            sy - cam_off[1],
            float(np.clip(sz + approach_height - cam_off[2], 0.20, 0.75))
        ])

        # orientation hint: 현재 카메라 방향 (= scan pose에선 scan_quat)
        T_cam = self._current_T_cam_to_base()
        msg = PoseStamped()
        msg.header.frame_id = BASE_FRAME
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = float(ee_pos[0])
        msg.pose.position.y = float(ee_pos[1])
        msg.pose.position.z = float(ee_pos[2])
        if T_cam is not None:
            T_ee = T_cam @ np.linalg.inv(self.T_cam_to_ee)
            q_xyzw = Rotation.from_matrix(T_ee[:3, :3]).as_quat()
            msg.pose.orientation.x = float(q_xyzw[0])
            msg.pose.orientation.y = float(q_xyzw[1])
            msg.pose.orientation.z = float(q_xyzw[2])
            msg.pose.orientation.w = float(q_xyzw[3])
        self.target_pub.publish(msg)
        cam_expected = ee_pos + cam_off
        self.get_logger().info(
            f"MOVE to {phrase}: EE=({ee_pos[0]*100:.1f},{ee_pos[1]*100:.1f},{ee_pos[2]*100:.1f})cm "
            f"→ cam@({cam_expected[0]*100:.1f},{cam_expected[1]*100:.1f},{cam_expected[2]*100:.1f})cm "
            f"(딸기 {approach_height*100:.0f}cm 위)")

    def send_pick(self):
        phrase, pos, angle = self._get_target()
        if pos is None:
            self.get_logger().warn("No valid object selected")
            return
        msg = self._make_pose_msg(pos, angle)
        self.pick_pub.publish(msg)
        self.get_logger().info(
            f"PICK {phrase}: X={pos[0]*1000:.1f} Y={pos[1]*1000:.1f} Z={pos[2]*1000:.1f} "
            f"angle={np.degrees(angle):.1f}deg")

    def publish_obstacles(self):
        obstacles = []
        for i, (phrase, pos_base, conf, bbox, _angle) in enumerate(self.detections):
            if pos_base is None or (self.locked and i == self.selected_idx):
                continue
            h_img, w_img = 480, 640
            obj_size = max(float(bbox[2]) * w_img * 0.001, float(bbox[3]) * h_img * 0.001, 0.03)
            obstacles.append({
                "name": f"{phrase}_{i}",
                "pos": [float(pos_base[0]), float(pos_base[1]), float(pos_base[2])],
                "dims": [obj_size, obj_size, obj_size]
            })
        msg = String()
        msg.data = json.dumps(obstacles)
        self.obstacles_pub.publish(msg)

    def destroy_node(self):
        self.pipeline.stop()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ObjectTrackingNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
