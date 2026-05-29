import cv2
import time
import cv2

# 리얼센스
cap = cv2.VideoCapture(4)

if not cap.isOpened():
    print("리얼센스 연결 실패 (노드 번호를 다시 확인하세요)")
else:
    print("리얼센스 연결 성공! 화면을 띄웁니다.")
    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow("RealSense Test", frame)
        if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()