"""
mid/vla_dataset_v0.2.0 → fin/vla_dataset_v0.2.0 복사 후 quantile stats 추가

호스트 또는 vla-train 컨테이너 안에서 모두 실행 가능:
    python3 /home/user/workspace/jeongwon_lab/src/prepare_fin_dataset.py

- 복사: 호스트에서 직접 수행 (컨테이너 안에서는 /data/vla 마운트 경로 기준)
- Quantile stats:
    - 호스트: 실행 중인 vla-train 컨테이너에 docker exec으로 위임
    - 컨테이너 안: Python 코드를 직접 실행
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# LeRobot 로컬 경로 추가 (import 전에 실행)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lerobot/src"))

from lerobot.scripts.augment_dataset_quantile_stats import compute_quantile_stats_for_dataset, has_quantile_stats
from lerobot.datasets import LeRobotDataset, write_stats

WORKSPACE   = Path(__file__).resolve().parent.parent
DEFAULT_SRC = WORKSPACE / "data/mid/vla_dataset_v0.4.2"
DEFAULT_DST = WORKSPACE / "data/fin/vla_dataset_v0.4.2"
CONTAINER   = "vla-train"
REPO_ID     = "vla_dataset_v0.4.2"

# 호스트 data/ → 컨테이너 /data/vla/ 마운트 기준
HOST_DATA_VLA = WORKSPACE / "data"
CONTAINER_DATA_VLA = "/data/vla"


def container_path(host_path: Path) -> str:
    rel = host_path.relative_to(HOST_DATA_VLA)
    return f"{CONTAINER_DATA_VLA}/{rel}"


def copy_dataset(src: Path, dst: Path) -> None:
    if dst.exists():
        print(f"[skip] 이미 존재: {dst}")
        return
    print(f"[1/2] 복사 중: {src} → {dst}")
    shutil.copytree(src, dst)
    print(f"      완료 ({sum(1 for _ in dst.rglob('*'))} 항목)")


def _run_quantile_stats_inline(dst_path: str, repo_id: str = REPO_ID) -> None:
    import logging
    logging.basicConfig(level=logging.WARNING)

    dataset = LeRobotDataset(repo_id=repo_id, root=dst_path)

    if has_quantile_stats(dataset.meta.stats):
        print("이미 quantile stats가 존재합니다. 건너뜁니다.")
    else:
        new_stats = compute_quantile_stats_for_dataset(dataset)
        dataset.meta.stats = new_stats
        write_stats(new_stats, dataset.meta.root)
        print("stats.json 업데이트 완료")


def add_quantile_stats(dst: Path) -> None:
    print("[2/2] Quantile stats 계산 중...")
    # repo_id는 dst 폴더명에서 유도 (예: vla_dataset_v0.4.3)
    _run_quantile_stats_inline(str(dst), repo_id=dst.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--dst", type=Path, default=DEFAULT_DST)
    args = parser.parse_args()

    if not args.src.exists():
        print(f"오류: src 경로가 없습니다: {args.src}")
        sys.exit(1)

    copy_dataset(args.src, args.dst)
    add_quantile_stats(args.dst)
    print(f"\n완료: {args.dst}")


if __name__ == "__main__":
    main()
