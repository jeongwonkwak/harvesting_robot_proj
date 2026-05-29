#!/bin/bash
# SmolVLA 학습 범용 스크립트
# 사용법: ./train.sh <config.yaml>
# 예시:   ./train.sh /workspace/scripts/smolvla_sft_v.0.1.0.yaml

set -eo pipefail

DEFAULT_CONFIG="/workspace/scripts/vla_sft_v.0.2.0.yaml"
CONFIG="${1:-$DEFAULT_CONFIG}"

# ── YAML 파싱 ─────────────────────────────────────────────────
yaml() { python3 -c "import yaml; v=yaml.safe_load(open('${CONFIG}'))['$1']; print(str(v).lower() if isinstance(v, bool) else v)"; }

DATASET_REPO_ID=$(yaml dataset_repo_id)
JOB_NAME=$(yaml job_name)
N_EPOCHS=$(yaml n_epochs)
BATCH_SIZE=$(yaml batch_size)
SAVE_FREQ=$(yaml save_freq)
LOG_FREQ=$(yaml log_freq)
SEED=$(yaml seed)
NUM_WORKERS=$(yaml num_workers)
LR=$(yaml lr)
WEIGHT_DECAY=$(yaml weight_decay)
GRAD_CLIP_NORM=$(yaml grad_clip_norm)
WARMUP_STEPS=$(yaml warmup_steps)
DECAY_LR=$(yaml decay_lr)
FREEZE_VISION=$(yaml freeze_vision_encoder)
GRADIENT_CHECKPOINTING=$(yaml gradient_checkpointing)
CHUNK_SIZE=$(yaml chunk_size)
BASE_MODEL_PATH=$(yaml base_model_path)
PEFT_R=$(python3 -c "import yaml; v=yaml.safe_load(open('${CONFIG}')); print(v.get('peft', {}).get('r', '') if v.get('peft') else '')")
VLM_MODEL_NAME=$(python3 -c "import yaml; v=yaml.safe_load(open('${CONFIG}')); print(v.get('vlm_model_name') or '')")
RENAME_MAP=$(python3 -c "import yaml; v=yaml.safe_load(open('${CONFIG}')); print(v.get('rename_map') or '')")

OUTPUT_DIR="/models/ours/${JOB_NAME}"

# ── 에폭 → 스텝 변환 ─────────────────────────────────────────
TOTAL_FRAMES=$(python3 -c "import json; print(json.load(open('${DATASET_REPO_ID}/meta/info.json'))['total_frames'])")
STEPS=$(( (TOTAL_FRAMES + BATCH_SIZE - 1) / BATCH_SIZE * N_EPOCHS ))

# ── 로그 설정 ────────────────────────────────────────────────
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/logs/${JOB_NAME}_${TIMESTAMP}.log"
mkdir -p "${OUTPUT_DIR}" /logs

echo "[${TIMESTAMP}] config=${CONFIG} epochs=${N_EPOCHS} steps=${STEPS} batch=${BATCH_SIZE} lr=${LR}" | tee "${LOG_FILE}"

# ── 실행 ─────────────────────────────────────────────────────
lerobot-train \
    --policy.path="${BASE_MODEL_PATH}" \
    ${VLM_MODEL_NAME:+--policy.vlm_model_name="${VLM_MODEL_NAME}"} \
    ${RENAME_MAP:+--rename_map="${RENAME_MAP}"} \
    --dataset.repo_id="${DATASET_REPO_ID}" \
    --steps="${STEPS}" \
    --batch_size="${BATCH_SIZE}" \
    --save_freq="${SAVE_FREQ}" \
    --log_freq="${LOG_FREQ}" \
    --seed="${SEED}" \
    --num_workers="${NUM_WORKERS}" \
    --policy.optimizer_lr="${LR}" \
    --policy.optimizer_weight_decay="${WEIGHT_DECAY}" \
    --policy.optimizer_grad_clip_norm="${GRAD_CLIP_NORM}" \
    --policy.scheduler_warmup_steps="${WARMUP_STEPS}" \
    --policy.scheduler_decay_lr="${DECAY_LR}" \
    --policy.freeze_vision_encoder="${FREEZE_VISION}" \
    --policy.gradient_checkpointing="${GRADIENT_CHECKPOINTING}" \
    ${PEFT_R:+--peft.r="${PEFT_R}"} \
    --policy.chunk_size="${CHUNK_SIZE}" \
    --policy.device=cuda \
    --dataset.use_imagenet_stats=false \
    --policy.push_to_hub=false \
    --output_dir="${OUTPUT_DIR}" \
    --job_name="${JOB_NAME}" \
    --wandb.enable=false \
    "${@:2}" 2>&1 | tee -a "${LOG_FILE}"
