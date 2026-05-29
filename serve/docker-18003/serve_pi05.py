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
from PIL import Image
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/vla-model")
MODEL_HOST_PATH = os.environ.get("MODEL_HOST_PATH", "")
DEVICE = os.environ.get("DEVICE", "cuda:0")

policy = None
tokenizer = None
tokenizer_max_length = 200
IMAGE_SIZE = (224, 224)


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
    logger.info(f"Pi05 ready in {time.time() - t0:.1f}s")
    yield
    del policy, tokenizer


app = FastAPI(title="Pi05 Server", lifespan=lifespan)


class PredictRequest(BaseModel):
    state: List[float]                        # 32-dim proprioceptive state
    base_image: str                           # base64 JPEG/PNG — base camera
    left_wrist_image: Optional[str] = None   # base64 JPEG/PNG — left wrist camera
    right_wrist_image: Optional[str] = None  # base64 JPEG/PNG — right wrist camera
    instruction: str
    reset_episode: bool = False


class PredictResponse(BaseModel):
    action: List[float]   # 32-dim continuous action
    latency_ms: float


def _decode_image(b64: str, size: tuple = IMAGE_SIZE) -> torch.Tensor:
    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB").resize(size)
    return torch.from_numpy(np.array(img, dtype=np.float32)).permute(2, 0, 1) / 255.0


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": policy is not None}


@app.get("/info")
def info():
    chunk_size = getattr(policy.config, "chunk_size", 50) if policy else 50
    return {
        "model": MODEL_PATH,
        "model_host_path": MODEL_HOST_PATH,
        "device": DEVICE,
        "action_dims": 32,
        "state_dims": 32,
        "cameras": ["base_image", "left_wrist_image", "right_wrist_image"],
        "chunk_size": chunk_size,
        "description": "32-dim action via π₀.₅ flow-matching VLA",
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
        left_img = _decode_image(req.left_wrist_image) if req.left_wrist_image else base_img.clone()
        right_img = _decode_image(req.right_wrist_image) if req.right_wrist_image else base_img.clone()

        # PI05 embeds state inside the language prompt (not as a separate tensor).
        # State must be in [-1, 1]; discretize into 256 bins matching the processor.
        state_np = np.clip(np.array(req.state, dtype=np.float32), -1.0, 1.0)
        bins = np.linspace(-1.0, 1.0, 257)[:-1]   # 256 left edges
        discretized = np.clip(np.digitize(state_np, bins) - 1, 0, 255)
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
        "observation.images.left_wrist_0_rgb": left_img.unsqueeze(0).to(DEVICE),
        "observation.images.right_wrist_0_rgb": right_img.unsqueeze(0).to(DEVICE),
        "observation.language.tokens": lang["input_ids"].to(DEVICE),
        "observation.language.attention_mask": lang["attention_mask"].bool().to(DEVICE),
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
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8002)))
