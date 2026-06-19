#!/usr/bin/env python3
"""
vla_dataset_v0.4.5 → vla_dataset_v0.4.6

같은 방향 연속 버튼 압버튼 사이의 짧은 정지 구간을 제거하고,
연속 burst들을 하나의 부드러운 선형 궤적으로 합친다.

조건: STILL 구간이 MAX_STILL_FRAMES 이하 AND 앞뒤 burst 방향 차이가 MAX_ANGLE_DEG 미만

처리 방식 (핵심 수정):
  burst_A → STILL → burst_B 가 조건 충족 시
  → [burst_A + STILL + burst_B] 전체를 burst_A_시작 → burst_B_끝 까지 선형 보간
  → STILL 프레임도 P1→P2 사이 중간 값을 갖게 되어 action ≠ 0
  연속 체인 (A→B→C 등)은 한 번에 묶어서 처리
"""

import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.5")
DST = Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.6")

MOVE_THR         = 1e-4   # xyz delta(m) 이하면 정지로 간주
MAX_STILL_FRAMES = 4      # 이 프레임 이하의 STILL만 보간 대상
MAX_ANGLE_DEG    = 30.0   # 앞뒤 burst 방향 차이 임계값


# ── 유틸 ──────────────────────────────────────────────────────────────────

def segment(states: np.ndarray) -> list[tuple]:
    """(kind, length, start, end_exclusive) 목록 반환."""
    diffs = np.linalg.norm(np.diff(states[:, :3], axis=0), axis=1)
    is_mv = diffs > MOVE_THR
    segs, i = [], 0
    while i < len(is_mv):
        kind = 'MOVE' if is_mv[i] else 'STILL'
        j = i
        while j < len(is_mv) and is_mv[j] == is_mv[i]:
            j += 1
        segs.append((kind, j - i, i, j))
        i = j
    return segs


def burst_direction(states: np.ndarray, s: int, e: int) -> np.ndarray | None:
    vec = states[e, :3] - states[s, :3]
    n   = np.linalg.norm(vec)
    return vec / n if n > 1e-5 else None


def angle_between(d1: np.ndarray, d2: np.ndarray) -> float:
    return float(np.degrees(np.arccos(np.clip(np.dot(d1, d2), -1.0, 1.0))))


# ── 에피소드 처리 ─────────────────────────────────────────────────────────

def process_episode(states: np.ndarray) -> tuple[np.ndarray, dict]:
    segs = segment(states)
    out  = states.copy()

    stats = {'chains': 0, 'modified_frames': 0,
             'skipped_angle': 0, 'skipped_long': 0}

    # MOVE 세그먼트 인덱스만 추려서 체인 탐색
    visited = set()
    si = 0
    while si < len(segs):
        kind, n, s, e = segs[si]
        if kind != 'MOVE' or si in visited:
            si += 1
            continue

        # 이 burst 를 체인 시작으로 삼고 확장 시도
        chain = [si]  # 세그먼트 인덱스 목록 (MOVE, STILL, MOVE, ...)
        ji = si + 1

        while ji + 1 < len(segs):
            still    = segs[ji]
            nxt_move = segs[ji + 1]

            if still[0] != 'STILL' or nxt_move[0] != 'MOVE':
                break

            # 길이 조건
            if still[1] > MAX_STILL_FRAMES:
                stats['skipped_long'] += still[1]
                break

            # 방향 조건: 체인 전체의 현재 방향 vs 다음 burst
            last_move = segs[chain[-1]]
            pd_ = burst_direction(states, last_move[2], last_move[3])
            nd_ = burst_direction(states, nxt_move[2], nxt_move[3])
            if pd_ is None or nd_ is None:
                break
            angle = angle_between(pd_, nd_)
            if angle >= MAX_ANGLE_DEG:
                stats['skipped_angle'] += still[1]
                break

            chain.append(ji)      # STILL
            chain.append(ji + 1)  # MOVE
            ji += 2

        # 체인에 STILL이 하나라도 포함된 경우에만 처리
        has_still = any(segs[idx][0] == 'STILL' for idx in chain)
        if has_still:
            chain_start = segs[chain[0]][2]       # 첫 MOVE의 시작 frame
            chain_end   = segs[chain[-1]][3]      # 마지막 MOVE의 끝 frame (exclusive)

            p_start = states[chain_start].copy()
            p_end   = states[chain_end - 1].copy()
            total   = chain_end - chain_start

            # 전체 구간을 p_start → p_end 선형 보간
            for k in range(chain_start, chain_end):
                t = (k - chain_start) / (total - 1) if total > 1 else 0.0
                out[k] = p_start + t * (p_end - p_start)

            stats['chains']          += 1
            stats['modified_frames'] += total

            for idx in chain:
                visited.add(idx)

        si = ji if ji > si else si + 1

    return out, stats


def recompute_actions(states: np.ndarray, orig_actions: np.ndarray) -> np.ndarray:
    N = len(states)
    new_actions = orig_actions.copy()
    for i in range(N - 1):
        delta     = states[i + 1, :6] - states[i, :6]
        grip_next = float(states[i + 1, 6])
        new_actions[i] = np.array([*delta, grip_next], dtype=np.float32)
    return new_actions


# ── parquet ───────────────────────────────────────────────────────────────

def process_parquet(src_path: Path, dst_path: Path):
    df = pd.read_parquet(src_path)
    new_state_rows, new_action_rows = {}, {}

    total_stats = {'chains': 0, 'modified_frames': 0,
                   'skipped_angle': 0, 'skipped_long': 0}

    for ep_idx in sorted(df['episode_index'].unique()):
        mask    = df['episode_index'] == ep_idx
        ep_df   = df[mask]
        states  = np.stack(ep_df['observation.state'].values).astype(np.float64)
        actions = np.stack(ep_df['action'].values).astype(np.float64)

        new_states, ep_stats = process_episode(states)
        new_actions = recompute_actions(new_states, actions)

        for k, v in ep_stats.items():
            total_stats[k] += v

        for i, row_idx in enumerate(ep_df.index):
            new_state_rows[row_idx]  = new_states[i].astype(np.float32)
            new_action_rows[row_idx] = new_actions[i].astype(np.float32)

    df['observation.state'] = pd.Series(new_state_rows)
    df['action']            = pd.Series(new_action_rows)
    df.to_parquet(dst_path, index=False)
    return df, total_stats


# ── stats ────────────────────────────────────────────────────────────────

def quantile_stats(arr: np.ndarray) -> dict:
    return {
        'min':   arr.min(axis=0).tolist(),
        'max':   arr.max(axis=0).tolist(),
        'mean':  arr.mean(axis=0).tolist(),
        'std':   arr.std(axis=0).tolist(),
        'count': [int(len(arr))] * arr.shape[1],
        'q01':   np.percentile(arr,  1, axis=0).tolist(),
        'q10':   np.percentile(arr, 10, axis=0).tolist(),
        'q50':   np.percentile(arr, 50, axis=0).tolist(),
        'q90':   np.percentile(arr, 90, axis=0).tolist(),
        'q99':   np.percentile(arr, 99, axis=0).tolist(),
    }


# ── 메인 ─────────────────────────────────────────────────────────────────

def main():
    if DST.exists():
        print(f"[오류] 이미 존재: {DST}")
        sys.exit(1)

    print(f"SRC: {SRC}")
    print(f"DST: {DST}")
    print(f"조건: STILL <= {MAX_STILL_FRAMES}f, 방향 차이 < {MAX_ANGLE_DEG}도\n")

    print("[1/4] meta/ 복사...")
    shutil.copytree(SRC / "meta", DST / "meta")

    print("[2/4] videos/ 심볼릭 링크...")
    (DST / "videos").symlink_to((SRC / "videos").resolve())

    print("[3/4] parquet 처리...")
    data_dst = DST / "data" / "chunk-000"
    data_dst.mkdir(parents=True)
    src_pq = SRC / "data" / "chunk-000" / "file-000.parquet"
    dst_pq = data_dst / "file-000.parquet"

    df_new, total_stats = process_parquet(src_pq, dst_pq)

    print(f"    병합된 체인 수     : {total_stats['chains']}")
    print(f"    보간된 총 프레임   : {total_stats['modified_frames']}")
    print(f"    건너뜀 (방향 차이) : {total_stats['skipped_angle']}f")
    print(f"    건너뜀 (길이 초과) : {total_stats['skipped_long']}f")

    print("[4/4] stats.json 재계산...")
    with open(SRC / "meta" / "stats.json") as f:
        src_stats = json.load(f)

    states_all  = np.stack(df_new['observation.state'].values).astype(np.float64)
    actions_all = np.stack(df_new['action'].values).astype(np.float64)
    new_stats   = dict(src_stats)
    new_stats['observation.state'] = quantile_stats(states_all)
    new_stats['action']            = quantile_stats(actions_all)

    with open(DST / "meta" / "stats.json", "w") as f:
        json.dump(new_stats, f, indent=4)

    # 검증
    df_src     = pd.read_parquet(src_pq)
    src_act    = np.stack(df_src['action'].values)
    new_act    = np.stack(df_new['action'].values)
    src_zero   = (np.linalg.norm(src_act[:, :3], axis=1) < MOVE_THR).mean()
    new_zero   = (np.linalg.norm(new_act[:, :3], axis=1) < MOVE_THR).mean()

    print(f"\n[검증]")
    print(f"    zero-action 비율: {src_zero*100:.1f}% → {new_zero*100:.1f}%")
    print(f"    감소량: {(src_zero - new_zero)*100:.1f}%p")
    print(f"\n완료: {DST}")


if __name__ == "__main__":
    main()
