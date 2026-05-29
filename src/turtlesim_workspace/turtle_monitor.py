import sys
import threading
import time
from collections import deque
from datetime import datetime

import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import TurtleStatus

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QProgressBar, QTextEdit, QGroupBox,
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QTimer
from PyQt5.QtGui import QFont

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ── ROS2 브릿지 ────────────────────────────────────────────────────────────────

class RosBridge(QObject):
    data_received = pyqtSignal(float, str, bool)

    def start(self):
        rclpy.init()
        self._node = _MonitorNode(self.data_received)
        threading.Thread(target=rclpy.spin, args=(self._node,), daemon=True).start()

    def stop(self):
        self._node.destroy_node()
        rclpy.shutdown()


class _MonitorNode(Node):
    def __init__(self, signal):
        super().__init__('turtle_monitor')
        self._signal = signal
        self.create_subscription(TurtleStatus, '/custom_order', self._cb, 10)

    def _cb(self, msg):
        self._signal.emit(msg.distance_to_wall, msg.current_state, msg.is_moving)


# ── 상태 뱃지 ──────────────────────────────────────────────────────────────────

_STATE_COLORS = {
    'NORMAL':  ('#27ae60', '#1e8449'),
    'WARN':    ('#e67e22', '#ca6f1e'),
    'STOP':    ('#e74c3c', '#cb4335'),
    'WAITING': ('#7f8c8d', '#616a6b'),
}

class StateBadge(QLabel):
    def __init__(self):
        super().__init__('WAITING')
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont('Arial', 13, QFont.Bold))
        self.setMinimumHeight(36)
        self.set_state('WAITING')

    def set_state(self, state):
        bg, border = _STATE_COLORS.get(state, _STATE_COLORS['WAITING'])
        self.setText(state)
        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                border: 2px solid {border};
                border-radius: 8px;
                color: white;
                padding: 4px 16px;
            }}
        """)


# ── distance 히스토리 그래프 ────────────────────────────────────────────────────

class DistanceGraph(FigureCanvas):
    MAX_POINTS = 40

    def __init__(self):
        fig = Figure(figsize=(6, 2.4), tight_layout=True)
        super().__init__(fig)
        self._ax = fig.add_subplot(111)
        self._buf = deque(maxlen=self.MAX_POINTS)
        self._setup()

    def _setup(self):
        ax = self._ax
        self.figure.patch.set_facecolor('#1e272e')
        ax.set_facecolor('#2c3e50')
        ax.set_ylim(-0.2, 5.8)
        ax.set_ylabel('distance (m)', color='#bdc3c7', fontsize=9)
        ax.set_xlabel('recv count', color='#bdc3c7', fontsize=9)
        ax.tick_params(colors='#bdc3c7', labelsize=8)
        for sp in ax.spines.values():
            sp.set_edgecolor('#4a5568')
        ax.axhline(y=3.0, color='#e67e22', linestyle='--', linewidth=1, alpha=0.8, label='WARN  3.0m')
        ax.axhline(y=1.0, color='#e74c3c', linestyle='--', linewidth=1, alpha=0.8, label='STOP  1.0m')
        ax.legend(loc='upper right', fontsize=7, labelcolor='white',
                  facecolor='#1e272e', edgecolor='#4a5568')
        self._line, = ax.plot([], [], color='#3498db', linewidth=2)
        self._fill = None

    def add_data(self, distance):
        self._buf.append(distance)
        xs = list(range(len(self._buf)))
        ys = list(self._buf)
        self._line.set_data(xs, ys)
        self._ax.set_xlim(0, max(self.MAX_POINTS - 1, len(xs) - 1))

        if self._fill:
            self._fill.remove()
        self._fill = self._ax.fill_between(xs, ys, alpha=0.15, color='#3498db')
        self.draw()


# ── 메인 윈도우 ────────────────────────────────────────────────────────────────

class MonitorWindow(QMainWindow):
    def __init__(self, bridge: RosBridge):
        super().__init__()
        self.setWindowTitle('TurtleStatus Monitor  ─  /custom_order')
        self.setMinimumSize(860, 620)
        self._recv_count = 0
        self._last_time = None

        self._build_ui()
        self._apply_style()

        bridge.data_received.connect(self._on_data)

        # 2초 이상 수신 없으면 DISCONNECTED 표시
        self._watchdog = QTimer()
        self._watchdog.timeout.connect(self._check_timeout)
        self._watchdog.start(1000)

    # ── UI 구성 ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        root_widget = QWidget()
        self.setCentralWidget(root_widget)
        root = QVBoxLayout(root_widget)
        root.setSpacing(8)
        root.setContentsMargins(10, 10, 10, 10)

        # 상단: 연결 패널 + 데이터 패널
        top = QHBoxLayout()
        top.setSpacing(8)
        top.addWidget(self._make_connection_panel(), 1)
        top.addWidget(self._make_data_panel(), 2)
        root.addLayout(top)

        # 중단: 그래프
        self._graph = DistanceGraph()
        graph_box = QGroupBox('distance_to_wall  history')
        graph_box.setLayout(QVBoxLayout())
        graph_box.layout().addWidget(self._graph)
        root.addWidget(graph_box, 2)

        # 하단: 로그
        log_box = QGroupBox('로그')
        log_layout = QVBoxLayout()
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumHeight(130)
        self._log.setFont(QFont('Monospace', 9))
        log_layout.addWidget(self._log)
        log_box.setLayout(log_layout)
        root.addWidget(log_box)

    def _make_connection_panel(self):
        group = QGroupBox('연결 상태')
        layout = QVBoxLayout()
        layout.setSpacing(12)

        self._conn_dot = QLabel('● WAITING')
        self._conn_dot.setAlignment(Qt.AlignCenter)
        self._conn_dot.setFont(QFont('Arial', 12, QFont.Bold))
        self._conn_dot.setStyleSheet('color: #7f8c8d;')

        self._hz_label   = self._stat_label('업데이트', '─')
        self._count_label = self._stat_label('수신 횟수', '0 회')
        self._topic_label = self._stat_label('토픽', '/custom_order')

        layout.addWidget(self._conn_dot)
        layout.addWidget(self._hz_label)
        layout.addWidget(self._count_label)
        layout.addWidget(self._topic_label)
        layout.addStretch()
        group.setLayout(layout)
        return group

    def _make_data_panel(self):
        group = QGroupBox('실시간 데이터')
        layout = QVBoxLayout()
        layout.setSpacing(14)

        # distance_to_wall
        dist_section = QVBoxLayout()
        dist_section.addWidget(self._tiny('distance_to_wall'))
        self._dist_val = QLabel('─ m')
        self._dist_val.setFont(QFont('Arial', 26, QFont.Bold))
        self._dist_val.setAlignment(Qt.AlignCenter)
        self._dist_bar = QProgressBar()
        self._dist_bar.setRange(0, 500)
        self._dist_bar.setTextVisible(False)
        self._dist_bar.setFixedHeight(12)
        dist_section.addWidget(self._dist_val)
        dist_section.addWidget(self._dist_bar)

        # current_state / is_moving
        badge_row = QHBoxLayout()
        badge_row.setSpacing(16)

        state_col = QVBoxLayout()
        state_col.addWidget(self._tiny('current_state'))
        self._state_badge = StateBadge()
        state_col.addWidget(self._state_badge)

        moving_col = QVBoxLayout()
        moving_col.addWidget(self._tiny('is_moving'))
        self._moving_label = QLabel('● ─')
        self._moving_label.setFont(QFont('Arial', 13, QFont.Bold))
        self._moving_label.setAlignment(Qt.AlignCenter)
        moving_col.addWidget(self._moving_label)

        badge_row.addLayout(state_col)
        badge_row.addLayout(moving_col)

        layout.addLayout(dist_section)
        layout.addLayout(badge_row)
        layout.addStretch()
        group.setLayout(layout)
        return group

    def _stat_label(self, title, value):
        lbl = QLabel(f'{title}:  {value}')
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setObjectName('stat')
        return lbl

    def _tiny(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet('color: #7f8c8d; font-size: 9pt;')
        return lbl

    # ── 데이터 수신 처리 ──────────────────────────────────────────────────────

    def _on_data(self, distance: float, state: str, is_moving: bool):
        now = time.time()
        if self._last_time:
            ms = (now - self._last_time) * 1000
            self._hz_label.setText(f'업데이트:  {ms:.1f} ms')
        self._last_time = now
        self._recv_count += 1

        # 연결 표시
        self._conn_dot.setText('● CONNECTED')
        self._conn_dot.setStyleSheet('color: #27ae60;')

        # distance
        self._dist_val.setText(f'{distance:.2f} m')
        self._dist_bar.setValue(int(distance * 100))
        bar_color = {'NORMAL': '#27ae60', 'WARN': '#e67e22', 'STOP': '#e74c3c'}.get(state, '#7f8c8d')
        self._dist_bar.setStyleSheet(f'QProgressBar::chunk {{ background: {bar_color}; border-radius: 4px; }}')

        # state / moving
        self._state_badge.set_state(state)
        if is_moving:
            self._moving_label.setText('● MOVING')
            self._moving_label.setStyleSheet('color: #27ae60; font-weight: bold;')
        else:
            self._moving_label.setText('● STOPPED')
            self._moving_label.setStyleSheet('color: #e74c3c; font-weight: bold;')

        self._count_label.setText(f'수신 횟수:  {self._recv_count} 회')

        # 그래프
        self._graph.add_data(distance)

        # 로그
        ts = datetime.now().strftime('%H:%M:%S')
        self._log.append(
            f'[{ts}]  dist={distance:.2f}m   state={state:<6}   moving={str(is_moving)}'
        )

    def _check_timeout(self):
        if self._last_time and time.time() - self._last_time > 2.0:
            self._conn_dot.setText('● DISCONNECTED')
            self._conn_dot.setStyleSheet('color: #e74c3c;')

    # ── 다크 테마 ──────────────────────────────────────────────────────────────

    def _apply_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e272e;
                color: #ecf0f1;
            }
            QGroupBox {
                border: 1px solid #4a5568;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #bdc3c7;
                font-size: 10pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
            }
            QProgressBar {
                border: 1px solid #4a5568;
                border-radius: 4px;
                background: #2c3e50;
            }
            QLabel#stat {
                color: #bdc3c7;
                font-size: 10pt;
            }
            QTextEdit {
                background: #2c3e50;
                color: #2ecc71;
                border: 1px solid #4a5568;
                border-radius: 4px;
            }
        """)


# ── 진입점 ─────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)

    bridge = RosBridge()
    bridge.start()

    window = MonitorWindow(bridge)
    window.show()

    try:
        sys.exit(app.exec_())
    finally:
        bridge.stop()


if __name__ == '__main__':
    main()
