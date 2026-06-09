#!/usr/bin/env python3
"""
VLA 추론 목업 테스트 앱 (Streamlit)
- 데이터셋의 첫 에피소드 이미지를 로드
- 목업 VLA 추론 결과 시뮬레이션
- 기본값이 입력되었을 때의 추론 결과 표시

실행: streamlit run src/vla_inference_mock_test.py
"""

import streamlit as st
import numpy as np
import cv2
import json
from pathlib import Path
from typing import Optional, Tuple
import math
import base64
import io
import urllib.request

# ──────────────────────────────────────────────────────────────────────────────
# 설정
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="VLA 추론 목업 테스트",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 사용 가능한 데이터셋 경로 (우선순위 순)
_CANDIDATE_PATHS = [
    Path("/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v1.0.0"),
    Path("/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.3"),
    Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.3"),
]

# 실제 존재하는 경로 선택
DATA_DIR = None
for path in _CANDIDATE_PATHS:
    if path.exists():
        DATA_DIR = path
        break

if DATA_DIR is None:
    raise FileNotFoundError(f"사용 가능한 데이터셋을 찾을 수 없습니다. 확인된 경로:\n" +
                           "\n".join(str(p) for p in _CANDIDATE_PATHS))

VIDEOS_DIR = DATA_DIR / "videos"
CAM1_DIR = VIDEOS_DIR / "observation.images.camera1/chunk-000"
CAM2_DIR = VIDEOS_DIR / "observation.images.camera2/chunk-000"

VLA_API_URL = "http://192.168.50.79:18003"

# Episode 0 샘플 Observation State (TCP Pose, 첫 프레임)
# [x_m, y_m, z_m, rx_rad, ry_rad, rz_rad]
SAMPLE_EPISODE = 0
SAMPLE_OBSERVATION_STATE = np.array([0.31287524, 0.27915237, 0.87901123, 1.56872585, 1.50528589, -1.56418996])

# ──────────────────────────────────────────────────────────────────────────────
# 목업 이미지 로드
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def load_mock_images() -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """데이터셋의 첫 에피소드 이미지 (첫 프레임) 로드"""

    def extract_first_frame(mp4_path: Path) -> Optional[np.ndarray]:
        """MP4 파일의 첫 프레임 추출"""
        if not mp4_path.exists():
            st.warning(f"파일을 찾을 수 없습니다: {mp4_path}")
            return None

        try:
            cap = cv2.VideoCapture(str(mp4_path))
            if not cap.isOpened():
                st.warning(f"비디오를 열 수 없습니다: {mp4_path}")
                return None

            ret, frame = cap.read()
            cap.release()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame
            else:
                st.warning(f"프레임을 읽을 수 없습니다: {mp4_path}")
                return None
        except Exception as e:
            st.warning(f"프레임 추출 실패 ({mp4_path}): {e}")
            return None

    # 첫 파일의 첫 프레임
    cam1_file = CAM1_DIR / "file-000.mp4"
    cam2_file = CAM2_DIR / "file-000.mp4"

    # 디버그: 경로 정보 출력
    st.info(f"데이터셋: {DATA_DIR.name}")
    st.caption(f"📁 Camera 1 경로: {cam1_file}")
    st.caption(f"📁 Camera 2 경로: {cam2_file}")

    cam1_frame = None
    cam2_frame = None

    if cam1_file.exists():
        cam1_frame = extract_first_frame(cam1_file)
    else:
        st.warning(f"Camera 1 파일을 찾을 수 없습니다: {cam1_file}")

    if cam2_file.exists():
        cam2_frame = extract_first_frame(cam2_file)
    else:
        st.warning(f"Camera 2 파일을 찾을 수 없습니다: {cam2_file}")

    return cam1_frame, cam2_frame



def resize_image(img: np.ndarray, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """이미지를 지정된 크기로 리사이즈"""
    return cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)


def encode_image_to_base64(image: np.ndarray, size: Tuple[int, int] = (256, 256)) -> str:
    """이미지를 base64 문자열로 인코딩"""
    try:
        from PIL import Image
        pil_img = Image.fromarray(image.astype(np.uint8)).resize(size)
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=90)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.error(f"이미지 인코딩 실패: {e}")
        return None


def simulate_vla_inference_mock(instruction: str, reset_episode: bool = False) -> dict:
    """목업 VLA 추론 (실제 서버 없이 테스트용)"""
    # 기본값 action 벡터 (32-dim)
    action = np.zeros(32, dtype=float)

    instruction_lower = instruction.lower()

    # 지시문에 따라 다른 action 생성 (gripper는 0~740 범위)
    if "strawberry" in instruction_lower or "pick" in instruction_lower:
        # 딸기 집기
        action[0] = 0.05      # ΔX: 50mm 오른쪽
        action[1] = 0.03      # ΔY: 30mm 앞쪽
        action[2] = -0.10     # ΔZ: 100mm 아래쪽
        action[6] = 703      # 그리퍼: 95% 닫기 (0.95 × 740)
    elif "grasp" in instruction_lower:
        # 파지
        action[2] = -0.08     # ΔZ: 80mm 아래쪽
        action[6] = 666      # 그리퍼: 90% 닫기 (0.90 × 740)
    elif "release" in instruction_lower or "drop" in instruction_lower:
        # 놓기
        action[2] = 0.10      # ΔZ: 100mm 위쪽
        action[6] = 37       # 그리퍼: 5% 열기 (0.05 × 740)
    elif "home" in instruction_lower:
        # 홈 복귀
        action[6] = 0.0       # 그리퍼: 열기
    else:
        # 기본: 작은 이동
        action[0] = np.random.uniform(-0.05, 0.05)
        action[1] = np.random.uniform(-0.05, 0.05)
        action[2] = np.random.uniform(-0.10, 0.05)
        action[6] = np.random.uniform(148, 592)  # 그리퍼: 20~80% (0.2~0.8 × 740)

    return {
        "action": action.tolist(),
        "latency_ms": np.random.uniform(100, 300),
        "instruction": instruction,
        "reset_episode": reset_episode
    }


# ──────────────────────────────────────────────────────────────────────────────
# VLA 추론 시뮬레이션
# ──────────────────────────────────────────────────────────────────────────────

def simulate_vla_inference(
    state: list,
    instruction: str,
    reset_episode: bool = False,
) -> dict:
    """
    VLA 추론 시뮬레이션

    Args:
        state: [tcp_x_m, tcp_y_m, tcp_z_m, rx_rad, ry_rad, rz_rad, gripper_ratio, 0×25]
        instruction: 작업 지시문
        reset_episode: 에피소드 리셋 여부

    Returns:
        VLA 응답 (action, latency_ms)
    """

    # 기본값을 사용한 목업 추론
    # action: [delta_x_m, delta_y_m, delta_z_m, delta_rx_rad, delta_ry_rad, delta_rz_rad, gripper_ratio, 0×25]

    action = np.zeros(32, dtype=float)

    # 다양한 지시에 따라 다른 action 생성
    instruction_lower = instruction.lower()

    if "strawberry" in instruction_lower or "pick" in instruction_lower:
        # 딸기 집기 시뮬레이션
        action[0] = 0.05      # dx: 50mm 오른쪽
        action[1] = 0.03      # dy: 30mm 앞쪽
        action[2] = -0.10     # dz: 100mm 아래쪽
        action[6] = 703      # gripper: 95% 닫기 (0.95 × 740)
    elif "grasp" in instruction_lower:
        # 파지 시뮬레이션
        action[2] = -0.08     # dz: 80mm 아래쪽
        action[6] = 666      # gripper: 90% 닫기 (0.90 × 740)
    elif "release" in instruction_lower or "drop" in instruction_lower:
        # 놓기 시뮬레이션
        action[2] = 0.10      # dz: 100mm 위쪽
        action[6] = 37       # gripper: 5% 열기 (0.05 × 740)
    elif "home" in instruction_lower:
        # 홈 포즈로 복귀
        action[6] = 0.0       # gripper: 열기
    else:
        # 기본: 작은 이동과 그리퍼 제어
        action[0] = np.random.uniform(-0.05, 0.05)
        action[1] = np.random.uniform(-0.05, 0.05)
        action[2] = np.random.uniform(-0.10, 0.05)
        action[6] = np.random.uniform(148, 592)  # gripper: 20~80% (0.2~0.8 × 740)

    # 시뮬레이션 레이턴시
    latency_ms = np.random.uniform(100, 300)

    return {
        "action": action.tolist(),
        "latency_ms": float(latency_ms),
        "instruction": instruction,
        "reset_episode": reset_episode,
    }


def calculate_state_vector(tcp_pose: list, gripper_pos: float = 100.0) -> list:
    """
    TCP 포즈를 32-dim state vector로 변환

    Args:
        tcp_pose: [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]
        gripper_pos: gripper position (0-100)

    Returns:
        32-dim state vector
    """
    state = [
        tcp_pose[0] / 1000.0,       # X mm → m
        tcp_pose[1] / 1000.0,       # Y mm → m
        tcp_pose[2] / 1000.0,       # Z mm → m
        tcp_pose[3] / 57.2958,      # Rx deg → rad
        tcp_pose[4] / 57.2958,      # Ry deg → rad
        tcp_pose[5] / 57.2958,      # Rz deg → rad
        gripper_pos / 100.0,        # position % → ratio [0, 1]
    ] + [0.0] * 25
    return state


def calculate_target_pose(
    current_pose: list,
    action: list,
) -> list:
    """
    VLA action을 기반으로 목표 포즈 계산

    Args:
        current_pose: 현재 TCP 포즈 [x_mm, y_mm, z_mm, rx_deg, ry_deg, rz_deg]
        action: VLA action [delta_x_m, delta_y_m, delta_z_m, delta_rx_rad, ...]

    Returns:
        목표 TCP 포즈
    """
    delta_mm = [action[i] * 1000 for i in range(3)]
    delta_deg = [action[i+3] * 57.2958 for i in range(3)]

    # 안전 클램프
    delta_mm = [max(-200, min(200, d)) for d in delta_mm]
    delta_deg = [max(-30, min(30, d)) for d in delta_deg]

    target = [
        current_pose[0] + delta_mm[0],
        current_pose[1] + delta_mm[1],
        current_pose[2] + delta_mm[2],
        current_pose[3] + delta_deg[0],
        current_pose[4] + delta_deg[1],
        current_pose[5] + delta_deg[2],
    ]

    return target


# ──────────────────────────────────────────────────────────────────────────────
# 실제 VLA API 호출
# ──────────────────────────────────────────────────────────────────────────────

def call_vla_api(state_vec, cam1, cam2, instruction, reset_episode: bool = False, timeout: int = 30) -> dict:
    """실제 VLA 서버(/predict) 호출.

    - state_vec: raw 단위(m/rad/ratio) 32-dim. 서버가 내부에서 QUANTILES 정규화함.
    - cam1 → base_image, cam2 → left_wrist_image (학습 rename_map: camera2→left_wrist_0_rgb).
    - 응답 action: 서버가 inverse MIN_MAX 역정규화한 raw 값 (delta=m/rad, gripper=ratio 0.811~1.0).
    """
    base_b64 = encode_image_to_base64(cam1) if cam1 is not None else None
    wrist_b64 = encode_image_to_base64(cam2) if cam2 is not None else None
    if base_b64 is None:
        raise RuntimeError("base_image(카메라1) 없음 — 추론 불가")

    payload = {
        "state": [float(x) for x in state_vec],
        "base_image": base_b64,
        "left_wrist_image": wrist_b64,     # camera2 → left_wrist_0_rgb (학습과 동일)
        "right_wrist_image": None,         # 학습에 없음 → 서버가 더미 처리
        "instruction": instruction,
        "reset_episode": bool(reset_episode),
    }
    req = urllib.request.Request(
        f"{VLA_API_URL}/predict",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())

    # 표시 호환을 위해 요청값 보강
    data["instruction"] = instruction
    data["reset_episode"] = reset_episode
    return data


# ──────────────────────────────────────────────────────────────────────────────
# Streamlit UI
# ──────────────────────────────────────────────────────────────────────────────

st.title("VLA 추론 테스트 (실제 API)")
st.caption(f"🌐 서버: {VLA_API_URL}/predict")

# 그리퍼 초기값
gripper_raw = 600  # 0-740 범위
gripper_percent = (gripper_raw / 740) * 100  # 퍼센트로 변환
reset_episode = False

with st.spinner("이미지 로드 중..."):
    cam1, cam2 = load_mock_images()

if cam1 is not None or cam2 is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("카메라 1 (base_image)")
        if cam1 is not None:
            st.image(cam1)
            st.caption(f"크기: {cam1.shape[1]}x{cam1.shape[0]}")
        else:
            st.error("카메라 1 이미지를 로드할 수 없습니다")

    with col2:
        st.subheader("카메라 2 (left_wrist_image)")
        if cam2 is not None:
            st.image(cam2)
            st.caption(f"크기: {cam2.shape[1]}x{cam2.shape[0]}")
        else:
            st.error("카메라 2 이미지를 로드할 수 없습니다")
else:
    st.error("이미지를 로드할 수 없습니다. 데이터 경로를 확인하세요.")

st.divider()

st.header("현재 로봇 상태")

st.caption(f"Episode {SAMPLE_EPISODE}, 첫 프레임 (관측된 TCP Pose)")

# Observation State에서 TCP 포즈 추출
tcp_x = SAMPLE_OBSERVATION_STATE[0] * 1000  # m → mm
tcp_y = SAMPLE_OBSERVATION_STATE[1] * 1000
tcp_z = SAMPLE_OBSERVATION_STATE[2] * 1000
tcp_rx = SAMPLE_OBSERVATION_STATE[3]  # rad
tcp_ry = SAMPLE_OBSERVATION_STATE[4]
tcp_rz = SAMPLE_OBSERVATION_STATE[5]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("위치 X", f"{tcp_x:.2f} mm")
with col2:
    st.metric("위치 Y", f"{tcp_y:.2f} mm")
with col3:
    st.metric("높이 Z", f"{tcp_z:.2f} mm")
with col4:
    st.metric("그리퍼", f"{gripper_raw}", delta="81%")

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("회전 Rx", f"{np.degrees(tcp_rx):.2f}°")
with col6:
    st.metric("회전 Ry", f"{np.degrees(tcp_ry):.2f}°")
with col7:
    st.metric("회전 Rz", f"{np.degrees(tcp_rz):.2f}°")

st.divider()

st.header("VLA 추론")

col_inst, col_btn = st.columns([3, 1])

with col_inst:
    instruction = st.text_input(
        "작업 지시문",
        value="Grasp the strawberry stem and pick it.",
        help="VLA에 전달할 작업 지시"
    )

with col_btn:
    st.write("")
    run_inference = st.button(
        "실행",
        key="run_inference_btn",
        use_container_width=True,
        type="primary"
    )

if run_inference:
    # State vector: 현재 TCP 포즈 + 그리퍼
    state_vec = np.array([
        tcp_x / 1000,  # mm → m
        tcp_y / 1000,
        tcp_z / 1000,
        tcp_rx,  # 라디안
        tcp_ry,
        tcp_rz,
        gripper_percent / 100,  # 퍼센트 → 비율
    ] + [0.0] * 25)

    with st.spinner(f"실제 VLA 추론 중... ({VLA_API_URL})"):
        try:
            vla_result = call_vla_api(state_vec, cam1, cam2, instruction, reset_episode)
        except Exception as e:
            st.error(f"VLA API 호출 실패: {e}")
            vla_result = None

    if vla_result is not None:
        st.session_state.last_inference = vla_result
        st.session_state.last_state = state_vec
        st.session_state.last_episode = SAMPLE_EPISODE

st.divider()

if "last_inference" in st.session_state:
    result = st.session_state.last_inference
    action = result['action']

    st.success("추론 완료")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("레이턴시", f"{result['latency_ms']:.1f} ms")
    with col2:
        st.metric("에피소드", f"Episode {st.session_state.last_episode}")
    with col3:
        st.metric("에피소드 리셋", "O" if result['reset_episode'] else "X")

    st.subheader("VLA Action 벡터")

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.metric("ΔX (mm)", f"{action[0]*1000:.1f}")
    with col2:
        st.metric("ΔY (mm)", f"{action[1]*1000:.1f}")
    with col3:
        st.metric("ΔZ (mm)", f"{action[2]*1000:.1f}")
    with col4:
        st.metric("ΔRx (°)", f"{action[3]*57.2958:.1f}")
    with col5:
        st.metric("ΔRy (°)", f"{action[4]*57.2958:.1f}")
    with col6:
        st.metric("ΔRz (°)", f"{action[5]*57.2958:.1f}")
    with col7:
        # 실서버 action[6] = ratio(0.811~1.0) → ×740으로 raw 환산 표시
        st.metric("Gripper", f"{action[6]*740:.0f} / 740", delta=f"ratio {action[6]:.3f}")

    st.subheader("계산된 목표 포즈")
    # 현재 TCP 포즈를 배열로 변환
    current_tcp = np.array([tcp_x, tcp_y, tcp_z,
                             np.degrees(tcp_rx), np.degrees(tcp_ry), np.degrees(tcp_rz)])
    target_pose = calculate_target_pose(current_tcp, action)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**위치 (mm)**")
        st.code(f"X: {target_pose[0]:.2f}\nY: {target_pose[1]:.2f}\nZ: {target_pose[2]:.2f}")
    with col2:
        st.write("**회전 (deg)**")
        st.code(f"Rx: {target_pose[3]:.2f}\nRy: {target_pose[4]:.2f}\nRz: {target_pose[5]:.2f}")

    with st.expander("상세 분석"):
        analysis_col1, analysis_col2 = st.columns(2)

        with analysis_col1:
            st.write("**선형 이동 분석**")
            deltas = [action[i]*1000 for i in range(3)]
            magnitude = math.sqrt(sum(d**2 for d in deltas))
            st.metric("전체 이동 거리", f"{magnitude:.2f} mm")
            for name, val in [("X", deltas[0]), ("Y", deltas[1]), ("Z", deltas[2])]:
                st.write(f"Δ{name}: {val:+.2f} mm")

        with analysis_col2:
            st.write("**회전 분석**")
            rots = [action[i+3]*57.2958 for i in range(3)]
            magnitude_rot = math.sqrt(sum(r**2 for r in rots))
            st.metric("전체 회전각", f"{magnitude_rot:.2f}°")
            for name, val in [("Rx", rots[0]), ("Ry", rots[1]), ("Rz", rots[2])]:
                st.write(f"Δ{name}: {val:+.2f}°")

    with st.expander("모든 데이터 보기"):
        st.write(f"**Full Action Vector ({len(action)}-dim)**")
        action_df = {
            "Index": list(range(len(action))),
            "Value": [f"{v:.6f}" for v in action]
        }
        st.dataframe(action_df, use_container_width=True)

        st.write("**Input State Vector (raw, 서버가 정규화)**")
        state_vec = st.session_state.last_state
        state_df = {
            "Index": list(range(len(state_vec))),
            "Value": [f"{v:.6f}" for v in state_vec]
        }
        st.dataframe(state_df, use_container_width=True)

else:
    st.info("추론을 실행하면 결과가 여기에 표시됩니다")

st.divider()
st.caption(f"VLA 실제 API 테스트 앱 | 서버: {VLA_API_URL} | 대시보드: http://localhost:8765")
