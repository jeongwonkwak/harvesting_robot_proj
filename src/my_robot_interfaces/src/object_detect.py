import cv2
import numpy as np
from ultralytics import YOLO

# ── 파라미터 ───────────────────────────────────────────────────────────────────
CAMERA_ID   = 6
MODEL_PATH  = '/home/user/robot_workspace/doosan_ws/vision/models/public/yolov8n.pt'   # 첫 실행 시 자동 다운로드 (~6MB)
CONF_THRESH = 0.5             # 신뢰도 임계값 (0~1)
MIN_AREA    = 500             # 이 픽셀 수보다 작은 박스는 무시

# 클래스별 색상 (BGR) - 같은 클래스는 항상 같은 색
_COLOR_PALETTE = [
    (0, 255, 0), (0, 128, 255), (255, 0, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 0, 255), (128, 255, 0),
]

def _box_color(class_id: int):
    return _COLOR_PALETTE[class_id % len(_COLOR_PALETTE)]


def draw_detections(frame, results):
    """YOLO 결과를 프레임에 그려 반환하고, 감지 정보 리스트도 반환."""
    out = frame.copy()
    detections = []

    for box in results[0].boxes:
        conf = float(box.conf)
        if conf < CONF_THRESH:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        area = (x2 - x1) * (y2 - y1)
        if area < MIN_AREA:
            continue

        cls_id   = int(box.cls)
        cls_name = results[0].names[cls_id]
        color    = _box_color(cls_id)
        cx, cy   = (x1 + x2) // 2, (y1 + y2) // 2

        # 박스 + 중심점
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        cv2.circle(out, (cx, cy), 5, color, -1)

        # 라벨 (이름 + 신뢰도)
        label = f'{cls_name} {conf:.2f}'
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(out, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(out, label, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

        detections.append({
            'class': cls_name, 'conf': conf,
            'cx': cx, 'cy': cy,
            'x': x1, 'y': y1, 'w': x2 - x1, 'h': y2 - y1,
            'area': area,
        })

    # 감지 수 표시
    count_text = f'Detected: {len(detections)}'
    cv2.putText(out, count_text, (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    return out, detections


def main():
    print(f'YOLOv8 모델 로딩 중: {MODEL_PATH}')
    model = YOLO(MODEL_PATH)
    print('모델 로딩 완료')

    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print(f'카메라 {CAMERA_ID}번 연결 실패')
        return

    print(f'카메라 {CAMERA_ID}번 연결 성공')
    print(f'신뢰도 임계값: {CONF_THRESH}  |  q: 종료')
    print('감지 가능 물체: COCO 80종 (사람, 컵, 병, 의자, 핸드폰 등)')

    detect_win = 'YOLO Object Detection'
    ret, frame = cap.read()
    if not ret:
        print('첫 프레임 읽기 실패')
        return

    cv2.imshow(detect_win, frame)
    cv2.waitKey(200)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        out, detections = draw_detections(frame, results)

        if detections:
            info = '  |  '.join(
                f'{d["class"]}({d["conf"]:.2f}) cx={d["cx"]} cy={d["cy"]}'
                for d in detections
            )
            print(f'\r{info}    ', end='')
        else:
            print('\r감지 없음                                              ', end='')

        cv2.imshow(detect_win, out)

        if cv2.waitKey(1) == ord('q'):
            break

    print('\n종료')
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
