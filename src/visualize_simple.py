#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import cv2
import json
import math
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

DATASET_DIR = Path('/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.3')
STATS_FILE = Path('/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.3/meta/stats.json')

# e0509 DH 파라미터
DH_PARAMS = [
    {"a": 0,      "d": 334,    "alpha": np.pi/2,   "offset": 0},
    {"a": 330,    "d": 0,      "alpha": 0,         "offset": 0},
    {"a": 304,    "d": 0,      "alpha": 0,         "offset": 0},
    {"a": 0,      "d": 332,    "alpha": np.pi/2,   "offset": 0},
    {"a": 0,      "d": 0,      "alpha": -np.pi/2,  "offset": 0},
    {"a": 0,      "d": 95,     "alpha": 0,         "offset": 0},
]

def dh_transform(a, d, alpha, theta):
    """DH 파라미터로부터 변환 행렬 계산"""
    c_theta = np.cos(theta)
    s_theta = np.sin(theta)
    c_alpha = np.cos(alpha)
    s_alpha = np.sin(alpha)

    T = np.array([
        [c_theta, -s_theta*c_alpha,  s_theta*s_alpha, a*c_theta],
        [s_theta,  c_theta*c_alpha, -c_theta*s_alpha, a*s_theta],
        [0,        s_alpha,          c_alpha,         d],
        [0,        0,                0,               1]
    ])
    return T

def rot_matrix_to_euler_zyx(R):
    """회전 행렬을 ZYX 오일러 각으로 변환"""
    sy = -R[2, 0]
    sy = np.clip(sy, -1, 1)
    y = np.arcsin(sy)

    if np.abs(np.cos(y)) > 1e-6:
        x = np.arctan2(R[2, 1], R[2, 2])
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = 0
        z = np.arctan2(-R[0, 1], R[1, 1])

    return np.array([x, y, z])

def tcp_to_joints_numeric(tcp_pose_mm_deg, initial_guess=None):
    """TCP Pose → Joint Angles (수치 역기구학)"""
    def forward_kinematics(joints_rad):
        T = np.eye(4)
        for i, params in enumerate(DH_PARAMS):
            theta = joints_rad[i] + params["offset"]
            T_i = dh_transform(
                params["a"] / 1000,
                params["d"] / 1000,
                params["alpha"],
                theta
            )
            T = T @ T_i

        pos_mm = T[:3, 3] * 1000
        euler_rad = rot_matrix_to_euler_zyx(T[:3, :3])
        return np.concatenate([pos_mm, euler_rad])

    def error_func(joints_rad):
        tcp_calc = forward_kinematics(joints_rad)
        tcp_target = np.array([
            tcp_pose_mm_deg[0], tcp_pose_mm_deg[1], tcp_pose_mm_deg[2],
            np.radians(tcp_pose_mm_deg[3]), np.radians(tcp_pose_mm_deg[4]), np.radians(tcp_pose_mm_deg[5])
        ])
        pos_error = np.sum((tcp_calc[:3] - tcp_target[:3]) ** 2)
        rot_error = np.sum((tcp_calc[3:] - tcp_target[3:]) ** 2) * 10000
        return pos_error + rot_error

    if initial_guess is None:
        x0 = np.zeros(6)
    else:
        x0 = np.array(initial_guess)

    try:
        from scipy.optimize import minimize
        result = minimize(error_func, x0, method='Nelder-Mead',
                         options={'maxiter': 1000, 'xatol': 1e-6, 'fatol': 1e-6})
        return result.x if result.fun < 0.01 else None
    except:
        return None

@st.cache_data
def load_data():
    df = pd.read_parquet(DATASET_DIR / 'data/chunk-000/file-000.parquet')
    epi = pd.read_parquet(DATASET_DIR / 'meta/episodes/chunk-000/file-000.parquet')
    return df, epi

@st.cache_data
def load_stats():
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            return json.load(f)
    return None

@st.cache_resource
def load_videos():
    cap1 = cv2.VideoCapture(str(list((DATASET_DIR / 'videos/observation.images.camera1/chunk-000').glob('*.mp4'))[0]))
    cap2 = cv2.VideoCapture(str(list((DATASET_DIR / 'videos/observation.images.camera2/chunk-000').glob('*.mp4'))[0]))
    return cap1, cap2

def get_img(cap, idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if ret else None

st.set_page_config(layout="wide")
st.markdown("""<style>
.stMetric{padding:0;margin:0;gap:0;}
[data-testid="metric-container"] > div:first-child {font-size: 7px !important; margin:0;padding:0;}
[data-testid="metric-container"] > div:last-child {font-size: 2px !important; margin:0;padding:0; line-height: 0.8;}
[data-testid="metric-container"] > div:last-child > div {font-size: 2px !important;}
[data-testid="metric-container"] > div:last-child > div > div {font-size: 2px !important;}
.stats-metric-container [data-testid="metric-container"] > div:last-child {font-size: 10px !important;}
.stats-metric-container [data-testid="metric-container"] > div:last-child > div > div {font-size: 10px !important;}
/* 테이블 폰트 크기 증대 */
.stDataFrame {
    font-size: 24px !important;
}
.stDataFrame thead th {
    font-size: 22px !important;
    padding: 25px !important;
}
.stDataFrame tbody td {
    font-size: 22px !important;
    padding: 25px !important;
}
div[data-testid="dataframe"] {
    font-size: 24px !important;
}
div[data-testid="dataframe"] th {
    font-size: 22px !important;
}
div[data-testid="dataframe"] td {
    font-size: 22px !important;
}
</style>""", unsafe_allow_html=True)

df, epi = load_data()
cap1, cap2 = load_videos()
stats = load_stats()

# 헤더
st.markdown("## 🤖 VLA Viewer")

# 에피소드 초기값 설정
ep = epi['episode_index'].values[0]
ep_data = df[df['episode_index'] == ep].reset_index(drop=True)

# 프레임 선택 및 에피소드 선택
col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 2.5, 0.8, 1.2])

with col1:
    if st.button("⬅️", use_container_width=True):
        if 'frame' not in st.session_state:
            st.session_state.frame = 0
        st.session_state.frame = max(0, st.session_state.frame - 1)

with col2:
    if st.button("➡️", use_container_width=True):
        if 'frame' not in st.session_state:
            st.session_state.frame = 0
        st.session_state.frame = min(len(ep_data)-1, st.session_state.frame + 1)

with col3:
    if 'frame' not in st.session_state:
        st.session_state.frame = 0
    frame = st.slider("Frame", 0, len(ep_data)-1, st.session_state.frame, label_visibility="collapsed")
    st.session_state.frame = frame

with col4:
    st.write(f"{frame} / {len(ep_data)-1}")

with col5:
    ep = st.selectbox("Episode", epi['episode_index'].values, format_func=lambda x: f"{x:03d}", label_visibility="collapsed")

# 선택한 에피소드로 데이터 업데이트
ep_data = df[df['episode_index'] == ep].reset_index(drop=True)
frame = min(frame, len(ep_data)-1)  # 프레임 범위 내 유지

st.divider()

# 그래프 - Episode Statistics (에피소드 선택 후)
st.markdown("### 📈 Episode Statistics")

# 통계 계산
episode_frames = df.groupby('episode_index').size()
total_episodes = len(episode_frames)
total_frames = episode_frames.sum()
avg_frames = episode_frames.mean()
max_frames = episode_frames.max()
min_frames = episode_frames.min()
total_duration = df['timestamp'].max() - df['timestamp'].min()
avg_duration_per_ep = total_duration / total_episodes

# 통계 메트릭 표시
stat_cols = st.columns(5)
with stat_cols[0]:
    st.metric("Total Episodes", int(total_episodes))
with stat_cols[1]:
    st.metric("Total Frames", int(total_frames))
with stat_cols[2]:
    st.metric("Avg Frames/Ep", f"{avg_frames:.1f}")
with stat_cols[3]:
    st.metric("Duration", f"{total_duration:.1f}s")
with stat_cols[4]:
    st.metric("Avg Duration/Ep", f"{avg_duration_per_ep:.1f}s")

# 그래프
fig, ax = plt.subplots(figsize=(12, 3))
colors = ['#FF6B6B' if idx == ep else '#4ECDC4' for idx in episode_frames.index]
bars = ax.bar(episode_frames.index, episode_frames.values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
ax.bar_label(bars, fontsize=7, padding=2)
ax.set_xlabel('Episode Index', fontsize=10, fontweight='bold')
ax.set_ylabel('Number of Frames', fontsize=10, fontweight='bold')
ax.set_xticks(episode_frames.index)
ax.set_xticklabels(episode_frames.index, rotation=45, ha='right', fontsize=8)
ax.grid(True, alpha=0.3, axis='y')
ax.tick_params(labelsize=9)
ax.axvline(ep-0.5, color='red', linestyle='--', alpha=0.7, linewidth=2, label=f'Current Episode: {ep}')
ax.axhline(avg_frames, color='green', linestyle=':', alpha=0.6, linewidth=1.5, label=f'Avg: {avg_frames:.1f}')
ax.legend(fontsize=9)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

# 현재 프레임
row = ep_data.iloc[frame]

# 정보 헤더
info_cols = st.columns(4)
with info_cols[0]:
    st.metric("Frame", int(row['frame_index']))
with info_cols[1]:
    st.metric("Time", f"{row['timestamp']:.2f}s")
with info_cols[2]:
    st.metric("Ep", f"{ep}/{len(epi)-1}")
with info_cols[3]:
    st.metric("Total", len(ep_data))

st.divider()

# 메인 - 4개 열
col1, col2, col3, col4 = st.columns([0.9, 1.05, 1.05, 1.05])

# 데이터 준비
state = row['observation.state']
tcp_pose = np.array([
    state[0] * 1000,  state[1] * 1000, state[2] * 1000,
    state[3], state[4], state[5],
])
state_len = len(state)
# 그리퍼 인덱스: 옛 13-dim[TCP6,Joint6,Grip]=12, v0.4.x 7-dim[x,y,z,rx,ry,rz,Grip]=6
if state_len >= 13:
    gripper_state = state[12]
elif state_len >= 7:
    gripper_state = state[6]
else:
    gripper_state = None
a = row['action']

# === Column 1: 카메라 ===
with col1:
    st.caption("Camera 1")
    img1 = get_img(cap1, frame)
    if img1 is not None:
        st.image(img1, width='stretch')

    st.caption("Camera 2")
    img2 = get_img(cap2, frame)
    if img2 is not None:
        st.image(img2, width='stretch')

# === Column 2: TCP + Gripper ===
with col2:
    st.markdown("<span style='font-size:12px'>**TCP + Gripper**</span>", unsafe_allow_html=True)
    tcp_items = []
    tcp_labels = ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']
    for i, label in enumerate(tcp_labels):
        if i < 3:
            val = f"{tcp_pose[i]:.2f} mm"
        else:
            val = f"{tcp_pose[i]:.4f} rad ({tcp_pose[i] * 180 / math.pi:.2f}°)"
        tcp_items.append({'Item': label, 'Value': val})

    if gripper_state is not None:
        gripper_raw = gripper_state * 740
        tcp_items.append({'Item': 'Gripper', 'Value': f'{gripper_raw:.0f} / 740'})

    st.dataframe(pd.DataFrame(tcp_items), use_container_width=True, hide_index=True)

# === Column 3: Joint ===
with col3:
    st.markdown("<span style='font-size:12px'>**Joint**</span>", unsafe_allow_html=True)
    joint_items = []
    if state_len >= 12:
        joints_rad = np.array(state[6:12])
        joints_deg = np.degrees(joints_rad)
        for i in range(6):
            joint_items.append({'Item': f'J{i+1}', 'Value': f"{joints_deg[i]:.2f}°"})
    else:
        tcp_mm_deg = np.array([
            tcp_pose[0], tcp_pose[1], tcp_pose[2],
            tcp_pose[3] * 180 / math.pi, tcp_pose[4] * 180 / math.pi, tcp_pose[5] * 180 / math.pi
        ])
        joints_rad = tcp_to_joints_numeric(tcp_mm_deg)
        if joints_rad is not None:
            joints_deg = np.degrees(joints_rad)
            for i in range(6):
                joint_items.append({'Item': f'J{i+1}', 'Value': f"{joints_deg[i]:.2f}°"})

    st.dataframe(pd.DataFrame(joint_items), use_container_width=True, hide_index=True)

# === Column 4: Action ===
with col4:
    st.markdown("<span style='font-size:12px'>**Action**</span>", unsafe_allow_html=True)
    action_labels_data = ['ΔX', 'ΔY', 'ΔZ', 'ΔRx', 'ΔRy', 'ΔRz', 'Grip']
    action_items = []
    for i, label in enumerate(action_labels_data):
        if i < 3:
            val = f"{a[i] * 1000:.5f} mm"
        elif i < 6:
            val = f"{a[i]:.5f} rad ({a[i] * 180 / math.pi:.2f}°)"
        else:
            val = f"{a[i]*740:.0f} / 740" if a[i] <= 1 else f"{a[i]:.0f} / 740"
        action_items.append({'Item': label, 'Value': val})

    st.dataframe(pd.DataFrame(action_items), use_container_width=True, hide_index=True)

st.divider()

# 전체 에피소드 프레임 표시
v_data = ep_data

# 데이터셋 형식 확인 (state 길이)
state_len = len(ep_data.iloc[0]['observation.state'])
has_joint_data = state_len >= 12

# === Row 1: TCP Pose, Action (EEF) ===
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.caption("TCP Pose Timeline")
    fig, axes = plt.subplots(2, 1, figsize=(7, 5))

    # Position (X, Y, Z in meters)
    for i in range(3):
        vals = [r['observation.state'][i] for _, r in v_data.iterrows()]
        label = ['X(m)', 'Y(m)', 'Z(m)'][i]
        axes[0].plot(v_data['timestamp'], vals, label=label, marker='o', markersize=2, linewidth=1)
    axes[0].axvline(row['timestamp'], color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    axes[0].set_ylabel('Position (m)', fontsize=8, fontweight='bold')
    axes[0].legend(ncol=3, fontsize=8, loc='upper left')
    axes[0].grid(True, alpha=0.2)
    axes[0].tick_params(labelsize=8)

    # Rotation (Rx, Ry, Rz in rad)
    for i in range(3):
        vals_rad = [r['observation.state'][i+3] for _, r in v_data.iterrows()]
        label_rad = ['Rx(rad)', 'Ry(rad)', 'Rz(rad)'][i]
        axes[1].plot(v_data['timestamp'], vals_rad, label=label_rad, marker='o', markersize=2, linewidth=1)

    axes[1].axvline(row['timestamp'], color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    axes[1].set_ylabel('Rotation (rad)', fontsize=8, fontweight='bold')
    axes[1].set_xlabel('Timestamp (s)', fontsize=8)
    axes[1].legend(ncol=3, fontsize=8, loc='upper left')
    axes[1].grid(True, alpha=0.2)
    axes[1].tick_params(labelsize=8)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with row1_col2:
    st.caption("Action (EEF) Timeline")
    fig, ax = plt.subplots(figsize=(7, 3))
    for i in range(6):  # A1~A6만 (ΔX, ΔY, ΔZ, ΔRx, ΔRy, ΔRz)
        vals = [r['action'][i] for _, r in v_data.iterrows()]
        label = ['ΔX', 'ΔY', 'ΔZ', 'ΔRx', 'ΔRy', 'ΔRz'][i]
        ax.plot(v_data['timestamp'], vals, label=label, marker='s', markersize=2, linewidth=1)
    ax.axvline(row['timestamp'], color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.legend(ncol=3, fontsize=8)
    ax.grid(True, alpha=0.2)
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# === Row 2: Gripper, Joint Angles ===
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.caption("Gripper Timeline")
    fig, ax = plt.subplots(figsize=(7, 3))
    grip_vals = [r['action'][6] for _, r in v_data.iterrows()]  # A7만 (Grip)
    ax.plot(v_data['timestamp'], grip_vals, label='Grip', marker='s', markersize=2, linewidth=1.5, color='purple')
    ax.axvline(row['timestamp'], color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)
    ax.tick_params(labelsize=8)
    ax.set_ylabel('Position (0~740)', fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

if has_joint_data:
    with row2_col2:
        st.caption("Joint Angles Timeline")
        fig, ax = plt.subplots(figsize=(7, 3))
        for i in range(6):
            vals = [r['observation.state'][6 + i] * 180 / math.pi for _, r in v_data.iterrows()]  # rad → deg
            ax.plot(v_data['timestamp'], vals, label=f'J{i+1}', marker='o', markersize=2, linewidth=1)
        ax.axvline(row['timestamp'], color='red', linestyle='--', alpha=0.5, linewidth=1.5)
        ax.legend(ncol=3, fontsize=8)
        ax.grid(True, alpha=0.2)
        ax.tick_params(labelsize=8)
        ax.set_ylabel('Degrees (°)', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

st.divider()

# ── 통계 정보 ───────────────────────────────────────────────────────────────
if stats:
    st.markdown("<h2 style='font-size:24px'>📊 Dataset Statistics</h2>", unsafe_allow_html=True)

    # TCP Pose 통계 (표)
    st.markdown("<span style='font-size:18px'>**Observation State (TCP Pose) Statistics**</span>", unsafe_allow_html=True)

    state_stats = stats.get('observation.state', {})
    rad_to_deg = 180 / math.pi

    # state 길이 확인
    mean_len = len(state_stats.get('mean', [0]*6))

    if mean_len >= 13:
        # EEF 포즈만 표시 (처음 6개)
        axes = ['X(m)', 'Y(m)', 'Z(m)', 'Rx(rad)', 'Ry(rad)', 'Rz(rad)']
        state_data = {
            'Axis': axes,
            'Mean': [f"{state_stats.get('mean', [0]*13)[i]:.6f}" + (f" ({state_stats.get('mean', [0]*13)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Std': [f"{state_stats.get('std', [0]*13)[i]:.6f}" + (f" ({state_stats.get('std', [0]*13)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Min': [f"{state_stats.get('min', [0]*13)[i]:.6f}" + (f" ({state_stats.get('min', [0]*13)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Max': [f"{state_stats.get('max', [0]*13)[i]:.6f}" + (f" ({state_stats.get('max', [0]*13)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
        }
    elif mean_len >= 12:
        # Joint State 포함 (12-dim, 그리퍼 없음)
        axes = ['X(m)', 'Y(m)', 'Z(m)', 'Rx(rad)', 'Ry(rad)', 'Rz(rad)']
        state_data = {
            'Axis': axes,
            'Mean': [f"{state_stats.get('mean', [0]*12)[i]:.6f}" + (f" ({state_stats.get('mean', [0]*12)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Std': [f"{state_stats.get('std', [0]*12)[i]:.6f}" + (f" ({state_stats.get('std', [0]*12)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Min': [f"{state_stats.get('min', [0]*12)[i]:.6f}" + (f" ({state_stats.get('min', [0]*12)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Max': [f"{state_stats.get('max', [0]*12)[i]:.6f}" + (f" ({state_stats.get('max', [0]*12)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
        }
    else:
        # 기존 6-dim state
        axes = ['X(m)', 'Y(m)', 'Z(m)', 'Rx(rad)', 'Ry(rad)', 'Rz(rad)']
        state_data = {
            'Axis': axes,
            'Mean': [f"{state_stats.get('mean', [0]*6)[i]:.6f}" + (f" ({state_stats.get('mean', [0]*6)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Std': [f"{state_stats.get('std', [0]*6)[i]:.6f}" + (f" ({state_stats.get('std', [0]*6)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Min': [f"{state_stats.get('min', [0]*6)[i]:.6f}" + (f" ({state_stats.get('min', [0]*6)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
            'Max': [f"{state_stats.get('max', [0]*6)[i]:.6f}" + (f" ({state_stats.get('max', [0]*6)[i] * rad_to_deg:.2f}°)" if i >= 3 else "") for i in range(6)],
        }
    st.dataframe(pd.DataFrame(state_data), use_container_width=True, hide_index=True)

    # Gripper 통계 (13-dim인 경우만)
    if mean_len >= 13:
        st.divider()
        st.markdown("<span style='font-size:18px'>**Gripper State Statistics**</span>", unsafe_allow_html=True)

        gripper_data = {
            'Metric': ['Mean', 'Std', 'Min', 'Max'],
            'Value (ratio [0,1])': [
                f"{state_stats.get('mean', [0]*13)[12]:.4f}",
                f"{state_stats.get('std', [0]*13)[12]:.4f}",
                f"{state_stats.get('min', [0]*13)[12]:.4f}",
                f"{state_stats.get('max', [0]*13)[12]:.4f}",
            ],
            'Value (%)': [
                f"{state_stats.get('mean', [0]*13)[12]*100:.1f}%",
                f"{state_stats.get('std', [0]*13)[12]*100:.1f}%",
                f"{state_stats.get('min', [0]*13)[12]*100:.1f}%",
                f"{state_stats.get('max', [0]*13)[12]*100:.1f}%",
            ],
        }
        st.dataframe(pd.DataFrame(gripper_data), use_container_width=True, hide_index=True)

    # Joint State 통계 (12-dim인 경우만)
    if mean_len >= 12:
        st.divider()
        st.markdown("<span style='font-size:18px'>**Joint State Statistics**</span>", unsafe_allow_html=True)

        joints = ['J1(rad)', 'J2(rad)', 'J3(rad)', 'J4(rad)', 'J5(rad)', 'J6(rad)']
        joint_data = {
            'Joint': joints,
            'Mean': [f"{state_stats.get('mean', [0]*12)[6+i]:.6f} ({state_stats.get('mean', [0]*12)[6+i] * rad_to_deg:.2f}°)" for i in range(6)],
            'Std': [f"{state_stats.get('std', [0]*12)[6+i]:.6f} ({state_stats.get('std', [0]*12)[6+i] * rad_to_deg:.2f}°)" for i in range(6)],
            'Min': [f"{state_stats.get('min', [0]*12)[6+i]:.6f} ({state_stats.get('min', [0]*12)[6+i] * rad_to_deg:.2f}°)" for i in range(6)],
            'Max': [f"{state_stats.get('max', [0]*12)[6+i]:.6f} ({state_stats.get('max', [0]*12)[6+i] * rad_to_deg:.2f}°)" for i in range(6)],
        }
        st.dataframe(pd.DataFrame(joint_data), use_container_width=True, hide_index=True)

    st.divider()

    # Actions 통계 (표)
    st.markdown("<span style='font-size:18px'>**Action Statistics**</span>", unsafe_allow_html=True)

    action_stats = stats.get('action', {})
    action_labels = ['ΔX (mm)', 'ΔY (mm)', 'ΔZ (mm)', 'ΔRx (rad/°)', 'ΔRy (rad/°)', 'ΔRz (rad/°)', 'Grip']

    action_data = {
        'Action': action_labels,
        'Mean': [],
        'Std': [],
        'Min': [],
        'Max': [],
    }

    for i in range(7):
        if i < 3:  # mm 단위 (m → mm: × 1000)
            mean_mm = action_stats.get('mean', [0]*7)[i] * 1000
            std_mm = action_stats.get('std', [0]*7)[i] * 1000
            min_mm = action_stats.get('min', [0]*7)[i] * 1000
            max_mm = action_stats.get('max', [0]*7)[i] * 1000
            mean_val = f"{mean_mm:.2f}"
            std_val = f"{std_mm:.2f}"
            min_val = f"{min_mm:.2f}"
            max_val = f"{max_mm:.2f}"
        else:  # rad → rad/° 변환
            rad_to_deg = 180 / math.pi
            mean_rad = action_stats.get('mean', [0]*7)[i]
            std_rad = action_stats.get('std', [0]*7)[i]
            min_rad = action_stats.get('min', [0]*7)[i]
            max_rad = action_stats.get('max', [0]*7)[i]
            mean_val = f"{mean_rad:.5f} ({mean_rad * rad_to_deg:.2f}°)"
            std_val = f"{std_rad:.5f} ({std_rad * rad_to_deg:.2f}°)"
            min_val = f"{min_rad:.5f} ({min_rad * rad_to_deg:.2f}°)"
            max_val = f"{max_rad:.5f} ({max_rad * rad_to_deg:.2f}°)"

        action_data['Mean'].append(mean_val)
        action_data['Std'].append(std_val)
        action_data['Min'].append(min_val)
        action_data['Max'].append(max_val)

    st.dataframe(pd.DataFrame(action_data), use_container_width=True, hide_index=True)

    st.divider()

    # Quantile 통계 (표)
    st.markdown("<span style='font-size:18px'>**Quantiles (Q1/Q10/Q50/Q90/Q99)**</span>", unsafe_allow_html=True)

    # TCP Pose Quantiles
    st.markdown("<span style='font-size:16px'>**TCP Pose (Axis 1-6)**</span>", unsafe_allow_html=True)
    rad_to_deg = 180 / math.pi
    axes_labels = ['X(m)', 'Y(m)', 'Z(m)', 'Rx(rad)', 'Ry(rad)', 'Rz(rad)']
    state_quant_data = {
        'Axis': axes_labels,
        'Q1%': [f"{state_stats.get('q01', [0]*6)[i]:.6f}" for i in range(6)],
        'Q10%': [f"{state_stats.get('q10', [0]*6)[i]:.6f}" for i in range(6)],
        'Q50%': [f"{state_stats.get('q50', [0]*6)[i]:.6f}" for i in range(6)],
        'Q90%': [f"{state_stats.get('q90', [0]*6)[i]:.6f}" for i in range(6)],
        'Q99%': [f"{state_stats.get('q99', [0]*6)[i]:.6f}" for i in range(6)],
    }
    st.dataframe(pd.DataFrame(state_quant_data), use_container_width=True, hide_index=True)

    # TCP Pose Quantiles 그래프
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()
    for i in range(6):
        q_values = [
            state_stats.get('q01', [0]*6)[i],
            state_stats.get('q10', [0]*6)[i],
            state_stats.get('q50', [0]*6)[i],
            state_stats.get('q90', [0]*6)[i],
            state_stats.get('q99', [0]*6)[i],
        ]
        q_labels = ['Q1%', 'Q10%', 'Q50%', 'Q90%', 'Q99%']
        axes[i].bar(q_labels, q_values, color=['#FF6B6B', '#FFA07A', '#4ECDC4', '#45B7AA', '#2C9D9D'], alpha=0.8, edgecolor='black')
        axes[i].set_title(axes_labels[i], fontsize=12, fontweight='bold')
        axes[i].tick_params(labelsize=9)
        axes[i].grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.divider()

    # Actions Quantiles
    st.markdown("<span style='font-size:16px'>**Actions (A1-A7)**</span>", unsafe_allow_html=True)
    a_quant_data = {
        'Action': action_labels,
        'Q1%': [],
        'Q10%': [],
        'Q50%': [],
        'Q90%': [],
        'Q99%': [],
    }

    for i in range(7):
        if i < 3:  # mm 단위
            scale = 1000
            q1_val = f"{action_stats.get('q01', [0]*7)[i] * scale:.5f}"
            q10_val = f"{action_stats.get('q10', [0]*7)[i] * scale:.5f}"
            q50_val = f"{action_stats.get('q50', [0]*7)[i] * scale:.5f}"
            q90_val = f"{action_stats.get('q90', [0]*7)[i] * scale:.5f}"
            q99_val = f"{action_stats.get('q99', [0]*7)[i] * scale:.5f}"
        else:  # rad → rad/° 변환
            rad_to_deg = 180 / math.pi
            q1_rad = action_stats.get('q01', [0]*7)[i]
            q10_rad = action_stats.get('q10', [0]*7)[i]
            q50_rad = action_stats.get('q50', [0]*7)[i]
            q90_rad = action_stats.get('q90', [0]*7)[i]
            q99_rad = action_stats.get('q99', [0]*7)[i]
            q1_val = f"{q1_rad:.5f} ({q1_rad * rad_to_deg:.2f}°)"
            q10_val = f"{q10_rad:.5f} ({q10_rad * rad_to_deg:.2f}°)"
            q50_val = f"{q50_rad:.5f} ({q50_rad * rad_to_deg:.2f}°)"
            q90_val = f"{q90_rad:.5f} ({q90_rad * rad_to_deg:.2f}°)"
            q99_val = f"{q99_rad:.5f} ({q99_rad * rad_to_deg:.2f}°)"

        a_quant_data['Q1%'].append(q1_val)
        a_quant_data['Q10%'].append(q10_val)
        a_quant_data['Q50%'].append(q50_val)
        a_quant_data['Q90%'].append(q90_val)
        a_quant_data['Q99%'].append(q99_val)

    st.dataframe(pd.DataFrame(a_quant_data), use_container_width=True, hide_index=True)

    # Actions Quantiles 그래프
    fig, axes = plt.subplots(2, 4, figsize=(14, 6))
    axes = axes.flatten()
    for i in range(7):
        if i < 3:  # mm 단위
            scale = 1000
            q_values = [
                action_stats.get('q01', [0]*7)[i] * scale,
                action_stats.get('q10', [0]*7)[i] * scale,
                action_stats.get('q50', [0]*7)[i] * scale,
                action_stats.get('q90', [0]*7)[i] * scale,
                action_stats.get('q99', [0]*7)[i] * scale,
            ]
        else:  # rad → 도 변환
            rad_to_deg = 180 / math.pi
            q_values = [
                action_stats.get('q01', [0]*7)[i] * rad_to_deg,
                action_stats.get('q10', [0]*7)[i] * rad_to_deg,
                action_stats.get('q50', [0]*7)[i] * rad_to_deg,
                action_stats.get('q90', [0]*7)[i] * rad_to_deg,
                action_stats.get('q99', [0]*7)[i] * rad_to_deg,
            ]
        q_labels = ['Q1%', 'Q10%', 'Q50%', 'Q90%', 'Q99%']
        axes[i].bar(q_labels, q_values, color=['#FF6B6B', '#FFA07A', '#4ECDC4', '#45B7AA', '#2C9D9D'], alpha=0.8, edgecolor='black')
        axes[i].set_title(f'A{i+1 if i < 6 else "Grip"}', fontsize=12, fontweight='bold')
        axes[i].tick_params(labelsize=9)
        axes[i].grid(True, alpha=0.3, axis='y')
    axes[7].remove()  # 마지막 빈 서브플롯 제거
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
