# 📦 Docker + Nginx 실습 정리 자료

---

# 1️⃣ Docker 개념

* Docker
  → 애플리케이션을 **컨테이너 단위로 실행**하는 플랫폼

### 핵심 개념

* **이미지(Image)** → 실행 파일 (설치 파일 느낌)
* **컨테이너(Container)** → 실행된 상태 (프로세스 느낌)

👉 흐름

```
이미지 → 실행 → 컨테이너 생성
```

---

# 2️⃣ Docker 설치 (Ubuntu)

```bash
sudo apt-get update

sudo apt-get install -y \
ca-certificates \
curl \
gnupg \
lsb-release
```

### 🔑 GPG 키 추가

```bash
sudo mkdir -m 0755 -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### 📦 레포지토리 등록

```bash
echo \
"deb [arch=$(dpkg --print-architecture) \
signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
sudo apt-get update
```

### 🚀 Docker 설치

```bash
sudo apt-get install -y \
docker-ce docker-ce-cli containerd.io \
docker-buildx-plugin docker-compose-plugin
```

---

# 3️⃣ 기본 명령어

### 컨테이너 실행 테스트

```bash
docker container run hello-world
```

### 상태 확인

```bash
docker container ls      # 실행 중
docker container ls -a   # 전체
docker image ls          # 이미지 목록
```

---

# 4️⃣ Docker 주요 옵션

| 옵션       | 설명         |
| -------- | ---------- |
| `-it`    | 터미널 접속     |
| `-d`     | 백그라운드 실행   |
| `--name` | 컨테이너 이름    |
| `-p`     | 포트포워딩      |
| `-v`     | 볼륨 연결      |
| `--rm`   | 종료 시 자동 삭제 |

---

# 5️⃣ Nginx 컨테이너 실습

* Nginx = 웹 서버

### 실행

```bash
docker run --name nginx -p 8080:80 nginx
```

👉 접속

```
http://127.0.0.1:8080
```

---

### 내부 접속

```bash
docker exec -it nginx /bin/bash
```

---

### 파일 복사

```bash
docker cp test.html nginx:/usr/share/nginx/html
```

👉 접속

```
http://127.0.0.1:8080/test.html
```

---

### 주요 경로

| 항목   | 경로                               |
| ---- | -------------------------------- |
| 설정파일 | `/etc/nginx/conf.d/default.conf` |
| 웹 루트 | `/usr/share/nginx/html`          |

---

# 6️⃣ 포트포워딩 개념

```
호스트 → VM → Docker
```

예:

```
192.168.56.1:8080 → 10.0.2.100:80 → 172.17.0.1:80
```

👉 의미

* 앞: 외부 접속 포트
* 뒤: 컨테이너 내부 포트

---

# 7️⃣ Dockerfile (이미지 만들기)

### 예제

```dockerfile
FROM ubuntu:16.04

COPY helloworld /usr/local/bin
RUN chmod +x /usr/local/bin/helloworld

CMD ["helloworld"]
```

---

### 이미지 생성

```bash
docker build . -t <이미지명>:<버전태그>

# 예시
docker build . -t myimage:latest   # 태그 생략 시 자동으로 latest
docker build . -t myimage:1.0      # 버전 지정
docker build . -t 아이디/myimage:1.0  # Docker Hub 배포용
```

### 실행

```bash
docker run myimage
```

---

# 8️⃣ Docker Hub 배포

```bash
docker login
```

```bash
docker tag <이미지명>:<버전태그> <아이디>/<이미지명>:<버전태그>
docker push <아이디>/<이미지명>:<버전태그>

# 예시
docker tag myimage:1.0 아이디/myimage:1.0
docker push 아이디/myimage:1.0
```

```bash
docker pull <아이디>/<이미지명>:<버전태그>

# 예시
docker pull 아이디/myimage:1.0
```

---

# 9️⃣ Tomcat 컨테이너

```bash
docker run --name tomcat -p 8080:8080 tomcat:9.0
```

### WAR 배포

```bash
docker cp myapp.war tomcat:/usr/local/tomcat/webapps
```

---

# 🔟 Docker Compose

👉 여러 컨테이너를 한번에 실행

* Docker Compose

---

### docker-compose.yml

```yaml
version: "3"
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

### Docker Hub에서 pull 받은 이미지 사용

```yaml
version: "3"
services:
  web:
    image: <아이디>/<이미지명>:<버전태그>   # pull 받은 이미지 지정
    ports:
      - "8080:80"

# 예시
# services:
#   web:
#     image: myid/myimage:1.0
#     ports:
#       - "8080:80"
```

👉 `docker compose up` 실행 시
- 로컬에 이미지 있으면 → 바로 사용
- 로컬에 없으면 → **자동으로 Docker Hub에서 pull** 후 실행

---

### 실행

```bash
docker compose up
```

### 종료

```bash
docker compose down
```

---

# 1️⃣1️⃣ 볼륨 (데이터 유지)

```bash
docker volume create myvolume
```

```bash
docker run -v myvolume:/data nginx
```

👉 컨테이너 삭제해도 데이터 유지됨

---

# 1️⃣2️⃣ VirtualBox 네트워크

* VirtualBox

### 종류

| 방식          | 설명      |
| ----------- | ------- |
| Host-only   | 내부 테스트  |
| NAT         | 외부 인터넷  |
| NAT Network | 클러스터 구성 |

👉 실무 추천: **NAT Network**

---

# 1️⃣3️⃣ 정리 핵심

✔ Docker = 실행 환경
✔ Nginx = 웹 서버
✔ Compose = 여러 컨테이너 관리

---

## 🚀 한 줄 요약

👉 “Docker로 실행하고, Nginx로 서비스하고, Compose로 묶는다”