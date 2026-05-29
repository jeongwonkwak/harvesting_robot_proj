# VLA Server 설정 가이드

SmolVLA 서버(Docker)를 올바르게 세팅하고 영구적으로 버그 패치를 반영하는 방법입니다.

---

## 문제 배경

SmolVLA 내부 코드(`smolvlm_with_expert.py`)에서 `attention_mask`를 boolean으로 변환하지 않아
추론 시 다음 오류가 발생합니다:

```
RuntimeError: Expected a boolean tensor for mask
```

컨테이너를 내렸다 올리면 이 변경이 사라지므로, **커스텀 이미지로 영구 반영**해야 합니다.

---

## 1단계: 현재 이미지 이름 확인

```bash
docker inspect vla-server --format='{{.Config.Image}}'
```

출력 예시: `smolvla:7dof`

---

## 2단계: Dockerfile 작성

```bash
cat > Dockerfile.vla-fixed << 'EOF'
FROM smolvla:7dof   # <- 위에서 확인한 이미지명으로 교체

RUN sed -i \
  's/torch\.where(attention_mask\[:, None, :, :\], att_weights, big_neg)/torch.where(attention_mask[:, None, :, :].bool(), att_weights, big_neg)/g' \
  /usr/local/lib/python3.12/dist-packages/lerobot/policies/smolvla/smolvlm_with_expert.py
EOF
```

> **이미지명을 반드시 실제 값으로 교체하세요.**

---

## 3단계: 커스텀 이미지 빌드

```bash
docker build -f Dockerfile.vla-fixed -t vla-server-fixed .
```

---

## 4단계: 기존 컨테이너 중지 후 새 이미지로 실행

기존 컨테이너 실행 명령을 확인:

```bash
docker inspect vla-server --format='{{json .HostConfig}}' | python3 -m json.tool | grep -E "Binds|PortBindings|Devices"
docker inspect vla-server --format='{{.Config.Cmd}} {{.Config.Entrypoint}}'
```

기존 컨테이너 중지:

```bash
docker stop vla-server
docker rm vla-server
```

새 이미지로 실행 (포트·볼륨 등 기존 옵션 유지):

```bash
docker run -d \
  --name vla-server \
  --gpus all \
  -p 16003:16003 \
  vla-server-fixed \
  <원래_실행_명령>   # <- 기존 CMD/Entrypoint로 교체
```

---

## 대안: docker commit (빠른 방법)

Dockerfile 없이 현재 수정된 컨테이너를 이미지로 저장:

```bash
# 1. fix 적용
docker exec vla-server sed -i \
  's/torch\.where(attention_mask\[:, None, :, :\], att_weights, big_neg)/torch.where(attention_mask[:, None, :, :].bool(), att_weights, big_neg)/g' \
  /usr/local/lib/python3.12/dist-packages/lerobot/policies/smolvla/smolvlm_with_expert.py

# 2. 현재 상태를 새 이미지로 저장
docker commit vla-server vla-server-fixed

# 3. 다음부터 vla-server-fixed 이미지 사용
```

---

## 패치 적용 확인

```bash
docker exec vla-server grep -n "bool" \
  /usr/local/lib/python3.12/dist-packages/lerobot/policies/smolvla/smolvlm_with_expert.py \
  | grep attention_mask
```

`.bool()` 가 포함된 줄이 보이면 정상입니다.

---

## 서버 상태 확인

```bash
# 헬스체크
curl http://192.168.50.79:16003/health
# 정상 응답: {"status": "ok", "model_loaded": true}
```

---

## 클라이언트 측 실행 (로봇 PC)

```bash
cd /home/user/robot_workspace/doosan_ws
source install/setup.bash
ros2 launch grasp_vla grasp.launch.py instruction:="pick up the silver cylindrical connector"
```

파라미터 예시:

| 파라미터 | 기본값 | 설명 |
|---|---|---|
| `instruction` | pick up the silver cylindrical connector | VLA 지시어 |
| `action_mode` | cartesian | `cartesian` 또는 `joint` |
| `max_steps` | 50 | 최대 스텝 수 |
| `step_hz` | 5.0 | 제어 주파수 |
| `gripper_port` | /dev/ttyUSB0 | 그리퍼 시리얼 포트 |
| `retreat_delta` | [0.0, -137.0, 61.0, 0.0, 0.0, 0.0] | 파지 후 후퇴 벡터 (mm/deg) |

---

## 모델 사양 (현재)

- **state_dims**: 7 (관절 6개 + 그리퍼 1개)
- **action_dims**: 7 (EEF delta 6개 + 그리퍼 명령 1개)
- **action_chunk_size**: 50
- **서버 주소**: `http://192.168.50.79:16003`
