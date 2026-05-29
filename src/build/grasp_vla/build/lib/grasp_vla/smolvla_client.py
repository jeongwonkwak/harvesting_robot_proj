"""
SmolVLA HTTP API client.

SmolVLA server (serve_smolvla.py) at http://192.168.50.79:16003
POST /predict → action [6-DoF], latency_ms
"""

import base64
import io
from dataclasses import dataclass
from typing import List, Optional

import numpy as np
import requests
from PIL import Image


@dataclass
class PredictResponse:
    action: np.ndarray   # shape (6,)  [dx, dy, dz, drx, dry, drz] or joint targets
    latency_ms: float


class SmolVLAClient:
    def __init__(self, base_url: str = "http://192.168.50.79:16003", timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=2.0)
            return r.ok and r.json().get("model_loaded", False)
        except Exception:
            return False

    def reset(self) -> None:
        """Tell the server to reset the action-chunk buffer (new episode)."""
        requests.post(f"{self.base_url}/reset", timeout=2.0)

    def predict(
        self,
        state: np.ndarray,           # shape (6,) – joint positions or EEF pose
        image_top: np.ndarray,       # RGB (H, W, 3) uint8 – main camera
        instruction: str,
        image_front: Optional[np.ndarray] = None,
        image_wrist: Optional[np.ndarray] = None,
        reset_episode: bool = False,
    ) -> PredictResponse:
        """
        Call SmolVLA server and return the next action.

        The server manages the action-chunk buffer internally.
        Pass reset_episode=True at the start of every new grasp attempt.
        """
        payload = {
            "state": state.tolist(),
            "camera1": _encode_image(image_top),
            "camera2": _encode_image(image_front) if image_front is not None else _encode_image(image_top),
            "camera3": _encode_image(image_wrist) if image_wrist is not None else _encode_image(image_top),
            "instruction": instruction,
            "reset_episode": reset_episode,
        }

        resp = requests.post(
            f"{self.base_url}/predict",
            json=payload,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()

        return PredictResponse(
            action=np.array(data["action"], dtype=np.float32),
            latency_ms=data["latency_ms"],
        )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _encode_image(image: np.ndarray, size: tuple = (256, 256)) -> str:
    """Convert numpy RGB array to base64 JPEG string."""
    pil = Image.fromarray(image.astype(np.uint8)).resize(size)
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()
