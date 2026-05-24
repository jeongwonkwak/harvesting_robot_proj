"""SmolVLA FastAPI 추론 서버 (스켈레톤).

목적
----
LeRobot 의 SmolVLA 모델을 HTTP 로 노출해서, `ros2-lab` 컨테이너의
ROS2 노드가 이미지 + 자연어 instruction 을 보내면 로봇 액션을 받아오도록
하는 추론 서버의 출발점입니다.

환경 변수
---------
- MODEL_PATH : 로드할 모델 경로 또는 HF 허브 ID  (기본: /models/vla-model)
- DEVICE     : 추론 디바이스 ("cuda:0" / "cpu")     (기본: cuda:0)
- PORT       : FastAPI 리스닝 포트                  (기본: 8000)

엔드포인트
----------
- GET  /health   : 헬스체크 (compose depends_on 용)
- POST /predict  : 이미지 + instruction → action 추론
- GET  /info     : 모델 메타정보 조회

TODO (팀원이 채울 부분)
-----------------------
1. LeRobot SmolVLA 정책 클래스 로딩 코드 작성
2. 입력 이미지 전처리 파이프라인 확정 (RealSense 해상도/포맷 매칭)
3. 액션 출력 스키마 합의 (관절 공간 vs 카르테시안)
4. 배치 추론 / 비동기 큐 (필요 시)
"""
from __future__ import annotations

import base64
import io
import logging
import os
from typing import List, Optional

import torch
from fastapi import FastAPI, HTTPException
from PIL import Image
from pydantic import BaseModel, Field

# -------------------------------------------------------------------- 환경 변수
MODEL_PATH: str = os.getenv("MODEL_PATH", "/models/vla-model")
DEVICE: str = os.getenv("DEVICE", "cuda:0")
PORT: int = int(os.getenv("PORT", "8000"))

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s | %(message)s",
)
log = logging.getLogger("smolvla-server")

app = FastAPI(title="Strawberry Harvest SmolVLA Server", version="0.1.0")

# 모듈 전역 모델 핸들 (lazy load)
_model = None
_model_meta: dict = {}


# -------------------------------------------------------------------- 스키마
class PredictRequest(BaseModel):
    """추론 요청 페이로드.

    image_b64: PNG/JPEG 인코딩된 이미지를 base64 로 직렬화한 문자열.
    instruction: 자연어 명령 (예: "pick up the red strawberry").
    state: 현재 관절 각도/그리퍼 상태 등 옵션 컨텍스트.
    """

    image_b64: str = Field(..., description="base64 인코딩된 이미지")
    instruction: str = Field(..., description="자연어 작업 지시")
    state: Optional[List[float]] = Field(
        default=None, description="현재 로봇 상태 벡터 (선택)"
    )


class PredictResponse(BaseModel):
    """추론 응답 페이로드.

    action: 예측된 액션 벡터 (관절 또는 카르테시안, 팀에서 스키마 합의 필요).
    """

    action: List[float]
    raw: Optional[dict] = None


# -------------------------------------------------------------------- 모델 로딩
def load_model() -> None:
    """SmolVLA 정책을 디스크/허브에서 로드.

    팀원이 LeRobot 의 적절한 API 로 교체해 주세요.
    예시(의사 코드):
        from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
        policy = SmolVLAPolicy.from_pretrained(MODEL_PATH)
        policy.to(DEVICE).eval()
    """
    global _model, _model_meta
    log.info("Loading SmolVLA model from %s on %s", MODEL_PATH, DEVICE)

    # TODO: 실제 로딩 코드로 교체
    _model = None  # placeholder
    _model_meta = {
        "model_path": MODEL_PATH,
        "device": DEVICE,
        "loaded": False,
        "note": "스켈레톤 상태 — 실제 SmolVLA 로딩 코드로 교체 필요",
    }
    log.warning("모델 로딩 미구현 상태 (placeholder). serve_smolvla.py 의 TODO 참고")


@app.on_event("startup")
def _on_startup() -> None:
    """서버 부팅 시 1회 실행되는 훅."""
    if not torch.cuda.is_available() and DEVICE.startswith("cuda"):
        log.warning("CUDA 사용 불가 — CPU 로 폴백")
    try:
        load_model()
    except Exception as exc:  # noqa: BLE001
        log.exception("모델 로딩 실패: %s", exc)


# -------------------------------------------------------------------- 엔드포인트
@app.get("/health")
def health() -> dict:
    """compose 헬스체크용. 모델 로딩 실패해도 200 을 반환해 기본 서비스는 살아있음을 알림."""
    return {
        "status": "ok",
        "model_loaded": _model is not None,
        "device": DEVICE,
    }


@app.get("/info")
def info() -> dict:
    """모델 메타정보."""
    return _model_meta


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    """이미지 + instruction → action 추론.

    팀원이 SmolVLA 의 실제 forward 로직으로 교체해 주세요.
    """
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="모델이 아직 로드되지 않았습니다. /info 확인 후 SmolVLA 로딩 코드 작성 필요.",
        )

    try:
        img = _decode_image(req.image_b64)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"이미지 디코딩 실패: {exc}") from exc

    # TODO: SmolVLA forward → action tensor
    # 예시(의사 코드):
    #   inputs = preprocess(img, req.instruction, req.state)
    #   with torch.no_grad():
    #       action = _model.select_action(inputs).cpu().tolist()
    action: List[float] = [0.0] * 7  # placeholder (7-DoF)

    return PredictResponse(action=action, raw={"image_size": img.size})


# -------------------------------------------------------------------- 유틸
def _decode_image(b64_str: str) -> Image.Image:
    """base64 문자열을 PIL Image 로 변환."""
    raw = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(raw)).convert("RGB")


# -------------------------------------------------------------------- 엔트리포인트
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "serve_smolvla:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        reload=False,
    )
