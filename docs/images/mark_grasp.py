"""
딸기 파지점 + 가림 영역 마킹 도구
- 좌클릭: 파지점 추가 (최대 4개, 연속 번호)
- 우클릭: 해당 이미지 파지점 모두 제거
- [가림 ON] 버튼 → 정면 이미지에서 드래그로 가림 영역 표시
- [가림 취소] 버튼 → 마지막 가림 영역 제거
- S키 / Save 버튼: 저장
"""
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
from matplotlib.widgets import Button, RectangleSelector
from PIL import Image
import numpy as np

font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

TARGET_W, TARGET_H = 900, 1050
BG        = '#111111'
WHITE     = '#FFFFFF'
RED       = '#FF2222'
OCC_COLOR = '#FFB800'   # 가림 영역 색 (주황)

images_info = [
    {'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2549.jpg',
     'crop': (0.05, 0.28, 0.97, 0.98), 'label': '정면 (Front)'},
    {'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2556.jpg',
     'crop': (0.05, 0.08, 0.95, 0.95), 'label': '좌측 (Left)'},
    {'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2553.jpg',
     'crop': (0.05, 0.05, 0.95, 0.90), 'label': '우측 (Right) ①'},
    {'path': '/home/user/robot_workspace/vla_ws/docs/images/IMG_2555.jpg',
     'crop': (0.05, 0.03, 0.95, 0.90), 'label': '우측 (Right) ②'},
]

cropped_imgs = []
for info in images_info:
    img = Image.open(info['path'])
    W, H = img.size
    l = int(info['crop'][0] * W); t = int(info['crop'][1] * H)
    r = int(info['crop'][2] * W); b = int(info['crop'][3] * H)
    img_c = img.crop((l, t, r, b)).resize((TARGET_W, TARGET_H), Image.LANCZOS)
    cropped_imgs.append(np.array(img_c))

grasp_points  = {i: [] for i in range(4)}
grasp_artists = {i: [] for i in range(4)}
global_counter = [0]
occ_mode      = [False]
occ_patches   = []   # [(patch, text), ...]

# ── 레이아웃 ──────────────────────────────────────────────────
fw = 13
fh = round(fw * TARGET_H / TARGET_W * 0.99 / 0.91, 1)
fig = plt.figure(figsize=(fw, fh))
fig.patch.set_facecolor(BG)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.01, wspace=0.01,
                       left=0.005, right=0.995, top=0.97, bottom=0.07)

ax_list = [
    fig.add_subplot(gs[0, 0]),
    fig.add_subplot(gs[0, 1]),
    fig.add_subplot(gs[1, 0]),
    fig.add_subplot(gs[1, 1]),
]

for ax, img_arr, info in zip(ax_list, cropped_imgs, images_info):
    ax.imshow(img_arr)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.text(TARGET_W * 0.5, TARGET_H * 0.06, info['label'],
            color=WHITE, fontsize=22, fontweight='bold', ha='center', va='top',
            transform=ax.transData, zorder=10,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='black',
                      alpha=1.0, edgecolor='white', linewidth=2.2))

fig.suptitle(
    '[ 좌클릭: 파지점 | 우클릭: 제거 | 가림ON 후 드래그: 가림 영역 | S: 저장 ]',
    color='#AAAAAA', fontsize=11, y=0.998)


# ── 파지점 ────────────────────────────────────────────────────
def draw_marker(ax, idx, px, py, number):
    r_out = TARGET_W * 0.05
    r_in  = r_out * 0.22
    arts  = []
    arts.append(ax.add_patch(plt.Circle((px, py), r_out, color=RED,
                                         fill=False, linewidth=3, zorder=5)))
    arts.append(ax.add_patch(plt.Circle((px, py), r_in, color=RED,
                                         fill=True, zorder=5)))
    arts.append(ax.text(px + r_out*1.15, py - r_out*1.15, str(number),
                        color=WHITE, fontsize=14, fontweight='bold',
                        ha='center', va='center', zorder=7,
                        bbox=dict(boxstyle='circle,pad=0.25', facecolor=RED,
                                  edgecolor=WHITE, linewidth=1.4)))
    off_x = -TARGET_W*0.22 if number % 2 == 1 else TARGET_W*0.22
    off_y = -TARGET_H*0.16
    lx, ly = px + off_x, py + off_y
    conn = 'arc3,rad=0.15' if number % 2 == 1 else 'arc3,rad=-0.15'
    arts.append(ax.annotate('', xy=(px, py), xytext=(lx, ly),
                             arrowprops=dict(arrowstyle='->', color=RED, lw=2.2,
                                             connectionstyle=conn), zorder=6))
    arts.append(ax.text(lx, ly - TARGET_H*0.04,
                        f'파지점 {number}\n(Grasp Point)',
                        color=RED, fontsize=15, fontweight='bold',
                        ha='center', va='bottom', zorder=6,
                        bbox=dict(boxstyle='round,pad=0.35', facecolor='black',
                                  alpha=0.75, edgecolor=RED, linewidth=1.5)))
    grasp_artists[idx].extend(arts)
    fig.canvas.draw_idle()


def clear_markers(idx):
    for a in grasp_artists[idx]:
        try: a.remove()
        except Exception: pass
    grasp_artists[idx].clear()
    grasp_points[idx].clear()
    fig.canvas.draw_idle()


# ── 가림 영역 ─────────────────────────────────────────────────
def on_rect_select(eclick, erelease):
    if not occ_mode[0]:
        return
    x0 = min(eclick.xdata, erelease.xdata)
    y0 = min(eclick.ydata, erelease.ydata)
    x1 = max(eclick.xdata, erelease.xdata)
    y1 = max(eclick.ydata, erelease.ydata)
    if abs(x1-x0) < 15 or abs(y1-y0) < 15:
        return

    patch = ax_list[0].add_patch(plt.Rectangle(
        (x0, y0), x1-x0, y1-y0,
        facecolor='none',
        edgecolor=OCC_COLOR, linewidth=2,
        hatch='////', zorder=4))
    occ_patches.append((patch, None))
    fig.canvas.draw_idle()


try:
    rect_sel = RectangleSelector(
        ax_list[0], on_rect_select, useblit=False, button=[1],
        interactive=False,
        props=dict(edgecolor=OCC_COLOR, fill=False, linewidth=2, linestyle='--'))
except TypeError:
    rect_sel = RectangleSelector(
        ax_list[0], on_rect_select, useblit=False, drawtype='box', button=[1],
        interactive=False,
        rectprops=dict(edgecolor=OCC_COLOR, fill=False, linewidth=2, linestyle='--'))
rect_sel.set_active(False)


# ── 클릭 핸들러 ──────────────────────────────────────────────
def on_click(event):
    if event.inaxes not in ax_list:
        return
    idx = ax_list.index(event.inaxes)
    px, py = event.xdata, event.ydata
    if px is None or py is None:
        return

    # 가림 모드: 정면(0)만, 우클릭 = 마지막 가림 제거
    if occ_mode[0]:
        if idx == 0 and event.button == 3 and occ_patches:
            p, _ = occ_patches.pop()
            p.remove()
            fig.canvas.draw_idle()
        return

    # 파지점 모드
    if event.button == 1:
        if global_counter[0] >= 4:
            print('최대 4개입니다. 우클릭으로 초기화하세요.')
            return
        global_counter[0] += 1
        grasp_points[idx].append((px, py))
        draw_marker(event.inaxes, idx, px, py, global_counter[0])
    elif event.button == 3:
        n = len(grasp_points[idx])
        global_counter[0] -= n
        clear_markers(idx)


# ── 가림 ON/OFF 버튼 ─────────────────────────────────────────
def toggle_occ(event):
    occ_mode[0] = not occ_mode[0]
    rect_sel.set_active(occ_mode[0])
    if occ_mode[0]:
        occ_btn.label.set_text('가림 ON (드래그)')
        occ_btn.color = '#553300'
        occ_btn.hovercolor = '#774400'
    else:
        occ_btn.label.set_text('가림 영역 표시')
        occ_btn.color = '#333333'
        occ_btn.hovercolor = '#555555'
    fig.canvas.draw_idle()


def undo_occ(event):
    if occ_patches:
        p, _ = occ_patches.pop()
        p.remove()
        fig.canvas.draw_idle()


# ── 저장 ─────────────────────────────────────────────────────
all_btn_axes = []

def save_final(event=None):
    out_path = '/home/user/robot_workspace/vla_ws/docs/images/composite_grasp.png'
    for ba in all_btn_axes:
        ba.set_visible(False)
    old_title = fig.texts[0].get_text()
    fig.texts[0].set_text('')
    fig.savefig(out_path, dpi=150, bbox_inches='tight',
                pad_inches=0.05, facecolor=BG)
    for ba in all_btn_axes:
        ba.set_visible(True)
    fig.texts[0].set_text(old_title)
    fig.canvas.draw_idle()
    print(f'Saved → {out_path}')


fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event',
                        lambda e: save_final() if e.key == 's' else None)

# 버튼 배치
save_ax = fig.add_axes([0.20, 0.015, 0.14, 0.04])
occ_ax  = fig.add_axes([0.42, 0.015, 0.20, 0.04])
undo_ax = fig.add_axes([0.65, 0.015, 0.16, 0.04])
all_btn_axes = [save_ax, occ_ax, undo_ax]

save_btn = Button(save_ax, '  Save (S)  ', color='#333333', hovercolor='#555555')
save_btn.label.set_color(WHITE); save_btn.label.set_fontsize(12)
save_btn.on_clicked(save_final)

occ_btn = Button(occ_ax, '가림 영역 표시', color='#333333', hovercolor='#555555')
occ_btn.label.set_color(OCC_COLOR); occ_btn.label.set_fontsize(12)
occ_btn.on_clicked(toggle_occ)

undo_btn = Button(undo_ax, '가림 취소', color='#333333', hovercolor='#555555')
undo_btn.label.set_color(OCC_COLOR); undo_btn.label.set_fontsize(12)
undo_btn.on_clicked(undo_occ)

plt.show()
