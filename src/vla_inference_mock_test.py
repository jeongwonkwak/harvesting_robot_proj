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
    Path("/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.5.2"),
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
CHUNK_SIZE = 50   # pi05 action chunk 길이 (서버 큐를 비우며 전체 수집할 때 사용)

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


def dim_names(kind: str) -> list:
    """32-dim 벡터의 차원 이름. kind: 'action' 또는 'state'"""
    if kind == "action":
        names = ["dx_m", "dy_m", "dz_m", "drx_rad", "dry_rad", "drz_rad", "grip_next"]
    else:
        names = ["x_m", "y_m", "z_m", "rx_rad", "ry_rad", "rz_rad", "gripper"]
    return names + [f"pad_{i}" for i in range(25)]


def dim_converted(values) -> list:
    """raw 값(m/rad/ratio)을 읽기 쉬운 단위(mm / ° / ×740 raw)로 환산한 문자열 목록."""
    out = []
    for i, v in enumerate(values):
        v = float(v)
        if i < 3:
            out.append(f"{v * 1000:.2f} mm")
        elif i < 6:
            out.append(f"{v * 57.2958:.3f} °")
        elif i == 6:
            out.append(f"{v * 740:.0f} /740")
        else:
            out.append("-")
    return out


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
        value="Approach to the strawberry stem.",
        help="VLA에 전달할 작업 지시"
    )
with col_btn:
    st.write("")
    run_inference = st.button("실행", key="run_inference_btn", use_container_width=True, type="primary")

reset_episode = st.checkbox(
    "reset_episode (매 추론마다 큐 초기화)",
    value=True,
    help="pi05는 chunk_size=50 액션 큐를 씁니다. 켜면 매번 새로 추론(프레임별 테스트용), "
         "끄면 서버가 큐에서 순차적으로 꺼내줍니다 — 끈 상태로 연속 실행하면 아래 "
         "'추론 호출 히스토리'에서 청크 소비 과정과 레이턴시 변화(큐에서 꺼낼 땐 급감)를 관찰할 수 있습니다."
)

extract_chunk = st.button(
    f"청크 전체 추출 — 현재 프레임에서 새 청크 생성 후 {CHUNK_SIZE}개 모두 수신",
    key="extract_chunk_btn", use_container_width=True,
    help="첫 호출만 reset_episode=True로 새 청크를 만들고, 이후 reset_episode=False로 "
         f"{CHUNK_SIZE - 1}번 더 호출해 서버 큐를 끝까지 비우며 전체 액션을 수집합니다. "
         "reset_episode 체크박스와 무관하게 동작합니다."
)

if extract_chunk:
    state_vec = np.array(list(state_arr) + [0.0] * 25)
    _chunk_results = []
    _prog = st.progress(0.0, text="청크 추출 중...")
    try:
        for i in range(CHUNK_SIZE):
            res = call_vla_api(state_vec, cam1, cam2, instruction, reset_episode=(i == 0))
            # 서버가 청크 전체를 한 번에 주는 경우(action_chunk 필드) 추가 호출 불필요
            if i == 0 and isinstance(res.get("action_chunk"), list) and len(res["action_chunk"]) > 1:
                _chunk_results = [
                    {"action": a, "latency_ms": res["latency_ms"] if j == 0 else 0.0}
                    for j, a in enumerate(res["action_chunk"])
                ]
                break
            _chunk_results.append(res)
            _prog.progress((i + 1) / CHUNK_SIZE, text=f"청크 추출 중... {i + 1}/{CHUNK_SIZE}")
    except Exception as e:
        st.warning(f"{len(_chunk_results)}개 수신 후 중단: {e}")
    _prog.empty()
    if _chunk_results:
        st.session_state.last_chunk = {
            "episode": selected_episode,
            "frame": selected_frame,
            "results": _chunk_results,
        }

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
        # 호출 히스토리 누적 (reset_episode=False일 때 큐 소비 과정 관찰용)
        _hist = st.session_state.setdefault("inference_history", [])
        _hist.append({
            "call": len(_hist) + 1,
            "frame": selected_frame,
            "reset": bool(reset_episode),
            "latency_ms": float(vla_result.get("latency_ms", 0.0)),
            "action": [float(v) for v in vla_result["action"][:7]],
        })

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
        st.dataframe({
            "Index": list(range(len(action))),
            "이름": dim_names("action")[:len(action)],
            "Value (raw)": [f"{float(v):.6f}" for v in action],
            "환산": dim_converted(action),
        }, use_container_width=True)
        if raw_action is not None:
            st.write(f"**Full Raw Action Vector — 정규화 공간 ({len(raw_action)}-dim)**")
            st.dataframe({
                "Index": list(range(len(raw_action))),
                "이름": dim_names("action")[:len(raw_action)],
                "Value": [f"{float(v):.6f}" for v in raw_action],
            }, use_container_width=True)
        st.write("**Input State Vector (raw)**")
        sv = st.session_state.last_state
        st.dataframe({
            "Index": list(range(len(sv))),
            "이름": dim_names("state")[:len(sv)],
            "Value (raw)": [f"{float(v):.6f}" for v in sv],
            "환산": dim_converted(sv),
        }, use_container_width=True)

else:
    st.info("추론을 실행하면 결과가 여기에 표시됩니다")

# ── 액션 청크 전체 보기 ───────────────────────────────────────────────────────
if "last_chunk" in st.session_state:
    ck = st.session_state.last_chunk
    ck_res = ck["results"]
    st.divider()
    st.header(f"액션 청크 전체 — {len(ck_res)}개 (Episode {ck['episode']}, frame {ck['frame']}에서 시작)")

    # 큐 동작 진단: 첫 호출(실추론) vs 이후(큐 pop) 레이턴시
    _lat = [float(r.get("latency_ms", 0.0)) for r in ck_res]
    if len(_lat) > 1:
        _lat_rest = float(np.mean(_lat[1:]))
        _diag = ("큐 정상 동작 (이후 호출이 큐에서 pop)" if _lat_rest < _lat[0] * 0.3
                 else "주의: 이후 호출도 첫 호출과 레이턴시가 비슷함 — 서버가 매번 재추론 중일 가능성")
        st.caption(f"레이턴시 — 첫 호출(실추론): {_lat[0]:.0f} ms / 이후 평균: {_lat_rest:.0f} ms → {_diag}")

    # GT: 청크 시작 프레임부터 같은 길이만큼 (에피소드 끝에서 잘림)
    _gt_df = load_episode_df(ck["episode"])
    _gt_rows = _gt_df[_gt_df["frame_index"] >= ck["frame"]].sort_values("frame_index").head(len(ck_res))
    _gt_mat = np.stack(_gt_rows["action"].values) if len(_gt_rows) else None

    _ck_mat = np.array([[float(v) for v in r["action"][:7]] for r in ck_res])
    _steps = list(range(len(ck_res)))

    try:
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        fig_c = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            subplot_titles=("위치 델타 (mm) — 실선: 모델 청크 / 점선: GT(데이터셋)",
                            "그리퍼 (/740)"),
            vertical_spacing=0.15,
        )
        _mk_c = dict(size=4, opacity=0.7)
        for dim, color, label in [(0, "#EF4444", "ΔX"), (1, "#22C55E", "ΔY"), (2, "#3B82F6", "ΔZ")]:
            fig_c.add_trace(go.Scatter(
                x=_steps, y=_ck_mat[:, dim] * 1000,
                name=f"{label} 모델", mode="lines+markers", marker=_mk_c,
                line=dict(color=color, width=1.5)), row=1, col=1)
            if _gt_mat is not None:
                fig_c.add_trace(go.Scatter(
                    x=_steps[:len(_gt_mat)], y=_gt_mat[:, dim] * 1000,
                    name=f"{label} GT", mode="lines",
                    line=dict(color=color, width=1, dash="dash"), opacity=0.5), row=1, col=1)
        fig_c.add_trace(go.Scatter(
            x=_steps, y=_ck_mat[:, 6] * 740,
            name="Grip 모델", mode="lines+markers", marker=_mk_c,
            line=dict(color="#F59E0B", width=1.5)), row=2, col=1)
        if _gt_mat is not None:
            fig_c.add_trace(go.Scatter(
                x=_steps[:len(_gt_mat)], y=_gt_mat[:, 6] * 740,
                name="Grip GT", mode="lines",
                line=dict(color="#F59E0B", width=1, dash="dash"), opacity=0.5), row=2, col=1)

        fig_c.update_layout(height=480, margin=dict(t=50, b=30, l=60, r=20),
                            template="plotly_dark",
                            legend=dict(orientation="h", y=1.1))
        fig_c.update_xaxes(title_text="청크 내 스텝 # (= 시작 프레임으로부터의 미래 스텝)", row=2, col=1)
        fig_c.update_yaxes(title_text="mm", row=1, col=1)
        fig_c.update_yaxes(title_text="/ 740", row=2, col=1)
        st.plotly_chart(fig_c, use_container_width=True)
    except ImportError:
        st.warning("plotly 미설치 — 차트 생략")

    with st.expander(f"청크 {len(ck_res)}개 전체 테이블", expanded=False):
        import pandas as pd
        _ck_rows = []
        for i, r in enumerate(ck_res):
            a = [float(v) for v in r["action"][:7]]
            row_d = {
                "step": i,
                "latency(ms)": round(float(r.get("latency_ms", 0.0)), 1),
                "ΔX(mm)": round(a[0] * 1000, 2),
                "ΔY(mm)": round(a[1] * 1000, 2),
                "ΔZ(mm)": round(a[2] * 1000, 2),
                "ΔRx(°)": round(a[3] * 57.2958, 3),
                "ΔRy(°)": round(a[4] * 57.2958, 3),
                "ΔRz(°)": round(a[5] * 57.2958, 3),
                "Grip": round(a[6], 3),
            }
            if _gt_mat is not None and i < len(_gt_mat):
                row_d["GT ΔX(mm)"] = round(float(_gt_mat[i, 0]) * 1000, 2)
                row_d["GT ΔY(mm)"] = round(float(_gt_mat[i, 1]) * 1000, 2)
                row_d["GT ΔZ(mm)"] = round(float(_gt_mat[i, 2]) * 1000, 2)
            _ck_rows.append(row_d)
        st.dataframe(pd.DataFrame(_ck_rows), use_container_width=True, hide_index=True)

    if st.button("청크 결과 지우기", key="clear_chunk_btn"):
        del st.session_state["last_chunk"]
        st.rerun()

# ── 모델 진단 ─────────────────────────────────────────────────────────────────
st.divider()
st.header("모델 진단")
st.caption("청크(오픈루프)와 별개로, 모델이 관측에 따라 출력을 제대로 조절하는지 검사합니다.")

diag_c1, diag_c2 = st.columns(2)
with diag_c1:
    n_probe = st.number_input("샘플 프레임 수", min_value=3, max_value=30, value=8, step=1,
                              key="diag_n_probe")
    run_framewise = st.button(
        "프레임별 GT 추적 진단", key="run_framewise_btn", use_container_width=True,
        help="에피소드 전체에서 균등 간격으로 프레임을 골라 각각 새 추론(reset=True)을 하고 "
             "첫 액션을 그 프레임의 GT와 비교합니다. 상관이 0 근처면 모델이 가속/감속 위상을 "
             "관측에서 읽지 못하는 것입니다 (목표 지점 오버슈트 위험).",
    )
with diag_c2:
    n_repeat = st.number_input("반복 횟수", min_value=2, max_value=20, value=5, step=1,
                               key="diag_n_repeat")
    run_repeat = st.button(
        "현재 프레임 반복 분산 진단", key="run_repeat_btn", use_container_width=True,
        help="같은 입력으로 새 추론(reset=True)을 반복해 출력 분산을 측정합니다. "
             "표준편차가 출력 크기 대비 크면(예: 30% 이상) 수렴 부족 신호입니다.",
    )

diag_c3, diag_c4 = st.columns(2)
with diag_c3:
    ablation_frame_b = st.number_input(
        "교차 비교 프레임 B", min_value=0, max_value=total_frames - 1,
        value=max(0, total_frames - 5), step=1, key="diag_ablation_b",
        help="현재 프레임(A)과 교차 조합할 프레임. 기본값은 에피소드 종반.")
with diag_c4:
    st.write("")
    run_ablation = st.button(
        "입력 의존성 진단 (이미지/state 교차)", key="run_ablation_btn", use_container_width=True,
        help="A·B 프레임의 이미지와 state를 교차 조합해 4가지로 추론합니다(각 2회 평균). "
             "출력이 state 교체에만 반응하고 이미지 교체에 무반응이면 모델이 이미지를 무시하는 "
             "지름길(state-only) 학습 상태입니다.")

if run_ablation:
    _fb = int(ablation_frame_b)
    _f1b = extract_frame(CAM1_DIR / f"file-{selected_episode:03d}.mp4", _fb)
    _f2b = extract_frame(CAM2_DIR / f"file-{selected_episode:03d}.mp4", _fb)
    _row_b = ep_df[ep_df["frame_index"] == _fb].iloc[0]
    _sv_a = np.array(list(state_arr) + [0.0] * 25)
    _sv_b = np.array(list(_row_b["observation.state"]) + [0.0] * 25)
    _combos = [("이미지A + stateA", cam1, cam2, _sv_a), ("이미지B + stateA", _f1b, _f2b, _sv_a),
               ("이미지A + stateB", cam1, cam2, _sv_b), ("이미지B + stateB", _f1b, _f2b, _sv_b)]
    _ab_out = {}
    _prog = st.progress(0.0, text="입력 의존성 진단 중...")
    try:
        for _k, (_nm, _i1, _i2, _sv) in enumerate(_combos):
            _accs = []
            for _ in range(2):
                _res = call_vla_api(_sv, _i1, _i2, instruction, reset_episode=True)
                _accs.append([float(v) for v in _res["action"][:3]])
            _ab_out[_nm] = np.mean(_accs, axis=0).tolist()
            _prog.progress((_k + 1) / len(_combos), text=f"입력 의존성 진단 중... {_k + 1}/4")
    except Exception as e:
        st.warning(f"중단: {e}")
    _prog.empty()
    if len(_ab_out) == 4:
        st.session_state.ablation_probe = {
            "episode": selected_episode, "fa": selected_frame, "fb": _fb, "out": _ab_out,
            "gt_a": [float(v) for v in gt_action[:3]],
            "gt_b": [float(v) for v in _row_b["action"][:3]],
        }

if run_framewise:
    _idxs = sorted(set(np.linspace(0, total_frames - 1, int(n_probe)).round().astype(int).tolist()))
    _fw_rows = []
    _prog = st.progress(0.0, text="프레임별 추적 진단 중...")
    try:
        for _k, _fidx in enumerate(_idxs):
            _f1 = extract_frame(CAM1_DIR / f"file-{selected_episode:03d}.mp4", int(_fidx))
            _f2 = extract_frame(CAM2_DIR / f"file-{selected_episode:03d}.mp4", int(_fidx))
            _row = ep_df[ep_df["frame_index"] == _fidx].iloc[0]
            _sv = np.array(list(_row["observation.state"]) + [0.0] * 25)
            _res = call_vla_api(_sv, _f1, _f2, instruction, reset_episode=True)
            _fw_rows.append({"frame": int(_fidx),
                             "model": [float(v) for v in _res["action"][:3]],
                             "gt": [float(v) for v in _row["action"][:3]]})
            _prog.progress((_k + 1) / len(_idxs), text=f"프레임별 추적 진단 중... {_k + 1}/{len(_idxs)}")
    except Exception as e:
        st.warning(f"{len(_fw_rows)}개 수행 후 중단: {e}")
    _prog.empty()
    if _fw_rows:
        st.session_state.framewise_probe = {"episode": selected_episode, "rows": _fw_rows}

if run_repeat:
    _sv = np.array(list(state_arr) + [0.0] * 25)
    _rp_outs = []
    _prog = st.progress(0.0, text="반복 분산 진단 중...")
    try:
        for _i in range(int(n_repeat)):
            _res = call_vla_api(_sv, cam1, cam2, instruction, reset_episode=True)
            _raw = _res.get("raw_action") or [float("nan")] * 7
            _rp_outs.append({"action": [float(v) for v in _res["action"][:7]],
                             "raw": [float(v) for v in _raw[:7]]})
            _prog.progress((_i + 1) / int(n_repeat), text=f"반복 분산 진단 중... {_i + 1}/{n_repeat}")
    except Exception as e:
        st.warning(f"{len(_rp_outs)}회 수행 후 중단: {e}")
    _prog.empty()
    if _rp_outs:
        st.session_state.repeat_probe = {"episode": selected_episode, "frame": selected_frame,
                                         "outs": _rp_outs,
                                         "gt": [float(v) for v in gt_action[:7]]}

if "framewise_probe" in st.session_state:
    fw = st.session_state.framewise_probe
    with st.expander(f"프레임별 GT 추적 결과 — Episode {fw['episode']}, {len(fw['rows'])}개 프레임",
                     expanded=True):
        _m = np.array([r["model"] for r in fw["rows"]])
        _g = np.array([r["gt"] for r in fw["rows"]])
        _fx = [r["frame"] for r in fw["rows"]]

        mc1, mc2, mc3 = st.columns(3)
        _dim_info = [("ΔX", "#EF4444"), ("ΔY", "#22C55E"), ("ΔZ", "#3B82F6")]
        _corrs = []
        for _d, (_col_ui, (_nm, _)) in enumerate(zip([mc1, mc2, mc3], _dim_info)):
            _corr = (float(np.corrcoef(_m[:, _d], _g[:, _d])[0, 1])
                     if _g[:, _d].std() > 1e-12 and _m[:, _d].std() > 1e-12 else float("nan"))
            _amp = float(np.abs(_m[:, _d]).mean() / max(np.abs(_g[:, _d]).mean(), 1e-12))
            _corrs.append(_corr)
            _col_ui.metric(f"{_nm} 상관", f"{_corr:+.2f}", delta=f"진폭비 {_amp:.2f}")
        _c_mean = np.nanmean(_corrs)
        if _c_mean > 0.7:
            st.caption("판정: 위상 추적 양호 — 모델이 관측에 따라 속도를 조절하고 있습니다.")
        elif _c_mean > 0.3:
            st.caption("판정: 부분 추적 — 방향은 따라가나 가속/감속 타이밍이 어긋납니다.")
        else:
            st.caption("판정: 위상 추적 실패 — 출력이 GT 프로파일과 무관합니다. "
                       "관측→속도 매핑을 못 배운 상태로, 폐루프 시 목표 오버슈트 위험이 큽니다.")

        try:
            import plotly.graph_objects as go
            fig_fw = go.Figure()
            for _d, (_nm, _color) in enumerate(_dim_info):
                fig_fw.add_trace(go.Scatter(x=_fx, y=_m[:, _d] * 1000, name=f"{_nm} 모델",
                                            mode="lines+markers",
                                            line=dict(color=_color, width=2)))
                fig_fw.add_trace(go.Scatter(x=_fx, y=_g[:, _d] * 1000, name=f"{_nm} GT",
                                            mode="lines", opacity=0.5,
                                            line=dict(color=_color, width=1, dash="dash")))
            fig_fw.update_layout(height=340, template="plotly_dark",
                                 margin=dict(t=30, b=30, l=60, r=20),
                                 legend=dict(orientation="h", y=1.12),
                                 xaxis_title="Frame", yaxis_title="mm")
            st.plotly_chart(fig_fw, use_container_width=True)
        except ImportError:
            pass
        if st.button("추적 결과 지우기", key="clear_framewise_btn"):
            del st.session_state["framewise_probe"]
            st.rerun()

if "repeat_probe" in st.session_state:
    rp = st.session_state.repeat_probe
    with st.expander(f"반복 분산 결과 — Episode {rp['episode']}, frame {rp['frame']}, "
                     f"{len(rp['outs'])}회", expanded=True):
        import pandas as pd
        _acts = np.array([o["action"][:3] for o in rp["outs"]])
        _rows_rp = [{"회차": _i + 1,
                     "ΔX(mm)": round(o["action"][0] * 1000, 2),
                     "ΔY(mm)": round(o["action"][1] * 1000, 2),
                     "ΔZ(mm)": round(o["action"][2] * 1000, 2),
                     "raw ΔX": round(o["raw"][0], 3),
                     "raw ΔY": round(o["raw"][1], 3),
                     "raw ΔZ": round(o["raw"][2], 3)}
                    for _i, o in enumerate(rp["outs"])]
        _rows_rp.append({"회차": "평균±표준편차",
                         "ΔX(mm)": f"{_acts[:,0].mean()*1000:+.2f}±{_acts[:,0].std()*1000:.2f}",
                         "ΔY(mm)": f"{_acts[:,1].mean()*1000:+.2f}±{_acts[:,1].std()*1000:.2f}",
                         "ΔZ(mm)": f"{_acts[:,2].mean()*1000:+.2f}±{_acts[:,2].std()*1000:.2f}",
                         "raw ΔX": "", "raw ΔY": "", "raw ΔZ": ""})
        _rows_rp.append({"회차": "GT",
                         "ΔX(mm)": round(float(rp["gt"][0]) * 1000, 2),
                         "ΔY(mm)": round(float(rp["gt"][1]) * 1000, 2),
                         "ΔZ(mm)": round(float(rp["gt"][2]) * 1000, 2),
                         "raw ΔX": "", "raw ΔY": "", "raw ΔZ": ""})
        st.dataframe(pd.DataFrame(_rows_rp), use_container_width=True, hide_index=True)
        _cv = (_acts.std(0) / np.maximum(np.abs(_acts.mean(0)), 1e-12)).max()
        st.caption(f"최대 변동계수(표준편차/|평균|): {_cv:.2f} — "
                   + ("0.3 이하: 안정적" if _cv <= 0.3 else "0.3 초과: 출력 분산 큼 (수렴 부족 신호)"))
        if st.button("분산 결과 지우기", key="clear_repeat_btn"):
            del st.session_state["repeat_probe"]
            st.rerun()

if "ablation_probe" in st.session_state:
    ab = st.session_state.ablation_probe
    with st.expander(f"입력 의존성 결과 — Episode {ab['episode']}, "
                     f"A=frame {ab['fa']} / B=frame {ab['fb']}", expanded=True):
        import pandas as pd
        _names = ["이미지A + stateA", "이미지B + stateA", "이미지A + stateB", "이미지B + stateB"]
        _tbl = [{"조합": _nm,
                 "ΔX(mm)": round(ab["out"][_nm][0] * 1000, 2),
                 "ΔY(mm)": round(ab["out"][_nm][1] * 1000, 2),
                 "ΔZ(mm)": round(ab["out"][_nm][2] * 1000, 2)} for _nm in _names]
        _tbl.append({"조합": f"GT (frame {ab['fa']})",
                     "ΔX(mm)": round(ab["gt_a"][0] * 1000, 2),
                     "ΔY(mm)": round(ab["gt_a"][1] * 1000, 2),
                     "ΔZ(mm)": round(ab["gt_a"][2] * 1000, 2)})
        _tbl.append({"조합": f"GT (frame {ab['fb']})",
                     "ΔX(mm)": round(ab["gt_b"][0] * 1000, 2),
                     "ΔY(mm)": round(ab["gt_b"][1] * 1000, 2),
                     "ΔZ(mm)": round(ab["gt_b"][2] * 1000, 2)})
        st.dataframe(pd.DataFrame(_tbl), use_container_width=True, hide_index=True)

        _base = np.array(ab["out"]["이미지A + stateA"])
        _img_eff = float(np.linalg.norm(np.array(ab["out"]["이미지B + stateA"]) - _base)) * 1000
        _st_eff = float(np.linalg.norm(np.array(ab["out"]["이미지A + stateB"]) - _base)) * 1000
        _ratio = _img_eff / max(_st_eff, 1e-9)
        if _ratio < 0.2:
            _verdict = "이미지 무시 (지름길 학습 의심) — state dropout 또는 waypoint 액션 검토 필요"
        elif _ratio < 0.7:
            _verdict = "이미지 부분 사용 — 비전 기여가 약함"
        else:
            _verdict = "이미지·state 균형 사용"
        st.caption(f"이미지 교체 영향 {_img_eff:.2f} mm vs state 교체 영향 {_st_eff:.2f} mm "
                   f"(비율 {_ratio:.2f}) → {_verdict}")
        if st.button("의존성 결과 지우기", key="clear_ablation_btn"):
            del st.session_state["ablation_probe"]
            st.rerun()

# ── 추론 호출 히스토리 (액션 큐 관찰) ─────────────────────────────────────────
_history = st.session_state.get("inference_history", [])
if _history:
    st.divider()
    with st.expander(
        f"추론 호출 히스토리 — 누적 {len(_history)}회 "
        "(reset_episode를 끄고 연속 실행하면 청크 큐 소비 과정이 보입니다)",
        expanded=not reset_episode,
    ):
        if st.button("히스토리 지우기", key="clear_history_btn"):
            st.session_state["inference_history"] = []
            st.rerun()

        import pandas as pd
        _rows = []
        for h in _history:
            a = h["action"]
            _rows.append({
                "호출": h["call"],
                "frame": h["frame"],
                "reset": "O" if h["reset"] else "X",
                "latency(ms)": round(h["latency_ms"], 1),
                "ΔX(mm)": round(a[0] * 1000, 2),
                "ΔY(mm)": round(a[1] * 1000, 2),
                "ΔZ(mm)": round(a[2] * 1000, 2),
                "ΔRx(°)": round(a[3] * 57.2958, 3),
                "ΔRy(°)": round(a[4] * 57.2958, 3),
                "ΔRz(°)": round(a[5] * 57.2958, 3),
                "Grip": round(a[6], 3),
            })
        st.dataframe(pd.DataFrame(_rows), use_container_width=True, hide_index=True)

        try:
            from plotly.subplots import make_subplots
            import plotly.graph_objects as go

            _calls = [h["call"] for h in _history]
            fig_h = make_subplots(
                rows=2, cols=1, shared_xaxes=True,
                subplot_titles=(
                    "호출 순서별 위치 델타 (mm)",
                    "레이턴시 (ms) — 큐에서 꺼낼 땐 급감, 매번 비슷하면 서버가 매번 재추론 중",
                ),
                vertical_spacing=0.18,
            )
            _mk_h = dict(size=5, opacity=0.7)
            for dim, color, label in [(0, "#EF4444", "ΔX"), (1, "#22C55E", "ΔY"), (2, "#3B82F6", "ΔZ")]:
                fig_h.add_trace(go.Scatter(
                    x=_calls, y=[h["action"][dim] * 1000 for h in _history],
                    name=f"{label} (mm)", mode="lines+markers", marker=_mk_h,
                    line=dict(color=color, width=1.5)), row=1, col=1)
            fig_h.add_trace(go.Scatter(
                x=_calls, y=[h["latency_ms"] for h in _history],
                name="latency (ms)", mode="lines+markers", marker=_mk_h,
                line=dict(color="#F59E0B", width=1.5)), row=2, col=1)

            # reset=True였던 호출 표시 (새 청크 시작점)
            for h in _history:
                if h["reset"]:
                    fig_h.add_vline(x=h["call"], line_width=1, line_dash="dot",
                                    line_color="#C084FC")

            fig_h.update_layout(height=420, margin=dict(t=50, b=30, l=60, r=20),
                                template="plotly_dark",
                                legend=dict(orientation="h", y=1.1))
            fig_h.update_xaxes(title_text="호출 # (점선 = reset_episode=True, 새 청크 시작)", row=2, col=1)
            fig_h.update_yaxes(title_text="mm", row=1, col=1)
            fig_h.update_yaxes(title_text="ms", row=2, col=1)
            st.plotly_chart(fig_h, use_container_width=True)
        except ImportError:
            pass

st.divider()
st.caption(f"VLA 실제 API 테스트 앱 | 서버: {VLA_API_URL} | 대시보드: http://localhost:8765")
