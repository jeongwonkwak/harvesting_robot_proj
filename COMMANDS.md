# OpenVLA-7B 서빙 명령어 정리

## 1. Docker 빌드 & 실행

```bash
cd /home/user/workspace/jeongwon_lab
docker compose up --build
```

---

## 2. 추론 요청 예시 (Python)

```python
import base64, requests

with open("camera_image.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

resp = requests.post("http://localhost:8000/predict", json={
    "image": b64,
    "instruction": "pick up the red cup",
    "unnorm_key": "bridge_orig"
})
print(resp.json()["action"])  # [dx, dy, dz, droll, dpitch, dyaw, gripper]
```

---

## 3. 서버 접근

### 방법 1 — SSH 터널 (방화벽 변경 불필요, 권장)

로컬 머신에서 실행:
```bash
ssh -L 8000:localhost:8000 user@192.168.50.67
```
접속 주소: `http://localhost:8000`

### 방법 2 — 방화벽 포트 개방

서버에서 실행:
```bash
sudo ufw allow 8000
```
접속 주소: `http://192.168.50.67:8000`

### 방화벽 상태 확인

```bash
sudo ufw status
```

---

## 4. API 엔드포인트

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/health` | 서버 상태 확인 |
| GET | `/info` | 모델 정보 |
| POST | `/predict` | 행동 예측 (image + instruction → 7-DoF action) |
