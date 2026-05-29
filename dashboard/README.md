# 딸기 수확 로봇 대시보드

실시간 수확 통계 + 카메라 피드 웹 대시보드 (FastAPI + WebSocket + MJPEG).

## 실행

```bash
cd src/dashboard

docker compose up -d          # 백그라운드 시작
docker compose up             # 포그라운드 (로그 확인)
docker compose down           # 중지
docker compose up -d --build  # 코드 수정 후 재빌드
```

브라우저: **http://localhost:8765**

## 카메라 설정 (docker-compose.yml)

| 상황 | 설정 |
|---|---|
| 웹캠 `/dev/video0` | `devices: - /dev/video0:/dev/video0` (기본) |
| RealSense D435 | `- /dev/bus/usb:/dev/bus/usb` + `privileged: true` |
| 카메라 없음 | `devices` 섹션 전체 주석 처리 |

카메라가 없어도 대시보드는 정상 동작 (카메라 패널에 "연결 없음" 표시).

## 상태 업데이트 (호스트 터미널)

```bash
export HARVEST_STATE_FILE=./data/harvest_state.json

python3 harvest_dashboard.py --update start_harvest    # 수확 시작 (타이머 시작)
python3 harvest_dashboard.py --update harvest_success  # 수확 성공
python3 harvest_dashboard.py --update harvest_fail     # 수확 실패
python3 harvest_dashboard.py --update damage           # 손상 감지
python3 harvest_dashboard.py --update reset            # 통계 초기화

python3 harvest_dashboard.py --msg "꼭지 가림 — 방향 변경" --level warning
python3 harvest_dashboard.py --status grasping
```

## 데모 모드 (Docker 없이 로컬 실행)

```bash
HARVEST_STATE_FILE=./data/harvest_state.json \
  python3 harvest_dashboard.py --demo
```

## 파일 구조

```
dashboard/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── README.md
├── harvest_dashboard.py
└── data/                  ← 상태 파일 볼륨 (git 제외)
    └── harvest_state.json
```

## 대시보드 구성

```
┌──────────────────── 🍓 헤더 (세션 정보 + 시계) ──────────────────────┐
│  수확량 │ 성공률 │ 평균파지 │ 현재수확시간 │ 손상률 │ 총시도  (6카드) │
├──────────┬──────────────────────┬─────────────────────────────────────┤
│ 로봇상태  │   실시간 메시지 로그  │        카메라 피드 (MJPEG)          │
│ (펄스)   │   (최신 40개)        │        RealSense / 웹캠             │
└──────────┴──────────────────────┴─────────────────────────────────────┘
```
