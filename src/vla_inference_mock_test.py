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
    Path("/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.5.0"),
    Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.5.0"),
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

# ──────────────────────────────────────────────────────────────────────────────
# 데이터 로드 (캐시)
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def load_full_df():
    import pandas as pd
    return pd.read_parquet(DATA_DIR / "data/chunk-000/file-000.parquet")

@st.cache_resource
def load_info():
    import json
    with open(DATA_DIR / "meta/info.json") as f:
        return json.load(f)

def load_episode_df(episode: int):
    df = load_full_df()
    return df[df["episode_index"] == episode].sort_values("frame_index").reset_index(drop=True)


def extract_frame(mp4_path: Path, frame_index: int) -> Optional[np.ndarray]:
    """MP4 파일에서 지정 프레임 추출"""
    if not mp4_path.exists():
        return None
    try:
        cap = cv2.VideoCapture(str(mp4_path))
        if not cap.isOpened():
            return None
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None
    except Exception:
        return None



def encode_image_to_base64(image: np.ndarray) -> str:
    """이미지를 base64 문자열로 인코딩"""
    try:
        from PIL import Image
        pil_img = Image.fromarray(image.astype(np.uint8))
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
st.caption(f"🌐 서버: {VLA_API_URL}/predict  |  데이터셋: {DATA_DIR.name}")

# ── 에피소드 선택 ─────────────────────────────────────────────────────────────
total_episodes = load_info().get("total_episodes", 32)
selected_episode = st.number_input(
    "에피소드 선택",
    min_value=0, max_value=total_episodes - 1, value=0, step=1,
    key="episode_selector",
)

# 에피소드 바뀌면 프레임 슬라이더 리셋
if st.session_state.get("_last_episode") != selected_episode:
    st.session_state["_last_episode"] = selected_episode
    st.session_state["frame_slider"] = 0

# ── 에피소드 데이터 로드 ──────────────────────────────────────────────────────
ep_df = load_episode_df(selected_episode)
total_frames = len(ep_df)
_grip_rows = ep_df[ep_df["action"].apply(lambda x: x[6] > 0.85)]["frame_index"]
grip_change_frame = int(_grip_rows.min()) if len(_grip_rows) > 0 else None

# ── 프레임 선택 슬라이더 ──────────────────────────────────────────────────────
st.subheader("프레임 선택")
if "_pending_frame" in st.session_state:
    st.session_state["frame_slider"] = st.session_state.pop("_pending_frame")
_grip_label = f"파지 시점: {grip_change_frame}" if grip_change_frame is not None else "파지 없음"
selected_frame = st.slider(
    f"Episode {selected_episode} — 프레임 (총 {total_frames}개, {_grip_label})",
    min_value=0,
    max_value=total_frames - 1,
    value=0,
    key="frame_slider",
    step=1,
)

row = ep_df[ep_df["frame_index"] == selected_frame].iloc[0]
state_arr = row["observation.state"]   # [x,y,z,rx,ry,rz,grip]
gt_action  = row["action"]             # [dx,dy,dz,drx,dry,drz,grip_next]

# ── 액션 타임라인 차트 ────────────────────────────────────────────────────────
with st.expander("액션 타임라인 차트", expanded=True):
    try:
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        actions_mat = np.stack(ep_df["action"].values)  # (N, 7)
        frames_idx  = ep_df["frame_index"].values

        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            subplot_titles=("위치 델타 (mm)", "그리퍼 다음 상태 (/ 740)"),
            vertical_spacing=0.15,
        )
        _mk = dict(size=4, opacity=0.6)
        fig.add_trace(go.Scatter(x=frames_idx, y=actions_mat[:, 0] * 1000,
                                 name="ΔX (mm)", mode="lines+markers", marker=_mk,
                                 line=dict(color="#EF4444", width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=frames_idx, y=actions_mat[:, 1] * 1000,
                                 name="ΔY (mm)", mode="lines+markers", marker=_mk,
                                 line=dict(color="#22C55E", width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=frames_idx, y=actions_mat[:, 2] * 1000,
                                 name="ΔZ (mm)", mode="lines+markers", marker=_mk,
                                 line=dict(color="#3B82F6", width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=frames_idx, y=actions_mat[:, 6] * 740,
                                 name="Grip_next", mode="lines+markers", marker=_mk,
                                 line=dict(color="#F59E0B", width=1.5)), row=2, col=1)

        fig.add_vline(x=selected_frame, line_width=2, line_color="#FACC15",
                      annotation_text=f"F{selected_frame}", annotation_position="top right")
        if grip_change_frame is not None:
            fig.add_vline(x=grip_change_frame, line_width=1.5, line_dash="dash", line_color="#C084FC",
                          annotation_text=f"파지 F{grip_change_frame}", annotation_position="top left")

        fig.update_layout(height=420, margin=dict(t=50, b=30, l=60, r=20),
                          template="plotly_dark", legend=dict(orientation="h", y=1.08),
                          clickmode="event+select")
        fig.update_xaxes(title_text="Frame (클릭하면 해당 프레임으로 이동)", row=2, col=1)
        fig.update_yaxes(title_text="mm", row=1, col=1)
        fig.update_yaxes(title_text="/ 740", row=2, col=1)

        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
        if event and event.selection and event.selection.points:
            clicked_x = int(round(event.selection.points[0]["x"]))
            clicked_x = max(0, min(total_frames - 1, clicked_x))
            if clicked_x != st.session_state.get("_chart_last_click"):
                st.session_state["_chart_last_click"] = clicked_x
                st.session_state["_pending_frame"] = clicked_x
                st.rerun()
    except ImportError:
        st.warning("plotly 미설치 — `pip install plotly` 후 재시작하세요.")

# ── 이미지 로드 ───────────────────────────────────────────────────────────────
cam1 = extract_frame(CAM1_DIR / f"file-{selected_episode:03d}.mp4", selected_frame)
cam2 = extract_frame(CAM2_DIR / f"file-{selected_episode:03d}.mp4", selected_frame)

col1, col2 = st.columns(2)
with col1:
    st.subheader("카메라 1 (base_image)")
    if cam1 is not None:
        st.image(cam1)
        st.caption(f"{cam1.shape[1]}×{cam1.shape[0]}")
    else:
        st.error("카메라 1 이미지 없음")
with col2:
    st.subheader("카메라 2 (left_wrist_image)")
    if cam2 is not None:
        st.image(cam2)
        st.caption(f"{cam2.shape[1]}×{cam2.shape[0]}")
    else:
        st.error("카메라 2 이미지 없음")

st.divider()

# ── 현재 로봇 상태 ────────────────────────────────────────────────────────────
st.header("현재 로봇 상태")
if grip_change_frame is not None:
    grip_phase = "파지 후" if state_arr[6] >= 1.0 else ("파지 시점" if selected_frame == grip_change_frame else ("파지 전" if selected_frame < grip_change_frame else "파지 전"))
else:
    grip_phase = "파지 없음"
st.caption(f"Episode {selected_episode}, frame {selected_frame} / {total_frames-1}  —  {grip_phase}")

tcp_x  = state_arr[0] * 1000
tcp_y  = state_arr[1] * 1000
tcp_z  = state_arr[2] * 1000
tcp_rx = state_arr[3]
tcp_ry = state_arr[4]
tcp_rz = state_arr[5]
gripper_raw = round(state_arr[6] * 740)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("위치 X", f"{tcp_x:.2f} mm")
with col2:
    st.metric("위치 Y", f"{tcp_y:.2f} mm")
with col3:
    st.metric("높이 Z", f"{tcp_z:.2f} mm")
with col4:
    st.metric("그리퍼", f"{gripper_raw} / 740", delta=f"ratio {state_arr[6]:.3f}")

col5, col6, col7 = st.columns(3)
with col5:
    st.metric("회전 Rx", f"{np.degrees(tcp_rx):.2f}°")
with col6:
    st.metric("회전 Ry", f"{np.degrees(tcp_ry):.2f}°")
with col7:
    st.metric("회전 Rz", f"{np.degrees(tcp_rz):.2f}°")

# ── 정답 액션 ─────────────────────────────────────────────────────────────────
with st.expander("정답 액션 (GT)", expanded=True):
    gc1, gc2, gc3, gc4, gc5, gc6, gc7 = st.columns(7)
    dx_mm   = float(gt_action[0]) * 1000
    dy_mm   = float(gt_action[1]) * 1000
    dz_mm   = float(gt_action[2]) * 1000
    drx_deg = float(gt_action[3]) * 57.2958
    dry_deg = float(gt_action[4]) * 57.2958
    drz_deg = float(gt_action[5]) * 57.2958
    grip_raw = float(gt_action[6]) * 740
    for col_ui, label, val in zip(
        [gc1, gc2, gc3, gc4, gc5, gc6, gc7],
        ["ΔX (mm)", "ΔY (mm)", "ΔZ (mm)", "ΔRx (°)", "ΔRy (°)", "ΔRz (°)", "Grip_next"],
        [dx_mm, dy_mm, dz_mm, drx_deg, dry_deg, drz_deg, grip_raw],
    ):
        with col_ui:
            if label == "Grip_next":
                st.metric(label, f"{val:.0f} / 740", delta=f"ratio {float(gt_action[6]):.3f}")
            else:
                st.metric(label, f"{val:.3f}")

st.divider()

# ── VLA 추론 ──────────────────────────────────────────────────────────────────
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
    run_inference = st.button("실행", key="run_inference_btn", use_container_width=True, type="primary")

reset_episode = st.checkbox(
    "reset_episode (매 추론마다 큐 초기화 — 테스트 시 항상 켜야 함)",
    value=True,
    help="pi05는 chunk_size=50 액션 큐를 씁니다. False면 이전 추론 결과를 그대로 반환해 프레임을 바꿔도 같은 값이 나옵니다."
)

if run_inference:
    state_vec = np.array(list(state_arr) + [0.0] * 25)

    with st.spinner(f"실제 VLA 추론 중... ({VLA_API_URL})"):
        try:
            vla_result = call_vla_api(state_vec, cam1, cam2, instruction, reset_episode)
        except Exception as e:
            st.error(f"VLA API 호출 실패: {e}")
            vla_result = None

    if vla_result is not None:
        st.session_state.last_inference = vla_result
        st.session_state.last_state = state_vec
        st.session_state.last_frame = selected_frame

st.divider()

if "last_inference" in st.session_state:
    result = st.session_state.last_inference
    action = result["action"]
    inferred_frame = st.session_state.get("last_frame", "?")

    st.success(f"추론 완료 (frame {inferred_frame})")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("레이턴시", f"{result['latency_ms']:.1f} ms")
    with col2:
        st.metric("에피소드", f"Episode {selected_episode}")
    with col3:
        st.metric("에피소드 리셋", "O" if result["reset_episode"] else "X")

    st.subheader("모델 출력 vs 정답 비교")

    # 정답은 추론 당시 프레임 기준
    gt_row = ep_df[ep_df["frame_index"] == inferred_frame]
    gt_a = gt_row.iloc[0]["action"] if len(gt_row) else [0]*7

    header_cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
    for col_ui, label in zip(header_cols[1:], ["ΔX(mm)", "ΔY(mm)", "ΔZ(mm)", "ΔRx(°)", "ΔRy(°)", "ΔRz(°)", "Grip/740"]):
        col_ui.markdown(f"**{label}**")

    scales = [1000, 1000, 1000, 57.2958, 57.2958, 57.2958, 740]
    row_cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
    row_cols[0].markdown("**모델 (역정규화)**")
    for col_ui, val, scale in zip(row_cols[1:], action[:7], scales):
        col_ui.markdown(f"{val*scale:.1f}")

    gt_vals_disp = [
        float(gt_a[0])*1000, float(gt_a[1])*1000, float(gt_a[2])*1000,
        float(gt_a[3])*57.2958, float(gt_a[4])*57.2958, float(gt_a[5])*57.2958,
        float(gt_a[6])*740,
    ]
    row_cols2 = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
    row_cols2[0].markdown("**정답**")
    for col_ui, val in zip(row_cols2[1:], gt_vals_disp):
        col_ui.markdown(f"{val:.3f}")

    raw_action = result.get("raw_action")
    if raw_action is not None:
        st.caption("raw_action: 모델이 직접 출력한 정규화 공간 값 [-1, 1]. 역정규화 전.")
        raw_header = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
        for col_ui, label in zip(raw_header[1:], ["ΔX", "ΔY", "ΔZ", "ΔRx", "ΔRy", "ΔRz", "Grip"]):
            col_ui.markdown(f"**{label}**")
        row_raw = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
        row_raw[0].markdown("**raw (정규화)**")
        for col_ui, val in zip(row_raw[1:], raw_action[:7]):
            col_ui.markdown(f"{float(val):.3f}")

    st.subheader("계산된 목표 포즈")
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

    with st.expander("모든 데이터 보기"):
        st.write(f"**Full Action Vector — 역정규화 ({len(action)}-dim)**")
        st.dataframe({"Index": list(range(len(action))), "Value": [f"{v:.6f}" for v in action]},
                     use_container_width=True)
        if raw_action is not None:
            st.write(f"**Full Raw Action Vector — 정규화 공간 ({len(raw_action)}-dim)**")
            st.dataframe({"Index": list(range(len(raw_action))), "Value": [f"{float(v):.6f}" for v in raw_action]},
                         use_container_width=True)
        st.write("**Input State Vector (raw)**")
        sv = st.session_state.last_state
        st.dataframe({"Index": list(range(len(sv))), "Value": [f"{v:.6f}" for v in sv]},
                     use_container_width=True)

else:
    st.info("추론을 실행하면 결과가 여기에 표시됩니다")

st.divider()
st.caption(f"VLA 실제 API 테스트 앱 | 서버: {VLA_API_URL} | 대시보드: http://localhost:8765")
