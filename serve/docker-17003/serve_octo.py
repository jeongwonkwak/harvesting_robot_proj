"""
Octo-base serving server using FastAPI (JAX-based).

Accepts primary + wrist camera images (base64), and a language instruction.
Returns a 7-DoF robot action. Manages 2-step observation history internally per episode.

Action chunking: pred_horizon=4 액션을 한 번에 추론하고 청크 버퍼에 쌓아둔다.
클라이언트가 /predict를 호출하면 버퍼에서 순서대로 꺼내주고,
버퍼가 비면 그때 다시 추론한다.
"""

import base64
import io
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import List, Optional

import jax
import jax.numpy as jnp
import numpy as np
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/public/octo-base")
DEVICE = os.environ.get("DEVICE", "cuda:0")  # JAX는 자체적으로 GPU 감지

WINDOW_SIZE = 2   # octo-base window_size
ACTION_DIM = 7
PRIMARY_SIZE = (256, 256)
WRIST_SIZE = (128, 128)

model = None
rng = None

obs_buffer: dict = {"image_primary": [], "image_wrist": []}
action_chunk: List[np.ndarray] = []  # 아직 실행 안 한 액션들


def _reset_buffer():
    obs_buffer["image_primary"] = []
    obs_buffer["image_wrist"] = []
    action_chunk.clear()


def _decode_image(b64: str, size: tuple) -> np.ndarray:
    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB").resize(size)
    return np.array(img, dtype=np.uint8)  # (H, W, 3)


def _build_obs_window() -> dict:
    """버퍼에서 (1, window, H, W, 3) 형태의 JAX 배열 반환."""
    def _pad_and_stack(frames, size):
        while len(frames) < WINDOW_SIZE:
            frames.insert(0, np.zeros((*size[::-1], 3), dtype=np.uint8))
        stacked = np.stack(frames[-WINDOW_SIZE:], axis=0)   # (window, H, W, 3)
        return jnp.array(stacked[None])                      # (1, window, H, W, 3)

    return {
        "image_primary": _pad_and_stack(obs_buffer["image_primary"], PRIMARY_SIZE),
        "image_wrist":   _pad_and_stack(obs_buffer["image_wrist"],   WRIST_SIZE),
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, rng
    logger.info(f"Loading Octo from {MODEL_PATH} ...")
    t0 = time.time()

    from octo.model.octo_model import OctoModel
    model = OctoModel.load_pretrained(MODEL_PATH)
    rng = jax.random.PRNGKey(0)

    logger.info(f"Octo ready in {time.time() - t0:.1f}s  |  devices: {jax.devices()}")
    yield
    del model


app = FastAPI(title="Octo-base Server", lifespan=lifespan)


class PredictRequest(BaseModel):
    image_primary: str            # base64 JPEG/PNG, 256x256으로 리사이즈됨
    image_wrist: Optional[str] = None  # base64, 128x128; None이면 검정 이미지 사용
    instruction: str
    reset_episode: bool = False   # 새 에피소드 시작 시 True


class PredictResponse(BaseModel):
    action: List[float]           # 7-DoF action
    latency_ms: float
    inferred: bool                # True면 이번 스텝에 실제 추론 발생, False면 청크에서 꺼냄
    chunk_remaining: int          # 청크 버퍼에 남은 액션 수


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.get("/info")
def info():
    return {
        "model": MODEL_PATH,
        "action_dims": ACTION_DIM,
        "window_size": WINDOW_SIZE,
        "pred_horizon": 4,
        "cameras": {
            "image_primary": list(PRIMARY_SIZE),
            "image_wrist": list(WRIST_SIZE),
        },
        "description": "7-DoF continuous action via diffusion; action chunking with pred_horizon=4",
    }


@app.post("/reset")
def reset_episode():
    _reset_buffer()
    return {"status": "reset"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    global rng

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if req.reset_episode:
        _reset_buffer()

    try:
        primary = _decode_image(req.image_primary, PRIMARY_SIZE)
        wrist = (
            _decode_image(req.image_wrist, WRIST_SIZE)
            if req.image_wrist
            else np.zeros((*WRIST_SIZE[::-1], 3), dtype=np.uint8)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    obs_buffer["image_primary"].append(primary)
    obs_buffer["image_wrist"].append(wrist)

    observations = _build_obs_window()

    try:
        tasks = model.create_tasks(texts=[req.instruction])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {e}")

    # 청크 버퍼가 비었을 때만 추론
    inferred = False
    t0 = time.time()
    if not action_chunk:
        rng, sample_rng = jax.random.split(rng)
        actions = model.sample_actions(observations, tasks, rng=sample_rng)
        # actions: (1, pred_horizon, action_dim)
        for a in np.array(actions[0]):  # pred_horizon개 순서대로 추가
            action_chunk.append(a)
        inferred = True
    latency_ms = (time.time() - t0) * 1000

    action = action_chunk.pop(0).tolist()

    return PredictResponse(
        action=action,
        latency_ms=round(latency_ms, 2),
        inferred=inferred,
        chunk_remaining=len(action_chunk),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8001)))
