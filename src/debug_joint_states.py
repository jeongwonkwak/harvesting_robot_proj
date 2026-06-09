#!/usr/bin/env python3
"""
ROS 2 bag 파일과 Parquet 데이터셋의 Joint State 비교
- 원본 bag의 Joint State 값
- Parquet로 변환된 Joint State 값
- 불일치 분석
"""

import sqlite3
import struct
import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path("/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.4.0")
DATASET_DIR = Path("/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.1")

# ── CDR Reader (bag_to_lerobot_eef.py에서 복사) ────────────────────────

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

    def read_uint8(self) -> int:
        v = self.buf[self.pos]
        self.pos += 1
        return v

    def read_float64(self) -> float:
        self._align(8)
        v = struct.unpack_from('<d', self.buf, self.pos)[0]
        self.pos += 8
        return v

    def read_string(self) -> str:
        length = self.read_uint32()
        s = self.buf[self.pos:self.pos + length - 1].decode('utf-8', errors='replace')
        self.pos += length
        return s


def parse_joint_states(raw: bytes) -> list:
    """Parse sensor_msgs/JointState → [j1_rad, ..., j6_rad]"""
    r = CDRReader(raw)
    r.read_uint32()      # sec
    r.read_uint32()      # nsec
    r.read_string()      # frame_id

    name_count = r.read_uint32()
    for _ in range(name_count):
        r.read_string()

    pos_count = r.read_uint32()
    positions = [r.read_float64() for _ in range(pos_count)]
    return positions[:6] if len(positions) >= 6 else positions


# ── Bag 파일 읽기 ────────────────────────────────────────────────────────

def read_bag_joint_states(bag_path: Path) -> list:
    """ROS 2 bag에서 Joint State 추출"""
    conn = sqlite3.connect(str(bag_path))
    cur = conn.cursor()

    # Topic ID 찾기
    cur.execute("SELECT id, name FROM topics WHERE name = '/dsr01/joint_states'")
    result = cur.fetchone()

    if not result:
        print(f"⚠️  /dsr01/joint_states 토픽을 찾을 수 없음")
        conn.close()
        return []

    topic_id = result[0]

    # 메시지 읽기
    cur.execute('SELECT timestamp, data FROM messages WHERE topic_id = ? ORDER BY timestamp', (topic_id,))
    messages = cur.fetchall()
    conn.close()

    joint_states = []
    timestamps = []

    for ts, raw in messages:
        try:
            joints = parse_joint_states(bytes(raw))
            joint_states.append(joints)
            timestamps.append(ts)
        except Exception as e:
            print(f"  파싱 오류 (ts={ts}): {e}")

    return timestamps, joint_states


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("🔍 Joint State 데이터 검증")
    print("=" * 80)

    # 1. Parquet 데이터셋 확인
    print("\n[1️⃣] Parquet 데이터셋의 Joint State")
    print("-" * 80)

    parquet_path = DATASET_DIR / "data/chunk-000/file-000.parquet"
    if not parquet_path.exists():
        print(f"❌ 파케이 파일을 찾을 수 없음: {parquet_path}")
        return

    df = pd.read_parquet(parquet_path)

    # state 길이 확인
    first_state = df['observation.state'].iloc[0]
    state_len = len(first_state)
    print(f"State 길이: {state_len}-dim")

    if state_len >= 12:
        print("✅ Joint State 포함됨 (12-dim: EEF 6 + Joint 6)")

        # Episode 0, Frame 0의 Joint State
        ep0_frame0 = df[(df['episode_index'] == 0) & (df['frame_index'] == 0)].iloc[0]
        joints_rad = np.array(ep0_frame0['observation.state'][6:12])
        joints_deg = np.degrees(joints_rad)

        print(f"\nEpisode 0, Frame 0:")
        print(f"  라디안: {joints_rad}")
        print(f"  도(°):  {joints_deg}")
    else:
        print("❌ Joint State 미포함 (6-dim: EEF만)")

    # 2. 원본 bag 파일 확인
    print("\n[2️⃣] 원본 ROS 2 bag 파일의 Joint State")
    print("-" * 80)

    episode_dirs = sorted(RAW_DIR.glob("episode_*_eef"))
    if not episode_dirs:
        episode_dirs = sorted(RAW_DIR.glob("episode_*"))

    if not episode_dirs:
        print("❌ Episode 디렉토리를 찾을 수 없음")
        return

    ep0_dir = episode_dirs[0]
    db_files = list(ep0_dir.glob("*.db3"))

    if not db_files:
        print(f"❌ bag 파일을 찾을 수 없음: {ep0_dir}")
        return

    print(f"Bag 파일: {db_files[0].name}")

    bag_timestamps, bag_joints = read_bag_joint_states(db_files[0])

    if bag_joints:
        first_joints_rad = np.array(bag_joints[0])
        first_joints_deg = np.degrees(first_joints_rad)

        print(f"\n첫 번째 메시지 (가장 초기 Joint State):")
        print(f"  라디안: {first_joints_rad}")
        print(f"  도(°):  {first_joints_deg}")

        # 예상값과 비교
        expected = np.array([18.91, 25.97, 1.00, 74.58, 78.17, -115.61])
        actual = first_joints_deg

        print(f"\n[3️⃣] 기대값 vs 실제값 비교")
        print("-" * 80)
        print(f"{'Joint':<8} {'기대값(°)':<12} {'실제값(°)':<12} {'오차(°)':<12} {'오차율(%)':<12}")
        print("-" * 80)

        for i in range(6):
            error = actual[i] - expected[i]
            error_pct = (error / expected[i] * 100) if expected[i] != 0 else 0
            print(f"J{i+1:<7} {expected[i]:>10.2f} {actual[i]:>11.2f} {error:>11.2f} {error_pct:>11.1f}%")

        # 종합 평가
        total_error = np.sum(np.abs(actual - expected))
        max_error = np.max(np.abs(actual - expected))

        print("-" * 80)
        print(f"{'합계':<8} {'':<12} {'':<12} {total_error:>11.2f}")
        print(f"{'최대 오차':<8} {'':<12} {'':<12} {max_error:>11.2f}°")

        if max_error > 10:
            print("\n🔴 심각한 오차 발생!")
            print("  → 센서 캘리브레이션 오류 또는 데이터 변환 문제 가능성")
        else:
            print("\n🟢 오차 범위 내")
    else:
        print("❌ Joint State 메시지를 찾을 수 없음")

    # 3. 시간 범위 확인
    if bag_timestamps and state_len >= 12:
        print(f"\n[4️⃣] 데이터 수집 범위")
        print("-" * 80)
        bag_duration = (bag_timestamps[-1] - bag_timestamps[0]) / 1e9
        parquet_duration = df['timestamp'].max() - df['timestamp'].min()

        print(f"Bag 파일:     {bag_duration:.2f}초 ({len(bag_timestamps)} 메시지)")
        print(f"Parquet 데이: {parquet_duration:.2f}초 ({len(df)} 프레임)")
        print(f"FPS:          {len(df) / parquet_duration:.1f}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
