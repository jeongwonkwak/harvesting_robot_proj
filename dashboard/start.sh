#!/bin/bash
# 딸기 수확 대시보드 실행 스크립트 (conda robot_env)
# RealSense + LG 웹캠 동시 스트리밍

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="$SCRIPT_DIR/data/harvest_state.json"
mkdir -p "$SCRIPT_DIR/data"

export HARVEST_STATE_FILE="$STATE_FILE"
export CAMERA_ID=6        # YOLO 인식 카메라 (RealSense /dev/video6)
export CAMERA_ID_1=4      # 전경 카메라      (LG 웹캠   /dev/video0)

echo ""
echo "  🍓 딸기 수확 대시보드 시작"
echo "  → http://localhost:8765"
echo "  → YOLO 카메라: /dev/video6 (RealSense)"
echo "  → 전경 카메라: /dev/video0 (LG 웹캠)"
echo ""

conda run -n robot_env --no-capture-output \
    python3 "$SCRIPT_DIR/harvest_dashboard.py" \
    --host 0.0.0.0 --port 8765
