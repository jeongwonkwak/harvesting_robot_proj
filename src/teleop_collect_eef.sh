#!/usr/bin/env bash
# 텔레오퍼레이션 + bag 녹화  (변환은 teleop_convert_eef.sh 에서 별도 수행)
#
# 사용법:
#   bash src/teleop_collect_eef.sh
#
# ── 여기만 수정하세요 ────────────────────────────────────────────────────────

EPISODE=""     # 비워두면 기존 에피소드 수 기준으로 자동 부여
TASK="Grasp the strawberry stem and pick it."

# RealSense 카메라 시리얼 번호 (rs-enumerate-devices | grep Serial 로 확인)
# 카메라가 1개만 연결되어 있거나 순서가 고정되어 있으면 비워둬도 됨
# 두 카메라가 동시에 연결된 경우 반드시 지정해야 카메라가 뒤바뀌지 않음
SERIAL_CAM1="215122254786"   # YOLO 인식 카메라 시리얼 (예: "123622270786")
SERIAL_CAM2="342622303457"   # 전경 카메라 시리얼     (예: "342622303457")

# 데이터 카테고리 — 아래 7가지 중 하나로 변경:
#   no_occlusion                S1. 폐색 없음           딸기가 명확히 보이는 기본 수확
#   unripe_occlusion_mild       S2. 미숙 딸기 폐색 (약) 초록 딸기가 빨간 딸기를 살짝 가림
#   unripe_occlusion_moderate   S3. 미숙 딸기 폐색 (중) 초록 딸기가 절반 정도 가림
#   unripe_occlusion_heavy      S4. 미숙 딸기 폐색 (강) 초록 딸기가 대부분 가림
#   leaf_occlusion_mild         S5. 잎 폐색 (약)        잎이 딸기를 살짝 가림
#   leaf_occlusion_moderate     S6. 잎 폐색 (중)        잎이 딸기를 절반 정도 가림
#   leaf_occlusion_heavy        S7. 잎 폐색 (강)        잎이 딸기를 대부분 가림
CATEGORY="no_occlusion"

# 홈 포즈 — 아래 4가지 중 하나로 변경:
#   top_right     우상단  (x+270mm, z+185mm)
#   top_left      좌상단  (x-270mm, z+185mm)
#   bottom_right  우하단  (x+270mm, z-185mm)
#   bottom_left   좌하단  (x-270mm, z-185mm)
HOME_POSE="top_right"

RAW_DIR="/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.3.0"     # 비워두면 <ws>/data/raw 기본값 사용

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
LOG_FILE="$LOG_DIR/teleop_eef_${CATEGORY}_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "로그 저장: $LOG_FILE"

# 경로 기본값 처리
[[ -z "$RAW_DIR" ]] && RAW_DIR="$WS_DIR/data/raw"

echo ""
echo "=================================================="
echo " 텔레오퍼레이션 EEF 녹화  (변환 없음)"
echo " 카테고리  : $CATEGORY"
echo " 태스크    : $TASK"
echo " 에피소드  : ${EPISODE:-자동 부여}"
echo " raw 저장  : $RAW_DIR"
echo " ※ 변환은 teleop_convert_eef.sh 로 별도 실행"
echo "=================================================="
echo ""

# ── [1] 텔레오퍼레이션 + 녹화 (변환 스킵) ───────────────────────────────────
TELEOP_ARGS=(
    --task         "${TASK}"
    --category     "${CATEGORY}"
    --raw-dir      "${RAW_DIR}"
    --home-pose    "${HOME_POSE}"
    --skip-convert
)
[[ -n "$EPISODE"     ]] && TELEOP_ARGS+=(--episode    "${EPISODE}")
[[ -n "$SERIAL_CAM1" ]] && TELEOP_ARGS+=(--serial-cam1 "${SERIAL_CAM1}")
[[ -n "$SERIAL_CAM2" ]] && TELEOP_ARGS+=(--serial-cam2 "${SERIAL_CAM2}")

python3 "$WS_DIR/src/teleop_record_and_convert_eef.py" "${TELEOP_ARGS[@]}"

# ── [2] LeRobot 변환 및 Quantile 통계는 teleop_convert_eef.sh 에서 수행 ─────
# (주석 처리)
#
# DATASET_NAME="vla_dataset_v1.0.0"
# MID_DIR="/home/user/robot_workspace/vla_ws/data/mid"
# LEROBOT_DIR="/home/user/robot_workspace/vla_ws/lerobot"
# DATASET_FULL_PATH="$MID_DIR/$DATASET_NAME"
#
# python3 "$WS_DIR/src/bag_to_lerobot_eef.py" \
#     --raw-dir    "${RAW_DIR}" \
#     --output-dir "${DATASET_FULL_PATH}" \
#     --task       "${TASK}"
#
# if [[ -d "$DATASET_FULL_PATH" ]]; then
#     python3 "$LEROBOT_DIR/src/lerobot/scripts/augment_dataset_quantile_stats.py" \
#         --repo-id "${DATASET_NAME}" \
#         --root    "${DATASET_FULL_PATH}"
# fi

echo ""
echo "=================================================="
echo " 녹화 완료  →  $RAW_DIR"
echo " 카테고리: $CATEGORY"
echo " ※ LeRobot 변환: bash src/teleop_convert_eef.sh"
echo "=================================================="
