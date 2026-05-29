#!/usr/bin/env python3
"""
strawberry_occlusion_meter.py

RealSense 카메라로 딸기의 폐색률을 실시간 측정.

폐색률 계산 방법 (Occluder-based):
  (잎 마스크 + 미성숙 딸기 bbox 가 타겟 딸기 bbox 안에서 차지하는 픽셀 비율)

  ┌─────────────────────────────────────────────────┐
  │  타겟 딸기 bbox                                  │
  │  ┌──────────┐                                   │
  │  │ 잎 마스크 │ ← HSV 녹색 검출                   │
  │  └──────────┘                                   │
  │       +  미성숙 딸기 bbox 교집합                  │
  │  ─────────────────────────────────────────────  │
  │            딸기 bbox 전체 면적                    │
  └─────────────────────────────────────────────────┘

YOLO 클래스:
  0: unripe_strawberry
  1: ripe_strawberry
  잎:  HSV 녹색 범위로 검출 (모델에 없음)

실행:
  python3 src/strawberry_occlusion_meter.py
  python3 src/strawberry_occlusion_meter.py --conf 0.4
  python3 src/strawberry_occlusion_meter.py --no-leaf     # leaf detection off
  python3 src/strawberry_occlusion_meter.py --save        # snapshot on Space
  python3 src/strawberry_occlusion_meter.py --expand 0.4  # ripe bbox expansion ratio
"""

import argparse
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

# ── 경로 ──────────────────────────────────────────────────────────────────────
WS_DIR     = Path('/home/user/robot_workspace/vla_ws')
YOLO_MODEL = str(WS_DIR / 'models/strawberry_yolo26m_unified/weights/last.pt')

# ── YOLO 클래스 ID ─────────────────────────────────────────────────────────────
CLS_UNRIPE = 0   # unripe_strawberry
CLS_RIPE   = 1   # ripe_strawberry

# ── 잎 HSV 범위 (녹색) ─────────────────────────────────────────────────────────
LEAF_HSV_LOWER = np.array([ 35,  40,  40])
LEAF_HSV_UPPER = np.array([ 85, 255, 255])

# ── ripe bbox 확장 비율 (기본값) ──────────────────────────────────────────────
# YOLO는 가려진 딸기의 보이는 부분만 bbox로 잡으므로
# 실제 딸기 크기를 추정하기 위해 bbox를 일정 비율로 확장
BBOX_EXPAND_DEFAULT = 0.35   # 0 = 확장 없음, 0.35 = 35% 확장

# ── 폐색 단계 (상한, 이름, BGR 색상) ──────────────────────────────────────────
LEVELS = [
    (0.10, 'No Occlusion', (  0, 200,   0)),   # 녹색
    (0.30, 'Mild',         (  0, 220, 220)),   # 노랑
    (0.60, 'Moderate',     (  0, 140, 255)),   # 주황
    (0.90, 'Heavy',        (  0,   0, 255)),   # 빨강
    (1.01, 'Extreme',      (150,   0, 200)),   # 보라
]


# ── 유틸 ──────────────────────────────────────────────────────────────────────

def get_level(ratio: float) -> tuple[str, tuple]:
    for thr, name, color in LEVELS:
        if ratio < thr:
            return name, color
    return LEVELS[-1][1], LEVELS[-1][2]


def detect_leaf_mask(frame_bgr: np.ndarray) -> np.ndarray:
    """HSV 녹색 범위로 잎 이진 마스크 생성."""
    hsv    = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask   = cv2.inRange(hsv, LEAF_HSV_LOWER, LEAF_HSV_UPPER)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel, iterations=1)
    mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    return mask


def expand_box(box: tuple, ratio: float, img_h: int, img_w: int) -> tuple:
    """
    bbox를 중심 기준으로 ratio 비율만큼 확장.
    YOLO가 가려진 딸기의 보이는 부분만 잡기 때문에
    실제 딸기 크기를 추정하기 위해 사용.
    """
    x1, y1, x2, y2 = box
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    hw = (x2 - x1) / 2.0 * (1.0 + ratio)
    hh = (y2 - y1) / 2.0 * (1.0 + ratio)
    return (
        max(0,     int(cx - hw)),
        max(0,     int(cy - hh)),
        min(img_w, int(cx + hw)),
        min(img_h, int(cy + hh)),
    )


def calc_occlusion(
    ripe_box: tuple,
    leaf_mask: np.ndarray,
    unripe_boxes: list,
    img_h: int,
    img_w: int,
    expand_ratio: float = BBOX_EXPAND_DEFAULT,
) -> dict:
    """
    타겟 딸기 bbox 기준 폐색률 반환.
    expand_ratio: ripe bbox 확장 비율 (YOLO가 보이는 부분만 잡는 문제 보정)
    반환값: {'total': float, 'by_leaf': float, 'by_unripe': float,
             'ripe_box_used': tuple}  (0.0 ~ 1.0)
    """
    # ripe bbox 확장 (occluder와의 겹침 영역 확보)
    rx1, ry1, rx2, ry2 = expand_box(ripe_box, expand_ratio, img_h, img_w)
    bbox_area = (rx2 - rx1) * (ry2 - ry1)
    if bbox_area <= 0:
        return {'total': 0.0, 'by_leaf': 0.0, 'by_unripe': 0.0,
                'ripe_box_used': ripe_box}

    # 잎: leaf_mask를 bbox 영역만 크롭해서 픽셀 수 계산
    leaf_px = int(np.count_nonzero(leaf_mask[ry1:ry2, rx1:rx2]))

    # 미성숙 딸기: bbox들을 마스크로 그린 뒤 교집합
    unripe_mask = np.zeros((img_h, img_w), dtype=np.uint8)
    for ux1, uy1, ux2, uy2 in unripe_boxes:
        unripe_mask[max(0,uy1):min(img_h,uy2), max(0,ux1):min(img_w,ux2)] = 255
    unripe_px = int(np.count_nonzero(unripe_mask[ry1:ry2, rx1:rx2]))

    # 합산 (중복 방지: OR 후 카운트)
    combined = cv2.bitwise_or(leaf_mask, unripe_mask)
    total_px = int(np.count_nonzero(combined[ry1:ry2, rx1:rx2]))

    return {
        'total':        min(total_px  / bbox_area, 1.0),
        'by_leaf':      min(leaf_px   / bbox_area, 1.0),
        'by_unripe':    min(unripe_px / bbox_area, 1.0),
        'ripe_box_used': (rx1, ry1, rx2, ry2),   # 확장된 bbox (시각화용)
    }


# ── 시각화 ────────────────────────────────────────────────────────────────────

def draw_overlay(
    frame: np.ndarray,
    ripe_detections: list,   # [(box, occ_dict), ...]
    leaf_mask: np.ndarray,
    unripe_boxes: list,
) -> np.ndarray:
    vis = frame.copy()
    h, w = vis.shape[:2]

    # 잎 반투명 녹색 오버레이
    leaf_layer = vis.copy()
    leaf_layer[leaf_mask > 0] = (20, 160, 60)
    cv2.addWeighted(vis, 0.72, leaf_layer, 0.28, 0, vis)

    # 미성숙 딸기 (청록 박스)
    for ux1, uy1, ux2, uy2 in unripe_boxes:
        cv2.rectangle(vis, (ux1, uy1), (ux2, uy2), (0, 200, 200), 2)
        cv2.putText(vis, 'unripe', (ux1, max(uy1 - 5, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 200, 200), 1, cv2.LINE_AA)

    # 익은 딸기: 폐색 단계별 색상 박스 + 수치
    for box, occ in ripe_detections:
        x1, y1, x2, y2   = box
        total             = occ['total']
        lvl_name, color   = get_level(total)

        # YOLO 원본 bbox
        cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)

        # 폐색률 + 단계
        cv2.putText(vis, f'{total*100:.1f}%  [{lvl_name}]',
                    (x1, max(y1 - 22, 16)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)

        # leaf / unripe 세분화
        cv2.putText(vis,
                    f'leaf:{occ["by_leaf"]*100:.0f}%  '
                    f'unripe:{occ["by_unripe"]*100:.0f}%',
                    (x1, max(y1 - 6, 28)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (210, 210, 210), 1, cv2.LINE_AA)

    # 상단 요약
    if ripe_detections:
        avg_total = sum(o['total'] for _, o in ripe_detections) / len(ripe_detections)
        avg_name, avg_color = get_level(avg_total)
        summary = (f'Ripe: {len(ripe_detections)}  '
                   f'Avg occlusion: {avg_total*100:.1f}%  [{avg_name}]')
        cv2.putText(vis, summary, (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, avg_color, 2, cv2.LINE_AA)
    else:
        cv2.putText(vis, 'No ripe strawberry detected', (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (120, 120, 120), 2, cv2.LINE_AA)

    return vis


# ── 메인 ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='딸기 폐색률 실시간 측정')
    parser.add_argument('--conf',    type=float, default=0.3,
                        help='YOLO confidence threshold (기본값: 0.3)')
    parser.add_argument('--no-leaf', action='store_true',
                        help='HSV 잎 검출 비활성화')
    parser.add_argument('--width',   type=int, default=640)
    parser.add_argument('--height',  type=int, default=480)
    parser.add_argument('--fps',     type=int, default=30)
    parser.add_argument('--expand',  type=float, default=BBOX_EXPAND_DEFAULT,
                        help=f'ripe bbox 확장 비율 (기본값: {BBOX_EXPAND_DEFAULT})'
                             '  0=확장 없음, 0.5=50%% 확장')
    parser.add_argument('--save',    action='store_true',
                        help='[Space] 로 현재 프레임 저장')
    args = parser.parse_args()

    # ── YOLO 로드 ──────────────────────────────────────────────────────────────
    print(f'YOLO 로드: {YOLO_MODEL}')
    yolo = YOLO(YOLO_MODEL)
    print(f'클래스: {yolo.names}')

    # ── RealSense 초기화 ───────────────────────────────────────────────────────
    use_rs = False
    try:
        import pyrealsense2 as rs
        pipeline = rs.pipeline()
        cfg      = rs.config()
        cfg.enable_stream(rs.stream.color,
                          args.width, args.height, rs.format.bgr8, args.fps)
        pipeline.start(cfg)
        print(f'RealSense 연결 완료 ({args.width}x{args.height}@{args.fps}fps)')
        use_rs = True
    except Exception as e:
        print(f'[WARNING] RealSense 연결 실패: {e}')
        print('웹캠(device 0) 으로 대체합니다.')
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print('[ERROR] 웹캠도 열리지 않습니다. 카메라를 확인하세요.')
            return

    save_dir = WS_DIR / 'data' / 'occlusion_snapshots'
    if args.save:
        save_dir.mkdir(parents=True, exist_ok=True)
        print(f'스냅샷 저장 경로: {save_dir}')

    WIN = 'Strawberry Occlusion Meter  [Q/Esc: 종료]'
    cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)

    print('\n================ 조작 방법 ================')
    print(' [Q] / [Esc] : 종료')
    if args.save:
        print(' [Space]     : 현재 프레임 스냅샷 저장')
    print(f' 잎 검출     : {"비활성화" if args.no_leaf else "HSV 녹색"}')
    print('==========================================\n')

    fps_timer = time.time()
    fps_count = 0
    fps_val   = 0.0

    try:
        while True:
            # ── 프레임 취득 ────────────────────────────────────────────────────
            if use_rs:
                frames = pipeline.wait_for_frames()
                cf = frames.get_color_frame()
                if not cf:
                    continue
                frame = np.asanyarray(cf.get_data())
            else:
                ret, frame = cap.read()
                if not ret:
                    break

            h, w = frame.shape[:2]

            # ── YOLO 추론 ──────────────────────────────────────────────────────
            results      = yolo.predict(frame, verbose=False, conf=args.conf)[0]
            ripe_boxes   = []
            unripe_boxes = []
            for box in results.boxes:
                cid         = int(box.cls[0])
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                if cid == CLS_RIPE:
                    ripe_boxes.append((x1, y1, x2, y2))
                else:
                    unripe_boxes.append((x1, y1, x2, y2))

            # ── 잎 마스크 ──────────────────────────────────────────────────────
            leaf_mask = (np.zeros((h, w), dtype=np.uint8)
                         if args.no_leaf
                         else detect_leaf_mask(frame))

            # ── 폐색률 계산 ────────────────────────────────────────────────────
            ripe_detections = []
            for box in ripe_boxes:
                occ = calc_occlusion(box, leaf_mask, unripe_boxes, h, w,
                                     expand_ratio=args.expand)
                ripe_detections.append((box, occ))
                lvl_name, _ = get_level(occ['total'])
                print(f'  ripe={box} -> expanded={occ["ripe_box_used"]}  '
                      f'unripe_boxes={len(unripe_boxes)}  '
                      f'total={occ["total"]*100:.1f}%  '
                      f'leaf={occ["by_leaf"]*100:.1f}%  '
                      f'unripe={occ["by_unripe"]*100:.1f}%  '
                      f'[{lvl_name}]')

            # ── 시각화 ─────────────────────────────────────────────────────────
            vis = draw_overlay(frame, ripe_detections, leaf_mask, unripe_boxes)

            # FPS
            fps_count += 1
            elapsed = time.time() - fps_timer
            if elapsed >= 0.5:
                fps_val   = fps_count / elapsed
                fps_count = 0
                fps_timer = time.time()
            cv2.putText(vis, f'{fps_val:.1f} fps', (w - 95, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 160, 160), 1, cv2.LINE_AA)

            cv2.imshow(WIN, vis)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q'), ord('Q')):
                break
            if args.save and key == ord(' '):
                ts   = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
                path = save_dir / f'occlusion_{ts}.jpg'
                cv2.imwrite(str(path), vis)
                print(f'[저장] {path}')

    finally:
        cv2.destroyAllWindows()
        if use_rs:
            pipeline.stop()
        else:
            cap.release()
        print('종료.')


if __name__ == '__main__':
    main()
