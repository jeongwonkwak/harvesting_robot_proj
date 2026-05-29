"""
pi05 LoRA 체크포인트 + pi05_base를 하나의 self-contained 모델로 변환합니다.

병합 과정:
  1. pi05_base의 모든 파일을 output에 복사
  2. LoRA 가중치(adapter_model.safetensors)를 base model.safetensors에 적용 (docker exec)
  3. 체크포인트의 policy_preprocessor / policy_postprocessor로 교체

사용법:
    python3 src/merge_pi05.py                  # 기본 경로 (최신 체크포인트 자동 탐색)
    python3 src/merge_pi05.py \\
        --checkpoint models/ours/pi05_sft_v.0.2.0/checkpoints/001840/pretrained_model \\
        --base       models/public/pi05_base \\
        --output     models/ours/pi05_sft_v.0.2.0/checkpoints/last/merged
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

WORKSPACE  = Path(__file__).resolve().parent.parent
CONTAINER  = "vla-train"

HOST_MODELS_OURS   = WORKSPACE / "models/ours"
HOST_MODELS_PUBLIC = WORKSPACE / "models/public"
CONT_MODELS_OURS   = "/models/ours"
CONT_MODELS_PUBLIC = "/models/public"

DEFAULT_MODEL_DIR  = HOST_MODELS_OURS / "pi05_sft_v.0.2.0"
DEFAULT_BASE       = HOST_MODELS_PUBLIC / "pi05_base"
DEFAULT_OUTPUT     = DEFAULT_MODEL_DIR / "checkpoints/last/merged"


def to_container_path(host_path: Path) -> str:
    try:
        rel = host_path.relative_to(HOST_MODELS_OURS)
        return f"{CONT_MODELS_OURS}/{rel}"
    except ValueError:
        pass
    try:
        rel = host_path.relative_to(HOST_MODELS_PUBLIC)
        return f"{CONT_MODELS_PUBLIC}/{rel}"
    except ValueError:
        raise ValueError(f"경로가 마운트 범위 밖입니다: {host_path}")


def find_latest_checkpoint(model_dir: Path) -> Path:
    ckpt_dirs = sorted(
        [d / "pretrained_model" for d in (model_dir / "checkpoints").iterdir()
         if d.is_dir() and d.name.isdigit() and (d / "pretrained_model").exists()],
        key=lambda p: int(p.parent.name),
    )
    if not ckpt_dirs:
        raise FileNotFoundError(f"체크포인트를 찾을 수 없습니다: {model_dir / 'checkpoints'}")
    latest = ckpt_dirs[-1]
    print(f"[자동 탐색] 최신 체크포인트: {latest}")
    return latest


def copy_base(base: Path, output: Path) -> None:
    if output.exists():
        print(f"[skip] output 이미 존재: {output}  (삭제 후 재실행하려면 직접 제거하세요)")
        return
    print(f"[1/3] base 복사: {base} → {output}")
    shutil.copytree(base, output)
    print(f"      완료 ({sum(1 for _ in output.rglob('*'))} 항목)")


def copy_policy_files(checkpoint: Path, output: Path) -> None:
    print(f"[2/3] policy_preprocessor / policy_postprocessor 교체")
    for pattern in [
        "policy_preprocessor.json",
        "policy_preprocessor_*.safetensors",
        "policy_postprocessor.json",
        "policy_postprocessor_*.safetensors",
    ]:
        for src in checkpoint.glob(pattern):
            dst = output / src.name
            shutil.copy2(src, dst)
            print(f"      {src.name}")


def merge_lora_weights(checkpoint: Path, output: Path) -> None:
    print(f"[3/3] LoRA 가중치 병합 (vla-train 컨테이너)...")

    adapter_path = to_container_path(checkpoint / "adapter_model.safetensors")
    adapter_cfg  = to_container_path(checkpoint / "adapter_config.json")
    base_weights = to_container_path(output / "model.safetensors")
    out_weights  = base_weights  # in-place 덮어쓰기

    python_code = f"""
import json, torch
from safetensors.torch import load_file, save_file
from pathlib import Path

adapter_cfg = json.loads(Path("{adapter_cfg}").read_text())
r           = adapter_cfg["r"]
lora_alpha  = adapter_cfg["lora_alpha"]
scale       = lora_alpha / r
print(f"  LoRA scale: {{lora_alpha}}/{{r}} = {{scale:.4f}}")

print("  base 가중치 로드 중...")
base    = load_file("{base_weights}", device="cpu")
print("  adapter 가중치 로드 중...")
adapter = load_file("{adapter_path}", device="cpu")

merged = dict(base)
applied = 0
for key, val in adapter.items():
    if ".lora_A." not in key:
        continue
    lora_B_key = key.replace(".lora_A.", ".lora_B.")
    if lora_B_key not in adapter:
        continue
    # base_model.model.<original_key>.lora_A.default.weight
    base_key = key
    base_key = base_key.replace("base_model.model.", "", 1)
    base_key = base_key.replace(".lora_A.default.weight", ".weight")
    if base_key not in merged:
        print(f"  [warn] base key not found: {{base_key}}")
        continue
    lora_A = adapter[key].float()
    lora_B = adapter[lora_B_key].float()
    delta  = (lora_B @ lora_A) * scale
    merged[base_key] = (merged[base_key].float() + delta).to(base[base_key].dtype)
    applied += 1

print(f"  적용된 LoRA 레이어: {{applied}}개")
print("  병합 가중치 저장 중...")
save_file(merged, "{out_weights}")
print("  완료")
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
    parser.add_argument("--checkpoint", type=Path, default=None,
                        help="pretrained_model 디렉토리 경로 (기본: 최신 체크포인트 자동 탐색)")
    parser.add_argument("--base",       type=Path, default=DEFAULT_BASE)
    parser.add_argument("--output",     type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    checkpoint = args.checkpoint or find_latest_checkpoint(DEFAULT_MODEL_DIR)

    print(f"checkpoint : {checkpoint}")
    print(f"base       : {args.base}")
    print(f"output     : {args.output}")
    print()

    if not checkpoint.exists():
        print(f"오류: checkpoint 경로가 없습니다: {checkpoint}")
        sys.exit(1)
    if not args.base.exists():
        print(f"오류: base 경로가 없습니다: {args.base}")
        sys.exit(1)

    copy_base(args.base, args.output)
    copy_policy_files(checkpoint, args.output)
    merge_lora_weights(checkpoint, args.output)

    total_size = sum(f.stat().st_size for f in args.output.rglob("*") if f.is_file())
    print(f"\n완료: {args.output}")
    print(f"총 크기: {total_size / 1e9:.2f} GB")


if __name__ == "__main__":
    main()
