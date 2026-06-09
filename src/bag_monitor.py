#!/usr/bin/env python3
"""
실시간 ROS 2 Bag 모니터링 대시보드
- 수집 중인 bag 파일의 모든 토픽 값을 실시간으로 그래프로 표시
- Joint State, TCP Pose, Gripper, 카메라 이미지 모니터링

실행:
  streamlit run src/bag_monitor.py
"""

import streamlit as st
import sqlite3
import struct
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import time

# ── 설정 ────────────────────────────────────────────────────────────────────

RAW_DIR = Path("/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.4.0")
TOPIC_NAMES = {
    'joints': '/dsr01/joint_states',
    'tcp': '/dsr01/tcp_pose',
    'gripper': '/gripper/position',
    'cam1': '/camera/camera/color/image_raw',
    'cam2': '/camera2/camera2/color/image_raw',
}

# ── 유틸리티 ────────────────────────────────────────────────────────────────

class CDRReader:
    def __init__(self, raw: bytes):
        self.buf = raw[4:]
        self.pos = 0

    def _align(self, n: int):
        r = self.pos % n
        if r:
            self.pos += n - r

    def read_uint32(self) -> int:
        self._align(4)
        v = struct.unpack_from('<I', self.buf, self.pos)[0]
        self.pos += 4
        return v

    def read_float64(self) -> float:
        self._align(8)
        v = struct.unpack_from('<d', self.buf, self.pos)[0]
        self.pos += 8
        return v

    def read_float32(self) -> float:
        self._align(4)
        v = struct.unpack_from('<f', self.buf, self.pos)[0]
        self.pos += 4
        return v

    def read_string(self) -> str:
        length = self.read_uint32()
        s = self.buf[self.pos:self.pos + length - 1].decode('utf-8', errors='replace')
        self.pos += length
        return s


def parse_joint_states(raw: bytes) -> list:
    """Parse JointState → [j1, j2, j3, j4, j5, j6] (rad)"""
    r = CDRReader(raw)
    r.read_uint32()
    r.read_uint32()
    r.read_string()
    name_count = r.read_uint32()
    for _ in range(name_count):
        r.read_string()
    pos_count = r.read_uint32()
    positions = [r.read_float64() for _ in range(pos_count)]
    return positions[:6] if len(positions) >= 6 else []


def parse_tcp_pose(raw: bytes) -> list:
    """Parse TCP Pose → [x, y, z, rx, ry, rz]"""
    r = CDRReader(raw)
    r.read_uint32()  # dim count
    r.read_uint32()  # data offset
    vals = []
    count = r.read_uint32()
    for _ in range(count):
        vals.append(r.read_float32())
    return vals[:6] if len(vals) >= 6 else []


def parse_gripper(raw: bytes) -> float:
    """Parse Float32 → gripper position"""
    r = CDRReader(raw)
    return r.read_float32()


def get_latest_episode():
    """최신 episode 디렉토리 찾기"""
    episode_dirs = sorted(RAW_DIR.glob("episode_*_eef"), reverse=True)
    if episode_dirs:
        db_files = list(episode_dirs[0].glob("*.db3"))
        if db_files:
            return episode_dirs[0], db_files[0]
    return None, None


def read_bag_data(db_path: Path):
    """Bag 파일에서 모든 토픽 데이터 읽기"""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # 토픽 ID 매핑
    cur.execute('SELECT id, name FROM topics')
    topics = {name: topic_id for topic_id, name in cur.fetchall()}

    data = {}

    # Joint States
    if topics.get(TOPIC_NAMES['joints']):
        cur.execute(
            'SELECT timestamp, data FROM messages WHERE topic_id = ? ORDER BY timestamp',
            (topics[TOPIC_NAMES['joints']],)
        )
        joints_raw = cur.fetchall()
        joints_list = []
        for ts, raw in joints_raw:
            try:
                joints = parse_joint_states(bytes(raw))
                if joints:
                    joints_list.append({'ts': ts/1e9, 'values': joints})
            except:
                pass
        data['joints'] = joints_list

    # TCP Pose
    if topics.get(TOPIC_NAMES['tcp']):
        cur.execute(
            'SELECT timestamp, data FROM messages WHERE topic_id = ? ORDER BY timestamp',
            (topics[TOPIC_NAMES['tcp']],)
        )
        tcp_raw = cur.fetchall()
        tcp_list = []
        for ts, raw in tcp_raw:
            try:
                tcp = parse_tcp_pose(bytes(raw))
                if tcp:
                    tcp_list.append({'ts': ts/1e9, 'values': tcp})
            except:
                pass
        data['tcp'] = tcp_list

    # Gripper
    if topics.get(TOPIC_NAMES['gripper']):
        cur.execute(
            'SELECT timestamp, data FROM messages WHERE topic_id = ? ORDER BY timestamp',
            (topics[TOPIC_NAMES['gripper']],)
        )
        gripper_raw = cur.fetchall()
        gripper_list = []
        for ts, raw in gripper_raw:
            try:
                grip = parse_gripper(bytes(raw))
                gripper_list.append({'ts': ts/1e9, 'value': grip})
            except:
                pass
        data['gripper'] = gripper_list

    # 메시지 개수
    for name, topic_id in topics.items():
        if name not in TOPIC_NAMES.values():
            continue
        cur.execute('SELECT COUNT(*) FROM messages WHERE topic_id = ?', (topic_id,))
        count = cur.fetchone()[0]
        data[f'count_{list(TOPIC_NAMES.keys())[list(TOPIC_NAMES.values()).index(name)]}'] = count

    conn.close()
    return data


# ── UI ──────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Bag 모니터링", layout="wide")
st.title("📊 ROS 2 Bag 실시간 모니터링")

# 사이드바
with st.sidebar:
    st.markdown("### 설정")

    # Episode 선택
    st.markdown("#### Episode 선택")
    col1, col2 = st.columns(2)
    with col1:
        auto_refresh = st.checkbox("🔄 자동 새로고침", value=True)
    with col2:
        refresh_interval = st.selectbox(
            "간격 (초)",
            [0.5, 1, 2, 5],
            index=1
        )

    latest_ep, latest_db = get_latest_episode()
    if latest_ep:
        st.info(f"📁 최신 Episode: {latest_ep.name}")
        st.caption(f"📄 Bag 파일: {latest_db.name}")
    else:
        st.error("Episode 디렉토리를 찾을 수 없습니다")

# 데이터 로드
if latest_db:
    data = read_bag_data(latest_db)

    # 메시지 개수
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Joint States", data.get('count_joints', 0))
    with col2:
        st.metric("TCP Pose", data.get('count_tcp', 0))
    with col3:
        st.metric("Gripper", data.get('count_gripper', 0))
    with col4:
        st.metric("Camera 1", data.get('count_cam1', 0))
    with col5:
        st.metric("Camera 2", data.get('count_cam2', 0))

    st.divider()

    # 🎯 통합 그래프 (모든 값을 한눈에)
    if data.get('joints') or data.get('tcp') or data.get('gripper'):
        st.markdown("### 📊 통합 모니터링 (정규화 그래프)")

        combined_data = []
        time_base = None

        # Joint State 추가 (0~100으로 정규화: -180~180 → 0~100)
        if data.get('joints'):
            for item in data['joints']:
                if time_base is None:
                    time_base = item['ts']
                time_s = item['ts'] - time_base
                for i, val in enumerate(item['values']):
                    # 라디안을 도로 변환 후 정규화 (-180~180 → 0~100)
                    deg = np.degrees(val)
                    normalized = ((deg + 180) / 360) * 100
                    combined_data.append({
                        'Time': time_s,
                        'Type': f'J{i+1}',
                        'Value': normalized,
                        'Category': 'Joint'
                    })


        # Gripper 추가 (0~100으로 정규화)
        if data.get('gripper'):
            for item in data['gripper']:
                if time_base is None:
                    time_base = item['ts']
                time_s = item['ts'] - time_base
                grip_norm = item['value'] * 100
                combined_data.append({
                    'Time': time_s,
                    'Type': 'Gripper',
                    'Value': grip_norm,
                    'Category': 'Gripper'
                })

        # 통합 데이터프레임 생성
        combined_df = pd.DataFrame(combined_data)

        # 색상 정의
        colors = {
            'J1': '#FF6B6B', 'J2': '#4ECDC4', 'J3': '#45B7AA',
            'J4': '#96CEB4', 'J5': '#FFEAA7', 'J6': '#DDA0DD',
            'Gripper': '#10B981'
        }

        fig = go.Figure()

        # 각 데이터 타입별 선 추가
        for data_type in combined_df['Type'].unique():
            df_subset = combined_df[combined_df['Type'] == data_type]
            fig.add_trace(go.Scatter(
                x=df_subset['Time'],
                y=df_subset['Value'],
                mode='lines',
                name=data_type,
                line=dict(
                    color=colors.get(data_type, '#999999'),
                    width=2
                ),
                hovertemplate=f'{data_type}: %{{y:.1f}}%<br>Time: %{{x:.2f}}s'
            ))

        fig.update_layout(
            title="📊 모든 센서값 통합 모니터링 (정규화: 0~100%)",
            xaxis_title="Time (s)",
            yaxis_title="정규화된 값 (%)",
            hovermode='x unified',
            height=500,
            template='plotly_dark'
        )

        st.plotly_chart(fig, use_container_width=True)

        # 범례 설명
        with st.expander("📝 범례 설명"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**관절 (Joint)**")
                st.caption("• J1 (빨강): 관절 1\n• J2 (청록): 관절 2\n• J3 (파랑-초록): 관절 3\n• J4 (초록): 관절 4\n• J5 (노랑): 관절 5\n• J6 (보라): 관절 6\n\n(정규화: -180~180° → 0~100%)")
            with col2:
                st.markdown("**그리퍼 (Gripper)**")
                st.caption("• 그리퍼 위치 (초록)\n• 0% = 완전히 열림\n• 100% = 완전히 닫힘")

    st.divider()

    # 1. Joint State 그래프
    if data.get('joints'):
        st.markdown("### 🤖 Joint Angles")
        joints_df = pd.DataFrame([
            {
                'Time (s)': item['ts'] - data['joints'][0]['ts'],
                'J1': np.degrees(item['values'][0]),
                'J2': np.degrees(item['values'][1]),
                'J3': np.degrees(item['values'][2]),
                'J4': np.degrees(item['values'][3]),
                'J5': np.degrees(item['values'][4]),
                'J6': np.degrees(item['values'][5]),
            }
            for item in data['joints']
        ])

        fig = go.Figure()
        for col in ['J1', 'J2', 'J3', 'J4', 'J5', 'J6']:
            fig.add_trace(go.Scatter(
                x=joints_df['Time (s)'],
                y=joints_df[col],
                mode='lines',
                name=col,
                hovertemplate=f'{col}: %{{y:.2f}}°<br>Time: %{{x:.2f}}s'
            ))
        fig.update_layout(
            title="관절 각도 변화",
            xaxis_title="Time (s)",
            yaxis_title="Angle (°)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # 통계
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        for i, col in enumerate(['J1', 'J2', 'J3', 'J4', 'J5', 'J6']):
            with [col1, col2, col3, col4, col5, col6][i]:
                st.metric(
                    col,
                    f"{joints_df[col].iloc[-1]:.2f}°",
                    delta=f"{joints_df[col].iloc[-1] - joints_df[col].iloc[0]:.2f}°"
                )

    st.divider()

    # 3. Gripper 그래프
    if data.get('gripper'):
        st.markdown("### 🔐 Gripper")
        gripper_df = pd.DataFrame([
            {
                'Time (s)': item['ts'] - data['gripper'][0]['ts'],
                'Position': item['value'],
            }
            for item in data['gripper']
        ])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=gripper_df['Time (s)'],
            y=gripper_df['Position'],
            mode='lines+markers',
            name='Gripper',
            fill='tozeroy',
            hovertemplate='Position: %{y:.6f}<br>Time: %{x:.2f}s'
        ))
        fig.update_layout(
            title="그리퍼 위치 변화",
            xaxis_title="Time (s)",
            yaxis_title="Position (ratio)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # 통계 및 경고
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("현재값", f"{gripper_df['Position'].iloc[-1]:.6f}")
        with col2:
            st.metric("최소값", f"{gripper_df['Position'].min():.6f}")
        with col3:
            st.metric("최대값", f"{gripper_df['Position'].max():.6f}")

        # 경고
        unique_vals = len(set(f"{v:.6f}" for v in gripper_df['Position']))
        if unique_vals == 1:
            st.error("⚠️ 모든 gripper 값이 동일합니다 (센서 오류?)")
        elif gripper_df['Position'].max() < 0.1:
            st.warning("⚠️ Gripper 값이 매우 낮습니다 (센서 연결 확인)")

    # 자동 새로고침
    if auto_refresh:
        st.info(f"🔄 {refresh_interval}초마다 자동 새로고침 중...")
        time.sleep(refresh_interval)
        st.rerun()
else:
    st.error("❌ Episode 디렉토리를 찾을 수 없습니다")
