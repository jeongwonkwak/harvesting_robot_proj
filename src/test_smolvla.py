#!/usr/bin/env python3
"""
SmolVLA 서버 간단 테스트 스크립트.

사용법:
  python3 test_smolvla.py                          # 더미 이미지 + 기본 state
  python3 test_smolvla.py --image /path/to/img.jpg # 실제 이미지
  python3 test_smolvla.py --url http://192.168.50.79:16003
  python3 test_smolvla.py --instruction "grasp the object"
"""

import argparse
import base64
import io
import json
import sys
from pathlib import Path

import numpy as np
import requests
from PIL import Image

# ── 기본값 ──────────────────────────────────────────────────────────────────
DEFAULT_URL         = "http://192.168.50.79:16003"
DEFAULT_INSTRUCTION = "pick up the object"
STATS_PATH          = Path("/home/user/robot_workspace/vla_ws/data/mid/smolvla_dataset_v1.1.0/meta/stats.json")

# 두산 e0509 홈 자세 (라디안)  — state 더미값으로 사용
HOME_STATE_RAD = np.array([0.0, 0.0, 1.5708, 0.0, 1.5708, 0.0, 0.0], dtype=np.float32)


# ── 유틸 ──────────────────────────────────────────────────────────────────────
def encode_image(img: np.ndarray, size=(256, 256)) -> str:
    pil = Image.fromarray(img.astype(np.uint8)).resize(size)
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


def load_image(path: str | None) -> np.ndarray:
    if path:
        img = np.array(Image.open(path).convert("RGB"))
        print(f"[이미지] {path}  shape={img.shape}")
        return img
    # 더미: 랜덤 RGB 480×640
    img = np.random.randint(0, 200, (480, 640, 3), dtype=np.uint8)
    print("[이미지] 더미 랜덤 이미지 사용 (480×640)")
    return img


def load_stats() -> tuple[np.ndarray, np.ndarray] | tuple[None, None]:
    if not STATS_PATH.exists():
        return None, None
    with open(STATS_PATH) as f:
        stats = json.load(f)
    mean = np.array(stats["action"]["mean"], dtype=np.float32)
    std  = np.array(stats["action"]["std"],  dtype=np.float32)
    return mean, std


# ── 메인 ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",         default=DEFAULT_URL)
    parser.add_argument("--image",       default=None,         help="이미지 경로 (없으면 더미)")
    parser.add_argument("--instruction", default=DEFAULT_INSTRUCTION)
    parser.add_argument("--steps",       type=int, default=3,  help="연속 predict 횟수")
    parser.add_argument("--no-reset",    action="store_true",  help="에피소드 reset 생략")
    args = parser.parse_args()

    url = args.url.rstrip("/")

    # 1. Health check
    print(f"\n{'='*55}")
    print(f"  SmolVLA 서버 테스트")
    print(f"  URL: {url}")
    print(f"{'='*55}")

    try:
        r = requests.get(f"{url}/health", timeout=3.0)
        health = r.json()
        loaded = health.get("model_loaded", False)
        status = "OK" if loaded else "모델 미로드"
        print(f"\n[Health] {status}  {health}")
        if not loaded:
            print("  → 서버가 응답하지만 모델이 로드되지 않았습니다.")
            sys.exit(1)
    except Exception as e:
        print(f"\n[Health] 연결 실패: {e}")
        sys.exit(1)

    # 2. 이미지 / state 준비
    img   = load_image(args.image)
    state = HOME_STATE_RAD.copy()
    print(f"[State]  {np.round(state, 4).tolist()}")
    print(f"[Task]   '{args.instruction}'")

    # 3. Stats 로드 (역정규화용)
    act_mean, act_std = load_stats()
    if act_mean is not None:
        print(f"[Stats]  로드됨 ({STATS_PATH.name})")
    else:
        print(f"[Stats]  없음 — 역정규화 생략")

    # 4. Reset
    if not args.no_reset:
        requests.post(f"{url}/reset", timeout=2.0)
        print("\n[Reset]  에피소드 리셋 완료")

    # 5. Predict 루프
    for step in range(1, args.steps + 1):
        payload = {
            "state":         state.tolist(),
            "camera1":       encode_image(img),
            "camera2":       encode_image(img),
            "camera3":       encode_image(img),
            "instruction":   args.instruction,
            "reset_episode": False,
        }

        try:
            resp = requests.post(f"{url}/predict", json=payload, timeout=10.0)
            resp.raise_for_status()
        except Exception as e:
            print(f"\n[Step {step}] 오류: {e}")
            break

        data   = resp.json()
        action = np.array(data["action"], dtype=np.float32)
        latency = data.get("latency_ms", -1)

        print(f"\n[Step {step}]  latency={latency:.1f}ms")
        print(f"  raw action : {np.round(action, 4).tolist()}")

        if act_mean is not None:
            action_dn = action * act_std + act_mean
            joints_deg = np.degrees(action_dn[:6])
            gripper    = float(np.clip(action_dn[6], 0.0, 1.0))
            print(f"  역정규화   : {np.round(action_dn, 4).tolist()}")
            print(f"  관절(deg)  : {np.round(joints_deg, 2).tolist()}")
            print(f"  그리퍼     : {gripper:.3f}  ({'열림' if gripper < 0.3 else '닫힘' if gripper > 0.7 else '중간'})")

    print(f"\n{'='*55}\n")


if __name__ == "__main__":
    main()
