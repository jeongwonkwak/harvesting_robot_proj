# VLA 모델 비교표

> 작성일: 2026-05-21  
> 목적: Doosan e0509 (6-DoF + 그리퍼) 파인튜닝 후보 모델 선정 참고용  
> ※ 불확실한 항목은 `?` 표기. 공식 문서/코드로 재확인 권장.

---

## 핵심 비교

| 항목 | OpenVLA | SmolVLA-base | Octo-base | π0 | RDT-1B |
|---|---|---|---|---|---|
| 출처 | Stanford / UC Berkeley | HuggingFace | UC Berkeley | Physical Intelligence | Tsinghua |
| 파라미터 | 7B | ~450M | ~93M | ~3B? | 1B |
| 라이선스 | Apache 2.0 | Apache 2.0 | Apache 2.0 | **비공개** | Apache 2.0 |
| HuggingFace | `openvla/openvla-7b` | `lerobot/smolvla-base` | `rail-berkeley/octo-base` | API만 | `robotics-diffusion-transformer/rdt-1b` |

---

## 입력

| 항목 | OpenVLA | SmolVLA-base | Octo-base | π0 | RDT-1B |
|---|---|---|---|---|---|
| 카메라 수 | 1대 | 1~3대 | 1~2대 (primary+wrist) | 다수 | 1~3대 |
| 언어 지시문 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 로봇 state 입력 | **✗** | **✓** | **✓** | **✓** | **✓** |

---

## 아키텍처

| 항목 | OpenVLA | SmolVLA-base | Octo-base | π0 | RDT-1B |
|---|---|---|---|---|---|
| 백본 | LLaMA-2 7B | SmolLM2 | Transformer | PaliGemma | DiT (Diffusion) |
| Vision Encoder | SigLIP + DINOv2 (융합) | SigLIP | ViT계열 (frozen, ?) | SigLIP | SigLIP |
| Text Encoder | LLaMA-2 tokenizer | SmolLM2 tokenizer | T5계열 (?) | PaliGemma tokenizer | T5 |
| Action 생성 방식 | 토큰화 (256bin 이산화) | Continuous chunk | Diffusion / chunk | Flow Matching | Diffusion |

---

## 출력 (Action Space)

| 항목 | OpenVLA | SmolVLA-base | Octo-base | π0 | RDT-1B |
|---|---|---|---|---|---|
| Action 유형 | EEF delta | **데이터셋 정의** | EEF delta (기본) | 관절각도 | **데이터셋 정의** |
| Action 차원 | 7 (Δx,Δy,Δz,Δrx,Δry,Δrz,grip) | 설정 가능 | 7? (?) | 7+ | 설정 가능 |
| 그리퍼 포함 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Action Chunk | ✗ (1스텝) | ✓ (50스텝) | ✓ | ✓ | ✓ |

---

## 학습 데이터 / 태스크 친숙도

| 항목 | OpenVLA | SmolVLA-base | Octo-base | π0 | RDT-1B |
|---|---|---|---|---|---|
| 학습 데이터 | Open X-Embodiment | LeRobot 공개 데이터셋 | Open X-Embodiment (800K+) | PI 독자 데이터 | OXE + 다수 |
| 테이블 위 집기 | ✓ 익숙 | △ 데이터 의존 | ✓ 익숙 | ✓ 익숙 | ✓ 익숙 |
| 수직/벽면 조작 | ✗ 취약 | ✗ 취약 | ✗ 취약 | △ | ✗ 취약 |
| 관절각도 직접 출력 | ✗ | ✓ (파인튜닝 시) | △ (재정의 필요) | ✓ | ✓ (파인튜닝 시) |

---

## 우리 환경 적합성 (Doosan e0509 + joint-space 제어)

| 항목 | OpenVLA | SmolVLA-base | Octo-base | π0 | RDT-1B |
|---|---|---|---|---|---|
| state 입력 가능 | **✗** | ✓ | ✓ | ✓ | ✓ |
| joint angle 출력 | ✗ (EEF) | ✓ | △ (재정의) | ✓ | ✓ |
| 파인튜닝 용이성 | △ (7B, 무거움) | ✓ (가벼움) | ✓ | ✗ (비공개) | △ (1B) |
| 현재 사용 중 | ✗ | **✓ (현재 사용)** | ✗ | ✗ | ✗ |
| 추천도 | ✗ | ✓✓ | ✓ | - | ✓ |

---

## 요약

- **현재 파이프라인 유지**: SmolVLA-base 파인튜닝 → 가장 현실적
- **대안 고려 시**: Octo-base (state 지원, 가볍고 다양한 사전학습)
- **고성능 필요 시**: RDT-1B (1B, 확장성 좋음)
- **OpenVLA**: state 입력 불가 + EEF delta 출력 → 우리 환경에 **비적합**
- **π0**: 성능 최고지만 weights 비공개 → 사용 불가

---

## 참고 링크

- OpenVLA: https://github.com/openvla/openvla
- SmolVLA: https://github.com/huggingface/lerobot
- Octo: https://github.com/octo-models/octo
- RDT-1B: https://github.com/thu-ml/RoboticsDiffusionTransformer

