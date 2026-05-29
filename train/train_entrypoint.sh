#!/bin/bash
set -e

# HuggingFace login (HF_TOKEN 환경변수가 있을 때만)
if [ -n "${HF_TOKEN}" ]; then
    echo "[INFO] Logging into HuggingFace Hub..."
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential
fi

# WandB login (WANDB_API_KEY 환경변수가 있을 때만)
if [ -n "${WANDB_API_KEY}" ]; then
    echo "[INFO] Logging into WandB..."
    wandb login "${WANDB_API_KEY}"
fi

exec "$@"
