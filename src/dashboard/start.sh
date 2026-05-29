#!/bin/bash
# 딸기 수확 대시보드 실행 스크립트 (conda robot_env)
# 시리얼 번호 확인: rs-enumerate-devices | grep "Serial Number"

# ── 여기만 수정하세요 ────────────────────────────────────────────────────────
SERIAL_CAM0="215122254786"   # YOLO 인식 카메라 시리얼 (D455)
SERIAL_CAM1="342622303457"   # 전경 카메라 시리얼      (D455F)
# ────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="$SCRIPT_DIR/data/harvest_state.json"
mkdir -p "$SCRIPT_DIR/data"

export HARVEST_STATE_FILE="$STATE_FILE"

echo ""
echo "  딸기 수확 대시보드 시작"
echo "  → http://localhost:8765"
echo "  → YOLO 카메라: ${SERIAL_CAM0}"
echo "  → 전경 카메라: ${SERIAL_CAM1}"
echo ""

conda run -n robot_env --no-capture-output \
    python3 "$SCRIPT_DIR/harvest_dashboard.py" \
    --host 0.0.0.0 --port 8765 \
    --serial-cam0 "$SERIAL_CAM0" \
    --serial-cam1 "$SERIAL_CAM1"
