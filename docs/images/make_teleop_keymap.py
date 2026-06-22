"""
텔레오퍼레이션 연출 이미지
- 흰색 배경
- 카메라 2개 + 방향 조작 UI
- 버튼 클릭 → 로봇 이동 연출
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
from PIL import Image
import numpy as np

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

# ── 이미지 로드 ────────────────────────────────────────────────────
ui_img  = Image.open('/home/user/robot_workspace/vla_ws/docs/images/스크린샷 2026-06-20 18-19-07.png')
cam_img = Image.open('/home/user/robot_workspace/vla_ws/docs/images/스크린샷 2026-06-20 18-19-21.png')

UW, UH = ui_img.size   # 302 x 667
CW, CH = cam_img.size  # 1302 x 481

# 카메라 좌/우 분리
cam_l = cam_img.crop((0,      0, CW//2, CH))  # 손목 카메라 (딸기)
cam_r = cam_img.crop((CW//2,  0, CW,    CH))  # 전방 카메라 (로봇)
CLW, CLH = cam_l.size
CRW, CRH = cam_r.size

# UI: 방향 조작 버튼만 크롭 (방향키 + Z버튼 섹션)
# 픽셀 분석 결과: ↑=y170, ←→=y218, 방향 섹션 끝=y~295
UI_CROP_Y1, UI_CROP_Y2 = 90, 310
ui_crop = ui_img.crop((0, UI_CROP_Y1, UW, UI_CROP_Y2))
UCW, UCH = ui_crop.size  # 302 x 220

# 버튼 중심 좌표 (크롭 기준 픽셀)
BUP   = (152, 170 - UI_CROP_Y1)   # ↑
BLEFT = (46,  218 - UI_CROP_Y1)   # ←
BSTOP = (152, 218 - UI_CROP_Y1)   # ■
BRITE = (258, 218 - UI_CROP_Y1)   # →
BDOWN = (152, 255 - UI_CROP_Y1)   # ↓ (추정)

# ── 캔버스 ────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 9), facecolor='white')

gs = gridspec.GridSpec(
    1, 3,
    figure=fig,
    left=0.01, right=0.99, top=0.99, bottom=0.01,
    wspace=0.03,
    width_ratios=[1.55, 1.55, 0.75],
)
ax_l = fig.add_subplot(gs[0, 0])
ax_r = fig.add_subplot(gs[0, 1])
ax_u = fig.add_subplot(gs[0, 2])

# ── 카메라 피드 ───────────────────────────────────────────────────
for ax, img, title, tc in [
    (ax_l, cam_l, '손목 카메라  (Wrist View)',  '#1a7f37'),
    (ax_r, cam_r, '전방 카메라  (Front View)',  '#0969da'),
]:
    ax.imshow(np.array(img))
    ax.axis('off')
    ax.set_facecolor('white')
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_edgecolor(tc)
        sp.set_linewidth(2.8)
    ax.text(0.5, 0.97, title,
            transform=ax.transAxes,
            color='white', fontsize=12, fontweight='bold',
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.35',
                      facecolor=tc + 'cc', edgecolor='none'))


# ── UI 패널 ───────────────────────────────────────────────────────
ax_u.imshow(np.array(ui_crop))
ax_u.set_xlim(-0.5, UCW - 0.5)
ax_u.set_ylim(UCH - 0.5, -0.5)  # imshow 기본 방향 유지
ax_u.axis('off')
ax_u.set_facecolor('#f6f8fa')
for sp in ax_u.spines.values():
    sp.set_visible(True)
    sp.set_edgecolor('#d0d7de')
    sp.set_linewidth(1.5)


# 패널 제목
ax_u.text(UCW / 2, -14, '방향 조작 패널',
          color='#24292f', fontsize=11, fontweight='bold',
          ha='center', va='center')


# ── 저장 ─────────────────────────────────────────────────────────
out = '/home/user/robot_workspace/vla_ws/docs/images/teleop_keymap.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
