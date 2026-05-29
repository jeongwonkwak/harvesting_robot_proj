"""
OpenVLA-7B serving server using FastAPI.

Accepts a base64-encoded image and a language instruction,
returns a 7-DoF robot action: (x, y, z, roll, pitch, yaw, gripper).
"""

import base64
import importlib.util
import io
import logging
import os
import sys
import time
import types
from contextlib import asynccontextmanager
from typing import Optional

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel
from transformers import AutoModelForVision2Seq, AutoProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/openvla-7b")
DEVICE = os.environ.get("DEVICE", "cuda:0")

model = None
processor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, processor
    logger.info(f"Loading model from {MODEL_PATH} on {DEVICE} ...")
    t0 = time.time()

    # Build a virtual "vlm" package from the .py files in MODEL_PATH.
    # This avoids sys.path/PYTHONPATH issues and handles relative imports inside modeling_prismatic.
    _pkg = types.ModuleType("vlm")
    _pkg.__path__ = [MODEL_PATH]
    _pkg.__package__ = "vlm"
    sys.modules["vlm"] = _pkg
    for _name in ("configuration_prismatic", "modeling_prismatic", "processing_prismatic"):
        _spec = importlib.util.spec_from_file_location(
            f"vlm.{_name}", f"{MODEL_PATH}/{_name}.py"
        )
        _mod = importlib.util.module_from_spec(_spec)
        _mod.__package__ = "vlm"
        sys.modules[f"vlm.{_name}"] = _mod
    for _name in ("configuration_prismatic", "modeling_prismatic", "processing_prismatic"):
        sys.modules[f"vlm.{_name}"].__spec__.loader.exec_module(sys.modules[f"vlm.{_name}"])

    from vlm.configuration_prismatic import OpenVLAConfig
    from vlm.processing_prismatic import PrismaticProcessor
    from vlm.modeling_prismatic import OpenVLAForActionPrediction
    AutoModelForVision2Seq.register(OpenVLAConfig, OpenVLAForActionPrediction, exist_ok=True)

    processor = PrismaticProcessor.from_pretrained(MODEL_PATH)

    load_kwargs = dict(
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    try:
        load_kwargs["attn_implementation"] = "flash_attention_2"
        model = AutoModelForVision2Seq.from_pretrained(MODEL_PATH, **load_kwargs).to(DEVICE)
        logger.info("Loaded with flash_attention_2")
    except Exception:
        load_kwargs.pop("attn_implementation")
        model = AutoModelForVision2Seq.from_pretrained(MODEL_PATH, **load_kwargs).to(DEVICE)
        logger.info("Loaded with default attention (flash_attn unavailable)")

    model.eval()
    logger.info(f"Model ready in {time.time() - t0:.1f}s")
    yield
    del model, processor


app = FastAPI(title="OpenVLA-7B Server", lifespan=lifespan)


class PredictRequest(BaseModel):
    image: str  # base64-encoded JPEG/PNG
    instruction: str
    unnorm_key: Optional[str] = None  # e.g. "bridge_orig"; None = no un-normalization


class PredictResponse(BaseModel):
    action: list[float]  # 7-DoF: [x, y, z, roll, pitch, yaw, gripper]
    latency_ms: float


@app.get("/health")
def health():
    return {"status": MODEL_PATH, "model_loaded": model is not None}


@app.get("/info")
def info():
    return {
        "model": MODEL_PATH,
        "device": DEVICE,
        "action_dims": 7,
        "description": "7-DoF end-effector delta: (x, y, z, roll, pitch, yaw, gripper)",
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        img_bytes = base64.b64decode(req.image)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    prompt = f"In: What action should the robot take to {req.instruction}?\nOut:"

    t0 = time.time()
    with torch.inference_mode():
        inputs = processor(prompt, image).to(DEVICE, dtype=torch.bfloat16)
        predict_kwargs = dict(do_sample=False)
        if req.unnorm_key:
            predict_kwargs["unnorm_key"] = req.unnorm_key
        action = model.predict_action(**inputs, **predict_kwargs)

    latency_ms = (time.time() - t0) * 1000

    if isinstance(action, torch.Tensor):
        action = action.cpu().float().numpy()
    action_list = np.array(action).flatten().tolist()

    return PredictResponse(action=action_list, latency_ms=round(latency_ms, 2))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
