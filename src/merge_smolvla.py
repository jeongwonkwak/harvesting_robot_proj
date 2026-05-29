"""
SmolVLA 체크포인트 + SmolVLM2 백본을 하나의 self-contained 모델로 변환합니다.

변환된 모델은 backbone/ 서브디렉토리에 백본을 포함하므로
서빙 시 별도의 백본 마운트가 필요 없습니다.

사용법:
    python3 src/merge_smolvla.py                        # 기본 경로 사용
    python3 src/merge_smolvla.py \\
        --checkpoint models/ours/.../pretrained_model \\
        --backbone   models/public/SmolVLM2-500M-Video-Instruct \\
        --output     models/ours/.../merged
"""

import argparse
import json
import shutil
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent

DEFAULT_CHECKPOINT = WORKSPACE / "models/ours/smolvla_sft_v.0.1.0/checkpoints/last/pretrained_model"
DEFAULT_BACKBONE   = WORKSPACE / "models/public/SmolVLM2-500M-Video-Instruct"
DEFAULT_OUTPUT     = WORKSPACE / "models/ours/smolvla_sft_v.0.1.0/merged"


def merge(checkpoint_path: Path, backbone_path: Path, output_path: Path) -> None:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    if not backbone_path.exists():
        raise FileNotFoundError(f"Backbone not found: {backbone_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    print("Copying checkpoint files...")
    for f in checkpoint_path.iterdir():
        if f.is_file():
            shutil.copy2(f, output_path / f.name)

    backbone_dest = output_path / "backbone"
    if backbone_dest.exists():
        shutil.rmtree(backbone_dest)
    backbone_size = sum(f.stat().st_size for f in backbone_path.rglob("*") if f.is_file())
    print(f"Copying backbone ({backbone_size / 1e9:.2f} GB)...")
    shutil.copytree(backbone_path, backbone_dest)

    config_path = output_path / "config.json"
    config = json.loads(config_path.read_text())
    config["vlm_model_name"] = "backbone"
    config_path.write_text(json.dumps(config, indent=2))

    total_size = sum(f.stat().st_size for f in output_path.rglob("*") if f.is_file())
    print(f"Done. Merged model saved to: {output_path}")
    print(f"Total size: {total_size / 1e9:.2f} GB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--backbone",   type=Path, default=DEFAULT_BACKBONE)
    parser.add_argument("--output",     type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    print(f"checkpoint : {args.checkpoint}")
    print(f"backbone   : {args.backbone}")
    print(f"output     : {args.output}")
    merge(args.checkpoint, args.backbone, args.output)
