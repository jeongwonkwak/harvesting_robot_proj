# SmolVLA Fine-tuning Guide (LeRobot)

LeRobot 프레임워크를 활용하여 SmolVLA를 Docker 환경에서 학습하는 방법을 설명합니다.

---

## 디렉토리 구조

```
jeongwon_lab/
├── train/
│   ├── Dockerfile.smolvla_train     # 학습 이미지 정의
│   ├── docker-compose.yml           # 컨테이너 설정
│   ├── train_entrypoint.sh          # 컨테이너 진입점
│   └── train.sh         # 학습 실행 스크립트 (볼륨 마운트)
├── data/vla/                        # 학습 데이터셋 (컨테이너 내 /data/vla)
├── models/
│   ├── public/smolvla_base/         # 베이스 모델 (컨테이너 내 /models/smolvla_base, read-only)
│   └── ours/                        # 학습 결과 저장 (컨테이너 내 /models/ours)
├── logs/                            # 학습 로그 (컨테이너 내 /logs)
├── lerobot/                         # lerobot 소스 (이미지 빌드 시 복사)
└── src/
    └── make_sample_dataset.py       # 샘플 데이터셋 생성 스크립트
```

---

## 데이터셋 준비

SmolVLA는 **LeRobotDataset v3.0 포맷**을 사용합니다. → 상세 포맷: [`DATASET_FORMAT.md`](./DATASET_FORMAT.md)

- 최소 권장: **task당 50 에피소드 이상**
- 25 에피소드 이하는 성능 저하 확인됨 (SmolVLA 논문)

### 샘플 데이터셋 생성 (테스트용)

```bash
python3 src/make_sample_dataset.py
# 출력: data/vla/smolvla_sft_dataset_v.0.1.0/ (5 에피소드)
```

### 로컬 데이터셋 경로

`train.sh`의 `DATASET_REPO_ID`에 컨테이너 내부 경로(`/data/vla/...`)를 지정합니다.

```bash
DATASET_REPO_ID="/data/vla/smolvla_sft_dataset_v.0.1.0"
```

---

## Docker 이미지 빌드

```bash
docker compose -f train/docker-compose.yml build
```

빌드 시 `lerobot/` 소스가 이미지 안으로 복사됩니다. lerobot 소스 변경 시 재빌드가 필요합니다.

> **flash_attn 제거**: 베이스 이미지(PyTorch 25.01)의 CUDA 버전과 호스트 CUDA 12.8 간 ABI 불일치로 인해 Dockerfile에서 flash_attn을 제거합니다. SmolVLA는 flash_attn 없이도 정상 동작합니다.

---

## 학습 실행

### 1. 컨테이너 시작

```bash
docker compose -f train/docker-compose.yml up -d
```

컨테이너가 시작되어도 학습은 자동으로 시작되지 않습니다.

### 2. 컨테이너 접속

```bash
docker exec -it vla-train bash
```

### 3. 학습 실행 (백그라운드)

```bash
nohup /workspace/train/train.sh > /dev/null 2>&1 &
```

`train.sh`는 볼륨 마운트되어 있어 컨테이너 재시작 없이 수정 내용이 즉시 반영됩니다.

### 4. 로그 확인

```bash
# 호스트에서
tail -f logs/<JOB_NAME>_<TIMESTAMP>.log

# 컨테이너 안에서
tail -f /logs/<JOB_NAME>_<TIMESTAMP>.log
```

---

## 학습 설정 변경

`train/train.sh`에서 수정합니다.

```bash
DATASET_REPO_ID="/data/vla/smolvla_sft_dataset_v.0.1.0"
JOB_NAME="smolvla_sft_v.0.1.0"
STEPS=20000
BATCH_SIZE=32
```

| 인자 | 설명 |
|---|---|
| `--policy.path` | 베이스 모델 경로 (로컬: `/models/smolvla_base`) |
| `--dataset.repo_id` | 학습 데이터셋 경로 |
| `--steps` | 학습 스텝 수 (A100 1장 기준 20,000 steps ≈ 약 4시간) |
| `--batch_size` | 배치 크기 |
| `--dataset.use_imagenet_stats=false` | 로컬 데이터셋 사용 시 필수 |
| `--policy.push_to_hub=false` | Hub 업로드 비활성화 |
| `--wandb.enable=false` | WandB 로깅 비활성화 |

> `--policy.dtype`, `--policy.gradient_checkpointing`은 SmolVLA에서 지원하지 않으므로 사용하지 않습니다.

---

## 학습 결과

체크포인트는 호스트의 `models/ours/<JOB_NAME>/` 에 저장됩니다.

```
models/ours/smolvla_sft_v.0.1.0/
├── checkpoints/
│   ├── 005000/pretrained_model/
│   ├── 010000/pretrained_model/
│   └── last/pretrained_model/     ← 최종 모델
└── train_smolvla_sft_v.0.1.0_<TIMESTAMP>.log
```

---

## 참고 링크

- [LeRobot GitHub](https://github.com/huggingface/lerobot)
- [SmolVLA 공식 문서](https://huggingface.co/docs/lerobot/en/smolvla)
- [smolvla_base 모델](https://huggingface.co/lerobot/smolvla_base)
- [SmolVLA 논문](https://arxiv.org/abs/2506.01844)
- [참고 데이터셋 (svla_so100_pickplace)](https://huggingface.co/datasets/lerobot/svla_so100_pickplace)
