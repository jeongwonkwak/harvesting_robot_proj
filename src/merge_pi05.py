import argparse
import os
import shutil
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

ADAPTER_PATH = Path("/models/ours/pi05_sft_v.0.7.0/checkpoints/009700/pretrained_model")
BASE_PATH    = Path("/models/public/pi05_base")
OUTPUT_PATH  = Path("/models/ours/pi05_sft_v.0.7.0/merged/10ep")

import torch
from peft import PeftModel
from lerobot.policies.pi05.modeling_pi05 import PI05Policy


def merge(adapter_path: str, base_path: str, output_path: str):
    adapter_path = Path(adapter_path)
    base_path = Path(base_path)
    output_path = Path(output_path)

    print(f"Loading base model from {base_path}")
    base_model = PI05Policy.from_pretrained(str(base_path), torch_dtype=torch.bfloat16)

    print(f"Loading LoRA adapter from {adapter_path}")
    model = PeftModel.from_pretrained(base_model, str(adapter_path))

    print("Merging LoRA weights into base model")
    model = model.merge_and_unload()

    print(f"Saving merged model to {output_path}")
    output_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(output_path))

    # copy tokenizer and processor files from base
    for fname in ["tokenizer.json", "tokenizer.model", "tokenizer_config.json",
                  "special_tokens_map.json"]:
        src = base_path / fname
        if src.exists():
            shutil.copy(src, output_path / fname)

    # copy preprocessor/postprocessor from adapter (has fine-tuned normalizer stats)
    for fname in ["policy_preprocessor.json", "policy_postprocessor.json",
                  "policy_preprocessor_step_2_normalizer_processor.safetensors",
                  "policy_postprocessor_step_0_unnormalizer_processor.safetensors"]:
        src = adapter_path / fname
        if src.exists():
            shutil.copy(src, output_path / fname)

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", default=ADAPTER_PATH)
    parser.add_argument("--base", default=BASE_PATH)
    parser.add_argument("--output", default=OUTPUT_PATH)
    args = parser.parse_args()

    merge(args.adapter, args.base, args.output)
