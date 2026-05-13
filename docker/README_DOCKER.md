# Strawberry Harvest - Docker 빌드 및 실행 가이드

> 두산 로봇(E0509) + Isaac Sim 5.1 + ROS2 Humble 통합 시뮬레이션 환경
> `strawberry_harvest` 팀 전용

---

## 1. 사전 준비 (호스트 1회만)

### 1-1. NVIDIA GPU 드라이버 확인
```bash
nvidia-smi
```
드라이버가 출력되지 않으면 먼저 NVIDIA 드라이버를 설치하세요.

### 1-2. NVIDIA Container Toolkit 설치
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && \
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

확인:
```bash
docker info | grep -i runtime
# → Runtimes: io.containerd.runc.v2 nvidia runc  가 나와야 함

docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
# → GPU 표가 정상 출력되면 성공
```

### 1-3. X11(GUI) 허용
```bash
xhost +local:docker
```

### 1-4. (선택) NGC 로그인 - Isaac Sim 이미지 받을 때 필요
```bash
docker login nvcr.io
# Username: $oauthtoken
# Password: <NGC API KEY>
```

---

## 2. 프로젝트 Docker 구조

```
/home/user01/harvesting_robot_miniproj/
├── docker/                     ← 도커 관련 모든 파일 (한 곳에 정리됨)
│   ├── docker-compose.yml      ← 4개 컨테이너 + profiles 정의
│   ├── Dockerfile              ← ros2-lab (Humble + YOLO26 + Pyqtree)
│   ├── Dockerfile.smolvla      ← smolvla-server (FastAPI + lerobot[smolvla])
│   ├── .env.example            ← USER_ID / ROS_DOMAIN_ID / ENABLE_GUI 템플릿
│   ├── README_DOCKER.md        ← 본 문서
│   └── smolvla/
│       └── serve_smolvla.py    ← SmolVLA FastAPI 서버 스켈레톤
└── src/                        ← ROS2 패키지 (팀원이 직접 작성)

# 호스트 공용 (도커 외부)
/home/user01/
├── curobo/                     ← cuRobo 소스 (ros2-lab 에 /root/curobo 로 마운트)
└── models/                     ← 모델 가중치 공용 폴더 (smolvla-server 에 /models 로 마운트)
    └── vla-model/              ← (직접 다운로드) SmolVLA 체크포인트
```

마운트 매핑:
| 호스트 경로 | 컨테이너 안 경로 | 어느 컨테이너 |
|-------------|-------------------|----------------|
| `/home/user01/harvesting_robot_miniproj` | `/root/dev` | ros2-lab |
| `/home/user01/curobo` | `/root/curobo` | ros2-lab |
| `/home/user01/harvesting_robot_miniproj/docker/smolvla` | `/app` | smolvla-server |
| `/home/user01/models` | `/models` | smolvla-server |

---

## 3. 팀원별 환경 변수 설정 (필수)

```bash
cd /home/user01/harvesting_robot_miniproj/docker
cp .env.example .env
```

`.env` 에서 3가지 값 설정:

| 변수 | 의미 | 권장 값 |
|------|------|---------|
| `USER_ID` | 컨테이너 이름 prefix (개인 인스턴스) | 본인 아이디 (예: `jiwoo`) |
| `ROS_DOMAIN_ID` | ROS2 DDS 도메인 (팀원 간 토픽 격리) | 팀원 1~4 → `1`~`4` |
| `ENABLE_GUI` | NoVNC GUI 자동 기동 여부 | RViz 안 쓰면 `0` (기본) |

> 로봇 도메인 `66` 과는 별개. 실로봇과 통신 시 `.env` 의 `ROS_DOMAIN_ID` 만 `66` 으로 변경.

### 개인 인스턴스 충돌 방지 원리
- `USER_ID=jiwoo` → 컨테이너 이름이 자동으로 `jiwoo_ros2_lab`, `jiwoo_sim_engine` ... 으로 prefix 됨.
- 같은 호스트 컴퓨터에서 팀원 4명이 동시에 띄워도 컨테이너 이름이 안 겹침.
- 이미지는 호스트 도커 데몬이 공유 → 한 번만 빌드하면 모두가 같은 이미지 사용.

---

## 4. 기본 빌드/실행 명령

### 4-0. 빌드 전 체크리스트 ⚠️
1. **BuildKit 활성화 필수** — Dockerfile 들이 `--mount=type=cache` 를 사용하므로 BuildKit 이 켜져 있어야 빌드 성공합니다.
   ```bash
   export DOCKER_BUILDKIT=1
   export COMPOSE_DOCKER_CLI_BUILD=1
   ```
   영구 설정은 `~/.bashrc` 에 위 두 줄 추가.
2. **NGC 로그인** — `nvcr.io/nvidia/isaac-sim:5.1.0` 과 `nvcr.io/nvidia/pytorch:25.01-py3` 모두 NGC 인증 필요.
   ```bash
   docker login nvcr.io
   # Username: $oauthtoken
   # Password: <NGC API KEY>
   ```
3. **디스크 여유 확인** — 4개 컨테이너 합쳐 약 **40~50GB** 사용. `df -h /var/lib/docker` 로 여유 확인.
4. **`.env` 파일 생성** — 섹션 3 참고. ROS_DOMAIN_ID 본인 번호로 설정.

### 4-1. 프로필 기반 부분 빌드/실행 ⭐ 핵심
```bash
cd /home/user01/harvesting_robot_miniproj/docker

# (A) 자기 파트만 띄우기 — 가장 권장
docker compose --profile dev   up -d --build   # ros2-lab + 두산 에뮬레이터
docker compose --profile vla   up -d --build   # smolvla-server
docker compose --profile sim   up -d           # Isaac Sim
docker compose --profile robot up -d           # 두산 에뮬레이터 단독

# (B) 여러 파트 동시 (조합 자유)
docker compose --profile dev --profile sim up -d
docker compose --profile dev --profile vla up -d

# (C) 통째로 4개 다 띄우기 (혼자 컴퓨터 점유할 때만)
docker compose --profile all up -d --build
```

### 4-2. 한 컴퓨터를 4명이 공유할 때 권장 분담
| 역할 | 띄울 프로필 | 비고 |
|------|-------------|------|
| “인프라 담당” 한 명 | `--profile sim --profile vla` | 무거운 isaac-sim, smolvla-server |
| 나머지 3명 | `--profile dev` | 가벼운 ros2-lab + 에뮬레이터 |

→ 같은 호스트의 `localhost:8000`(smolvla) / `localhost:8011`(Isaac) 으로 모두 접근 가능.

### 4-3. 중지/정리
```bash
docker compose --profile all down            # 컨테이너만 정리
docker compose --profile all down -v         # 볼륨까지 정리
docker compose stop <서비스>                  # 특정 서비스만 멈춤
```

### 4-4. 로그 확인
```bash
# ROS2 제어부 로그 실시간
docker compose logs -f ros2-lab

# Isaac Sim 준비 완료 대기 (약 60~90초)
docker compose logs -f isaac-sim | grep -E "app ready|Streaming|http|url|8011"

# SmolVLA 서버 로그
docker compose logs -f smolvla-server
```

---

## 5. 컨테이너 진입

컨테이너 이름은 `.env` 의 `USER_ID` 값이 prefix 로 붙습니다. 예: `USER_ID=jiwoo` → `jiwoo_ros2_lab`.

> ⚠️ **`${USER_ID}` 는 셸 변수입니다.** 아래 명령어를 그대로 복붙할 때, 셸이 `.env` 를 자동으로 안 읽으니 **둘 중 하나** 선택:
> ```bash
> # (방법 A) 셸에 .env 값을 한 번 로드
> set -a && source .env && set +a
>
> # (방법 B) 컨테이너 이름을 직접 (예: USER_ID=team1 인 경우)
> docker exec -it team1_ros2_lab bash
> ```

| 역할 | 컨테이너 이름 | 진입 명령 |
|------|---------------|----------|
| Isaac Sim 엔진 | `${USER_ID}_sim_engine`   | `docker exec -it ${USER_ID}_sim_engine bash` |
| 두산 로봇 에뮬레이터 | `${USER_ID}_robot_emulator` | `docker exec -it ${USER_ID}_robot_emulator bash` |
| ROS2 제어부 (메인 작업 환경) | `${USER_ID}_ros2_lab` | `docker exec -it ${USER_ID}_ros2_lab bash` |
| SmolVLA 추론 서버 | `${USER_ID}_smolvla_server` | `docker exec -it ${USER_ID}_smolvla_server bash` |

ROS2 컨테이너에서 진입 없이 바로 명령 실행 (`.bashrc` / `/etc/profile.d/ros2.sh` / ENV PATH 어디서든 ros2 가 잡힘):
```bash
docker exec -it ${USER_ID}_ros2_lab bash -c "ros2 topic list"
```

---

## 6. 접속 포트 (GUI / 스트리밍 / 추론 API)

| 서비스 | URL/포트 | 설명 |
|--------|----------|------|
| NoVNC 가상 데스크톱 | `http://<호스트IP>:8080/vnc.html` | XFCE 데스크톱 (rviz2, rqt 등) |
| Isaac Sim WebRTC 뷰어 | `http://<호스트IP>:9000` | 시뮬레이션 화면 |
| Isaac Sim API | `<호스트IP>:8011` | nginx가 내부 프록시로 사용 |
| 두산 로봇 에뮬레이터 | `localhost:12345` | TCP 통신 |
| SmolVLA 추론 API | `http://<호스트IP>:8000` | FastAPI 서버 (`/health`, `/predict`, `/info`) |

---

## 7. 빌드 명령 요약 치트시트

```bash
cd /home/user01/harvesting_robot_miniproj/docker

# 부분 기동 (자기 파트)
docker compose --profile dev up -d --build
docker compose --profile vla up -d --build
docker compose --profile sim up -d
docker compose --profile robot up -d

# 전부 기동
docker compose --profile all up -d --build

# 정리
docker compose --profile all down
docker compose stop ros2-lab

# 로그
docker compose logs -f ros2-lab
docker compose logs -f smolvla-server
docker compose logs -f isaac-sim | grep -E "app ready|Streaming|http|url|8011"

# 진입 (USER_ID 는 본인 .env 값)
docker exec -it ${USER_ID}_ros2_lab bash
docker exec -it ${USER_ID}_smolvla_server bash

# ros2-lab 안에서 바로 ROS 명령
docker exec -it ${USER_ID}_ros2_lab \
  bash -c "source /opt/ros/humble/setup.bash && ros2 topic list"
```

---

## 8. 자주 나는 문제 해결

| 증상 | 원인 / 해결 |
|------|-------------|
| `docker compose up` 시 GPU 인식 실패 | 섹션 1-2 NVIDIA Container Toolkit 재설치 후 `sudo systemctl restart docker` |
| Isaac Sim 컨테이너가 곧바로 꺼짐 | `ACCEPT_EULA=Y` 확인, NGC 로그인 여부 확인, `nvidia-smi` 호스트에서 동작 확인 |
| ros2-lab 빌드 중 `apt` 느림 | Dockerfile이 Kakao 미러로 변경되어 있으므로 일시적 네트워크 이슈일 수 있음. 재시도 |
| 토픽이 보이지 않음 (`ros2 topic list` 비어있음) | 팀원 모두 `.env` 의 `ROS_DOMAIN_ID` 가 같은지 확인. **로봇 통신 시에는 본인의 도메인과 로봇 도메인이 같아야 함** |
| NoVNC 화면이 검은색 | `docker compose logs ros2-lab` 에서 `Xvfb`, `startxfce4` 정상 시작 여부 확인 |
| WebRTC 뷰어가 `서버 오류` | `docker compose logs -f isaac-sim` 에서 `app ready` 로그 나올 때까지 대기 (약 60~90초) |
| `Permission denied: /dev/bus/usb` | RealSense 카메라 미연결이면 무시 가능. 연결 시 호스트에서 `lsusb` 로 인식 확인 |
| SmolVLA 서버가 503 응답 | `docker compose logs -f smolvla-server` 확인. `serve_smolvla.py` 의 `load_model()` 이 아직 placeholder 일 수 있음 (팀원 작업 필요) |
| SmolVLA 모델 가중치 못 찾음 | 호스트의 `/home/user01/models/vla-model/` 에 가중치 배치 (컨테이너에는 `/models/vla-model` 로 보임). 또는 `.env` 의 `MODEL_PATH` 를 HF 허브 ID 로 변경 |
| 컨테이너 모두 OOM (GPU 메모리 부족) | Isaac Sim + YOLO + SmolVLA 동시 가동 시 발생. SmolVLA 환경변수 `DEVICE=cuda:0` 을 `cpu` 로 임시 변경하거나 한 컨테이너씩 기동 |

---

## 9. 우리 팀 스택 패키지 (메인 5개 기준 최소 구성)

빌드된 `ros2-lab` 컨테이너 안에서 바로 import 가능한 것 (✅) 과 별도 처리 필요한 것 (🛠️) 으로 구분.

### 9-A. `ros2-lab` 에 사전 설치된 것 (✅)

| 분야 | 패키지 / 버전 | 주요 import |
|------|---------------|-------------|
| **PyTorch** | `torch==2.7.0+cu128`, `torchvision==0.22.0` (RTX 50 sm_120 지원) | `import torch` |
| **공통 수치** | `numpy==1.26.0` | `import numpy` |
| **비전 (YOLO26)** | `ultralytics`, `opencv-python==4.11.0.86`, `pillow==11.3.0` | `from ultralytics import YOLO` |
| **Quadtree** | `Pyqtree` | `from pyqtree import Index` |
| **HTTP 클라이언트** | `requests` | SmolVLA 서버 호출 |
| **ROS2 Humble 코어** | `ros2_control`, `ros2_controllers`, `control-msgs`, `realtime-tools`, `moveit`(코어), `moveit-configs-utils`, `moveit-ros-move-group`, `joint-state-publisher` | apt |
| **빌드 도구** | `python3-colcon-common-extensions`, `build-essential`, `cmake` | colcon, gcc |

### 9-B. 컨테이너 진입 후 1회 수동 설치 (🛠️)

| 분야 | 처리 방법 | 비고 |
|------|-----------|------|
| **cuRobo** | `pip install -e /root/curobo` (호스트에서 마운트됨) | §13 참고. 자동 의존성: `warp-lang`, `yourdfpy`, `trimesh`, `scipy`, `scikit-image`, `pybind11`, `networkx`, `numpy-quaternion`, `pyyaml`, `tqdm` |
| **Doosan ROS2 드라이버** | `colcon build` (소스 `/opt/doosan_ws/src/doosan-robot2` 미리 클론됨) | §11 참고 |

### 9-C. 별도 컨테이너 전담 (🚫 ros2-lab 에서는 import 안 됨)

| 분야 | 어느 컨테이너 | 들어 있는 것 |
|------|---------------|--------------|
| **SmolVLA / Transformers** | `smolvla-server` | `lerobot[smolvla]`, `transformers`, `accelerate`, `huggingface_hub`, `safetensors`, `datasets`, `einops`, `sentencepiece`, `fastapi`, `uvicorn`, `pydantic`, `opencv-python-headless` |
| **Isaac Sim 5.1** | `isaac-sim` | NGC 이미지 그대로 |

### 9-D. ros2-lab 안에서 YOLO 동작 확인
```bash
docker exec -it ${USER_ID}_ros2_lab bash
python3 -c "
import torch
from ultralytics import YOLO
import numpy as np
m = YOLO('yolo11n.pt')   # 자동 다운로드
r = m.predict(np.zeros((640,640,3), dtype='uint8'), device='cuda:0', verbose=False)
print('OK | device =', r[0].boxes.data.device, '| torch', torch.__version__)
"
```

### 9-E. SmolVLA 서버 호출 예시 (ros2-lab 내부에서)
```python
import base64, requests, cv2

img = cv2.imread("test.jpg")
_, buf = cv2.imencode(".jpg", img)
b64 = base64.b64encode(buf).decode()

resp = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"image_b64": b64, "instruction": "pick up the red strawberry"},
    timeout=10,
)
print(resp.json())
```

### 9-F. 빠진 항목 (메인 5개 외 — 필요 시 컨테이너 안에서 개별 설치)
- `shapely`, `open3d`, `trimesh`(명시), `Rtree`, `onnx`, `onnxruntime-gpu`, `httpx`
- MoveIt 보강 (`moveit-planners-ompl`, `moveit-servo`, `pilz-industrial-motion-planner` 등)
- `octomap`, `octomap-msgs`, `tf2-tools`
- RealSense / ArUco / cv-bridge ROS 패키지
- 개발 편의 (`tmux`, `vim`, `nano`, `htop`, `net-tools`)

---

## 10. SmolVLA 추론 서버 빌드/운영

### 10-1. 빌드만 따로 하기
```bash
cd /home/user01/harvesting_robot_miniproj/docker
docker compose build smolvla-server
```
첫 빌드는 PyTorch NGC 이미지(~10GB) + lerobot 의존성 때문에 **15~30분** 정도 걸립니다.

### 10-2. 서버 코드 수정 (핫리로드 안 됨, 컨테이너 재시작 필요)
```bash
# 호스트에서 docker/smolvla/serve_smolvla.py 수정 후
docker compose restart smolvla-server
docker compose logs -f smolvla-server
```
> `serve_smolvla.py` 는 호스트 ↔ 컨테이너 마운트되어 있으므로 코드 변경은 즉시 반영되지만, FastAPI 가 재시작되어야 적용됩니다.

### 10-3. 헬스체크 / 상태 확인
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/info
```

### 10-4. 모델 가중치 배치
호스트 공용 폴더 `/home/user01/models/` 를 사용합니다 (이미 존재).

1) HuggingFace 허브에서 직접 받기:
```bash
huggingface-cli download <repo_id> --local-dir /home/user01/models/vla-model
```
2) 또는 `MODEL_PATH` 를 허브 ID 로 바꾸고 컨테이너 안에서 자동 다운로드 (HF 캐시는 `~/.cache/huggingface` 볼륨으로 보존).

### 10-5. 서버 코드 직접 실행 (디버깅용)
```bash
docker exec -it ${USER_ID}_smolvla_server bash
cd /app
python serve_smolvla.py
```

---

## 11. Doosan ROS2 드라이버 빌드 (최초 1회)

Dockerfile 에서 `/opt/doosan_ws/src/doosan-robot2` 로 소스만 클론해 두었습니다.
컨테이너 안에서 직접 빌드하세요:

```bash
docker exec -it ${USER_ID}_ros2_lab bash
cd /opt/doosan_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source /opt/doosan_ws/install/setup.bash   # 이미 .bashrc 에 자동 source 됨
```

빌드 후 새 터미널에서 `ros2 pkg list | grep dsr` 로 패키지 노출 확인:
```bash
ros2 pkg list | grep dsr
# dsr_bringup2, dsr_controller2, dsr_description2, dsr_msgs2, dsr_example2 ...
```

에뮬레이터에 연결해서 토픽 확인:
```bash
ros2 launch dsr_bringup2 dsr_bringup2.launch.py \
  mode:=virtual host:=127.0.0.1 port:=12345 model:=e0509
ros2 topic list | grep dsr
```

> 클론이 실패했다면 Dockerfile 의 git clone 단계 로그 확인 후 수동으로 클론하세요.

---

## 12. 전체 4컨테이너 기동 순서 (참고)

```bash
cd /home/user01/harvesting_robot_miniproj/docker
docker compose --profile all up -d --build

# 1) Isaac Sim 준비 대기 (60~90s)
docker compose logs -f isaac-sim | grep -E "app ready|Streaming"

# 2) SmolVLA 서버 헬스체크
curl http://127.0.0.1:8000/health

# 3) ROS2 토픽 확인
docker exec -it ${USER_ID}_ros2_lab \
  bash -c "source /opt/ros/humble/setup.bash && ros2 topic list"

# 4) (선택) NoVNC 접속 — .env 에 ENABLE_GUI=1 설정 시
# http://<호스트IP>:8080/vnc.html
```

---

## 13. cuRobo 설치 (최초 1회, ros2-lab 컨테이너 안에서)

호스트 `/home/user01/curobo` 가 컨테이너의 `/root/curobo` 로 마운트되어 있습니다. 이미지 빌드 시 자동 설치는 하지 않으므로 컨테이너 진입 후 1회 설치합니다.

```bash
docker exec -it ${USER_ID}_ros2_lab bash
cd /root/curobo
pip install -e .
```

자동으로 함께 설치되는 의존성: `warp-lang`, `yourdfpy`, `trimesh`, `scipy`, `scikit-image`, `pybind11`, `networkx`, `numpy-quaternion`, `pyyaml`, `tqdm`.

설치 확인:
```bash
python3 -c "from curobo.types.robot import RobotConfig; print('cuRobo OK')"
```

## 14. 부분 빌드/실행 매트릭스 ⭐

| 시나리오 | 명령 | 띄워지는 것 |
|----------|------|-------------|
| YOLO 파인튜닝만 | `docker compose --profile dev up -d` | ros2-lab + dsr_emulator |
| cuRobo 모션 디버깅 | `docker compose --profile dev --profile sim up -d` | ros2-lab + 에뮬레이터 + Isaac Sim |
| SmolVLA 서버 개발 | `docker compose --profile vla up -d` | smolvla-server 만 |
| 통합 테스트 | `docker compose --profile all up -d` | 4개 전부 |
| 에뮬레이터만 확인 | `docker compose --profile robot up -d` | dsr_emulator 만 |
