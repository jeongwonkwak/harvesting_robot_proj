import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from PIL import Image
import numpy as np

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

BG    = '#FFFFFF'
GRAY  = '#F5F5F5'
DARK  = '#222222'
BLUE  = '#2563EB'
GREEN = '#16A34A'
ARROW = '#94A3B8'

# ── 이미지 & 레이블 ───────────────────────────────────────────
steps = [
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/스크린샷 2026-06-10 15-29-59.png',
        'tag':   '(a)',
        'title': '버튼식 텔레오퍼레이션 수집 데이터',
        'desc':  '버튼 입력마다 step이 생성되어 고주파 노이즈가 심함',
        'color': '#DC2626',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/image.png',
        'tag':   '(b)',
        'title': 'Spline 보간 적용 후',
        'desc':  '스플라인으로 궤적을 재샘플링하여 진폭이 줄고 연속성 확보',
        'color': '#D97706',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/image (1).png',
        'tag':   '(c)',
        'title': '선형 보간 추가 후',
        'desc':  '선형 보간으로 급격한 변화를 평탄화',
        'color': '#2563EB',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/스크린샷 2026-06-13 18-38-45.png',
        'tag':   '(d)',
        'title': '최종 결과 — 학습 데이터와 유사한 패턴 확인',
        'desc':  '모델 출력(실선)이 GT(점선)와 유사하게 수렴',
        'color': '#16A34A',
    },
]

# 공통 너비로 리사이즈
TARGET_W = 1600
imgs = []
for s in steps:
    img = Image.open(s['path']).convert('RGB')
    W, H = img.size
    new_H = int(H * TARGET_W / W)
    imgs.append(img.resize((TARGET_W, new_H), Image.LANCZOS))

# ── Figure 구성 ───────────────────────────────────────────────
# 각 step: 타이틀 행 + 이미지 행 / 사이에 화살표 행
n = len(steps)
# 행 높이 비율: [title, image, arrow] × n (마지막은 arrow 없음)
img_ratios = [np.array(im).shape[0] for im in imgs]
title_h    = 0.45   # inches
arrow_h    = 0.50   # inches

total_img_h = sum(r / 150 for r in img_ratios)   # 150 dpi 기준
fig_w = 14
fig_h = total_img_h + n * title_h + (n-1) * arrow_h + 0.3

fig = plt.figure(figsize=(fig_w, fig_h), facecolor=BG)

# 행 높이 목록 (points)
row_heights = []
for i, ratio in enumerate(img_ratios):
    row_heights.append(title_h)
    row_heights.append(ratio / 150)
    if i < n - 1:
        row_heights.append(arrow_h)

from matplotlib.gridspec import GridSpec
gs = GridSpec(len(row_heights), 1, figure=fig,
              hspace=0,
              left=0.01, right=0.99,
              top=1 - 0.1/fig_h,
              bottom=0.1/fig_h,
              height_ratios=row_heights)

row = 0
for i, (step, img) in enumerate(zip(steps, imgs)):
    # ── 타이틀 행 ──────────────────────────────────────────
    ax_title = fig.add_subplot(gs[row])
    ax_title.set_facecolor(step['color'] + '18')   # 옅은 배경
    ax_title.axis('off')

    # 태그 + 제목
    ax_title.text(0.012, 0.55, step['tag'],
                  transform=ax_title.transAxes,
                  fontsize=15, fontweight='bold', color=step['color'],
                  va='center')
    ax_title.text(0.055, 0.55, step['title'],
                  transform=ax_title.transAxes,
                  fontsize=14, fontweight='bold', color=DARK,
                  va='center')
    ax_title.text(0.055, 0.12, step['desc'],
                  transform=ax_title.transAxes,
                  fontsize=10, color='#555555',
                  va='center')

    # 왼쪽 컬러 바
    ax_title.add_patch(mpatches.FancyBboxPatch(
        (0, 0), 0.006, 1,
        boxstyle='square,pad=0',
        transform=ax_title.transAxes,
        facecolor=step['color'], clip_on=False, zorder=5))

    row += 1

    # ── 이미지 행 ──────────────────────────────────────────
    ax_img = fig.add_subplot(gs[row])
    ax_img.imshow(np.array(img))
    ax_img.axis('off')
    ax_img.set_facecolor(BG)
    row += 1

    # ── 화살표 행 ──────────────────────────────────────────
    if i < n - 1:
        ax_arr = fig.add_subplot(gs[row])
        ax_arr.set_facecolor(BG)
        ax_arr.axis('off')
        ax_arr.annotate(
            '', xy=(0.5, 0.1), xytext=(0.5, 0.9),
            xycoords='axes fraction', textcoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color=ARROW,
                            lw=2.5, mutation_scale=20))
        row += 1

out = '/home/user/robot_workspace/vla_ws/docs/images/pipeline_fig.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
print(f'Saved: {out}')
