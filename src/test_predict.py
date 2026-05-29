import base64
import io

import numpy as np
import requests
from PIL import Image

URL = "http://192.168.50.79:16003/predict"

img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
buf = io.BytesIO()
img.save(buf, format="JPEG")
b64 = base64.b64encode(buf.getvalue()).decode()

resp = requests.post(URL, json={
    "image": b64,
    "instruction": "pick up the red cup",
    "unnorm_key": "bridge_orig",
})

print(resp.status_code)
print(resp.text)
