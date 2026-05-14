# syntax=docker/dockerfile:1
FROM osrf/ros:humble-desktop

USER root

# 1. APT 미러 서버 국내(Kakao) 변경으로 다운로드 고속화
RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

# 2. 필수 시스템 패키지, GUI 도구 및 🌟비전/캘리브레이션 지원 패키지 통합 설치
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    # [그룹 A] 기본 빌드 및 개발 유틸리티
    python3-pip \
    curl \
    nginx \
    git \
    wget \
    # [그룹 B] NoVNC 및 가상 데스크톱 (GUI) 도구
    xfce4 \
    xfce4-goodies \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    dbus-x11 \
    x11-utils \
    # [그룹 C] 하드웨어 및 센서 인터페이스 유틸리티 - DISABLED (메인 5개 외)
    #          ※ RealSense 직접 연결 시 활성화. 현재는 ros2-lab 에서 USB 직접 안 씀.
    # usbutils
    # v4l-utils
    # liburdfdom-tools
    # [그룹 D] 두산 협동로봇 하드웨어 드라이버 필수 의존성 (유지: Doosan 빌드 시 필요)
    libpoco-dev \
    libyaml-cpp-dev \
    # [그룹 E] ROS 2 기본 조인트 상태 관리 (유지: dsr_bringup2 launch 호환)
    ros-humble-joint-state-publisher \
    # ros-humble-joint-state-publisher-gui   # ← GUI 안 쓰면 불필요
    # [그룹 F] ROS 2 Control & MoveIt2 핵심 코어 (유지: Doosan 드라이버/MoveIt 코어만)
    # ros-humble-rmw-cyclonedds-cpp          # ← FastRTPS 로 통일했으므로 불필요
    ros-humble-control-msgs \
    ros-humble-realtime-tools \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-moveit \
    ros-humble-moveit-configs-utils \
    ros-humble-moveit-ros-move-group \
    # [그룹 G] 비전 인식 및 로봇 캘리브레이션 카메라 패키지 - DISABLED (메인 5개 외)
    #          ※ realsense / aruco 가 필요하면 아래 주석 해제
    # ros-humble-realsense2-camera
    # ros-humble-realsense2-description
    # ros-humble-aruco-ros
    # ros-humble-cv-bridge
    # ros-humble-image-transport-plugins
    # [그룹 H] MoveIt2 보강 - DISABLED (cuRobo 사용 → MoveIt 보강 불요)
    # ros-humble-moveit-planners-ompl
    # ros-humble-moveit-ros-visualization
    # ros-humble-moveit-setup-assistant
    # ros-humble-moveit-servo
    # ros-humble-moveit-simple-controller-manager
    # ros-humble-pilz-industrial-motion-planner
    # [그룹 I] 3D 점유 그리드 & TF 디버깅 - DISABLED (Pyqtree 만 사용)
    # ros-humble-octomap
    # ros-humble-octomap-msgs
    # ros-humble-tf2-tools
    # [그룹 J] Doosan ROS2 드라이버 + cuRobo 소스 빌드용 의존성 (유지)
    python3-colcon-common-extensions \
    build-essential \
    cmake \
    # [그룹 K] 개발 편의 도구 - DISABLED (필요 시 컨테이너 진입 후 apt install)
    # tmux
    # vim
    # nano
    # htop
    # iputils-ping
    # net-tools
    && rm -rf /var/lib/apt/lists/*

# 3. Rust 기반 고속 패키지 매니저 uv 도입 및 🌟파이썬 의존성 정리
#    핀 정책 (호스트 isaacsim 5.1 환경과 동일하게 맞춰 충돌 회피)
#      - torch 2.7.0 / torchvision 0.22.0  (CUDA 12.6 휠)
#      - numpy 1.26.0  (1.23.5 핀은 폐기 — Isaac/YOLO/cuRobo 모두 ≥1.24 요구)
#      - scipy 는 cuRobo 가 자동으로 끌고 오므로 명시 제거
RUN pip3 install uv

# 3-a) numpy/setuptools 등 일반 pypi 패키지 (분리해서 핀 충돌 방지)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    numpy==1.26.0 \
    "setuptools==58.2.0" \
    "empy==3.3.4" \
    "catkin_pkg"
    # scipy                                 # ← cuRobo 의존성으로 자동 설치됨
    # torchaudio                            # ← 오디오 안 씀

# 3-b) PyTorch — RTX 50 시리즈(Blackwell, sm_120) 지원하는 cu128 휠 전용
#      ※ pytorch 공식 인덱스만 사용 (pypi 와 섞으면 cu126 휠로 잘못 깔림)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    --index-url https://download.pytorch.org/whl/cu128 \
    torch==2.7.0 \
    torchvision==0.22.0

# 3-1. 🌟 우리 팀 메인 스택 (YOLO26 / Quadtree / HTTP 클라이언트)
#       ※ Transformers/HF 스택 (transformers, accelerate, huggingface_hub, safetensors,
#         datasets, einops, sentencepiece) 은 smolvla-server 컨테이너 전담이므로 제거.
#       ※ shapely / open3d / trimesh / Rtree / onnx / onnxruntime-gpu / httpx 는 제거.
#         (필요 시 컨테이너 진입 후 개별 `pip install` 로 처리)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    # --- [비전] YOLO26 (Ultralytics) ---
    ultralytics \
    "opencv-python==4.11.0.86" \
    "pillow==11.3.0" \
    # --- [Quadtree] 2D 분할만 사용 ---
    Pyqtree \
    # --- [HTTP 클라이언트] SmolVLA 서버 호출용 ---
    requests

# 3-2. 🌟 cuRobo (로봇 모션) — 호스트 /home/user01/curobo 가 compose volumes 로
#       /root/curobo 에 마운트됩니다. 컨테이너 첫 실행 후 수동 설치:
#         $ pip install -e /root/curobo
#       자동으로 함께 깔리는 의존성: warp-lang, yourdfpy, trimesh, scipy,
#         scikit-image, pybind11, networkx, numpy-quaternion, pyyaml, tqdm
#       (사전 설치는 안 함 — 이미지 크기·빌드시간 절약)

# 4. 환경 변수 및 원격 라이브러리 패스 확보
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV LD_LIBRARY_PATH=""
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}
ENV QT_X11_NO_MITSHM=1

# 5. 호스트 개발 경로 동기화를 위한 작업 공간 설정
#    compose에서 호스트의 프로젝트 루트를 이 경로로 마운트합니다.
ARG USER_WS=/root/dev
WORKDIR ${USER_WS}

# 5-1. 🌟 Doosan ROS2 드라이버 소스 클론 (별도 워크스페이스 /opt/doosan_ws)
#       - 두산 에뮬레이터(TCP 12345)를 ROS2 토픽/서비스로 노출하는 드라이버.
#       - 빌드는 컨테이너 진입 후 한 번만 수행: `cd /opt/doosan_ws && colcon build`
#       - 사용자 워크스페이스(/root/dev)와 분리해서 충돌/재빌드 비용 최소화.
RUN mkdir -p /opt/doosan_ws/src && \
    cd /opt/doosan_ws/src && \
    git clone --depth 1 -b humble https://github.com/doosan-robotics/doosan-robot2.git || \
    echo "[경고] doosan-robot2 클론 실패 — 네트워크 또는 브랜치 확인 후 수동 클론 필요"

# 6. 터미널 접속 시 ROS 2 자동 소싱 셋업 — 4가지 모드 모두 커버
#    (a) /root/.bashrc           : 인터랙티브 non-login (docker exec bash)
#    (b) /etc/bash.bashrc        : 인터랙티브 (전역)
#    (c) /etc/profile.d/ros2.sh  : login shell (bash -lc 패턴)
#    (d) ENV PATH/LD/PYTHONPATH  : 비인터랙티브 non-login (bash -c "..." 만 쓸 때)
RUN for f in /root/.bashrc /etc/bash.bashrc; do \
        echo "source /opt/ros/humble/setup.bash" >> $f ; \
        echo "if [ -f /opt/doosan_ws/install/setup.bash ]; then source /opt/doosan_ws/install/setup.bash; fi" >> $f ; \
        echo "if [ -f ${USER_WS}/install/setup.bash ]; then source ${USER_WS}/install/setup.bash; fi" >> $f ; \
    done && \
    printf '%s\n' \
      'source /opt/ros/humble/setup.bash' \
      'if [ -f /opt/doosan_ws/install/setup.bash ]; then source /opt/doosan_ws/install/setup.bash; fi' \
      "if [ -f ${USER_WS}/install/setup.bash ]; then source ${USER_WS}/install/setup.bash; fi" \
      > /etc/profile.d/ros2.sh && \
    chmod +x /etc/profile.d/ros2.sh

# 6-1. ROS2 핵심 환경변수를 ENV 로 박아 모든 bash 모드에서 ros2 명령 인식
ENV ROS_DISTRO=humble \
    ROS_VERSION=2 \
    ROS_PYTHON_VERSION=3 \
    AMENT_PREFIX_PATH=/opt/ros/humble \
    PATH=/opt/ros/humble/bin:/usr/local/bin:/usr/bin:/bin \
    LD_LIBRARY_PATH=/opt/ros/humble/lib:/opt/ros/humble/opt/rviz_ogre_vendor/lib:${LD_LIBRARY_PATH} \
    PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages

# 6-2. YOLO/Ultralytics 설정 폴더 미리 생성 (writable 경고 회피)
RUN mkdir -p /root/.config/Ultralytics

# 7. Isaac Sim WebRTC 웹페이지 자산 생성 (9000 포트용)
RUN mkdir -p /var/www/streaming && cat > /var/www/streaming/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Isaac Sim Streaming</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #1a1a2e; color: #eee; font-family: sans-serif; }
    #header { padding: 16px; background: #16213e; display: flex; align-items: center; gap: 16px; }
    #header h1 { font-size: 1.2rem; color: #00d2ff; }
    #status { padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; background: #333; }
    #status.ready { background: #1a5c1a; color: #4cff4c; }
    #status.error { background: #5c1a1a; color: #ff4c4c; }
    #container { display: flex; justify-content: center; align-items: center; height: calc(100vh - 54px); }
    #videoContainer { position: relative; width: 100%; max-width: 1920px; }
    video { width: 100%; height: auto; display: block; background: #000; }
    #overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); text-align: center; pointer-events: none; }
    #connectBtn { margin-top: 16px; padding: 12px 32px; font-size: 1rem; background: #00d2ff; color: #000; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; pointer-events: all; }
    #connectBtn:hover { background: #00a8cc; }
    #connectBtn:disabled { background: #555; color: #999; cursor: not-allowed; }
    #log { position: fixed; bottom: 0; left: 0; right: 0; max-height: 120px; overflow-y: auto; background: rgba(0,0,0,0.85); font-size: 0.75rem; padding: 8px; font-family: monospace; }
  </style>
</head>
<body>
  <div id="header">
    <h1>🚀 Isaac Sim WebRTC Streaming</h1>
    <span id="status">대기 중</span>
  </div>
  <div id="container">
    <div id="videoContainer">
      <video id="video" autoplay playsinline muted></video>
      <div id="overlay">
        <p>Isaac Sim 화면이 여기에 표시됩니다</p>
        <button id="connectBtn" onclick="startStreaming()">▶ 스트리밍 시작</button>
      </div>
    </div>
  </div>
  <div id="log"></div>

<script>
const API = '/api';
function log(msg) {
  const d = document.getElementById('log');
  d.innerHTML += `<div>[${new Date().toLocaleTimeString()}] ${msg}</div>`;
  d.scrollTop = d.scrollHeight;
}

function setStatus(msg, cls) {
  const s = document.getElementById('status');
  s.textContent = msg;
  s.className = cls || '';
}

async function checkReady() {
  try {
    const r = await fetch(`${API}/v1/streaming/ready`);
    const data = await r.json();
    log('서버 상태: ' + JSON.stringify(data));
    return r.ok;
  } catch(e) {
    log('서버 연결 실패: ' + e.message);
    return false;
  }
}

async function startStreaming() {
  document.getElementById('connectBtn').disabled = true;
  setStatus('연결 중...');
  log('Isaac Sim 스트리밍 서버 확인 중...');
  const ready = await checkReady();
  if (!ready) {
    setStatus('서버 오류', 'error');
    document.getElementById('connectBtn').disabled = false;
    return;
  }

  const pc = new RTCPeerConnection({
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
  });
  pc.ontrack = (event) => {
    log('스트림 수신: ' + event.track.kind);
    if (event.track.kind === 'video') {
      document.getElementById('video').srcObject = event.streams[0];
      document.getElementById('overlay').style.display = 'none';
      setStatus('스트리밍 중', 'ready');
    }
  };

  pc.oniceconnectionstatechange = () => {
    log('ICE 상태: ' + pc.iceConnectionState);
    if (pc.iceConnectionState === 'failed') {
      setStatus('연결 실패', 'error');
      document.getElementById('connectBtn').disabled = false;
    }
  };
  pc.addTransceiver('video', { direction: 'recvonly' });
  pc.addTransceiver('audio', { direction: 'recvonly' });

  try {
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    log('WebRTC Offer 생성 완료, 서버로 전송 중...');

    await new Promise(resolve => {
      if (pc.iceGatheringState === 'complete') resolve();
      else pc.onicegatheringstatechange = () => {
        if (pc.iceGatheringState === 'complete') resolve();
      };
      setTimeout(resolve, 3000);
    });
    const resp = await fetch(`${API}/v1/streaming/creds`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        stunIp: 'stun.l.google.com',
        stunPort: 19302
      })
    });
    if (!resp.ok) throw new Error('Credential API 실패: ' + resp.status);
    const creds = await resp.json();
    log('크리덴셜 수신: ' + JSON.stringify(creds));
    setStatus('ICE 협상 중...');

  } catch(e) {
    log('오류: ' + e.message);
    setStatus('연결 실패', 'error');
    document.getElementById('connectBtn').disabled = false;
  }
}

window.onload = async () => {
  log('Isaac Sim 서버 상태 확인 중...');
  const ready = await checkReady();
  if (ready) {
    setStatus('준비 완료', 'ready');
    log('준비 완료. 스트리밍 시작 버튼을 누르세요.');
  } else {
    setStatus('서버 대기 중');
    log('Isaac Sim 서버가 아직 준비되지 않았습니다. 잠시 후 새로고침하세요.');
  }
};
</script>
</body>
</html>
EOF

# 8. Nginx 설정: 내부 루프백 주소를 실제 호스트 IP로 대치하여 안정적 프록시 확보
RUN cat > /etc/nginx/sites-available/default << 'EOF'
server {
    listen 9000;
    server_name _;

    location / {
        root /var/www/streaming;
        index index.html;
    }

    location /api/ {
        # network_mode: host 이므로 같은 호스트의 Isaac Sim(8011)을
        # 루프백으로 안전하게 프록시 (호스트 IP 변경에 영향받지 않음)
        proxy_pass http://127.0.0.1:8011/;
        proxy_http_version 1.1;
        proxy_set_header Host 127.0.0.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 60s;

        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type" always;

        if ($request_method = OPTIONS) {
            return 204;
        }
    }
}
EOF

# 9. NoVNC 가상 데스크톱 구동을 위한 진입점 스크립트 작성
RUN cat > /usr/local/bin/start_gui.sh << 'EOF'
#!/bin/bash
set -e

DISPLAY_NUM=99
export DISPLAY=:${DISPLAY_NUM}

echo "[1/6] Preparing X11 socket directory..."
mkdir -p /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

echo "[2/6] Starting Xvfb on :${DISPLAY_NUM}..."
rm -f /tmp/.X${DISPLAY_NUM}-lock
Xvfb :${DISPLAY_NUM} -screen 0 1920x1080x24 -ac +extension GLX &

for i in $(seq 1 10);
do
    xdpyinfo -display :${DISPLAY_NUM} >/dev/null 2>&1 && echo "  Xvfb ready." && break
    echo "  Waiting for Xvfb... ($i/10)"
    sleep 1
done

echo "[3/6] Starting XFCE desktop..."
DISPLAY=:${DISPLAY_NUM} startxfce4 &

echo "[4/6] Starting x11vnc on :5900..."
x11vnc -display :${DISPLAY_NUM} -nopw -forever -shared \
       -bg -rfbport 5900 -o /var/log/x11vnc.log
sleep 1

echo "[5/6] Starting nginx (Isaac Sim WebRTC client on :9000)..."
nginx

echo "[6/6] Starting NoVNC on 0.0.0.0:8080..."
exec websockify --web=/usr/share/novnc/ 0.0.0.0:8080 localhost:5900
EOF

RUN chmod +x /usr/local/bin/start_gui.sh