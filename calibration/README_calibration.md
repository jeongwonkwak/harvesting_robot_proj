# Calibration

고정 카메라와 Doosan E0509 로봇 베이스 간의 좌표 변환 행렬(Eye-to-Hand)을 구하는 캘리브레이션 모듈입니다.

---

## 개요

카메라가 로봇 베이스에 고정된 Eye-to-Hand 구성에서, ArUco 마커를 TCP에 부착하고 여러 자세에서 데이터를 수집하여 카메라 좌표계와 로봇 베이스 좌표계 간의 변환 행렬 `T_cam_to_base`를 SVD 방식으로 추정합니다.

---

## 파일 구성

### 스크립트

| 파일 | 설명 |
|------|------|
| `calibrate_eye_to_hand.py` | Eye-to-Hand 캘리브레이션 메인 스크립트. RealSense 카메라로 ArUco 마커를 감지하고 로봇 TCP 위치와 함께 수집한 데이터를 SVD로 fitting하여 변환 행렬을 계산한다. 스페이스 키로 샘플 수집, c로 캘리브레이션 실행, s로 저장. |
| `calibrate_eye_to_hand_org.py` | 위 스크립트의 원본 백업 버전. |
| `calibrate_z_offset.py` | Z축 오프셋 보정 스크립트. 펜을 카메라로 감지한 위치와 로봇이 직접 이동한 TCP 위치를 비교하여 Z 방향 오차를 추가 보정한다. |

### 데이터 파일

| 파일 | 설명 |
|------|------|
| `calibration_joint_poses.txt` | 캘리브레이션 데이터 수집 시 사용하는 권장 관절 각도 목록. J1~J6 순서, 단위 degree. 10개 포즈로 구성되며 마커가 카메라를 정면으로 향하도록 최적화된 포즈들이다. |

### 결과 파일 (config/)

각 세션 폴더에 아래 두 파일이 저장된다.

| 파일 | 설명 |
|------|------|
| `calibration_eye_to_hand.npz` | 캘리브레이션 결과 행렬. `T_cam_to_base`(4x4), `R_axes`, `t_offset`, 카메라 내부 파라미터(`camera_matrix`, `dist_coeffs`), 수집 데이터(`cam_positions`, `robot_positions`) 포함. |
| `calibration_eye_to_hand_errors.json` | 세션별 오차 통계. 샘플 수, mean/max/min/std(mm), 샘플별 오차(`per_sample_mm`), 판정 결과 포함. |

---

## 실행 방법

```bash
# 캘리브레이션 수행
python calibrate_eye_to_hand.py --robot-ip 192.168.137.100 --marker-size 0.1

# 기존 캘리브레이션 결과 테스트
python calibrate_eye_to_hand.py --test

# ArUco 마커 이미지 생성
python calibrate_eye_to_hand.py --print-marker --marker-id 0
```

조작 키:
- `Space`: 현재 자세에서 샘플 수집
- `c`: 캘리브레이션 계산 실행
- `s`: 결과 저장
- `r`: 수집 데이터 초기화
- `q`: 종료

---

## 세션별 결과 요약

### 20260506 - 초기 시도

- 샘플 수: 30개
- 평균 오차: **844.86 mm**
- 판정: 재캘리브레이션 권장
- 원인 분석: 포즈 다양성이 부족하고 J4가 큰 포즈(60~90도)가 다수 포함되어 마커가 카메라에 대해 크게 기울어진 상태에서 데이터 수집. ArUco 검출 정확도 저하 및 데이터 산포(offset_std ~60cm)가 심해 SVD fitting 신뢰도가 낮음.

### 20260507 - 동일 데이터 재처리

- 샘플 수: 30개 (0506 데이터 재사용)
- 평균 오차: **550.63 mm**
- 방법: rotation_aware_NLS (비선형 최소제곱)
- 판정: 여전히 대오차
- 결과: 방법을 바꾸더라도 수집 포즈 자체의 품질 문제가 근본 원인임을 확인. 포즈 재설계 필요.

### 20260508 - 포즈 최적화 후 재수집

- 샘플 수: 10개
- 평균 오차: **38.12 mm**
- 판정: 좋음
- 개선 요인:
  - J3=90도 고정 (J3=110도는 마커가 카메라 시야에서 벗어나는 경향)
  - J4, J5를 10도 이하로 제한하여 마커 기울기 최소화
  - J6=90도 통일로 마커 방향 일관성 확보
  - 마커가 카메라 이미지 평면과 최대한 평행하게 유지되어 solvePnP 정확도 향상

---

## 포즈 설계 원칙

`calibration_joint_poses.txt`의 포즈는 아래 기준으로 선정되었다.

- **J3 = 90도 고정**: J3가 클수록 TCP가 위로 솟아 마커가 카메라 시야 밖으로 빠지거나 기울어짐
- **J4, J5 소각도 유지 (10도 이내)**: 마커 평면이 카메라 이미지 평면과 평행에 가깝도록 유지
- **J6 = 90도 고정**: 마커 방향 일관성
- **J1, J2로 공간 다양성 확보**: 변환 행렬 추정의 조건수(condition number) 개선을 위해 다양한 XY 위치 분포 필요

---

## 출력 결과 활용

저장된 `calibration_eye_to_hand.npz`를 로드하여 카메라 좌표를 로봇 베이스 좌표로 변환:

```python
import numpy as np

data = np.load("config/20260508_120156/calibration_eye_to_hand.npz")
T_cam_to_base = data["T_cam_to_base"]  # 4x4 변환 행렬

# 카메라 좌표 -> 로봇 베이스 좌표
point_cam = np.array([x, y, z, 1.0])
point_base = T_cam_to_base @ point_cam
```
