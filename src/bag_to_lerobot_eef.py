#!/usr/bin/env python3
"""
Convert ROS2 bag files (SQLite3) → LeRobot v3.0 dataset (EEF delta action).

bag_to_lerobot.py 와 동일한 구조이나 아래가 다름:
  - state[t]  = [x_m, y_m, z_m, rx_rad, ry_rad, rz_rad]        ← 6-dim, m/rad (LIBERO 호환)
  - action[t] = [Δx_m, Δy_m, Δz_m, Δrx_rad, Δry_rad, Δrz_rad, grip_next]
                  eef[t+1] - eef[t]    (마지막 프레임은 delta=0)
  ※ Doosan 원시 데이터(mm/deg)는 파싱 후 m/rad로 변환하여 저장

Topics consumed:
  /dsr01/tcp_pose                 std_msgs/msg/Float32MultiArray  (6 floats: EEF pose)
  /gripper/position               std_msgs/msg/Float32
  /camera/camera/color/image_raw  sensor_msgs/msg/Image

실행:
  python3 src/bag_to_lerobot_eef.py
  python3 src/bag_to_lerobot_eef.py --task "Pick up the red object."
"""

import argparse
import json
import re
import sqlite3
import struct
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import yaml

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RAW_DIR      = Path('/home/user/robot_workspace/vla_ws/data/raw/final_project')
OUTPUT_DIR   = Path('/home/user/robot_workspace/vla_ws/data/mid')
DATASET_NAME = 'vla_dataset_v1.0.0'

FPS          = 5
TASK         = 'Grasp the strawberry stem and pick it.'
ROBOT_TYPE   = 'dsr01'
CAMERA_NAME  = 'camera1'
CAMERA2_NAME = 'camera2'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _json_compact_arrays(obj, indent=2) -> str:
    raw = json.dumps(obj, indent=indent)
    return re.sub(
        r'\[([^\[\]]*)\]',
        lambda m: '[' + re.sub(r'\s+', ' ', m.group(1).strip()) + ']',
        raw,
        flags=re.DOTALL,
    )


# ── CDR Deserializer ──────────────────────────────────────────────────────────

class CDRReader:
    def __init__(self, raw: bytes):
        self.buf = raw[4:]
        self.pos = 0

    def _align(self, n: int):
        r = self.pos % n
        if r:
            self.pos += n - r

    def read_uint32(self) -> int:
        self._align(4)
        v = struct.unpack_from('<I', self.buf, self.pos)[0]
        self.pos += 4
        return v

    def read_int32(self) -> int:
        self._align(4)
        v = struct.unpack_from('<i', self.buf, self.pos)[0]
        self.pos += 4
        return v

    def read_uint8(self) -> int:
        v = self.buf[self.pos]
        self.pos += 1
        return v

    def read_float32(self) -> float:
        self._align(4)
        v = struct.unpack_from('<f', self.buf, self.pos)[0]
        self.pos += 4
        return v

    def read_float64(self) -> float:
        self._align(8)
        v = struct.unpack_from('<d', self.buf, self.pos)[0]
        self.pos += 8
        return v

    def read_float32_array(self) -> list:
        count = self.read_uint32()
        if count == 0:
            return []
        self._align(4)
        vals = list(struct.unpack_from(f'<{count}f', self.buf, self.pos))
        self.pos += count * 4
        return vals

    def read_float64_array(self) -> list:
        count = self.read_uint32()
        if count == 0:
            return []
        self._align(8)
        vals = list(struct.unpack_from(f'<{count}d', self.buf, self.pos))
        self.pos += count * 8
        return vals

    def read_string(self) -> str:
        length = self.read_uint32()
        s = self.buf[self.pos:self.pos + length - 1].decode('utf-8', errors='replace')
        self.pos += length
        return s

    def read_bytes(self, n: int) -> bytes:
        v = self.buf[self.pos:self.pos + n]
        self.pos += n
        return v


# ── Message Parsers ───────────────────────────────────────────────────────────

def parse_float32_msg(raw: bytes) -> float:
    return CDRReader(raw).read_float32()


def parse_tcp_pose(raw: bytes) -> list:
    """
    Parse std_msgs/Float32MultiArray → [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg].

    CDR layout of Float32MultiArray:
      MultiArrayLayout layout:
        MultiArrayDimension[] dim  (usually empty → uint32 count=0)
        uint32 data_offset         (= 0)
      float32[] data               (uint32 count + N floats)
    """
    r = CDRReader(raw)
    dim_count = r.read_uint32()          # dim 배열 길이 (퍼블리시 시 0)
    for _ in range(dim_count):
        r.read_string()                  # label
        r.read_uint32()                  # size
        r.read_uint32()                  # stride
    r.read_uint32()                      # data_offset
    vals = r.read_float32_array()        # [x, y, z, rx, ry, rz]
    return list(vals[:6]) if len(vals) >= 6 else vals


def parse_joint_states(raw: bytes) -> list:
    """
    Parse sensor_msgs/JointState → [j1_rad, j2_rad, ..., j6_rad] (position field only).

    CDR layout of JointState:
      Header header                (timestamp, frame_id) ← 먼저 건너뜀
      string[] name                (joint names)
      float64[] position           (joint positions in radians)
      float64[] velocity           (joint velocities)
      float64[] effort             (joint efforts)
    """
    r = CDRReader(raw)

    # Header 건너뛰기
    r.read_uint32()      # sec
    r.read_uint32()      # nsec
    r.read_string()      # frame_id

    # name (string array)
    name_count = r.read_uint32()
    for _ in range(name_count):
        r.read_string()

    # position (float64 array)
    pos_count = r.read_uint32()
    positions = [r.read_float64() for _ in range(pos_count)]

    return positions[:6] if len(positions) >= 6 else positions


def parse_image(raw: bytes) -> np.ndarray:
    r = CDRReader(raw)
    r.read_int32()    # stamp.sec
    r.read_uint32()   # stamp.nanosec
    r.read_string()   # frame_id
    height = r.read_uint32()
    width  = r.read_uint32()
    encoding = r.read_string()
    r.read_uint8()    # is_bigendian
    r.read_uint32()   # step
    data_len = r.read_uint32()
    img_bytes = r.read_bytes(data_len)

    if encoding == 'mono8':
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width)
        img = np.stack([img, img, img], axis=-1)
    elif encoding == 'bgr8':
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width, 3)
        img = img[:, :, ::-1].copy()
    else:
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width, 3)
    return img


# ── Bag Reader ────────────────────────────────────────────────────────────────

def read_bag(db_path: Path) -> dict:
    conn = sqlite3.connect(str(db_path))
    cur  = conn.cursor()
    cur.execute('SELECT id, name FROM topics')
    topics = {row[0]: row[1] for row in cur.fetchall()}
    data = {name: [] for name in topics.values()}
    cur.execute('SELECT topic_id, timestamp, data FROM messages ORDER BY timestamp')
    for topic_id, ts, raw in cur.fetchall():
        data[topics[topic_id]].append((ts, bytes(raw)))
    conn.close()
    return data


# ── Synchronization ───────────────────────────────────────────────────────────

def _nearest(sorted_ts: np.ndarray, query: np.ndarray) -> np.ndarray:
    idx  = np.searchsorted(sorted_ts, query)
    idx  = np.clip(idx, 0, len(sorted_ts) - 1)
    left = np.clip(idx - 1, 0, len(sorted_ts) - 1)
    closer_left = np.abs(sorted_ts[left] - query) <= np.abs(sorted_ts[idx] - query)
    idx[closer_left] = left[closer_left]
    return idx


def _eef_delta_m_rad(eef_now: list, eef_next: list) -> list:
    """
    EEF delta를 m/rad 단위로 반환.
    eef_now/eef_next: Doosan 원시값 [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg].
    """
    delta_mm  = [eef_next[i] - eef_now[i] for i in range(3)]
    delta_deg = [eef_next[i] - eef_now[i] for i in range(3, 6)]
    # 회전 wrap-around 보정: ±180° 범위
    for i in range(3):
        while delta_deg[i] >  180.0: delta_deg[i] -= 360.0
        while delta_deg[i] < -180.0: delta_deg[i] += 360.0
    delta_m   = [v / 1000.0          for v in delta_mm]
    delta_rad = [np.radians(v)        for v in delta_deg]
    return delta_m + delta_rad


def synchronize(bag_data: dict, fps: int = 10) -> dict | None:
    CAM  = '/camera/camera/color/image_raw'
    CAM2 = '/camera2/camera2/color/image_raw'
    TCP  = '/dsr01/tcp_pose'
    GRP  = '/gripper/position'
    JNT  = '/dsr01/joint_states'

    for key in (CAM, TCP):
        if key not in bag_data or len(bag_data[key]) == 0:
            print(f'    Missing topic: {key}')
            return None

    has_cam2 = CAM2 in bag_data and len(bag_data[CAM2]) > 0
    if not has_cam2:
        print(f'    [INFO] {CAM2} 없음 — 단일 카메라 모드로 변환.')

    cam_ts = np.array([t for t, _ in bag_data[CAM]], dtype=np.int64)
    tcp_ts = np.array([t for t, _ in bag_data[TCP]], dtype=np.int64)
    jnt_ts = np.array([t for t, _ in bag_data.get(JNT, [])], dtype=np.int64) if JNT in bag_data else None

    t_start = cam_ts[0]
    t_end   = cam_ts[-1]
    if t_start >= t_end:
        return None

    tcp_duration = (tcp_ts[-1] - tcp_ts[0]) / 1e9
    cam_duration = (t_end - t_start) / 1e9
    coverage = cam_duration / tcp_duration if tcp_duration > 0 else 1.0
    if coverage < 0.9:
        print(f'    [WARNING] 카메라가 세션의 {coverage*100:.0f}%만 커버됨.')

    step_ns = int(1e9 / fps)
    grid    = np.arange(t_start, t_end, step_ns, dtype=np.int64)
    if len(grid) == 0:
        return None

    cam_idx = _nearest(cam_ts, grid)
    tcp_idx = _nearest(tcp_ts, grid)
    jnt_idx = _nearest(jnt_ts, grid) if jnt_ts is not None and len(jnt_ts) > 0 else None

    # EEF pose 파싱
    eef_poses = [parse_tcp_pose(bag_data[TCP][i][1]) for i in tcp_idx]

    # Joint States 파싱
    if jnt_idx is not None:
        joint_angles = [parse_joint_states(bag_data[JNT][i][1]) for i in jnt_idx]
    else:
        print(f'    [WARNING] {JNT} 없음 — joint states=0.0 채움.')
        joint_angles = [[0.0] * 6 for _ in range(len(grid))]

    # 그리퍼
    grp_msgs = bag_data.get(GRP, [])
    if grp_msgs:
        grp_ts  = np.array([t for t, _ in grp_msgs], dtype=np.int64)
        grp_idx = _nearest(grp_ts, grid)
        grips   = [parse_float32_msg(grp_msgs[i][1]) for i in grp_idx]

        # 그리퍼 값 범위 확인
        print(f'    [DEBUG] Gripper raw values (첫 10개): {grips[:10]}')
        print(f'    [DEBUG] Gripper 범위: min={min(grips):.4f}, max={max(grips):.4f}, mean={np.mean(grips):.4f}')
    else:
        print(f'    [WARNING] {GRP} 없음 — gripper=0.0 채움.')
        grips = [0.0] * len(grid)

    # 카메라 1 이미지 파싱
    print(f'    Decoding cam1 ({len(grid)} frames) ...', end='', flush=True)
    images, prev = [], -1
    for i in cam_idx:
        if i == prev:
            images.append(images[-1])
        else:
            images.append(parse_image(bag_data[CAM][i][1]))
            prev = i
    print(' done')

    # 카메라 2 이미지 파싱 (있을 경우)
    images2 = None
    if has_cam2:
        cam2_ts  = np.array([t for t, _ in bag_data[CAM2]], dtype=np.int64)
        cam2_idx = _nearest(cam2_ts, grid)
        print(f'    Decoding cam2 ({len(grid)} frames) ...', end='', flush=True)
        imgs2, prev2 = [], -1
        for i in cam2_idx:
            if i == prev2:
                imgs2.append(imgs2[-1])
            else:
                imgs2.append(parse_image(bag_data[CAM2][i][1]))
                prev2 = i
        images2 = imgs2
        print(' done')

    # state: [x_m, y_m, z_m, rx_rad, ry_rad, rz_rad, gripper] — 7-dim (EEF only)
    states = []
    for i, eef in enumerate(eef_poses):
        tcp_state = [
            eef[0] / 1000.0, eef[1] / 1000.0, eef[2] / 1000.0,
            np.radians(eef[3]), np.radians(eef[4]), np.radians(eef[5]),
        ]
        gripper_state = [grips[i]]  # Gripper current position
        states.append(tcp_state + gripper_state)

    # action: [Δx_m, Δy_m, Δz_m, Δrx_rad, Δry_rad, Δrz_rad, grip_next] — 7-dim
    # grip_next는 0~740 범위 (로봇 그리퍼 제어값)
    actions = []
    n = len(states)
    for t in range(n):
        if t < n - 1:
            delta = _eef_delta_m_rad(eef_poses[t], eef_poses[t + 1])
            grip_next = grips[t + 1] * 740.0  # ratio (0~1) → raw (0~740)
        else:
            delta     = [0.0] * 6
            grip_next = grips[t] * 740.0  # ratio (0~1) → raw (0~740)
        actions.append(delta + [grip_next])

    return {
        'timestamps': (grid - grid[0]) / 1e9,
        'states':     states,
        'actions':    actions,
        'images':     images,
        'images2':    images2,   # None이면 단일 카메라 에피소드
    }


# ── Video Encoder ─────────────────────────────────────────────────────────────

class FFmpegVideoWriter:
    def __init__(self, output_path: Path, fps: int, width: int, height: int):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            'ffmpeg', '-y',
            '-f', 'rawvideo', '-vcodec', 'rawvideo',
            '-s', f'{width}x{height}', '-pix_fmt', 'rgb24',
            '-r', str(fps), '-i', 'pipe:0',
            '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            str(output_path),
        ]
        self._proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def write(self, frame: np.ndarray):
        self._proc.stdin.write(frame.tobytes())

    def release(self):
        self._proc.stdin.close()
        self._proc.wait()


# ── Dataset Builder ───────────────────────────────────────────────────────────

CATALOG_FILENAME = 'episodes_catalog.yaml'


def load_catalog(raw_dir: Path) -> dict:
    """raw_dir/episodes_catalog.yaml 를 읽어 episodes 딕셔너리를 반환."""
    catalog_path = raw_dir / CATALOG_FILENAME
    if not catalog_path.exists():
        return {}
    with open(catalog_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return (data or {}).get('episodes', {})


def build_dataset(
    raw_dir:         Path,
    output_dir:      Path,
    task:            str,
    fps:             int  = 10,
    robot_type:      str  = 'dsr01',
    camera_name:     str  = 'camera1',
    camera2_name:    str  = 'camera2',
    category:        str  = '',
    skip_review:     bool = False,
    category_filter: str  = '',
    episode_start:   int  = None,
    episode_end:     int  = None,
    episode_list:    str  = None,
    use_symlink:     bool = False,
):
    catalog = load_catalog(raw_dir)
    if catalog:
        print(f'카탈로그 로드: {raw_dir / CATALOG_FILENAME}  ({len(catalog)}개 항목)')
    else:
        print(f'카탈로그 없음 — --task / --category 인수 사용')

    # EEF bag은 _eef 접미사로 저장됨
    episode_dirs = sorted(raw_dir.glob('episode_*_eef'))
    if not episode_dirs:
        # 접미사 없는 경우도 허용 (수동 실행 시)
        episode_dirs = sorted(raw_dir.glob('episode_*'))
    if not episode_dirs:
        raise FileNotFoundError(f'No episode dirs in {raw_dir}')

    # ── 에피소드 필터링 ───────────────────────────────────────────────────────
    total_episodes = len(episode_dirs)
    if episode_list:
        indices = [int(x.strip()) for x in episode_list.split(',')]
        episode_dirs = [episode_dirs[i] for i in indices if i < len(episode_dirs)]
        print(f'에피소드 목록 필터: {episode_list}  →  {len(episode_dirs)}개 선택')
    elif episode_start is not None or episode_end is not None:
        start = episode_start or 0
        end = episode_end if episode_end is not None else total_episodes - 1
        episode_dirs = episode_dirs[start:end+1]
        print(f'에피소드 범위 필터: [{start}:{end}]  →  {len(episode_dirs)}개 선택')
    else:
        print(f'전체 에피소드 변환: {len(episode_dirs)}개')

    if not episode_dirs:
        raise ValueError(f'필터 조건으로 선택된 에피소드가 없습니다')

    print(f'Found {len(episode_dirs)} bag directories\n')

    CHUNKS_SIZE = 1000
    all_rows, all_states, all_actions = [], [], []
    ep_count, global_idx = 0, 0
    frame_shape, video_paths, video2_paths = None, [], []
    has_dual_cam = False  # 하나라도 cam2 있으면 True → 메타데이터에 포함
    task_registry: dict[str, int] = {}  # task_str → task_index
    ep_tasks_per_ep: list[str] = []     # episode 순서대로 task 문자열 보관
    ep_has_cam2: list[bool] = []        # episode별 cam2 유무

    def get_task_index(t: str) -> int:
        if t not in task_registry:
            task_registry[t] = len(task_registry)
        return task_registry[t]

    for ep_dir in episode_dirs:
        ep_info      = catalog.get(ep_dir.name, {})
        quality      = ep_info.get('quality', 'good')
        ep_task      = (ep_info.get('task') or '').strip() or task
        ep_category  = (ep_info.get('category') or '').strip()
        notes        = (ep_info.get('notes') or '').strip()

        # 카탈로그 필터링
        if quality == 'skip':
            print(f'  [skip] {ep_dir.name}: quality=skip')
            continue
        if quality == 'review' and skip_review:
            print(f'  [skip] {ep_dir.name}: quality=review (--skip-review)')
            continue
        if category_filter and ep_category and ep_category != category_filter:
            print(f'  [skip] {ep_dir.name}: category={ep_category!r} ≠ filter={category_filter!r}')
            continue
        if quality == 'review':
            note_str = f' — {notes}' if notes else ''
            print(f'  [REVIEW] {ep_dir.name}{note_str}')

        db_files = list(ep_dir.glob('*.db3'))
        if not db_files:
            print(f'  [skip] {ep_dir.name}: no .db3 file')
            continue

        print(f'  Bag: {ep_dir.name}  category={ep_category or "(미지정)"}  task_idx={get_task_index(ep_task)}')
        bag_data = read_bag(db_files[0])

        print(f'  Episode {ep_count}: {ep_dir.name}')
        result = synchronize(bag_data, fps=fps)
        if result is None:
            print('    [skip] insufficient data')
            continue

        ep_task_idx = get_task_index(ep_task)
        n = len(result['timestamps'])
        for f_idx in range(n):
            all_rows.append({
                'index':             global_idx + f_idx,
                'episode_index':     ep_count,
                'frame_index':       f_idx,
                'timestamp':         float(result['timestamps'][f_idx]),
                'task_index':        ep_task_idx,
                'observation.state': result['states'][f_idx],
                'action':            result['actions'][f_idx],
            })

        images  = result['images']
        images2 = result.get('images2')
        ep_cam2 = images2 is not None
        if ep_cam2:
            has_dual_cam = True

        if frame_shape is None:
            frame_shape = images[0].shape[:2]
        h, w = frame_shape

        chunk_idx = ep_count // CHUNKS_SIZE
        file_idx  = ep_count % CHUNKS_SIZE

        # ── 카메라 1 인코딩 ───────────────────────────────────────────────────
        video_path = (
            output_dir / 'videos'
            / f'observation.images.{camera_name}'
            / f'chunk-{chunk_idx:03d}' / f'file-{file_idx:03d}.mp4'
        )
        video_paths.append(video_path)
        ep_tasks_per_ep.append(ep_task)
        ep_has_cam2.append(ep_cam2)

        print(f'    Encoding cam1 ({len(images)} frames) ...', end='', flush=True)
        writer = FFmpegVideoWriter(video_path, fps, w, h)
        for frame in images:
            writer.write(frame)
        writer.release()
        print(f' done → {video_path.name}')
        del images

        # ── 카메라 2 인코딩 (있을 경우) ──────────────────────────────────────
        if ep_cam2:
            video2_path = (
                output_dir / 'videos'
                / f'observation.images.{camera2_name}'
                / f'chunk-{chunk_idx:03d}' / f'file-{file_idx:03d}.mp4'
            )
            video2_paths.append(video2_path)
            print(f'    Encoding cam2 ({len(images2)} frames) ...', end='', flush=True)
            writer2 = FFmpegVideoWriter(video2_path, fps, w, h)
            for frame2 in images2:
                writer2.write(frame2)
            writer2.release()
            print(f' done → {video2_path.name}')
        else:
            video2_paths.append(None)
        del images2

        all_states.extend(result['states'])
        all_actions.extend(result['actions'])
        global_idx += n
        ep_count   += 1
        print(f'    {n} frames  ({n/fps:.1f}s)')

    if not all_rows:
        raise RuntimeError('No valid episodes.')

    total_frames = global_idx
    print(f'\nTotal: {ep_count} episodes, {total_frames} frames')

    # ── Parquet ───────────────────────────────────────────────────────────────
    parquet_path = output_dir / 'data' / 'chunk-000' / 'file-000.parquet'
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.table({
        'index':             pa.array([r['index']             for r in all_rows], type=pa.int64()),
        'episode_index':     pa.array([r['episode_index']     for r in all_rows], type=pa.int64()),
        'frame_index':       pa.array([r['frame_index']       for r in all_rows], type=pa.int64()),
        'timestamp':         pa.array([r['timestamp']         for r in all_rows], type=pa.float64()),
        'task_index':        pa.array([r['task_index']        for r in all_rows], type=pa.int64()),
        'observation.state': pa.array([r['observation.state'] for r in all_rows], type=pa.list_(pa.float64())),
        'action':            pa.array([r['action']            for r in all_rows], type=pa.list_(pa.float64())),
    })
    pq.write_table(table, parquet_path)
    print(f'Saved parquet → {parquet_path}')

    # ── Meta ──────────────────────────────────────────────────────────────────
    meta_dir = output_dir / 'meta'
    meta_dir.mkdir(parents=True, exist_ok=True)

    # task_registry가 비어있으면 기본 task 사용 (카탈로그 없을 때)
    if not task_registry:
        task_registry[task] = 0
    tasks_df = pd.DataFrame(
        {'task_index': list(task_registry.values())},
        index=pd.Index(list(task_registry.keys()), name='task'),
    )
    tasks_df.to_parquet(meta_dir / 'tasks.parquet')

    states_np  = np.array(all_states)
    actions_np = np.array(all_actions)
    stats = {
        'observation.state': {
            'mean': states_np.mean(axis=0).tolist(),
            'std':  states_np.std(axis=0).tolist(),
            'min':  states_np.min(axis=0).tolist(),
            'max':  states_np.max(axis=0).tolist(),
        },
        'action': {
            'mean': actions_np.mean(axis=0).tolist(),
            'std':  actions_np.std(axis=0).tolist(),
            'min':  actions_np.min(axis=0).tolist(),
            'max':  actions_np.max(axis=0).tolist(),
        },
    }
    (meta_dir / 'stats.json').write_text(json.dumps(stats, indent=2))

    h, w = frame_shape if frame_shape else (480, 640)
    features = {
        f'observation.images.{camera_name}': {
            'dtype': 'video',
            'shape': [3, h, w],
            'names': ['channels', 'height', 'width'],
        },
        'observation.state': {
            'dtype': 'float32',
            'shape': [7],
            'names': ['x_m', 'y_m', 'z_m', 'rx_rad', 'ry_rad', 'rz_rad', 'gripper'],
        },
        'action': {
            'dtype': 'float32',
            'shape': [7],
            'names': ['dx_m', 'dy_m', 'dz_m', 'drx_rad', 'dry_rad', 'drz_rad', 'grip_next'],
        },
        'timestamp':     {'dtype': 'float32', 'shape': [1], 'names': None},
        'frame_index':   {'dtype': 'int64',   'shape': [1], 'names': None},
        'episode_index': {'dtype': 'int64',   'shape': [1], 'names': None},
        'index':         {'dtype': 'int64',   'shape': [1], 'names': None},
        'task_index':    {'dtype': 'int64',   'shape': [1], 'names': None},
    }
    if has_dual_cam:
        features[f'observation.images.{camera2_name}'] = {
            'dtype': 'video',
            'shape': [3, h, w],
            'names': ['channels', 'height', 'width'],
        }

    info = {
        'codebase_version': 'v3.0',
        'category':         category,
        'fps':              fps,
        'robot_type':       robot_type,
        'total_episodes':   ep_count,
        'total_frames':     total_frames,
        'total_tasks':      len(task_registry),
        'chunks_size':      1000,
        'data_files_size_in_mb':  round(parquet_path.stat().st_size / 1024 / 1024, 3),
        'video_files_size_in_mb': round(sum(
            p.stat().st_size for p in video_paths + [p for p in video2_paths if p]
        ) / 1024 / 1024, 3),
        'splits':    {'train': f'0:{ep_count}'},
        'data_path': 'data/chunk-{chunk_index:03d}/file-{file_index:03d}.parquet',
        'video_path':'videos/{video_key}/chunk-{chunk_index:03d}/file-{file_index:03d}.mp4',
        'features':  features,
    }
    (meta_dir / 'info.json').write_text(json.dumps(info, indent=2))

    # episodes parquet (LeRobot v3.0 필수)
    ep_rows = []
    for r in all_rows:
        if r['frame_index'] == 0:
            ep_rows.append({'episode_index': r['episode_index'], 'start': r['index']})
    for i, er in enumerate(ep_rows):
        nxt  = ep_rows[i + 1]['start'] if i + 1 < len(ep_rows) else total_frames
        length = nxt - er['start']
        row_update = {
            'tasks':                                              [ep_tasks_per_ep[i]],
            'length':                                             length,
            'dataset_from_index':                                 er['start'],
            'dataset_to_index':                                   nxt,
            'data/chunk_index':                                   0,
            'data/file_index':                                    0,
            f'videos/observation.images.{camera_name}/chunk_index': 0,
            f'videos/observation.images.{camera_name}/file_index':  i,
            f'videos/observation.images.{camera_name}/from_timestamp': 0.0,
            f'videos/observation.images.{camera_name}/to_timestamp':   length / fps,
            'meta/episodes/chunk_index':                          0,
            'meta/episodes/file_index':                           0,
        }
        # 카메라 2 메타 (있을 경우)
        if has_dual_cam and ep_has_cam2[i]:
            row_update.update({
                f'videos/observation.images.{camera2_name}/chunk_index': 0,
                f'videos/observation.images.{camera2_name}/file_index':  i,
                f'videos/observation.images.{camera2_name}/from_timestamp': 0.0,
                f'videos/observation.images.{camera2_name}/to_timestamp':   length / fps,
            })
        ep_rows[i].update(row_update)

    ep_path = meta_dir / 'episodes' / 'chunk-000' / 'file-000.parquet'
    ep_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(
        pa.Table.from_pandas(pd.DataFrame(ep_rows), preserve_index=False),
        ep_path, compression='snappy',
    )

    dual_ep_count = sum(1 for x in ep_has_cam2 if x)
    print(f'\nDataset ready → {output_dir}')
    print(f'  Episodes : {ep_count}  (듀얼 카메라: {dual_ep_count}개)')
    print(f'  Frames   : {total_frames}')
    print(f'  Task     : {task}')
    print(f'  Action   : EEF delta [Δx_m,Δy_m,Δz_m,Δrx_rad,Δry_rad,Δrz_rad, grip_next] (7-dim)')
    print(f'  State    : [x_m,y_m,z_m,rx_rad,ry_rad,rz_rad, gripper] (7-dim, EEF only)')
    print(f'  Cameras  : {camera_name}' + (f' + {camera2_name}' if has_dual_cam else ' (단일)'))


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='ROS2 bag → LeRobot v3.0 dataset (EEF delta action)'
    )
    parser.add_argument('--raw-dir',      type=Path, default=RAW_DIR)
    parser.add_argument('--output-dir',   type=Path, default=None)
    parser.add_argument('--dataset-name', type=str,  default=DATASET_NAME)
    parser.add_argument('--task',         type=str,  default=TASK)
    parser.add_argument('--fps',          type=int,  default=FPS)
    parser.add_argument('--robot-type',   type=str,  default=ROBOT_TYPE)
    parser.add_argument('--camera-name',  type=str,  default=CAMERA_NAME)
    parser.add_argument('--camera2-name', type=str,  default=CAMERA2_NAME,
                        help='전경 카메라 이름 (LeRobot feature key)')
    parser.add_argument('--category',        type=str,  default='',
                        help='데이터셋 전체 카테고리 레이블 (info.json에 기록)')
    parser.add_argument('--category-filter', type=str,  default='',
                        help='이 카테고리의 에피소드만 변환 (카탈로그 기반)')
    parser.add_argument('--skip-review',     action='store_true',
                        help='카탈로그에서 quality=review 에피소드 제외')
    parser.add_argument('--episode-start',   type=int, default=None,
                        help='변환할 에피소드 시작 번호 (0-indexed)')
    parser.add_argument('--episode-end',     type=int, default=None,
                        help='변환할 에피소드 종료 번호 (포함, 0-indexed)')
    parser.add_argument('--episode-list',    type=str, default=None,
                        help='특정 에피소드만 변환 (쉼표로 구분: 0,2,5)')
    parser.add_argument('--use-symlink',     action='store_true',
                        help='중복 에피소드를 심볼릭 링크로 저장 (용량 절약)')
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = OUTPUT_DIR / args.dataset_name

    print(f'raw-dir    : {args.raw_dir}')
    print(f'output-dir : {args.output_dir}')
    print(f'task       : {args.task}')
    print(f'fps        : {args.fps}')
    print()

    build_dataset(
        raw_dir=args.raw_dir,
        output_dir=args.output_dir,
        task=args.task,
        fps=args.fps,
        robot_type=args.robot_type,
        camera_name=args.camera_name,
        camera2_name=args.camera2_name,
        category=args.category,
        skip_review=args.skip_review,
        category_filter=args.category_filter,
        episode_start=args.episode_start,
        episode_end=args.episode_end,
        episode_list=args.episode_list,
        use_symlink=args.use_symlink,
    )


if __name__ == '__main__':
    main()
