import base64
import io

import numpy as np
import requests
from PIL import Image

URL = "http://192.168.50.79:16003"


def make_dummy_image(h: int = 256, w: int = 256) -> str:
    img = Image.fromarray(np.random.randint(0, 255, (h, w, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()


camera1 = make_dummy_image()
camera2 = make_dummy_image()
camera3 = make_dummy_image()

state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 6-DoF: e.g. joint positions

payload = {
    "state": state,
    "camera1": camera1,
    "camera2": camera2,
    "camera3": camera3,
    "instruction": "pick up the strawberry",
    "reset_episode": True,
}

resp = requests.post(f"{URL}/predict", json=payload)
print("status:", resp.status_code)
print("response:", resp.json())
