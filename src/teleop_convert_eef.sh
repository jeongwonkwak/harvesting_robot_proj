#!/usr/bin/env bash
# raw bag → LeRobot EEF 데이터셋 변환 + Quantile 통계
# teleop_collect_eef.sh 로 녹화한 raw bag 파일을 LeRobot 형식으로 변환합니다.
#
# 사용법:
#   bash src/teleop_convert_eef.sh
#
# 에피소드 선택 예시:
#   1) 전체 변환:      EPISODE_MODE="all"
#   2) 범위 변환:      EPISODE_MODE="range", EPISODE_START=0, EPISODE_END=10
#   3) 목록 변환:      EPISODE_MODE="list", EPISODE_LIST="0,2,5,8"
#   4) 용량 절약:      USE_SYMLINK="true" (중복 에피소드를 심볼릭 링크로 저장)
#
# ── 여기만 수정하세요 ────────────────────────────────────────────────────────

DATASET_NAME="vla_dataset_v0.5.2"   # v0.5.0과 동일 raw, 동기화만 nearest → 보간 (발견 #8 해결)

# 작업 지시문 — meta/tasks.parquet에 기록되어 학습·추론 시 그대로 사용됨.
# raw bag에는 지시문이 없으므로 여기서 명시하지 않으면 bag_to_lerobot_eef.py의
# 하드코딩 기본값이 들어간다. episodes_catalog.yaml에 에피소드별 task가 있으면 그쪽이 우선.
TASK="Approach to the strawberry stem."

RAW_DIR="/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.5.0"     # 변환할 raw bag 경로
MID_DIR="/home/user/robot_workspace/vla_ws/data/mid"                   # LeRobot 데이터셋 저장 경로
LEROBOT_DIR="/home/user/robot_workspace/vla_ws/lerobot"

# ── 에피소드 선택 ──────────────────────────────────────────────────────────
# EPISODE_MODE: "all" (전체) | "range" (범위) | "list" (목록)
EPISODE_MODE="all"

# EPISODE_MODE="range" 일 때: 시작 및 종료 에피소드 번호 (0-indexed)
EPISODE_START=17
EPISODE_END=49

# EPISODE_MODE="list" 일 때: 특정 에피소드만 (쉼표로 구분)
# EPISODE_LIST="0,2,5,8"

# 용량 절약: 중복 에피소드를 심볼릭 링크로 저장 (true 추천)
USE_SYMLINK="true"

# ── 기타 필터링 옵션 ────────────────────────────────────────────────────────
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
echo " 지시문    : $TASK"
echo " raw 경로  : $RAW_DIR"
echo " mid 경로  : $DATASET_FULL_PATH"
echo "=================================================="
echo ""

# ── [1] bag → LeRobot 변환 ───────────────────────────────────────────────────
echo "에피소드 모드: $EPISODE_MODE"
[[ "$EPISODE_MODE" == "range" ]] && echo "에피소드 범위: $EPISODE_START ~ $EPISODE_END"
[[ "$EPISODE_MODE" == "list" ]] && echo "선택 에피소드: ${EPISODE_LIST:-없음}"
[[ "$USE_SYMLINK" == "true" ]] && echo "심볼릭 링크 사용: ON (용량 절약)"
echo ""

CONVERT_ARGS=(
    --raw-dir    "${RAW_DIR}"
    --output-dir "${DATASET_FULL_PATH}"
    --task       "${TASK}"
)
[[ -n "${CATEGORY_FILTER:-}" ]] && CONVERT_ARGS+=(--category-filter "${CATEGORY_FILTER}")
[[ "${SKIP_REVIEW:-}" == "true" ]] && CONVERT_ARGS+=(--skip-review)
[[ "$EPISODE_MODE" == "range" ]] && CONVERT_ARGS+=(--episode-start "${EPISODE_START}" --episode-end "${EPISODE_END}")
[[ "$EPISODE_MODE" == "list" && -n "${EPISODE_LIST:-}" ]] && CONVERT_ARGS+=(--episode-list "${EPISODE_LIST}")
[[ "$USE_SYMLINK" == "true" ]] && CONVERT_ARGS+=(--use-symlink)

python3 "$WS_DIR/src/bag_to_lerobot_eef.py" "${CONVERT_ARGS[@]}"

echo ""
echo "=================================================="
echo " 완료  →  $DATASET_FULL_PATH"
echo " 데이터셋: $DATASET_NAME"
echo "=================================================="
echo ""
echo "다음 단계:"
echo "  1. mid/ 데이터셋 확인: $DATASET_FULL_PATH"
echo "  2. fin/ 데이터셋 생성 및 quantile stats 추가:"
echo "     python3 src/prepare_fin_dataset.py --src \"$DATASET_FULL_PATH\" --dst \"$MID_DIR/../fin/$DATASET_NAME\""
echo "=================================================="
