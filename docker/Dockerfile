FROM nvcr.io/nvidia/isaac-sim:5.1.0

USER root

# 1. ROS 2 Jazzy 저장소 등록
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    gnupg2 \
    lsb-release && \
    add-apt-repository -y universe && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu noble main" \
    | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 2. 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    git-lfs \
    wget \
    vim \
    ros-jazzy-desktop \
    ros-jazzy-realsense2-description \
    ros-jazzy-moveit-msgs \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    && rm -rf /var/lib/apt/lists/*

# 3. PyTorch 설치
RUN pip3 install --break-system-packages \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu121

# 4. AI / Vision 패키지 설치
# 4. AI / Vision 패키지 설치
RUN pip3 install --break-system-packages \
    "numpy<2" \
    "protobuf<6" \
    ultralytics \
    onnxruntime-gpu \
    opencv-python \
    pyrealsense2

# 5. 환경 변수
ENV ROS_DISTRO=jazzy
ENV ISAAC_SIM_PATH="/isaac-sim"

# ROS source 자동 실행
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc

# 6. Workspace 생성
WORKDIR /root/robot_ws
RUN mkdir -p src

CMD ["bash"]