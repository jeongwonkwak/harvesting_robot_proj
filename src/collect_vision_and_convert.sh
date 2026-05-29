#!/usr/bin/env bash
# teleop_records.csv 웨이포인트 재생 → ROS2 bag 녹화 → LeRobot 데이터셋 변환
#
# 사용법:
#   bash collect_vision_and_convert.sh
#
# ── 여기만 수정하세요 ────────────────────────────────────────────────────────

EPISODE="001"
TASK="Approach the red object closely and pick it up."
CSV_FILE="teleop_records/20260520_172142.csv"   # 비워두면 teleop_records.csv 기본값 사용

DATASET_NAME="vla_dataset_v1.1.0"              # bag_to_lerobot.py 의 --dataset-name 과 일치
MID_DIR=""                                      # 비워두면 <ws>/data/mid 기본값 사용
LEROBOT_DIR="/workspace/lerobot"               # augment_dataset_quantile_stats.py 위치

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
LOG_FILE="$LOG_DIR/vision_episode_${EPISODE}_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "로그 저장: $LOG_FILE"

# CSV_FILE: 비어있으면 기본값, 상대 경로면 src/ 기준으로 절대 경로 변환
if [[ -z "$CSV_FILE" ]]; then
    CSV_FILE="$WS_DIR/src/teleop_records.csv"
elif [[ "$CSV_FILE" != /* ]]; then
    CSV_FILE="$WS_DIR/src/$CSV_FILE"
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "[ERROR] CSV 파일을 찾을 수 없습니다: $CSV_FILE"
    exit 1
fi

BAG_DIR="$WS_DIR/data/raw/episode_${EPISODE}_$(date +%Y%m%d_%H%M%S)"
QOS_FILE="$WS_DIR/config/bag_qos_overrides.yaml"

echo "=================================================="
echo " [1/3] 인프라 시작 (RealSense + 그리퍼 퍼블리셔 + bag recorder)"
echo "=================================================="

# RealSense (color + aligned depth)
ros2 launch realsense2_camera rs_launch.py \
    enable_color:=true \
    enable_depth:=true \
    rgb_camera.color_profile:=640x480x30 \
    depth_module.depth_profile:=640x480x30 \
    align_depth.enable:=true &
RS_PID=$!

# 그리퍼 상태 퍼블리셔
ros2 run grasp_vla gripper_state_publisher_node &
GRIP_PID=$!

# RealSense가 실제로 프레임을 내보낼 때까지 대기 (USB 재열거로 인한 재시작 완료 후)
echo "카메라 첫 프레임 대기 중 (최대 30초)..."
timeout 30 bash -c \
    'until ros2 topic echo /camera/camera/color/image_raw --no-arr --once > /dev/null 2>&1; do sleep 0.5; done' \
    && echo "카메라 준비 완료" \
    || { echo "[ERROR] 카메라 타임아웃 (30초). RealSense 연결을 확인하세요."; kill $GRIP_PID $RS_PID 2>/dev/null; exit 1; }

# bag recorder — 카메라, 관절 상태, 그리퍼 위치를 동시 녹화
ros2 bag record \
    --qos-profile-overrides-path "$QOS_FILE" \
    -o "$BAG_DIR" \
    /dsr01/joint_states \
    /camera/camera/color/image_raw \
    /gripper/position &
BAG_PID=$!

sleep 1

echo ""
echo "=================================================="
echo " [2/3] 에피소드 재생: teleop 기록 웨이포인트 순서대로 이동"
echo " CSV: $CSV_FILE"
echo "=================================================="
python3 "$WS_DIR/episode_secenario/replay_teleop_records.py" \
    --csv "$CSV_FILE"

echo ""
echo " 에피소드 완료. 인프라 종료 중 ..."
kill $BAG_PID $GRIP_PID $RS_PID 2>/dev/null || true
wait $BAG_PID 2>/dev/null || true

echo ""
echo "=================================================="
echo " [3/4] LeRobot 데이터셋 변환 시작"
echo "=================================================="

# MID_DIR 미지정 시 기본값
if [[ -z "$MID_DIR" ]]; then
    MID_DIR="$WS_DIR/data/mid"
fi
DATASET_FULL_PATH="$MID_DIR/$DATASET_NAME"

python3 "$WS_DIR/src/bag_to_lerobot.py" \
    --task "${TASK}" \
    --dataset-name "${DATASET_NAME}" \
    --output-dir "${MID_DIR}/${DATASET_NAME}"

echo ""
echo "=================================================="
echo " [4/4] Quantile 통계 계산 및 메타데이터 추가"
echo " 경로: $DATASET_FULL_PATH"
echo "=================================================="
python3 "$LEROBOT_DIR/src/lerobot/scripts/augment_dataset_quantile_stats.py" \
    --repo-id "${DATASET_NAME}" \
    --root "${DATASET_FULL_PATH}"

echo ""
echo "=================================================="
echo " 완료  →  $DATASET_FULL_PATH"
echo "=================================================="
