#!/usr/bin/env bash
# cuRobo 파지 파이프라인 실행 후 LeRobot 데이터셋으로 자동 변환
# ── 여기만 수정하세요 ────────────────────────────────────────────────────────

SESSION="curobo_001"
TASK="Approach the red object closely and pick it up."

# ────────────────────────────────────────────────────────────────────────────
set -eo pipefail

WS_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -f "$WS_DIR/install/setup.bash" ]]; then
    source "$WS_DIR/install/setup.bash"
elif [[ -f /opt/ros/humble/setup.bash ]]; then
    source /opt/ros/humble/setup.bash
fi

LOG_DIR="$WS_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/curobo_${SESSION}_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "로그 저장: $LOG_FILE"

echo "=================================================="
echo " [1/2] cuRobo 데이터 수집 시작  (session=${SESSION})"
echo " YOLO 창에서 'a' 키로 Auto 모드 → 연속 파지"
echo " 수집 완료 후 Ctrl+C 로 종료"
echo "=================================================="
ros2 launch grasp_vla collect_curobo.launch.py \
    session:="${SESSION}"

echo ""
echo "=================================================="
echo " [2/2] LeRobot 데이터셋 변환 시작"
echo "=================================================="
python3 "$WS_DIR/src/bag_to_lerobot.py" \
    --task "${TASK}"

echo ""
echo "=================================================="
echo " 완료"
echo "=================================================="
