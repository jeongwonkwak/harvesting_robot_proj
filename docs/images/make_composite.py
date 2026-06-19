import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
from PIL import Image
import numpy as np

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

TARGET_W, TARGET_H = 900, 1050
BG = '#111111'
WHITE = '#FFFFFF'

images = [
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2549.jpg',
        'crop': (0.05, 0.28, 0.97, 0.98),
        'label': '정면 (Front)',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2553.jpg',
        'crop': (0.05, 0.05, 0.95, 0.90),
        'label': '우측 (Right) ①',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2555.jpg',
        'crop': (0.05, 0.03, 0.95, 0.90),
        'label': '우측 (Right) ②',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2554.jpg',
        'crop': (0.02, 0.03, 0.88, 0.90),
        'label': '좌측 (Left) ①',
    },
    {
        'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2556.jpg',
        'crop': (0.05, 0.08, 0.95, 0.95),
        'label': '좌측 (Left) ②',
    },
]

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 6, figure=fig, hspace=0.04, wspace=0.04,
                       left=0.01, right=0.99, top=0.96, bottom=0.01)

ax_list = [
    fig.add_subplot(gs[0, 0:2]),
    fig.add_subplot(gs[0, 2:4]),
    fig.add_subplot(gs[0, 4:6]),
    fig.add_subplot(gs[1, 1:3]),
    fig.add_subplot(gs[1, 3:5]),
]

for ax, info in zip(ax_list, images):
    img = Image.open(info['path'])
    W, H = img.size
    l, t, r, b = (int(info['crop'][i] * (W if i % 2 == 0 else H)) for i in range(4))
    img_c = img.crop((l, t, r, b)).resize((TARGET_W, TARGET_H), Image.LANCZOS)

    ax.imshow(np.array(img_c))
    ax.set_facecolor(BG)
    ax.axis('off')

    ax.text(
        TARGET_W * 0.5, TARGET_H * 0.04,
        info['label'],
        color=WHITE, fontsize=15, fontweight='bold',
        ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='black',
                  alpha=0.72, edgecolor='white', linewidth=1.5)
    )

fig.suptitle(
    '실험실 딸기 세팅  —  시점별 촬영',
    color=WHITE, fontsize=17, fontweight='bold', y=1.01
)

out = '/home/user/robot_workspace/vla_ws/docs/images/composite_grasp.png'
plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.08, facecolor=BG)
print(f'Saved: {out}')
