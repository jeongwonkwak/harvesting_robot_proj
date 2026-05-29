#!/usr/bin/env python3
"""
Convert ROS2 bag files (SQLite3) → LeRobot v3.0 dataset.

Input structure:
  <raw_dir>/
    episode_*_YYYYMMDD_HHMMSS/
      *.db3
      metadata.yaml

Output structure:
  <output_dir>/
    data/chunk-000/file-000.parquet
    videos/observation.images.<camera_name>/chunk-000/file-000.mp4
    meta/info.json
    meta/stats.json
    meta/tasks.parquet

Topics consumed:
  /dsr01/joint_states             sensor_msgs/msg/JointState  (first 6 joints)
  /gripper/position               std_msgs/msg/Float32         (gripper)
  /camera/camera/color/image_raw  sensor_msgs/msg/Image        (RGB)

curobo 세션 bag (curobo_* 폴더):
  /dsr01/curobo/pick_complete     std_msgs/msg/Empty  (에피소드 경계 마커)
  pick_complete 타임스탬프를 기준으로 에피소드 자동 분리
"""

import argparse
import json
import re
import sqlite3
import struct
import subprocess
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 설정값 (CLI 인수 없이 바로 실행할 때 여기를 수정하세요)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RAW_DIR     = Path('/home/user/robot_workspace/vla_ws/data/raw')
OUTPUT_DIR  = Path('/home/user/robot_workspace/vla_ws/data/mid')
DATASET_NAME = 'smolvla_dataset_v1.1.0'   # OUTPUT_DIR 아래 생성되는 폴더 이름

FPS         = 10
TASK        = 'robot manipulation task'
ROBOT_TYPE  = 'dsr01'
CAMERA_NAME = 'camera1'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _json_compact_arrays(obj, indent=2) -> str:
    """JSON 직렬화: 객체는 들여쓰기, 배열은 한 줄로."""
    raw = json.dumps(obj, indent=indent)
    return re.sub(
        r'\[([^\[\]]*)\]',
        lambda m: '[' + re.sub(r'\s+', ' ', m.group(1).strip()) + ']',
        raw,
        flags=re.DOTALL,
    )


# ── CDR Deserializer ──────────────────────────────────────────────────────────

class CDRReader:
    """Minimal CDR deserializer for ROS2 messages (little-endian)."""

    def __init__(self, raw: bytes):
        self.buf = raw[4:]  # skip 4-byte encapsulation header
        self.pos = 0

    def _align(self, n: int):
        r = self.pos % n
        if r:
            self.pos += n - r

    def read_int32(self) -> int:
        self._align(4)
        v = struct.unpack_from('<i', self.buf, self.pos)[0]
        self.pos += 4
        return v

    def read_uint32(self) -> int:
        self._align(4)
        v = struct.unpack_from('<I', self.buf, self.pos)[0]
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

    def read_string(self) -> str:
        length = self.read_uint32()  # includes null terminator
        s = self.buf[self.pos:self.pos + length - 1].decode('utf-8', errors='replace')
        self.pos += length
        return s

    def read_float64_array(self) -> list:
        count = self.read_uint32()
        if count == 0:
            return []
        self._align(8)
        vals = list(struct.unpack_from(f'<{count}d', self.buf, self.pos))
        self.pos += count * 8
        return vals

    def read_bytes(self, n: int) -> bytes:
        v = self.buf[self.pos:self.pos + n]
        self.pos += n
        return v


# ── Message Parsers ───────────────────────────────────────────────────────────

def parse_float32_msg(raw: bytes) -> float:
    return CDRReader(raw).read_float32()


_JOINT_ORDER = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']

def parse_joint_state(raw: bytes) -> list:
    """Return joint positions (radians) in [joint_1..joint_6] order."""
    r = CDRReader(raw)
    r.read_int32()   # stamp.sec
    r.read_uint32()  # stamp.nanosec
    r.read_string()  # frame_id
    name_count = r.read_uint32()
    names = [r.read_string() for _ in range(name_count)]
    positions = r.read_float64_array()
    name_to_pos = dict(zip(names, positions))
    # 이름 기반 추출 (순서 보장); 이름 없으면 위치 순 첫 6개로 폴백
    if all(j in name_to_pos for j in _JOINT_ORDER):
        return [name_to_pos[j] for j in _JOINT_ORDER]
    return list(positions[:6])


def parse_image(raw: bytes) -> np.ndarray:
    """Return RGB numpy array (H, W, 3) uint8."""
    r = CDRReader(raw)
    r.read_int32()   # stamp.sec
    r.read_uint32()  # stamp.nanosec
    r.read_string()  # frame_id
    height = r.read_uint32()
    width = r.read_uint32()
    encoding = r.read_string()
    r.read_uint8()   # is_bigendian
    r.read_uint32()  # step
    data_len = r.read_uint32()
    img_bytes = r.read_bytes(data_len)

    if encoding == 'mono8':
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width)
        img = np.stack([img, img, img], axis=-1)
    elif encoding == 'bgr8':
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width, 3)
        img = img[:, :, ::-1].copy()
    else:  # rgb8 and others
        img = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width, 3)

    return img


# ── Bag Reader ────────────────────────────────────────────────────────────────

def read_bag(db_path: Path) -> dict:
    """Read all messages from SQLite3 bag. Returns {topic: [(ts_ns, data), ...]}."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM topics')
    topics = {row[0]: row[1] for row in cur.fetchall()}
    data = {name: [] for name in topics.values()}
    cur.execute('SELECT topic_id, timestamp, data FROM messages ORDER BY timestamp')
    for topic_id, ts, raw in cur.fetchall():
        data[topics[topic_id]].append((ts, bytes(raw)))
    conn.close()
    return data


def _filter_time(bag_data: dict, t_start: int, t_end: int) -> dict:
    """Return a copy of bag_data with messages filtered to [t_start, t_end)."""
    return {
        topic: [(ts, d) for ts, d in msgs if t_start <= ts < t_end]
        for topic, msgs in bag_data.items()
    }


def split_by_pick_complete(bag_data: dict) -> list:
    """
    curobo 세션 bag을 pick_complete 신호 기준으로 에피소드 목록으로 분리.
    pick_complete 가 없으면 전체를 하나의 에피소드로 반환.
    """
    PICK = '/dsr01/curobo/pick_complete'
    pick_ts = [ts for ts, _ in bag_data.get(PICK, [])]
    if not pick_ts:
        return [bag_data]

    # 전체 시작 시각
    all_ts = [ts for msgs in bag_data.values() for ts, _ in msgs]
    if not all_ts:
        return [bag_data]
    t_bag_start = min(all_ts)

    # 에피소드 경계: [bag_start, pc0, pc1, ..., pcN]
    # → N개 에피소드 (각각 pc 직전까지)
    boundaries = [t_bag_start] + sorted(pick_ts)
    episodes = []
    for i in range(len(boundaries) - 1):
        ep = _filter_time(bag_data, boundaries[i], boundaries[i + 1])
        episodes.append(ep)
    return episodes


# ── Synchronization ───────────────────────────────────────────────────────────

def _nearest(sorted_ts: np.ndarray, query: np.ndarray) -> np.ndarray:
    idx = np.searchsorted(sorted_ts, query)
    idx = np.clip(idx, 0, len(sorted_ts) - 1)
    left = np.clip(idx - 1, 0, len(sorted_ts) - 1)
    closer_left = np.abs(sorted_ts[left] - query) <= np.abs(sorted_ts[idx] - query)
    idx[closer_left] = left[closer_left]
    return idx


def synchronize(bag_data: dict, fps: int = 30) -> dict | None:
    """
    Resample all streams onto a uniform fps grid.
    action[t] = state[t+1]  (last frame repeats the last state)
    """
    CAM = '/camera/camera/color/image_raw'
    JNT = '/dsr01/joint_states'
    GRP = '/gripper/position'

    for key in (CAM, JNT):
        if key not in bag_data or len(bag_data[key]) == 0:
            print(f'    Missing topic: {key}')
            return None

    cam_ts = np.array([t for t, _ in bag_data[CAM]], dtype=np.int64)
    jnt_ts = np.array([t for t, _ in bag_data[JNT]], dtype=np.int64)

    # 카메라를 기준 타임라인으로 사용 (관절·그리퍼는 고주파라 nearest 매핑 항상 가능)
    t_start = cam_ts[0]
    t_end = cam_ts[-1]
    if t_start >= t_end:
        return None

    # 카메라 커버리지 경고: 관절 녹화 시간 대비 카메라 커버 비율이 낮으면 USB 불안정 의심
    jnt_duration = (jnt_ts[-1] - jnt_ts[0]) / 1e9
    cam_duration = (t_end - t_start) / 1e9
    coverage = cam_duration / jnt_duration if jnt_duration > 0 else 1.0
    if coverage < 0.9:
        print(f'    [WARNING] 카메라가 세션의 {coverage*100:.0f}%만 커버됨 '
              f'(카메라 {cam_duration:.1f}s / 관절 {jnt_duration:.1f}s). '
              f'USB 재열거로 인한 카메라 드롭 의심. 영상이 잘릴 수 있습니다.')

    step_ns = int(1e9 / fps)
    grid = np.arange(t_start, t_end, step_ns, dtype=np.int64)
    if len(grid) == 0:
        return None

    cam_idx = _nearest(cam_ts, grid)
    jnt_idx = _nearest(jnt_ts, grid)

    # Parse joints and gripper (fast, no image decode)
    joints = [parse_joint_state(bag_data[JNT][i][1]) for i in jnt_idx]

    grp_msgs = bag_data.get(GRP, [])
    if grp_msgs:
        grp_ts = np.array([t for t, _ in grp_msgs], dtype=np.int64)
        grp_idx = _nearest(grp_ts, grid)
        grips = [parse_float32_msg(grp_msgs[i][1]) for i in grp_idx]
    else:
        print(f'    [WARNING] {GRP} 토픽 없음 — gripper를 0.0으로 채웁니다.')
        grips = [0.0] * len(grid)

    # Parse images (slow)
    print(f'    Decoding {len(grid)} frames ...', end='', flush=True)
    images = []
    prev = -1
    for i in cam_idx:
        if i == prev:
            images.append(images[-1])
        else:
            images.append(parse_image(bag_data[CAM][i][1]))
            prev = i
    print(' done')

    states = [j + [g] for j, g in zip(joints, grips)]
    actions = states[1:] + [states[-1]]

    return {
        'timestamps': (grid - grid[0]) / 1e9,
        'states': states,
        'actions': actions,
        'images': images,
    }


# ── Video Encoder ─────────────────────────────────────────────────────────────

class FFmpegVideoWriter:
    """Stream RGB frames → H.264 MP4 via ffmpeg subprocess (libx264)."""

    def __init__(self, output_path: Path, fps: int, width: int, height: int):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            'ffmpeg', '-y',
            '-f', 'rawvideo', '-vcodec', 'rawvideo',
            '-s', f'{width}x{height}',
            '-pix_fmt', 'rgb24',
            '-r', str(fps),
            '-i', 'pipe:0',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '18',
            str(output_path),
        ]
        self._proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def write(self, frame_rgb: np.ndarray):
        self._proc.stdin.write(frame_rgb.tobytes())

    def release(self):
        self._proc.stdin.close()
        self._proc.wait()


def encode_video(frames: list, output_path: Path, fps: int = 30):
    """Encode RGB frames → H.264 MP4 via ffmpeg libx264."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    h, w = frames[0].shape[:2]
    writer = FFmpegVideoWriter(output_path, fps, w, h)
    for frame in frames:
        writer.write(frame)
    writer.release()


# ── Dataset Builder ───────────────────────────────────────────────────────────

def build_dataset(
    raw_dir: Path,
    output_dir: Path,
    task: str,
    fps: int = 30,
    robot_type: str = 'dsr01',
    camera_name: str = 'camera1',
):
    episode_dirs = sorted(raw_dir.glob('episode_*')) + sorted(raw_dir.glob('curobo_*'))
    if not episode_dirs:
        raise FileNotFoundError(f'No episode_* or curobo_* directories in {raw_dir}')

    print(f'Found {len(episode_dirs)} bag directories\n')

    CHUNKS_SIZE = 1000
    all_rows = []
    all_states = []
    all_actions = []
    ep_count = 0
    global_idx = 0
    frame_shape = None
    video_paths = []

    for ep_dir in episode_dirs:
        db_files = list(ep_dir.glob('*.db3'))
        if not db_files:
            print(f'  [skip] {ep_dir.name}: no .db3 file')
            continue

        print(f'  Bag: {ep_dir.name}')
        bag_data = read_bag(db_files[0])

        # curobo 세션 bag이면 pick_complete 기준으로 에피소드 분리
        sub_episodes = split_by_pick_complete(bag_data)
        if len(sub_episodes) > 1:
            print(f'    curobo 세션: {len(sub_episodes)}개 에피소드로 분리')

        for sub_idx, sub_data in enumerate(sub_episodes):
            label = ep_dir.name if len(sub_episodes) == 1 else f'{ep_dir.name}[{sub_idx}]'
            print(f'  Episode {ep_count}: {label}')
            result = synchronize(sub_data, fps=fps)

            if result is None:
                print('    [skip] insufficient overlapping data')
                continue

            n = len(result['timestamps'])
            for f_idx in range(n):
                all_rows.append({
                    'index': global_idx + f_idx,
                    'episode_index': ep_count,
                    'frame_index': f_idx,
                    'timestamp': float(result['timestamps'][f_idx]),
                    'task_index': 0,
                    'observation.state': result['states'][f_idx],
                    'action': result['actions'][f_idx],
                })

            images = result['images']
            if frame_shape is None:
                h, w = images[0].shape[:2]
                frame_shape = (h, w)
            else:
                h, w = frame_shape

            chunk_idx = ep_count // CHUNKS_SIZE
            file_idx = ep_count % CHUNKS_SIZE
            video_path = (
                output_dir / 'videos'
                / f'observation.images.{camera_name}'
                / f'chunk-{chunk_idx:03d}' / f'file-{file_idx:03d}.mp4'
            )
            video_paths.append(video_path)

            print(f'    Encoding {len(images)} frames to video ...', end='', flush=True)
            writer = FFmpegVideoWriter(video_path, fps, w, h)
            for frame in images:
                writer.write(frame)
            writer.release()
            print(f' done → {video_path.name}')

            del images
            all_states.extend(result['states'])
            all_actions.extend(result['actions'])
            global_idx += n
            ep_count += 1
            print(f'    {n} frames  ({n / fps:.1f}s)')

    if not all_rows:
        raise RuntimeError('No valid episodes to convert')

    total_frames = global_idx
    print(f'\nTotal: {ep_count} episodes, {total_frames} frames')

    # ── Parquet ───────────────────────────────────────────────────────────────
    parquet_path = output_dir / 'data' / 'chunk-000' / 'file-000.parquet'
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    table = pa.table({
        'index':             pa.array([r['index'] for r in all_rows],             type=pa.int64()),
        'episode_index':     pa.array([r['episode_index'] for r in all_rows],     type=pa.int64()),
        'frame_index':       pa.array([r['frame_index'] for r in all_rows],       type=pa.int64()),
        'timestamp':         pa.array([r['timestamp'] for r in all_rows],         type=pa.float64()),
        'task_index':        pa.array([r['task_index'] for r in all_rows],        type=pa.int64()),
        'observation.state': pa.array([r['observation.state'] for r in all_rows], type=pa.list_(pa.float64())),
        'action':            pa.array([r['action'] for r in all_rows],            type=pa.list_(pa.float64())),
    })
    pq.write_table(table, parquet_path)
    print(f'Saved parquet → {parquet_path}')

    # ── JSON (사람이 읽기 쉬운 형태로 추가 저장) ──────────────────────────────
    json_path = output_dir / 'data' / 'chunk-000' / 'file-000.json'
    json_records = []
    for r in all_rows:
        json_records.append({
            'index':             r['index'],
            'episode_index':     r['episode_index'],
            'frame_index':       r['frame_index'],
            'timestamp':         round(r['timestamp'], 4),
            'task_index':        r['task_index'],
            'observation.state': [round(v, 6) for v in r['observation.state']],
            'action':            [round(v, 6) for v in r['action']],
        })
    json_path.write_text(_json_compact_arrays(json_records))
    print(f'Saved json   → {json_path}')

    # ── Meta ──────────────────────────────────────────────────────────────────
    meta_dir = output_dir / 'meta'
    meta_dir.mkdir(parents=True, exist_ok=True)

    # tasks.parquet  (task column as pandas index, matching LeRobot convention)
    tasks_df = pd.DataFrame({'task_index': [0]}, index=pd.Index([task], name='task'))
    tasks_df.to_parquet(meta_dir / 'tasks.parquet')

    # stats.json
    states_np = np.array(all_states)
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

    # info.json
    h, w = frame_shape if frame_shape else (480, 640)
    info = {
        'codebase_version': 'v3.0',
        'fps': fps,
        'robot_type': robot_type,
        'total_episodes': ep_count,
        'total_frames': total_frames,
        'total_tasks': 1,
        'chunks_size': 1000,
        'data_files_size_in_mb': round(parquet_path.stat().st_size / 1024 / 1024, 3),
        'video_files_size_in_mb': round(sum(p.stat().st_size for p in video_paths) / 1024 / 1024, 3),
        'splits': {'train': f'0:{ep_count}'},
        'data_path': 'data/chunk-{chunk_index:03d}/file-{file_index:03d}.parquet',
        'video_path': 'videos/{video_key}/chunk-{chunk_index:03d}/file-{file_index:03d}.mp4',
        'features': {
            f'observation.images.{camera_name}': {
                'dtype': 'video',
                'shape': [3, h, w],
                'names': ['channels', 'height', 'width'],
            },
            'observation.state': {
                'dtype': 'float32',
                'shape': [7],
                'names': ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'gripper'],
            },
            'action': {
                'dtype': 'float32',
                'shape': [7],
                'names': ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'gripper'],
            },
            'timestamp':     {'dtype': 'float32', 'shape': [1], 'names': None},
            'frame_index':   {'dtype': 'int64',   'shape': [1], 'names': None},
            'episode_index': {'dtype': 'int64',   'shape': [1], 'names': None},
            'index':         {'dtype': 'int64',   'shape': [1], 'names': None},
            'task_index':    {'dtype': 'int64',   'shape': [1], 'names': None},
        },
    }
    (meta_dir / 'info.json').write_text(json.dumps(info, indent=2))

    print(f'\nDataset ready at {output_dir}')
    print(f'  Episodes : {ep_count}')
    print(f'  Frames   : {total_frames}')
    print(f'  Task     : {task}')


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Convert ROS2 bag files to LeRobot v3.0 dataset format'
    )
    parser.add_argument('--raw-dir',      type=Path, default=RAW_DIR)
    parser.add_argument('--output-dir',   type=Path, default=None)
    parser.add_argument('--dataset-name', type=str,  default=DATASET_NAME)
    parser.add_argument('--task',         type=str,  default=TASK)
    parser.add_argument('--fps',          type=int,  default=FPS)
    parser.add_argument('--robot-type',   type=str,  default=ROBOT_TYPE)
    parser.add_argument('--camera-name',  type=str,  default=CAMERA_NAME)
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
    )


if __name__ == '__main__':
    main()
