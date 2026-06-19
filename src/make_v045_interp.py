#!/usr/bin/env python3
"""
vla_dataset_v0.4.4 → vla_dataset_v0.4.5
observation.state의 연속 중복 프레임에 선형 보간을 적용하고 action(delta)을 재계산한다.

v0.4.4는 bag 동기화 시 nearest 방식을 사용해서 동일 raw 샘플이 연속 2회 이상
선택되는 아티팩트(6.2% 중복 프레임)가 있다.
v0.4.5는 이 중복 구간을 앞뒤 keyframe 사이의 선형 보간값으로 대체한다.
"""

import json
import os
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.4")
DST = Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.5")


# ── 보간 ────────────────────────────────────────────────────────────────────

def interp_states(states: np.ndarray) -> tuple[np.ndarray, int]:
    """연속으로 완전히 동일한 프레임을 전후 keyframe 사이의 선형 보간값으로 대체.

    반환: (보간된 states, 수정된 프레임 수)
    """
    out = states.copy()
    N = len(states)

    # is_dup[i] = True  ↔  states[i] == states[i-1]  (i >= 1)
    diffs = np.diff(states, axis=0)                        # (N-1, D)
    is_dup = np.concatenate([[False], np.all(diffs == 0, axis=1)])  # (N,)

    keyframes = np.where(~is_dup)[0]   # 중복이 아닌 프레임 인덱스

    modified = 0
    for ki in range(len(keyframes) - 1):
        k0, k1 = keyframes[ki], keyframes[ki + 1]
        gap = k1 - k0
        if gap <= 1:
            continue
        # k0+1 … k1-1 구간이 중복 → 선형 보간
        for j in range(k0 + 1, k1):
            t = (j - k0) / gap
            out[j] = states[k0] + t * (states[k1] - states[k0])
            modified += 1

    return out, modified


def recompute_actions(states: np.ndarray, orig_actions: np.ndarray) -> np.ndarray:
    """state 기반으로 action(delta) 재계산.

    action[t] = [Δx, Δy, Δz, Δrx, Δry, Δrz, grip_next]
      - Δ* = state[t+1] - state[t]  (6-dim EEF delta)
      - grip_next = state[t+1][6]   (다음 프레임 그리퍼 값, ratio 0~1)
    마지막 프레임은 delta=0, grip=현재 상태 유지 (원본 동작 그대로).
    """
    N = len(states)
    new_actions = orig_actions.copy()

    for i in range(N - 1):
        delta = states[i + 1, :6] - states[i, :6]
        grip_next = float(states[i + 1, 6])
        new_actions[i] = np.array([*delta, grip_next], dtype=np.float32)
    # new_actions[-1]은 원본 유지 (delta=0, grip=current)

    return new_actions


# ── parquet 처리 ─────────────────────────────────────────────────────────────

def process_parquet(src_path: Path, dst_path: Path) -> dict:
    df = pd.read_parquet(src_path)

    # 에피소드별 처리
    new_state_rows = {}   # index → new array
    new_action_rows = {}

    total_modified = 0
    episode_report = {}

    for ep_idx in sorted(df['episode_index'].unique()):
        mask = df['episode_index'] == ep_idx
        ep_df = df[mask]

        states  = np.stack(ep_df['observation.state'].values).astype(np.float64)
        actions = np.stack(ep_df['action'].values).astype(np.float64)

        new_states, n_mod = interp_states(states)
        new_actions = recompute_actions(new_states, actions)

        total_modified += n_mod
        episode_report[int(ep_idx)] = n_mod

        for i, row_idx in enumerate(ep_df.index):
            new_state_rows[row_idx]  = new_states[i].astype(np.float32)
            new_action_rows[row_idx] = new_actions[i].astype(np.float32)

    df['observation.state'] = pd.Series(new_state_rows)
    df['action']            = pd.Series(new_action_rows)

    df.to_parquet(dst_path, index=False)

    return {'total_modified': total_modified, 'by_episode': episode_report}


# ── stats 재계산 ─────────────────────────────────────────────────────────────

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


def recompute_stats(df: pd.DataFrame, src_stats: dict) -> dict:
    """observation.state, action만 재계산하고 나머지는 원본 유지."""
    new_stats = dict(src_stats)

    states  = np.stack(df['observation.state'].values).astype(np.float64)
    actions = np.stack(df['action'].values).astype(np.float64)

    new_stats['observation.state'] = quantile_stats(states)
    new_stats['action']            = quantile_stats(actions)

    return new_stats


# ── 메인 ─────────────────────────────────────────────────────────────────────

def main():
    if DST.exists():
        print(f"[오류] 이미 존재: {DST}")
        sys.exit(1)

    print(f"SRC: {SRC}")
    print(f"DST: {DST}\n")

    # 1. meta/ 복사
    print("[1/4] meta/ 복사...")
    shutil.copytree(SRC / "meta", DST / "meta")

    # 2. videos/ 심볼릭 링크 (321 MB 절약)
    print("[2/4] videos/ 심볼릭 링크...")
    (DST / "videos").symlink_to((SRC / "videos").resolve())

    # 3. parquet 보간 처리
    print("[3/4] parquet 보간 처리...")
    data_dst = DST / "data" / "chunk-000"
    data_dst.mkdir(parents=True)

    src_parquet = SRC / "data" / "chunk-000" / "file-000.parquet"
    dst_parquet = data_dst / "file-000.parquet"

    report = process_parquet(src_parquet, dst_parquet)

    total_frames = sum(report['by_episode'].values())  # 보간 대상 중복 프레임 합계는 total_modified
    print(f"    보간된 프레임 수: {report['total_modified']} / {sum(v for v in report['by_episode'].values()) + report['total_modified']}")
    print("    에피소드별 보간 프레임 수:")
    for ep, n in report['by_episode'].items():
        if n > 0:
            print(f"      ep{ep:02d}: {n}프레임")

    # 4. stats.json 재계산
    print("[4/4] stats.json 재계산...")
    with open(SRC / "meta" / "stats.json") as f:
        src_stats = json.load(f)

    df_new = pd.read_parquet(dst_parquet)
    new_stats = recompute_stats(df_new, src_stats)

    with open(DST / "meta" / "stats.json", "w") as f:
        json.dump(new_stats, f, indent=4)

    # 검증: 중복 프레임 잔존 여부
    print("\n[검증] 중복 프레임 잔존 확인...")
    remaining = 0
    for ep_idx in df_new['episode_index'].unique():
        ep = df_new[df_new['episode_index'] == ep_idx]
        s = np.stack(ep['observation.state'].values)
        d = np.diff(s, axis=0)
        remaining += np.all(d == 0, axis=1).sum()
    total_pairs = len(df_new) - df_new['episode_index'].nunique()
    print(f"    잔존 중복 프레임 쌍: {remaining} / {total_pairs} ({100*remaining/total_pairs:.2f}%)")
    if remaining == 0:
        print("    → 중복 프레임 완전 제거됨")
    else:
        print("    → 일부 잔존 (에피소드 끝 직전 중복은 keyframe 없어서 보간 불가)")

    print(f"\n완료: {DST}")


if __name__ == "__main__":
    main()
