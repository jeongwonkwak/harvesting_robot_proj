#!/usr/bin/env python3
"""
ros2_bridge.py — ROS2 → 대시보드 브리지

1. /dsr01/joint_states + /dsr01/system/get_current_pose
   → HARVEST_STATE_FILE 실시간 업데이트
2. /camera/camera/color/image_raw, /camera2/camera2/color/image_raw
   → ThreadingHTTPServer MJPEG 스트림 (포트 8766)
"""

import http.server
import json
import math
import os
import socketserver
import threading
import time
from datetime import datetime
from pathlib import Path

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from sensor_msgs.msg import Image, JointState
from std_msgs.msg import Float32, Float32MultiArray

try:
    from dsr_msgs2.srv import GetCurrentPose
    _DSR_AVAILABLE = True
except ImportError:
    _DSR_AVAILABLE = False
    print("[Bridge] dsr_msgs2 없음 — TCP pose 폴링 비활성화")

try:
    import cv2
    import numpy as np
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False
    print("[Bridge] opencv 없음 — 카메라 스트림 비활성화")

STATE_FILE   = Path(os.environ.get("HARVEST_STATE_FILE", "/data/harvest_state.json"))
MJPEG_PORT   = int(os.environ.get("MJPEG_PORT", "8766"))
CAM0_TOPIC   = os.environ.get("CAM0_TOPIC", "/camera/camera/color/image_raw")
CAM1_TOPIC   = os.environ.get("CAM1_TOPIC", "/camera2/camera2/color/image_raw")
CAM0_SERIAL  = os.environ.get("REALSENSE_SERIAL_0", "215122254786")
CAM1_SERIAL  = os.environ.get("REALSENSE_SERIAL_1", "342622303457")
YOLO_SEG_MODEL  = os.environ.get("YOLO_SEG_MODEL",  os.environ.get("YOLO_MODEL", ""))  # 비활성화
YOLO_POSE_MODEL = os.environ.get("YOLO_POSE_MODEL", "")
YOLO_CONF       = float(os.environ.get("YOLO_CONF", "0.3"))
UPDATE_HZ    = 10.0
TCP_POLL_HZ  = 5.0

# ROS2 토픽에 프레임이 없을 때 USB 폴백까지 기다리는 시간(초)
_ROS2_WAIT_S = 8.0

_JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]

_frame_lock      = [threading.Lock(), threading.Lock()]
_frame_jpeg      = [None, None]          # MJPEG 서버가 서빙하는 최종 JPEG
_frame_last_ros2 = [0.0, 0.0]

# ── YOLO 비동기 워커 (전용 스레드) ───────────────────────────────────────────
# _raw_frame[0]: YOLO 워커가 소비하는 최신 raw BGR 프레임
# _raw_display[0]: 합성 워커가 소비하는 최신 raw BGR 프레임 (YOLO와 별도)
# _yolo_overlay[0]: YOLO 워커가 생성한 오버레이 BGR (raw에 합성)
_raw_frame       = [None, None]
_raw_frame_lock  = [threading.Lock(), threading.Lock()]
_raw_display     = [None]               # slot 0 raw ndarray (합성용)
_raw_display_lock = threading.Lock()
_yolo_overlay    = [None]               # slot 0 YOLO overlay ndarray
_yolo_overlay_lock = threading.Lock()
_yolo_seg        = None   # 세그멘테이션 모델 (ripe/unripe/sick)
_yolo_pose       = None   # 포즈 모델 (줄기 3키포인트)
_yolo_model_lock = threading.Lock()
_yolo_det_count      = 0      # 가장 최근 프레임에서 감지된 ripe 딸기 수
_yolo_harvest_cand   = False  # 현재 프레임에 HARVEST 후보(ripe 마스크 안 줄기) 존재 여부

# seg 클래스 시각화 (BGR)
_SEG_COLORS = {0: (60, 60, 220), 1: (50, 200, 50), 2: (30, 200, 200)}
_SEG_NAMES  = {0: "ripe", 1: "unripe", 2: "sick"}
# 키포인트 시각화: stem_base=주황, stem_mid=빨강, stem_tip=초록 (BGR)
_KPT_COLORS = [(30, 120, 255), (30, 30, 220), (50, 200, 50)]


def _load_yolo():
    global _yolo_seg, _yolo_pose
    try:
        from ultralytics import YOLO as _YOLO
    except ImportError:
        print("[YOLO] ultralytics 미설치 — 모델 로드 불가")
        return

    dummy = np.zeros((480, 640, 3), dtype=np.uint8)

    if YOLO_SEG_MODEL and Path(YOLO_SEG_MODEL).exists():
        try:
            m = _YOLO(YOLO_SEG_MODEL)
            m.predict(dummy, verbose=False, conf=YOLO_CONF)
            with _yolo_model_lock:
                _yolo_seg = m
            print(f"[YOLO] 세그 모델 로드 완료: {YOLO_SEG_MODEL}")
        except Exception as e:
            print(f"[YOLO] 세그 모델 로드 실패: {e}")
    else:
        print(f"[YOLO] 세그 모델 없음 (YOLO_SEG_MODEL={YOLO_SEG_MODEL!r})")

    if YOLO_POSE_MODEL and Path(YOLO_POSE_MODEL).exists():
        try:
            m = _YOLO(YOLO_POSE_MODEL)
            m.predict(dummy, verbose=False, conf=YOLO_CONF)
            with _yolo_model_lock:
                _yolo_pose = m
            print(f"[YOLO] 포즈 모델 로드 완료: {YOLO_POSE_MODEL}")
        except Exception as e:
            print(f"[YOLO] 포즈 모델 로드 실패: {e}")
    else:
        print(f"[YOLO] 포즈 모델 없음 (YOLO_POSE_MODEL={YOLO_POSE_MODEL!r})")


YOLO_INFER_W, YOLO_INFER_H = 320, 240  # 추론 해상도 (화면 표시는 원본 640×480 유지)

def _yolo_worker():
    """슬롯 0 전용 YOLO 추론 스레드. 320×240으로 축소 추론 후 결과를 원본 스케일로 복원."""
    global _yolo_det_count, _yolo_harvest_cand

    while True:
        with _raw_frame_lock[0]:
            frame = _raw_frame[0]
            _raw_frame[0] = None

        if frame is None:
            time.sleep(0.01)
            continue

        with _yolo_model_lock:
            seg_model  = _yolo_seg
            pose_model = _yolo_pose

        H_orig, W_orig = frame.shape[:2]
        sx = W_orig / YOLO_INFER_W  # x 스케일 복원 비율
        sy = H_orig / YOLO_INFER_H

        # 추론용 축소 이미지
        small = cv2.resize(frame, (YOLO_INFER_W, YOLO_INFER_H))

        ripe_count  = 0
        has_harvest = False
        seg_entries = []

        # ── 세그멘테이션 추론 (320×240) ────────────────────────────────────
        if seg_model is not None:
            try:
                r0 = seg_model.predict(small, verbose=False, conf=YOLO_CONF)[0]
                overlay = frame.copy()
                for i, box in enumerate(r0.boxes):
                    cls_id = int(box.cls[0])
                    conf_v = float(box.conf[0])
                    # 좌표를 원본 해상도로 복원
                    x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                    x1, x2 = int(x1*sx), int(x2*sx)
                    y1, y2 = int(y1*sy), int(y2*sy)
                    color = _SEG_COLORS.get(cls_id, (200, 200, 200))

                    poly = None
                    if r0.masks is not None and i < len(r0.masks.xy):
                        poly_s = np.array(r0.masks.xy[i], dtype=np.float32)
                        if len(poly_s) >= 3:
                            poly = (poly_s * [sx, sy]).astype(np.int32)
                            cv2.fillPoly(overlay, [poly], color)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{_SEG_NAMES.get(cls_id, str(cls_id))} {conf_v:.2f}",
                                (x1, max(y1 - 8, 12)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

                    seg_entries.append({'cls_id': cls_id, 'poly': poly,
                                        'box': (x1, y1, x2, y2)})
                    if cls_id == 0:
                        ripe_count += 1

                cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
            except Exception as e:
                print(f"[YOLO] 세그 추론 오류: {e}")

        # ── 포즈 추론 (320×240) ─────────────────────────────────────────────
        if pose_model is not None:
            try:
                r0 = pose_model.predict(small, verbose=False, conf=YOLO_CONF)[0]
                for i, box in enumerate(r0.boxes):
                    bconf = float(box.conf[0])
                    bx1, by1, bx2, by2 = [int(v) for v in box.xyxy[0].tolist()]
                    bx1, bx2 = int(bx1*sx), int(bx2*sx)
                    by1, by2 = int(by1*sy), int(by2*sy)
                    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2

                    is_harvest = False
                    for seg in seg_entries:
                        if seg['cls_id'] != 0:
                            continue
                        if seg['poly'] is not None and len(seg['poly']) >= 3:
                            if cv2.pointPolygonTest(seg['poly'],
                                                    (float(cx), float(cy)), False) >= 0:
                                is_harvest = True
                                break
                        else:
                            sx1, sy1, sx2, sy2 = seg['box']
                            if sx1 <= cx <= sx2 and sy1 <= cy <= sy2:
                                is_harvest = True
                                break

                    if r0.keypoints is not None and i < len(r0.keypoints.data):
                        pts = r0.keypoints.data[i].cpu().numpy()
                        prev = None
                        for ki, (kx, ky, kv) in enumerate(pts):
                            if kv < 0.3:
                                prev = None
                                continue
                            kc = _KPT_COLORS[ki]
                            kxi, kyi = int(kx * sx), int(ky * sy)
                            if prev is not None:
                                cv2.line(frame, prev, (kxi, kyi), (180, 180, 180), 2)
                            cv2.circle(frame, (kxi, kyi), 5, kc, -1)
                            cv2.circle(frame, (kxi, kyi), 5, (255, 255, 255), 1)
                            prev = (kxi, kyi)

                    if is_harvest:
                        has_harvest = True
                        cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 255), 3)
                        cv2.putText(frame, f"HARVEST {bconf:.2f}",
                                    (bx1, max(by1 - 22, 22)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            except Exception as e:
                print(f"[YOLO] 포즈 추론 오류: {e}")

        _yolo_det_count    = ripe_count
        _yolo_harvest_cand = has_harvest

        # annotated frame을 overlay로 저장 (합성 워커가 raw 위에 덮어씀)
        try:
            with _yolo_overlay_lock:
                _yolo_overlay[0] = frame  # YOLO가 그린 annotated BGR ndarray
        except Exception:
            pass


def _display_composer_worker():
    """슬롯 0: raw 프레임에 YOLO overlay를 합성해 30fps로 _frame_jpeg[0] 갱신."""
    enc = [cv2.IMWRITE_JPEG_QUALITY, 50]
    while True:
        with _raw_display_lock:
            raw = _raw_display[0]
        if raw is not None:
            with _yolo_overlay_lock:
                overlay = _yolo_overlay[0]
            # overlay가 있으면 합성, 없으면 raw 그대로
            display = overlay if overlay is not None else raw
            try:
                _, buf = cv2.imencode(".jpg", display, enc)
                with _frame_lock[0]:
                    _frame_jpeg[0] = buf.tobytes()
            except Exception:
                pass
        time.sleep(1 / 30)


def _make_placeholder(text: str) -> bytes:
    """카메라 미연결 시 보여줄 회색 placeholder JPEG"""
    if not _CV2_AVAILABLE:
        return b""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)
    cv2.putText(img, text, (60, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (160, 160, 160), 2, cv2.LINE_AA)
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 40])
    return buf.tobytes()


_PLACEHOLDER = [None, None]


def _get_placeholder(slot: int) -> bytes:
    if _PLACEHOLDER[slot] is None:
        labels = ["YOLO CAM — 대기 중", "전경 CAM — 대기 중"]
        _PLACEHOLDER[slot] = _make_placeholder(labels[slot])
    return _PLACEHOLDER[slot] or b""


# ── MJPEG HTTP 핸들러 ─────────────────────────────────────────────────────────

class MJPEGHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # 로그 억제

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/cam0", "/camera/0"):
            self._stream(0)
        elif path in ("/cam1", "/camera/1"):
            self._stream(1)
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bridge OK")

    def _stream(self, slot: int):
        self.send_response(200)
        self.send_header("Content-Type",
                         "multipart/x-mixed-replace; boundary=frame")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            while True:
                with _frame_lock[slot]:
                    jpg = _frame_jpeg[slot]
                if not jpg:
                    jpg = _get_placeholder(slot)
                if jpg:
                    chunk = (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + jpg + b"\r\n"
                    )
                    self.wfile.write(chunk)
                    self.wfile.flush()
                time.sleep(1 / 30)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass


def _run_mjpeg_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("0.0.0.0", MJPEG_PORT), MJPEGHandler) as srv:
        print(f"[Bridge] MJPEG 서버 시작 → :{MJPEG_PORT}/cam0  /cam1")
        srv.serve_forever()


# ── ROS2 브리지 노드 ──────────────────────────────────────────────────────────

class ROS2Bridge(Node):
    def __init__(self):
        super().__init__("harvest_ros2_bridge")
        self._lock           = threading.Lock()
        self._joint_deg      = [0.0] * 6
        self._tcp_pose       = [0.0] * 6
        self._tcp_ready      = False
        self._tcp_pending    = False
        self._grip_ratio     = None   # teleop-api가 publish하는 그리퍼 위치 ratio(0~1)
        self._last_ripe_count = 0     # _write_state 에서 신규 감지 판별용

        self.create_subscription(JointState, "/dsr01/joint_states",
                                 self._joint_cb, 10)

        # teleop-api(teleop_api_server.py)가 publish하는 EEF pose 토픽 구독.
        # dsr_msgs2 서비스가 없는 환경에서도 TCP 좌표를 받을 수 있다.
        self.create_subscription(Float32MultiArray, "/dsr01/tcp_pose",
                                 self._tcp_topic_cb, 10)
        # 그리퍼 위치 토픽 (ratio 0=열림 ~ 1=닫힘)
        self.create_subscription(Float32, "/gripper/position",
                                 self._gripper_cb, 10)

        # dsr_msgs2가 있으면 서비스 폴링도 병행 (정확한 TCP). 없으면 토픽만 사용.
        if _DSR_AVAILABLE:
            self._pose_cli = self.create_client(
                GetCurrentPose, "/dsr01/system/get_current_pose"
            )
            self.create_timer(1.0 / TCP_POLL_HZ, self._poll_tcp)

        if _CV2_AVAILABLE:
            cam_qos = QoSProfile(
                reliability=ReliabilityPolicy.RELIABLE,
                durability=DurabilityPolicy.TRANSIENT_LOCAL,
                history=HistoryPolicy.KEEP_LAST,
                depth=1,
            )
            self.create_subscription(Image, CAM0_TOPIC,
                                     lambda m: self._img_cb(m, 0), cam_qos)
            self.create_subscription(Image, CAM1_TOPIC,
                                     lambda m: self._img_cb(m, 1), cam_qos)
            self.get_logger().info(
                f"카메라 구독: {CAM0_TOPIC}, {CAM1_TOPIC}"
            )

        self.create_timer(1.0 / UPDATE_HZ, self._write_state)
        self.get_logger().info(
            f"ROS2 Bridge 시작 — 상태:{STATE_FILE}  MJPEG:{MJPEG_PORT}"
        )

    def _joint_cb(self, msg: JointState):
        name_pos = {n: p for n, p in zip(msg.name, msg.position)}
        arm = [name_pos.get(j, 0.0) for j in _JOINT_NAMES]
        with self._lock:
            self._joint_deg = [round(math.degrees(v), 2) for v in arm]

    def _poll_tcp(self):
        if self._tcp_pending or not self._pose_cli.service_is_ready():
            return
        self._tcp_pending = True
        self._pose_cli.call_async(
            GetCurrentPose.Request()
        ).add_done_callback(self._tcp_cb)

    def _tcp_cb(self, fut):
        self._tcp_pending = False
        try:
            r = fut.result()
            if r and r.success:
                with self._lock:
                    self._tcp_pose  = [round(v, 2) for v in r.pos]
                    self._tcp_ready = True
        except Exception:
            pass

    def _tcp_topic_cb(self, msg: Float32MultiArray):
        """teleop-api가 publish하는 /dsr01/tcp_pose 토픽 [x,y,z,rx,ry,rz] mm/deg."""
        if len(msg.data) >= 6:
            with self._lock:
                self._tcp_pose  = [round(v, 2) for v in msg.data[:6]]
                self._tcp_ready = True

    def _gripper_cb(self, msg: Float32):
        """그리퍼 위치 ratio(0=열림 ~ 1=닫힘)."""
        with self._lock:
            self._grip_ratio = float(msg.data)

    def _img_cb(self, msg: Image, slot: int):
        # ROS2 executor 스레드 — YOLO 절대 금지. raw 저장만 하고 즉시 리턴.
        try:
            channels = {"rgb8": 3, "bgr8": 3, "mono8": 1}.get(msg.encoding, 3)
            arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(
                msg.height, msg.width, channels
            ).copy()
            if msg.encoding == "rgb8":
                arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            _frame_last_ros2[slot] = time.time()
            if slot == 0:
                # 합성 워커용 raw 저장 (항상 최신 프레임 유지)
                with _raw_display_lock:
                    _raw_display[0] = arr.copy()
                # YOLO 워커에도 전달
                with _raw_frame_lock[0]:
                    _raw_frame[0] = arr
            else:
                _, buf = cv2.imencode(".jpg", arr, [cv2.IMWRITE_JPEG_QUALITY, 50])
                with _frame_lock[slot]:
                    _frame_jpeg[slot] = buf.tobytes()
        except Exception as e:
            self.get_logger().warn(f"이미지 변환 오류 ({slot}): {e}")

    def _write_state(self):
        try:
            s: dict = {}
            if STATE_FILE.exists():
                try:
                    s = json.loads(STATE_FILE.read_text())
                except Exception:
                    s = {}
            with self._lock:
                s["joint_angles"] = list(self._joint_deg)
                if self._tcp_ready:
                    s["tcp_pose"] = list(self._tcp_pose)
                if self._grip_ratio is not None:
                    # ratio 0(열림)~1(닫힘) → 대시보드 position 100(열림)~0(닫힘)
                    ratio = max(0.0, min(1.0, self._grip_ratio))
                    pos_pct = round((1.0 - ratio) * 100, 1)
                    raw_pos = round(ratio * 740)   # 0(열림)~740(닫힘) 실제 위치
                    state = "open" if pos_pct >= 95 else ("closed" if pos_pct <= 5 else "grasping")
                    s["gripper"] = {"position": pos_pct,
                                    "raw_pos": raw_pos,
                                    "state": state,
                                    "force": s.get("gripper", {}).get("force", 30.0)}
            # YOLO 감지 수: 이전 write 시점보다 ripe 수가 늘었을 때만 detected_count 누적
            cur_ripe = _yolo_det_count
            if cur_ripe > self._last_ripe_count:
                s["detected_count"] = s.get("detected_count", 0) + (cur_ripe - self._last_ripe_count)
            self._last_ripe_count = cur_ripe
            s["ripe_visible"]      = cur_ripe > 0
            s["harvest_candidate"] = _yolo_harvest_cand

            s["last_updated"] = datetime.now().isoformat()
            tmp = STATE_FILE.with_suffix(".tmp")
            tmp.write_text(json.dumps(s, ensure_ascii=False, indent=2))
            os.replace(tmp, STATE_FILE)
        except Exception as e:
            self.get_logger().warn(f"상태 파일 쓰기 실패: {e}")


# ── pyrealsense2 USB 폴백 워커 ───────────────────────────────────────────────

def _usb_camera_worker(serial: str, slot: int) -> None:
    """ROS2 토픽에 프레임이 없을 때 pyrealsense2로 직접 USB 접근"""
    if not _CV2_AVAILABLE:
        return
    try:
        import pyrealsense2 as rs
    except ImportError:
        print(f"[USB{slot}] pyrealsense2 없음 — USB 폴백 불가")
        return

    enc = [cv2.IMWRITE_JPEG_QUALITY, 50]
    print(f"[USB{slot}] ROS2 토픽 대기 중 ({_ROS2_WAIT_S:.0f}초)...")
    time.sleep(_ROS2_WAIT_S)

    while True:
        # ROS2 토픽이 활성화되면 물러남
        if time.time() - _frame_last_ros2[slot] < 2.0:
            time.sleep(1.0)
            continue

        print(f"[USB{slot}] ROS2 토픽 없음 — RealSense USB 직접 열기 (serial={serial})")
        pipeline = None
        try:
            ctx = rs.context()
            if len(ctx.query_devices()) == 0:
                raise RuntimeError("RealSense 장치 없음")
            cfg = rs.config()
            if serial:
                cfg.enable_device(serial)
            # D455(slot0) 는 depth 동시 활성화 없으면 color 프레임이 나오지 않음
            if slot == 0:
                cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            cfg.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
            pipeline = rs.pipeline()
            pipeline.start(cfg)
            print(f"[USB{slot}] RealSense 연결 성공 — 워밍업 중...")
            # 카메라 안정화 대기 (D455 등은 첫 프레임까지 시간이 더 필요)
            for _ in range(60):
                try: pipeline.wait_for_frames(timeout_ms=500)
                except Exception: pass
            print(f"[USB{slot}] 워밍업 완료")

            while True:
                # ROS2 토픽이 다시 살아나면 USB 닫기
                if time.time() - _frame_last_ros2[slot] < 2.0:
                    print(f"[USB{slot}] ROS2 토픽 복구 — USB 닫기")
                    break
                fr = pipeline.wait_for_frames(timeout_ms=5000)
                cf = fr.get_color_frame()
                if cf:
                    arr = cv2.cvtColor(np.asanyarray(cf.get_data()).copy(), cv2.COLOR_RGB2BGR)
                    if slot == 0:
                        # YOLO 워커 스레드에 위임 (블로킹 금지)
                        with _raw_frame_lock[0]:
                            _raw_frame[0] = arr
                    else:
                        _, buf = cv2.imencode(".jpg", arr, enc)
                        with _frame_lock[slot]:
                            _frame_jpeg[slot] = buf.tobytes()
        except Exception as e:
            print(f"[USB{slot}] 오류: {e}")
        finally:
            if pipeline:
                try: pipeline.stop()
                except Exception: pass
        time.sleep(3)


# ── 진입점 ────────────────────────────────────────────────────────────────────

def main():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    threading.Thread(target=_run_mjpeg_server, daemon=True).start()
    threading.Thread(target=_load_yolo, daemon=True).start()
    threading.Thread(target=_yolo_worker, daemon=True).start()
    threading.Thread(target=_display_composer_worker, daemon=True).start()
    time.sleep(0.5)

    # ROS2 토픽 없을 때 USB 폴백 (USB_FALLBACK=false 로 비활성화 가능)
    usb_fallback = os.environ.get('USB_FALLBACK', 'true').lower() != 'false'
    if usb_fallback:
        if CAM0_SERIAL:
            threading.Thread(target=_usb_camera_worker,
                             args=(CAM0_SERIAL, 0), daemon=True).start()
        if CAM1_SERIAL:
            threading.Thread(target=_usb_camera_worker,
                             args=(CAM1_SERIAL, 1), daemon=True).start()
    else:
        print("[Bridge] USB 폴백 비활성화 — ROS2 토픽만 사용")

    rclpy.init()
    node     = ROS2Bridge()
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
