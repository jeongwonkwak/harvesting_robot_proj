# VLA 추론 목업 테스트 앱

**목표**: 로봇 연결이 없거나 카메라가 없을 때, 데이터셋의 실제 이미지로 VLA 추론을 시뮬레이션하고 테스트하기

## 빠른 시작

### 1. Streamlit 앱 실행

```bash
cd /home/user/robot_workspace/vla_ws
streamlit run src/vla_inference_mock_test.py
```

브라우저에서 `http://localhost:8501` 자동으로 열립니다.

### 2. 앱 사용

#### 📸 **카메라 이미지 탭**
- 데이터셋의 첫 에피소드 이미지 두 장 표시
- Camera 1 (base_image): 기본 카메라
- Camera 2 (wrist_image): 손목 카메라

#### 🔮 **VLA 추론 탭**
- **홈 포즈 선택**: top_left, top_right, bottom_left, bottom_right
- **그리퍼 상태**: 0% (완전 열림) ~ 100% (완전 닫힘)
- **작업 지시문**: VLA에 전달할 지시 입력
- **에피소드 리셋**: 새로운 그래스핑 시퀀스 시작 여부

**▶ 추론 실행** 버튼을 누르면:
1. 현재 상태를 32-dim state vector로 변환
2. VLA 추론 시뮬레이션 실행
3. 반환된 action 벡터 상세 표시
4. 계산된 목표 포즈 표시

#### 📊 **결과 분석 탭**
- Action 성분 분석 (선형 이동, 회전, 그리퍼)
- 전체 이동 거리 / 회전각 계산
- 지시문과의 일관성 분석

## 데이터 구조

```
/home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.1/videos/
├── observation.images.camera1/
│   └── chunk-000/
│       ├── file-000.mp4  ← 첫 에피소드
│       ├── file-001.mp4
│       └── ...
└── observation.images.camera2/
    └── chunk-000/
        ├── file-000.mp4  ← 첫 에피소드
        ├── file-001.mp4
        └── ...
```

각 MP4 파일의 **첫 프레임**이 목업 이미지로 사용됩니다.

## 기술 상세

### State Vector (32-dim)

입력으로 전달되는 로봇 상태:

```
[
  tcp_x_m,      # TCP X 위치 (meter)
  tcp_y_m,      # TCP Y 위치 (meter)
  tcp_z_m,      # TCP Z 위치 (meter)
  rx_rad,       # Rx 회전 (radian)
  ry_rad,       # Ry 회전 (radian)
  rz_rad,       # Rz 회전 (radian)
  gripper_ratio,# 그리퍼 개폐도 (0.0 ~ 1.0)
  0.0,          # padding × 25
  ...
  0.0
]
```

### Action Vector (32-dim)

VLA가 반환하는 로봇 동작:

```
[
  delta_x_m,       # X축 이동 (meter)
  delta_y_m,       # Y축 이동 (meter)
  delta_z_m,       # Z축 이동 (meter)
  delta_rx_rad,    # Rx 회전 (radian)
  delta_ry_rad,    # Ry 회전 (radian)
  delta_rz_rad,    # Rz 회전 (radian)
  gripper_ratio,   # 그리퍼 목표값 (0.0 ~ 1.0)
  0.0,             # padding × 25
  ...
  0.0
]
```

### 목업 추론 규칙

지시문에 따라 다른 action을 반환합니다:

| 지시문 | 반응 |
|--------|------|
| `strawberry`, `pick` | ΔX: 50mm, ΔY: 30mm, ΔZ: -100mm, 그리퍼: 95% |
| `grasp` | ΔZ: -80mm, 그리퍼: 90% |
| `release`, `drop` | ΔZ: +100mm, 그리퍼: 5% |
| `home` | 그리퍼: 0% (열기) |
| 기타 | 작은 무작위 이동 |

## 홈 포즈 좌표

| 포즈 | X (mm) | Y (mm) | Z (mm) | Rx (°) | Ry (°) | Rz (°) |
|------|--------|--------|--------|--------|--------|--------|
| top_left | -30.89 | 153.46 | 728.41 | 101.39 | 64.83 | -93.78 |
| **top_right** | 314.90 | 279.89 | 883.40 | 89.90 | 86.29 | -89.62 |
| bottom_left | -30.89 | -153.46 | 600.00 | 101.39 | 64.83 | -93.78 |
| bottom_right | 314.90 | -279.89 | 600.00 | 89.90 | 86.29 | -89.62 |

## 대시보드와의 차이

이 앱은 **테스트 전용**입니다. 실제 로봇 제어는 대시보드를 사용하세요:

### 이 앱 (vla_inference_mock_test.py)
- ✅ 카메라 없이 동작
- ✅ 로봇 연결 없이 동작
- ✅ VLA 추론 결과 시뮬레이션
- ✅ 인터페이스 테스트
- ❌ 실제 로봇 제어 불가

### 대시보드 (harvest_dashboard.py)
- ✅ 실제 로봇 연결
- ✅ 실제 VLA API 호출
- ✅ 로봇 동작 수행
- ✅ 실시간 모니터링
- ⚠️ 카메라 필수

## 문제 해결

### "데이터 경로를 찾을 수 없습니다"
- 데이터셋이 설치되어 있는지 확인:
```bash
ls -la /home/user/robot_workspace/vla_ws/data/fin/vla_dataset_v0.4.1/videos/
```

### "MP4를 디코딩할 수 없습니다"
- OpenCV와 ffmpeg 설치 확인:
```bash
python3 -c "import cv2; print(cv2.VideoCapture('test.mp4'))"
ffmpeg -version
```

### 추론이 너무 느립니다
- Streamlit 캐시 활용 (이미지는 캐시됨)
- 첫 실행 후 빠른 응답 예상

## 향후 개선

- [ ] 실제 VLA 모델 통합
- [ ] 로봇 상태 DB 연동
- [ ] 추론 결과 로깅
- [ ] 여러 에피소드 선택
- [ ] 실시간 비디오 스트리밍

## 참고

- **VLA 추론 서버**: `http://192.168.50.79:18003/predict`
- **대시보드**: `python3 src/harvest_dashboard.py`
- **원본 이미지**: MP4 → 224×224로 리사이즈됨
