"""
학습 로그 파일을 파싱해서 그래프를 저장합니다.

사용법:
    # 특정 로그 파일 하나
    python3 src/plot_train_log.py logs/pi05_sft_v.0.3.0_20260601_031253.log

    # 여러 로그 비교
    python3 src/plot_train_log.py logs/pi05_sft_v.0.2.0_*.log logs/pi05_sft_v.0.3.0_*.log

    # logs/ 디렉토리 전체
    python3 src/plot_train_log.py --all
"""

import argparse
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

WORKSPACE = Path(__file__).resolve().parent.parent

# ── 경로 설정 ──────────────────────────────────────────────────
LOG_DIR = WORKSPACE / "logs"
OUT_DIR = LOG_DIR / "plots"

# 그릴 로그 파일 지정 (None이면 LOG_DIR 전체 최신 1개, 리스트로 여러 개 비교 가능)
TARGET_LOGS = [
    LOG_DIR / "pi05_sft_v.0.3.0_20260601_031253.log",
]
# ──────────────────────────────────────────────────────────────

PATTERN = re.compile(
    r"step:(\d+\.?\d*[KMG]?).*?epch:([0-9.]+).*?loss:([0-9.]+).*?grdn:([0-9.]+).*?lr:([0-9.e+\-]+)"
    r".*?updt_s:([0-9.]+).*?data_s:([0-9.]+)"
)

def parse_num(s: str) -> float:
    s = s.strip()
    if s.endswith("K"):
        return float(s[:-1]) * 1_000
    if s.endswith("M"):
        return float(s[:-1]) * 1_000_000
    if s.endswith("G"):
        return float(s[:-1]) * 1_000_000_000
    return float(s)


def parse_log(path: Path) -> dict:
    rows = {"step": [], "epch": [], "loss": [], "grdn": [], "lr": [], "updt_s": [], "data_s": []}
    for line in path.read_text().splitlines():
        m = PATTERN.search(line)
        if not m:
            continue
        rows["step"].append(int(parse_num(m.group(1))))
        rows["epch"].append(float(m.group(2)))
        rows["loss"].append(float(m.group(3)))
        rows["grdn"].append(float(m.group(4)))
        rows["lr"].append(float(m.group(5)))
        rows["updt_s"].append(float(m.group(6)))
        rows["data_s"].append(float(m.group(7)))
    return {k: np.array(v) for k, v in rows.items()}


def smooth(x, w=5):
    if len(x) < w:
        return x
    kernel = np.ones(w) / w
    return np.convolve(x, kernel, mode="valid")


def plot(datasets: dict[str, dict], out_path: Path):
    metrics = [
        ("loss",   "Loss",              True),
        ("grdn",   "Gradient Norm",     False),
        ("lr",     "Learning Rate",     False),
        ("updt_s", "Update Time (s)",   False),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Training Curves", fontsize=14, fontweight="bold")
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    for ax, (key, title, do_smooth) in zip(axes.flat, metrics):
        for i, (label, data) in enumerate(datasets.items()):
            if len(data["step"]) == 0:
                continue
            x = data["step"]
            y = data[key]
            color = colors[i % len(colors)]

            if do_smooth and len(y) >= 5:
                w = max(3, len(y) // 10)
                ax.plot(x, y, alpha=0.25, color=color, linewidth=0.8, label=f"{label} (raw)")
                ax.plot(x[w - 1:], smooth(y, w), color=color, linewidth=1.8, label=f"{label} (smoothed)")
            else:
                ax.plot(x, y, color=color, linewidth=1.8, label=label)

        ax.set_title(title)
        ax.set_xlabel("Step")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v)}"))
        ax.grid(True, alpha=0.3)
        if len(datasets) > 1:
            ax.legend(fontsize=8)

    # loss 단독 큰 그래프 (하단 두 칸 합치기 대신 범례 추가)
    axes[1][1].set_visible(False)
    ax_loss = fig.add_subplot(2, 2, 4)
    for i, (label, data) in enumerate(datasets.items()):
        if len(data["step"]) == 0:
            continue
        color = colors[i % len(colors)]
        x, y = data["step"], data["loss"]
        if len(y) >= 5:
            w = max(3, len(y) // 10)
            ax_loss.plot(x, y, alpha=0.25, color=color, linewidth=0.8, label=f"{label} (raw)")
            ax_loss.plot(x[w - 1:], smooth(y, w), color=color, linewidth=1.8, label=f"{label} (smoothed)")
        else:
            ax_loss.plot(x, y, color=color, linewidth=1.8, label=label)
    ax_loss.set_title("Loss (log scale)")
    ax_loss.set_xlabel("Step")
    ax_loss.set_yscale("log")
    ax_loss.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v)}"))
    ax_loss.grid(True, which="both", alpha=0.3)
    if len(datasets) > 1:
        ax_loss.legend(fontsize=8)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"저장: {out_path}")


def summary(label: str, data: dict):
    if len(data["loss"]) == 0:
        print(f"[{label}] 데이터 없음")
        return
    loss = data["loss"]
    print(f"[{label}]  steps={len(loss)}  "
          f"loss 초반={loss[:3].mean():.3f}  "
          f"loss 후반={loss[-3:].mean():.3f}  "
          f"min={loss.min():.3f}  max={loss.max():.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="*", help="로그 파일 경로")
    parser.add_argument("--all", action="store_true", help="LOG_DIR 디렉토리 전체")
    parser.add_argument("--out", type=Path, default=None, help="저장 경로 (기본: OUT_DIR)")
    args = parser.parse_args()

    if args.all:
        paths = sorted(LOG_DIR.glob("*.log"))
    elif args.logs:
        paths = [Path(p) for p in args.logs]
    elif TARGET_LOGS:
        paths = [Path(p) for p in TARGET_LOGS]
    else:
        paths = sorted(LOG_DIR.glob("*.log"))[-1:]

    if not paths:
        print("로그 파일을 찾을 수 없습니다.")
        sys.exit(1)

    datasets = {}
    for p in paths:
        data = parse_log(p)
        label = p.stem
        datasets[label] = data
        summary(label, data)

    stem = "__vs__".join(p.stem for p in paths) if len(paths) <= 3 else f"{len(paths)}_runs"
    out_path = args.out or OUT_DIR / f"{stem}.png"
    plot(datasets, out_path)


if __name__ == "__main__":
    main()
