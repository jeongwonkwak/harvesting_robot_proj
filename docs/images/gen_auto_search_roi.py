"""
Auto Search ROI visualization — 재생성 스크립트
ALIGN / PULL_DOWN / HOME 웨이포인트 추가 포함
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── 실제 웨이포인트 (절대 좌표, mm) ──────────────────────────────────────────
HOME_ABS     = np.array([312.3, 279.0, 877.8])
ALIGN_ABS    = np.array([288.2, 549.2, 789.1])
PULL_DOWN_ABS= np.array([283.7, 524.9, 783.8])

# HOME 기준 상대 좌표 (mm)
def rel(p): return p - HOME_ABS

HOME_R      = rel(HOME_ABS)       # (0, 0, 0)
ALIGN_R     = rel(ALIGN_ABS)      # (-24.1, 270.2, -88.7)
PULL_DOWN_R = rel(PULL_DOWN_ABS)  # (-28.6, 245.9, -94.0)

# ── 오토서치 파라미터 (기본값) ─────────────────────────────────────────────
DX, DY, DZ = 80, 80, 40
ROI_R       = 120
N_WP        = 6
N_EPISODES  = 5

# ── 웨이포인트 생성 (harvest_dashboard.py _generateSearchWaypoints 동일 로직) ─
def generate_episode(seed):
    rng = np.random.RandomState(seed)
    ox = (rng.random() - 0.5) * 2 * DX
    oy = (rng.random() - 0.5) * 2 * DY
    oz = (rng.random() - 0.5) * 2 * DZ

    ox = -abs(ox)  # 항상 -X 방향(왼쪽) 접근 — +X 쪽은 카메라에서 파지점 사각지대

    pts = [HOME_R.copy()]
    for i in range(N_WP):
        t = (i + 1) / (N_WP + 1)
        w = math.sin(t * math.pi)
        pts.append(np.array([
            ALIGN_R[0] * t + ox * w,
            min(ALIGN_R[1] * t + oy * w, ALIGN_R[1]),  # +Y 방향 진입 금지
            ALIGN_R[2] * t + oz * w,
        ]))
    pts.append(ALIGN_R.copy())
    return pts   # 각 pt = [dx, dy, dz] relative to HOME


episodes = [generate_episode(s) for s in [7, 13, 42, 99, 3]]

# ── 스타일 ────────────────────────────────────────────────────────────────
BG      = "#12172a"
GRID    = "#1e2740"
COLORS  = ["#6aabf7","#f76aab","#6af7b4","#f7b46a","#b46af7"]
HOME_C  = "#4ade80"
ALIGN_C = "#fbbf24"
PDOWN_C = "#f87171"
ROI_C   = "#f59e0b"

fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), facecolor=BG)
fig.suptitle("Auto Search — ROI & Random Waypoint Visualization (default settings)",
             color="white", fontsize=12, y=0.98)

ax_xy, ax_xz = axes
for ax in axes:
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a3450")
    ax.tick_params(colors="#8899bb")
    ax.xaxis.label.set_color("#8899bb")
    ax.yaxis.label.set_color("#8899bb")
    ax.grid(color=GRID, linewidth=0.6, zorder=0)


def plot_view(ax, get_xy, xlabel, ylabel, title, xlim, ylim,
             y_limit=None, x_limit=None, show_roi=True):
    # +Y 금지 경계 — 수직선(x_limit) 또는 수평선(y_limit)
    if y_limit is not None:
        ax.axhline(y_limit, color="#f87171", linewidth=1.2,
                   linestyle="--", zorder=2, alpha=0.8)
        ax.fill_between(xlim, y_limit, ylim[1],
                        color="#f87171", alpha=0.07, zorder=1)
        ax.text(xlim[0] + 4, y_limit + 4, "+Y limit (ALIGN)",
                color="#f87171", fontsize=7.5, va="bottom")
    if x_limit is not None:
        ax.axvline(x_limit, color="#f87171", linewidth=1.2,
                   linestyle="--", zorder=2, alpha=0.8)
        ax.fill_betweenx(ylim, x_limit, xlim[1],
                         color="#f87171", alpha=0.07, zorder=1)
        ax.text(x_limit + 4, ylim[0] + 4, "+Y limit (ALIGN)",
                color="#f87171", fontsize=7.5, va="bottom")

    # ROI 원 (Top View에서만 — XZ 투영 시 Y 거리가 사라져 HOME이 원 안에 들어오는 착시)
    if show_roi:
        cx, cy = get_xy(ALIGN_R)
        circle = plt.Circle((cx, cy), ROI_R, color=ROI_C,
                             fill=False, linestyle="--", linewidth=1.8, zorder=2)
        ax.add_patch(circle)

    # 에피소드 궤적
    for ep_i, pts in enumerate(episodes):
        xs, ys = zip(*[get_xy(p) for p in pts])
        ax.plot(xs, ys, color=COLORS[ep_i], linewidth=1.4,
                marker="o", markersize=4, markerfacecolor=COLORS[ep_i],
                label=f"Episode {ep_i+1}", zorder=3)

    # ALIGN → PULL_DOWN → HOME 연결선 (회색, 단순 선)
    chain = [ALIGN_R, PULL_DOWN_R, HOME_R]
    cxs, cys = zip(*[get_xy(p) for p in chain])
    ax.plot(cxs, cys, color="#94a3b8", linewidth=1.6,
            linestyle="-", zorder=4)

    # HOME
    hx, hy = get_xy(HOME_R)
    ax.scatter(hx, hy, marker="s", s=110, color=HOME_C, zorder=6, label="HOME")
    ax.annotate("HOME", (hx, hy), textcoords="offset points",
                xytext=(6, 5), color=HOME_C, fontsize=8)

    # ALIGN (오토서치 목표 = 기존 REPOSITION 역할)
    ax_val, ay_val = get_xy(ALIGN_R)
    ax.scatter(ax_val, ay_val, marker="*", s=200, color=ALIGN_C, zorder=6, label="ALIGN")
    ax.annotate("ALIGN", (ax_val, ay_val), textcoords="offset points",
                xytext=(6, 5), color=ALIGN_C, fontsize=8)

    # PULL_DOWN
    px, py = get_xy(PULL_DOWN_R)
    ax.scatter(px, py, marker="v", s=100, color=PDOWN_C, zorder=6, label="PULL_DOWN")
    ax.annotate("PULL_DOWN", (px, py), textcoords="offset points",
                xytext=(6, -12), color=PDOWN_C, fontsize=8)

    # 점선 박스 (탐색 범위) — 축 이름으로 크기 결정
    bx, by = get_xy(ALIGN_R)
    axis_pair = tuple(sorted([xlabel[0], ylabel[0]]))
    if axis_pair == ("X", "Y"):
        bw, bh = (DY*2, DX*2) if xlabel.startswith("Y") else (DX*2, DY*2)
    else:
        bw, bh = (DZ*2, DX*2) if xlabel.startswith("Z") else (DX*2, DZ*2)
    rect = mpatches.FancyBboxPatch(
        (bx - bw/2, by - bh/2), bw, bh,
        boxstyle="square,pad=0", linestyle="--",
        edgecolor="#4a5577", facecolor="none", linewidth=0.8, zorder=1)
    ax.add_patch(rect)

    handles, labels = ax.get_legend_handles_labels()
    if show_roi:
        roi_patch = mpatches.Patch(facecolor="none", edgecolor=ROI_C,
                                   linestyle="--", label=f"ROI r={ROI_R}mm")
        handles.append(roi_patch)
        labels.append(f"ROI r={ROI_R}mm")

    ax.legend(handles, labels, fontsize=7, loc="upper left",
              facecolor="#1a2035", edgecolor="#2a3450", labelcolor="white")

    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, color="white", fontsize=10, pad=6)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")  # 1mm = 1mm → 원이 원으로 표시됨


cx, cz_align = ALIGN_R[0], ALIGN_R[2]
margin = 40

plot_view(ax_xy,
          get_xy=lambda p: (p[1], p[0]),          # Y → 가로, X → 세로
          xlabel="Y (mm)", ylabel="X (mm)",
          title="Top View (XY)",
          xlim=(HOME_R[1] - margin, ALIGN_R[1] + ROI_R + margin),
          ylim=(ALIGN_R[0] + ROI_R + margin, ALIGN_R[0] - ROI_R - margin),  # X축 반전: 아래=+, 위=-
          x_limit=ALIGN_R[1])                      # +Y 경계를 수직선으로

# Side View: 궤적 전체 X/Z 범위 + 여백
all_xs = [p[0] for ep in episodes for p in ep] + [HOME_R[0], ALIGN_R[0], PULL_DOWN_R[0]]
all_zs = [p[2] for ep in episodes for p in ep] + [HOME_R[2], ALIGN_R[2], PULL_DOWN_R[2]]
xz_xpad = max(abs(min(all_xs)), abs(max(all_xs))) + margin
plot_view(ax_xz,
          get_xy=lambda p: (p[0], p[2]),
          xlabel="X (mm)", ylabel="Z (mm)",
          title="Side View (XZ)",
          xlim=(-xz_xpad, xz_xpad),
          ylim=(max(all_zs) + margin, min(all_zs) - margin),  # Z축 반전: 아래=+, 위=-
          show_roi=False)

caption = (f"X(search) range: dX={DX}mm  dY={DY}mm  dZ={DZ}mm  |  "
           f"ROI radius={ROI_R}mm  |  Waypoints={N_WP}  |  Arc path (sine weight)  |  "
           f"ALIGN -> PULL_DOWN -> HOME")
fig.text(0.5, 0.01, caption, ha="center", fontsize=8, color="#8899bb")

plt.tight_layout(rect=[0, 0.04, 1, 0.97])
out = "/home/user/robot_workspace/vla_ws/docs/images/auto_search_roi.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"저장: {out}")
