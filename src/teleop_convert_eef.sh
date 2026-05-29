#!/usr/bin/env bash
# raw bag → LeRobot EEF 데이터셋 변환 + Quantile 통계
# teleop_collect_eef.sh 로 녹화한 raw bag 파일을 LeRobot 형식으로 변환합니다.
#
# 사용법:
#   bash src/teleop_convert_eef.sh
#
# ── 여기만 수정하세요 ────────────────────────────────────────────────────────

DATASET_NAME="vla_dataset_v0.3.0"

RAW_DIR="/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.3.0"     # 변환할 raw bag 경로
MID_DIR="/home/user/robot_workspace/vla_ws/data/mid"                   # LeRobot 데이터셋 저장 경로
LEROBOT_DIR="/home/user/robot_workspace/vla_ws/lerobot"

# 선택 옵션 (필요 시 주석 해제)
# CATEGORY_FILTER=""   # 특정 카테고리만 변환 (예: "no_occlusion")
# SKIP_REVIEW="true"   # quality=review 에피소드 제외

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
LOG_FILE="$LOG_DIR/convert_eef_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "로그 저장: $LOG_FILE"

# 경로 기본값 처리
[[ -z "$RAW_DIR" ]] && RAW_DIR="$WS_DIR/data/raw"
[[ -z "$MID_DIR" ]] && MID_DIR="$WS_DIR/data/mid"
DATASET_FULL_PATH="$MID_DIR/$DATASET_NAME"

echo ""
echo "=================================================="
echo " raw → LeRobot EEF 변환"
echo " 데이터셋  : $DATASET_NAME"
echo " raw 경로  : $RAW_DIR"
echo " mid 경로  : $DATASET_FULL_PATH"
echo "=================================================="
echo ""

# ── [1] bag → LeRobot 변환 ───────────────────────────────────────────────────
CONVERT_ARGS=(
    --raw-dir    "${RAW_DIR}"
    --output-dir "${DATASET_FULL_PATH}"
)
[[ -n "${CATEGORY_FILTER:-}" ]] && CONVERT_ARGS+=(--category-filter "${CATEGORY_FILTER}")
[[ "${SKIP_REVIEW:-}" == "true" ]] && CONVERT_ARGS+=(--skip-review)

python3 "$WS_DIR/src/bag_to_lerobot_eef.py" "${CONVERT_ARGS[@]}"

# ── [2] Quantile 통계 계산 및 메타데이터 추가 ─────────────────────────────────
if [[ -d "$DATASET_FULL_PATH" ]]; then
    echo ""
    echo "=================================================="
    echo " Quantile 통계 계산 및 메타데이터 추가"
    echo " 경로: $DATASET_FULL_PATH"
    echo "=================================================="
    python3 "$LEROBOT_DIR/src/lerobot/scripts/augment_dataset_quantile_stats.py" \
        --repo-id "${DATASET_NAME}" \
        --root    "${DATASET_FULL_PATH}"
else
    echo "[WARNING] 데이터셋 경로를 찾을 수 없어 quantile 통계를 건너뜁니다: $DATASET_FULL_PATH"
fi

echo ""
echo "=================================================="
echo " 완료  →  $DATASET_FULL_PATH"
echo " 데이터셋: $DATASET_NAME"
echo "=================================================="
