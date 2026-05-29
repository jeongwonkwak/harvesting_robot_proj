"""
SmolVLA serving server using FastAPI (LeRobot-based).

Accepts robot state, up to 3 camera images (base64), and a language instruction.
Returns a 7-DoF robot action (6 joints + gripper). Manages action-chunk buffer internally per episode.
"""

import base64
import io
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import List, Optional

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/public/smolvla_base")
MODEL_HOST_PATH = os.environ.get("MODEL_HOST_PATH", "")
DEVICE = os.environ.get("DEVICE", "cuda:0")

policy = None
tokenizer = None
tokenizer_max_length = 48


def _get_tokenizer(p):
    for attr in ("language_tokenizer", "tokenizer", "text_tokenizer"):
        if hasattr(p, attr):
            return getattr(p, attr)
    if hasattr(p, "model"):
        for attr in ("language_tokenizer", "tokenizer"):
            if hasattr(p.model, attr):
                return getattr(p.model, attr)
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global policy, tokenizer, tokenizer_max_length
    logger.info(f"Loading SmolVLA from {MODEL_PATH} on {DEVICE} ...")
    t0 = time.time()

    try:
        from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
    except ImportError:
        try:
            from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
        except ImportError:
            from lerobot.policies.smolvla import SmolVLAPolicy

    try:
        from lerobot.common.policies.smolvla.configuration_smolvla import SmolVLAConfig
    except ImportError:
        from lerobot.policies.smolvla.configuration_smolvla import SmolVLAConfig

    # Force CUDA lazy-init before from_pretrained, which may modify CUDA_VISIBLE_DEVICES internally
    if DEVICE.startswith("cuda"):
        torch.zeros(1, device=DEVICE)

    config = SmolVLAConfig.from_pretrained(MODEL_PATH)
    # vlm_model_name이 상대 경로이고 실제로 존재하면 MODEL_PATH 기준으로 해석
    if not os.path.isabs(config.vlm_model_name):
        candidate = os.path.join(MODEL_PATH, config.vlm_model_name)
        if os.path.isdir(candidate):
            config.vlm_model_name = candidate
    policy = SmolVLAPolicy.from_pretrained(MODEL_PATH, config=config)
    policy.to(DEVICE)
    policy.eval()
    policy.reset()

    tokenizer = _get_tokenizer(policy)
    if tokenizer is None:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(config.vlm_model_name)
    tokenizer_max_length = getattr(policy.config, "tokenizer_max_length", 48)
    logger.info(f"Tokenizer ready (max_length={tokenizer_max_length})")

    logger.info(f"SmolVLA ready in {time.time() - t0:.1f}s")
    yield
    del policy, tokenizer


app = FastAPI(title="SmolVLA Server", lifespan=lifespan)


class PredictRequest(BaseModel):
    state: List[float]           # 7-DoF robot state (6 joints + gripper)
    camera1: str                 # base64 JPEG/PNG (required)
    camera2: Optional[str] = None
    camera3: Optional[str] = None
    instruction: str
    reset_episode: bool = False  # call policy.reset() before this step (new episode)


class PredictResponse(BaseModel):
    action: List[float]          # 7-DoF action (6 joints + gripper)
    latency_ms: float


def _decode_image(b64: str, size: tuple = (256, 256)) -> torch.Tensor:
    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB").resize(size)
    return torch.from_numpy(np.array(img)).permute(2, 0, 1).float() / 255.0


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": policy is not None}


@app.get("/info")
def info():
    return {
        "model": MODEL_PATH,
        "model_host_path": MODEL_HOST_PATH,
        "vlm_backbone": policy.config.vlm_model_name if policy is not None else None,
        "device": DEVICE,
        "action_dims": 7,
        "state_dims": 7,
        "cameras": ["camera1", "camera2", "camera3"],
        "chunk_size": 50,
        "description": "7-DoF action; action chunk managed internally",
    }


@app.post("/reset")
def reset_episode():
    if policy is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    policy.reset()
    return {"status": "reset"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if policy is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if len(req.state) != 7:
        raise HTTPException(status_code=400, detail=f"state must be 7-DoF (6 joints + gripper), got {len(req.state)}")

    if req.reset_episode:
        policy.reset()

    try:
        cam1 = _decode_image(req.camera1)
        cam2 = _decode_image(req.camera2) if req.camera2 else cam1
        cam3 = _decode_image(req.camera3) if req.camera3 else cam1
        lang = tokenizer(
            req.instruction,
            max_length=tokenizer_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")

    obs = {
        "observation.images.camera1": cam1.unsqueeze(0).to(DEVICE),
        "observation.images.camera2": cam2.unsqueeze(0).to(DEVICE),
        "observation.images.camera3": cam3.unsqueeze(0).to(DEVICE),
        "observation.state": torch.tensor(
            req.state, dtype=torch.float32, device=DEVICE
        ).unsqueeze(0),
        "observation.language.tokens": lang["input_ids"].to(DEVICE),
        "observation.language.attention_mask": lang["attention_mask"].to(DEVICE),
    }

    t0 = time.time()
    with torch.inference_mode():
        action = policy.select_action(obs)
    latency_ms = (time.time() - t0) * 1000

    if isinstance(action, torch.Tensor):
        action = action.cpu().float().numpy()
    action_list = np.array(action).flatten().tolist()

    return PredictResponse(action=action_list, latency_ms=round(latency_ms, 2))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
