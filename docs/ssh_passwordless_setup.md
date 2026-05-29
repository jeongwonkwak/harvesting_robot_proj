# SSH 비밀번호 없이 서버 접속 설정

## 1단계 — 로컬 PC에서 SSH 키 생성

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- 저장 경로: 엔터 (기본값 `~/.ssh/id_ed25519` 사용)
- 패스프레이즈: 엔터 2번 (없음)

이미 키가 있으면 이 단계 건너뜀 (`~/.ssh/id_ed25519.pub` 파일 존재 여부 확인)

---

## 2단계 — 공개키를 서버에 복사

```bash
ssh-copy-id username@서버IP
```

이때 **마지막으로 한 번** 비밀번호 입력.

`ssh-copy-id`가 없으면 수동으로:

```bash
cat ~/.ssh/id_ed25519.pub | ssh username@서버IP \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

---

## 3단계 — 접속 확인

```bash
ssh username@서버IP
```

비밀번호 없이 바로 접속되면 완료.

---

## (선택) ~/.ssh/config 등록 — 짧은 이름으로 접속

`~/.ssh/config` 파일에 아래 내용 추가:

```
Host myserver
    HostName 192.168.1.100
    User username
    IdentityFile ~/.ssh/id_ed25519
```

이후부터는 아래 한 줄로 접속:

```bash
ssh myserver
```

---

## 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 여전히 비밀번호 요구 | 서버 `authorized_keys` 권한 오류 | 서버에서 `chmod 600 ~/.ssh/authorized_keys` |
| Permission denied | 키 파일 권한 오류 | 로컬에서 `chmod 600 ~/.ssh/id_ed25519` |
| 서버가 키 인증 비허용 | sshd 설정 문제 | 서버 `/etc/ssh/sshd_config`에서 `PubkeyAuthentication yes` 확인 |
