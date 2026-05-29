import cv2
import time

# 1. 확인된 6번 노드로 연결
cap = cv2.VideoCapture(6, cv2.CAP_V4L2)

# 2. 리얼센스 권장 해상도 및 FPS 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# 3. 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('realsense_1min.avi', fourcc, 30.0, (640, 480))

print("🔴 리얼센스 D455 녹화를 시작합니다... (1분 뒤 종료)")
start_time = time.time()

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("프레임을 읽을 수 없습니다.")
            break

        # 저장 및 화면 표시
        out.write(frame)
        cv2.imshow('RealSense Recording...', frame)

        # 1분(60초) 체크
        if time.time() - start_time > 60:
            print("✅ 1분 녹화 완료!")
            break

        # 'q' 누르면 즉시 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 자원 해제 (에러가 나도 안전하게 닫기 위해 try-finally 사용)
    cap.release()
    out.release()
    cv2.destroyAllWindows()