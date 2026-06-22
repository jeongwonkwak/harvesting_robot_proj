"""
π₀.₅ (Pi05) serving server using FastAPI (LeRobot-based).

Accepts robot state (32-dim), three camera images (base64 JPEG/PNG),
and a language instruction. Returns a 32-dim continuous action.
"""

import base64
import io
import logging
import os
import sys
import time
from contextlib import asynccontextmanager
from typing import List, Optional

# lerobot's import chain (factory → xvla → florence2) unconditionally imports
# flash_attn even though PI05Policy never uses it. The pre-built wheel is
# ABI-incompatible with PyTorch 2.10+cu128 in the nvcr base image.
# transformers also calls importlib.util.find_spec("flash_attn"), which
# requires __spec__ to be a real ModuleSpec — a plain MagicMock won't work.
# The stub below satisfies both callers without loading the broken .so.
try:
    import flash_attn  # noqa: F401
except (ImportError, OSError):
    import importlib.abc
    import importlib.machinery
    import types
    from unittest.mock import MagicMock

    # flash_attn's .so is ABI-incompatible with PyTorch 2.10+cu128.
    # PI05Policy never calls flash_attn at runtime; this finder stubs out
    # flash_attn and every flash_attn.* submodule so the import chain
    # (lerobot xvla/florence2, transformers) completes without errors.
    class _FAStub(types.ModuleType):
        __version__ = "0.0.0"   # keeps transformers' is_flash_attn_2_available() → False

        def __getattr__(self, name):
            obj = MagicMock()
            setattr(self, name, obj)
            return obj

    class _FALoader(importlib.abc.Loader):
        def create_module(self, spec):
            mod = _FAStub(spec.name)
            mod.__spec__ = spec
            return mod

        def exec_module(self, module):
            pass

    class _FAFinder(importlib.abc.MetaPathFinder):
        _loader = _FALoader()

        def find_spec(self, fullname, path, target=None):
            if fullname == "flash_attn" or fullname.startswith("flash_attn."):
                return importlib.machinery.ModuleSpec(
                    fullname, self._loader, is_package=True
                )

    sys.meta_path.insert(0, _FAFinder())

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from PIL import Image, ImageOps
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/vla-model")
MODEL_HOST_PATH = os.environ.get("MODEL_HOST_PATH", "")
STATS_PATH = os.environ.get("STATS_PATH", MODEL_PATH)
DEVICE = os.environ.get("DEVICE", "cuda:0")
CONVERT_ABS_TO_DELTA = os.environ.get("CONVERT_ABS_TO_DELTA", "false").lower() == "true"

policy = None
tokenizer = None
tokenizer_max_length = 200
IMAGE_SIZE = (224, 224)

# QUANTILES normalization stats for observation.state, loaded from the
# trained checkpoint's normalizer safetensors. The training pipeline applies
# QUANTILES (mapping [q01, q99] → [-1, 1]) to state before discretization;
# we must replicate that here for the prompt to match the training distribution.
state_q01: Optional[np.ndarray] = None
state_q99: Optional[np.ndarray] = None
N_STATE_REAL = 0   # actual state dim from training stats (e.g., 7 for v0.4.x)

# QUANTILES stats for action. The model outputs normalized actions in [-1, 1];
# inverse QUANTILES maps them back to the original units (m, rad, etc.).
action_q01: Optional[np.ndarray] = None
action_q99: Optional[np.ndarray] = None


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
    global state_q01, state_q99, N_STATE_REAL, action_q01, action_q99
    logger.info(f"Loading Pi05 from {MODEL_PATH} on {DEVICE} ...")
    t0 = time.time()

    from lerobot.policies.pi05 import PI05Policy

    if DEVICE.startswith("cuda"):
        torch.zeros(1, device=DEVICE)

    policy = PI05Policy.from_pretrained(MODEL_PATH)
    policy.to(DEVICE)
    policy.eval()
    policy.reset()

    tokenizer = _get_tokenizer(policy)
    if tokenizer is None:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    tokenizer_max_length = getattr(policy.config, "tokenizer_max_length", 200)
    logger.info(f"Tokenizer ready (max_length={tokenizer_max_length})")

    stats_path = os.path.join(
        STATS_PATH, "policy_preprocessor_step_2_normalizer_processor.safetensors"
    )
    from safetensors.torch import load_file
    if os.path.exists(stats_path):
        stats = load_file(stats_path)
        state_q01 = stats["observation.state.q01"].cpu().numpy().astype(np.float32)
        state_q99 = stats["observation.state.q99"].cpu().numpy().astype(np.float32)
        N_STATE_REAL = int(state_q01.shape[0])
        action_q01 = stats["action.q01"].cpu().numpy().astype(np.float32)
        action_q99 = stats["action.q99"].cpu().numpy().astype(np.float32)
        logger.info(
            f"Loaded state QUANTILES stats: N={N_STATE_REAL} "
            f"q01_range=[{state_q01.min():.4f},{state_q01.max():.4f}] "
            f"q99_range=[{state_q99.min():.4f},{state_q99.max():.4f}]"
        )
        logger.info(
            f"Loaded action QUANTILES stats: N={action_q01.shape[0]} "
            f"q01_range=[{action_q01.min():.4f},{action_q01.max():.4f}] "
            f"q99_range=[{action_q99.min():.4f},{action_q99.max():.4f}]"
        )
    else:
        logger.warning(
            f"Stats file not found at {stats_path}. "
            "Running without normalization (identity): state clipped to [-1,1], action returned as-is."
        )
    logger.info(f"Pi05 ready in {time.time() - t0:.1f}s")
    yield
    del policy, tokenizer


app = FastAPI(title="Pi05 Server", lifespan=lifespan)


class PredictRequest(BaseModel):
    # Raw state in original units (m for translations, rad for rotations, etc.),
    # padded to 32 dims for backward compat. Only the first N_STATE_REAL dims
    # (e.g., 7 for v0.4.x) are used; the rest are ignored. The server applies
    # QUANTILES normalization internally — do NOT pre-normalize on the client.
    state: List[float]
    base_image: str                           # base64 JPEG/PNG — base camera
    left_wrist_image: Optional[str] = None   # base64 JPEG/PNG — left wrist camera
    right_wrist_image: Optional[str] = None  # base64 JPEG/PNG — right wrist camera
    instruction: str
    reset_episode: bool = False


class PredictResponse(BaseModel):
    # Continuous action sliced to the original dataset dim (e.g., 7 for v0.4.x)
    # — see policy.config.output_features[ACTION].shape[0].
    action: List[float]
    raw_action: List[float]   # normalized action in [-1, 1] before inverse MIN_MAX
    latency_ms: float


def _decode_image(b64: str, size: tuple = IMAGE_SIZE) -> torch.Tensor:
    # Match training-time resize_with_pad_torch: aspect-ratio-preserving resize
    # followed by symmetric black padding to `size`. Otherwise a 640x480 frame
    # gets squashed to 224x224 at inference while training saw letterboxed input.
    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
    img = ImageOps.pad(img, size, method=Image.BILINEAR, color=(0, 0, 0), centering=(0.5, 0.5))
    return torch.from_numpy(np.array(img, dtype=np.float32)).permute(2, 0, 1) / 255.0


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": policy is not None}


@app.get("/info")
def info():
    chunk_size = getattr(policy.config, "chunk_size", 50) if policy else 50
    action_dim = (
        policy.config.output_features["action"].shape[0] if policy else N_STATE_REAL
    )
    return {
        "model": MODEL_PATH,
        "model_host_path": MODEL_HOST_PATH,
        "device": DEVICE,
        "action_dims": action_dim,
        "state_dims": N_STATE_REAL,
        "cameras": ["base_image", "left_wrist_image", "right_wrist_image"],
        "chunk_size": chunk_size,
        "description": f"{action_dim}-dim action via π₀.₅ flow-matching VLA",
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

    if len(req.state) != 32:
        raise HTTPException(
            status_code=400,
            detail=f"state must be 32-dim, got {len(req.state)}",
        )

    if req.reset_episode:
        policy.reset()

    try:
        base_img = _decode_image(req.base_image)
        left_img = _decode_image(req.left_wrist_image) if req.left_wrist_image else None
        right_img = _decode_image(req.right_wrist_image) if req.right_wrist_image else None

        # PI05 embeds state inside the language prompt (not as a separate tensor).
        # Apply QUANTILES normalization (matches NormalizerProcessorStep during
        # training): map [q01, q99] → [-1, 1] for the first N_STATE_REAL dims,
        # then discretize into 256 bins. Padding dims (N_STATE_REAL..) are
        # dropped because the training prompt only contained the real state dims.
        n_state = N_STATE_REAL if N_STATE_REAL > 0 else len(req.state)
        raw = np.array(req.state[:n_state], dtype=np.float32)
        if state_q01 is not None and state_q99 is not None:
            denom = (state_q99 - state_q01)
            denom = np.where(denom == 0, 1e-8, denom)
            normalized = 2.0 * (raw - state_q01) / denom - 1.0
        else:
            # No stats: treat input as already in [-1, 1]
            normalized = raw
        normalized = np.clip(normalized, -1.0, 1.0)
        bins = np.linspace(-1.0, 1.0, 257)[:-1]   # 256 left edges
        discretized = np.clip(np.digitize(normalized, bins) - 1, 0, 255)
        state_str = " ".join(map(str, discretized))

        instruction = req.instruction.strip().replace("_", " ").replace("\n", " ")
        prompt = f"Task: {instruction}, State: {state_str};\nAction: "

        lang = tokenizer(
            prompt,
            max_length=tokenizer_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")

    obs = {
        "observation.images.base_0_rgb": base_img.unsqueeze(0).to(DEVICE),
        "observation.language.tokens": lang["input_ids"].to(DEVICE),
        "observation.language.attention_mask": lang["attention_mask"].bool().to(DEVICE),
    }
    if left_img is not None:
        obs["observation.images.left_wrist_0_rgb"] = left_img.unsqueeze(0).to(DEVICE)
    if right_img is not None:
        obs["observation.images.right_wrist_0_rgb"] = right_img.unsqueeze(0).to(DEVICE)

    t0 = time.time()
    with torch.inference_mode():
        action = policy.select_action(obs)
    latency_ms = (time.time() - t0) * 1000

    if isinstance(action, torch.Tensor):
        action = action.cpu().float().numpy()
    action = np.array(action, dtype=np.float32).flatten()

    # Inverse QUANTILES: model outputs normalized action in [-1, 1];
    # map back to original units (m, rad) using training stats.
    # raw = (norm + 1) * (q99 - q01) / 2 + q01
    raw_action = action.copy()
    if action_q01 is not None and action_q99 is not None:
        n = min(action.shape[0], action_q01.shape[0])
        action[:n] = (action[:n] + 1.0) * (action_q99[:n] - action_q01[:n]) / 2.0 + action_q01[:n]

    # CONVERT_ABS_TO_DELTA: 베이스 모델용. action[:6](모델이 예측한 절대 EEF 좌표) -
    # req.state[:6](클라이언트가 보낸 현재 EEF pose, m/rad) = delta. 클라이언트가
    # state에 EEF pose(m/rad)를 담아야 정확함. joint positions를 보내면 틀린 delta 나옴.
    if CONVERT_ABS_TO_DELTA:
        eef = np.array(req.state[:6], dtype=np.float32)
        action[:6] = action[:6] - eef

    return PredictResponse(action=action.tolist(), raw_action=raw_action.tolist(), latency_ms=round(latency_ms, 2))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8002)))
