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

WORKSPACE   = Path(__file__).resolve().parent.parent
DEFAULT_SRC = WORKSPACE / "../data/vla/mid/vla_dataset_v0.4.0"
DEFAULT_DST = WORKSPACE / "../data/vla/fin/vla_dataset_v0.4.0"
CONTAINER   = "vla-train"
REPO_ID     = "vla_dataset_v0.4.0"

# 호스트 data/vla/ → 컨테이너 /data/vla/ 마운트 기준
HOST_DATA_VLA = WORKSPACE / "../data/vla"
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


def _run_quantile_stats_inline(dst_path: str) -> None:
    import logging
    logging.basicConfig(level=logging.WARNING)

    from lerobot.scripts.augment_dataset_quantile_stats import (
        compute_quantile_stats_for_dataset,
        has_quantile_stats,
    )
    from lerobot.datasets import LeRobotDataset, write_stats

    dataset = LeRobotDataset(repo_id=REPO_ID, root=dst_path)

    if has_quantile_stats(dataset.meta.stats):
        print("이미 quantile stats가 존재합니다. 건너뜁니다.")
    else:
        new_stats = compute_quantile_stats_for_dataset(dataset)
        dataset.meta.stats = new_stats
        write_stats(new_stats, dataset.meta.root)
        print("stats.json 업데이트 완료")


def add_quantile_stats(dst: Path) -> None:
    in_container = not shutil.which("docker")

    if in_container:
        print("[2/2] Quantile stats 계산 중 (컨테이너 내 직접 실행)...")
        # 컨테이너 안에서는 dst가 이미 컨테이너 경로이므로 그대로 사용
        _run_quantile_stats_inline(str(dst))
    else:
        print("[2/2] Quantile stats 계산 중 (vla-train 컨테이너)...")
        dst_in_container = container_path(dst)

        python_code = f"""
import logging
logging.basicConfig(level=logging.WARNING)

from lerobot.scripts.augment_dataset_quantile_stats import (
    compute_quantile_stats_for_dataset,
    has_quantile_stats,
)
from lerobot.datasets import LeRobotDataset, write_stats

dataset = LeRobotDataset(repo_id="{REPO_ID}", root="{dst_in_container}")

if has_quantile_stats(dataset.meta.stats):
    print("이미 quantile stats가 존재합니다. 건너뜁니다.")
else:
    new_stats = compute_quantile_stats_for_dataset(dataset)
    dataset.meta.stats = new_stats
    write_stats(new_stats, dataset.meta.root)
    print("stats.json 업데이트 완료")
"""

        result = subprocess.run(
            ["docker", "exec", CONTAINER, "python", "-c", python_code],
            text=True,
        )
        if result.returncode != 0:
            print("오류: docker exec 실패")
            sys.exit(1)


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
