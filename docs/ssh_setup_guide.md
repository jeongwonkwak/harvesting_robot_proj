# SSH 첫 접속 설정 가이드 (로컬 → 서버)

## 서버 쪽 설정

### 1. OpenSSH 서버 설치 및 실행

```bash
sudo apt update
sudo apt install -y openssh-server

# 서비스 시작 및 자동 시작 등록
sudo systemctl start ssh
sudo systemctl enable ssh

# 실행 확인
sudo systemctl status ssh
```

### 2. 방화벽 허용 (UFW 사용 시)

```bash
sudo ufw allow ssh
sudo ufw enable
```

### 3. 서버 IP 확인

```bash
ip addr show
# 또는
hostname -I
```

---

## 로컬 쪽 설정

### 4. SSH 키 생성 (없으면)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# 엔터 3번 (기본 경로, 패스프레이즈 없음)
```

### 5. 공개키를 서버에 등록

```bash
ssh-copy-id username@서버IP
# 이때 마지막으로 한 번 비밀번호 입력
```

`ssh-copy-id` 없으면 수동으로:

```bash
cat ~/.ssh/id_ed25519.pub | ssh username@서버IP \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### 6. 접속 확인

```bash
ssh username@서버IP
# 비밀번호 없이 접속되면 완료
```

---

## (선택) ~/.ssh/config — 단축 이름으로 접속

`~/.ssh/config` 파일에 추가:

```
Host myserver
    HostName 192.168.1.100
    User username
    IdentityFile ~/.ssh/id_ed25519
```

이후 아래 명령 하나로 접속:

```bash
ssh myserver
```

---

## 설정 요약

| 단계 | 위치 | 명령 |
|---|---|---|
| SSH 서버 설치 | 서버 | `sudo apt install openssh-server` |
| 방화벽 허용 | 서버 | `sudo ufw allow ssh` |
| 키 생성 | 로컬 | `ssh-keygen -t ed25519` |
| 공개키 등록 | 로컬 | `ssh-copy-id user@서버IP` |
| 단축 이름 설정 | 로컬 | `~/.ssh/config` 편집 |

---

## 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| `Connection refused` | SSH 서버 미실행 | 서버에서 `sudo systemctl start ssh` |
| `Permission denied` | 키 권한 오류 | `chmod 600 ~/.ssh/id_ed25519` |
| 여전히 비밀번호 요구 | `authorized_keys` 권한 오류 | 서버에서 `chmod 600 ~/.ssh/authorized_keys` |
| 같은 네트워크인데 연결 안 됨 | 방화벽 차단 | `sudo ufw allow ssh` |
