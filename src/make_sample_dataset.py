"""
SmolVLA sample dataset 생성 스크립트
출력: /home/user/workspace/jeongwon_lab/data/vla/fin/smolvla_sft_dataset_v.0.1.0/
"""

import json
import subprocess
import numpy as np
import pandas as pd
from pathlib import Path

# ── 설정 ─────────────────────────────────────────────────────────────────────
ROOT       = Path("/home/user/workspace/jeongwon_lab/data/vla/fin/smolvla_sft_dataset_v.0.1.0")
FPS        = 30          # 초당 프레임 수 = 로봇 제어 주기
N_EPISODES = 5           # 생성할 에피소드 수
N_FRAMES   = 300         # 에피소드당 프레임 수 (10초 × 30fps)
ACTION_DIM = 7           # 관절 6개 + 그리퍼 1개
STATE_DIM  = 7
IMG_H      = 720         # RealSense D455 세로
IMG_W      = 1280        # RealSense D455 가로
CAM_KEY    = "observation.images.camera1"   # smolvla_base pretrained 규칙에 맞춤 (실제 수집 시 rename_map으로 cam_wrist → camera1 매핑)
TASK_STR   = "Pull off the silver connector from the strawberry."

JOINT_NAMES = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "gripper"]

# ── 디렉토리 생성 ─────────────────────────────────────────────────────────────
for d in [
    ROOT / "meta" / "episodes" / "chunk-000",
    ROOT / "data"  / "chunk-000",
    ROOT / "videos" / CAM_KEY / "chunk-000",
]:
    d.mkdir(parents=True, exist_ok=True)

# ── 1. 프레임 데이터 생성 ─────────────────────────────────────────────────────
rng = np.random.default_rng(42)
all_records = []
all_states  = []
all_actions = []

for ep_idx in range(N_EPISODES):
    state_base = rng.uniform(-0.5, 0.5, STATE_DIM).astype(np.float32)
    global_offset = ep_idx * N_FRAMES
    for i in range(N_FRAMES):
        state  = (state_base + rng.normal(0, 0.01, STATE_DIM)).astype(np.float32)
        action = (state + rng.normal(0, 0.02, ACTION_DIM)).astype(np.float32)
        all_records.append({
            "index":               global_offset + i,
            "episode_index":       ep_idx,
            "frame_index":         i,
            "timestamp":           round(i / FPS, 6),
            "task_index":          0,
            "observation.state":   state.tolist(),
            "action":              action.tolist(),
        })
        all_states.append(state)
        all_actions.append(action)

# ── 2. data/chunk-000/file-000.parquet ───────────────────────────────────────
pd.DataFrame(all_records).to_parquet(
    ROOT / "data" / "chunk-000" / "file-000.parquet", index=False
)
print("✓ data/chunk-000/file-000.parquet")

# ── 3. videos/.../file-000.mp4 (모든 에피소드 이어붙인 더미 영상) ───────────────
total_duration = N_EPISODES * N_FRAMES / FPS
video_path = ROOT / "videos" / CAM_KEY / "chunk-000" / "file-000.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-f", "lavfi",
    "-i", f"color=c=gray:size={IMG_W}x{IMG_H}:rate={FPS}:duration={total_duration}",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    str(video_path),
], check=True, capture_output=True)
print(f"✓ videos/{CAM_KEY}/chunk-000/file-000.mp4  ({total_duration:.0f}초)")

# ── 4. meta/episodes/chunk-000/file-000.parquet ──────────────────────────────
state_arr  = np.array(all_states,  dtype=np.float32)
action_arr = np.array(all_actions, dtype=np.float32)

ep_rows = []
for ep_idx in range(N_EPISODES):
    s = state_arr [ep_idx*N_FRAMES:(ep_idx+1)*N_FRAMES]
    a = action_arr[ep_idx*N_FRAMES:(ep_idx+1)*N_FRAMES]
    ep_rows.append({
        "episode_index":                      ep_idx,
        "tasks":                              [TASK_STR],
        "length":                             N_FRAMES,
        "data/chunk_index":                   0,
        "data/file_index":                    0,
        f"videos/{CAM_KEY}/chunk_index":      0,
        f"videos/{CAM_KEY}/file_index":       0,
        "meta/episodes/chunk_index":          0,
        "meta/episodes/file_index":           0,
        "dataset_from_index":                 ep_idx * N_FRAMES,
        "dataset_to_index":                   (ep_idx + 1) * N_FRAMES,
        f"videos/{CAM_KEY}/from_timestamp":   ep_idx * (N_FRAMES / FPS),
        f"videos/{CAM_KEY}/to_timestamp":     (ep_idx + 1) * (N_FRAMES / FPS),
        "stats/observation.state/mean":       s.mean(0).tolist(),
        "stats/observation.state/std":        s.std(0).tolist(),
        "stats/observation.state/min":        s.min(0).tolist(),
        "stats/observation.state/max":        s.max(0).tolist(),
        "stats/action/mean":                  a.mean(0).tolist(),
        "stats/action/std":                   a.std(0).tolist(),
        "stats/action/min":                   a.min(0).tolist(),
        "stats/action/max":                   a.max(0).tolist(),
    })

pd.DataFrame(ep_rows).to_parquet(
    ROOT / "meta" / "episodes" / "chunk-000" / "file-000.parquet", index=False
)
print("✓ meta/episodes/chunk-000/file-000.parquet")

# ── 5. meta/tasks.parquet ─────────────────────────────────────────────────────
# task text must be the DataFrame index (index name="task"), task_index is the only column
# load_tasks() reads this and uses .iloc[task_idx].name to retrieve the task string
pd.DataFrame(
    {"task_index": [0]},
    index=pd.Index([TASK_STR], name="task"),
).to_parquet(ROOT / "meta" / "tasks.parquet")
print("✓ meta/tasks.parquet")

# ── 6. meta/stats.json ───────────────────────────────────────────────────────
def stats(arr):
    return {"mean": arr.mean(0).tolist(), "std": arr.std(0).tolist(),
            "min":  arr.min(0).tolist(),  "max": arr.max(0).tolist()}

with open(ROOT / "meta" / "stats.json", "w") as f:
    json.dump({"observation.state": stats(state_arr), "action": stats(action_arr)}, f, indent=2)
print("✓ meta/stats.json")

# ── 7. meta/info.json ─────────────────────────────────────────────────────────
info = {
    "codebase_version": "v3.0",
    "fps": FPS,
    "robot_type": "so100_follower",
    "total_episodes": N_EPISODES,
    "total_frames":   N_EPISODES * N_FRAMES,
    "total_tasks":    1,
    "chunks_size":    1000,
    "data_files_size_in_mb":  512,
    "video_files_size_in_mb": 512,
    "splits": {"train": f"0:{N_EPISODES}"},
    "data_path":  "data/chunk-{chunk_index:03d}/file-{file_index:03d}.parquet",
    "video_path": "videos/{video_key}/chunk-{chunk_index:03d}/file-{file_index:03d}.mp4",
    "features": {
        CAM_KEY: {"dtype": "video", "shape": [3, IMG_H, IMG_W],
                  "names": ["channels", "height", "width"]},
        "observation.state": {"dtype": "float32", "shape": [STATE_DIM],  "names": JOINT_NAMES},
        "action":            {"dtype": "float32", "shape": [ACTION_DIM], "names": JOINT_NAMES},
        "timestamp":     {"dtype": "float32", "shape": [1], "names": None},
        "frame_index":   {"dtype": "int64",   "shape": [1], "names": None},
        "episode_index": {"dtype": "int64",   "shape": [1], "names": None},
        "index":         {"dtype": "int64",   "shape": [1], "names": None},
        "task_index":    {"dtype": "int64",   "shape": [1], "names": None},
    },
}
with open(ROOT / "meta" / "info.json", "w") as f:
    json.dump(info, f, indent=2)
print("✓ meta/info.json")

print(f"\n완료: {ROOT}")
print(f"  에피소드: {N_EPISODES}건 × {N_FRAMES}프레임 = 총 {N_EPISODES*N_FRAMES}프레임")
