# PI05 Upstream Scaling Bug — 이미지 임베딩 스케일 제거로 인한 서빙 파괴

## 증상

- v0.5.2 모델 ablation ratio: **0.05** (이미지 무시, shortcut learning 지속)
- v0.5.3 모델 (로컬 포크로 서빙 교체 후) ablation ratio: **9.57** (이미지 정상 사용)

## 원인

upstream lerobot 커밋 `01dcb4c2` (`fix(pi05): update pi05 with transformers v5.4.0 interface`, **2026-05-15**)이 `modeling_pi05.py`에서 이미지/언어 임베딩 스케일링 코드를 제거함.

### 제거된 코드 1: Image feature scaling

```python
# 제거 전 (로컬 포크 / 학습 시 코드):
features = image_outputs.pooler_output * self.paligemma.config.text_config.hidden_size**0.5
# sqrt(2048) ≈ 45.25 배 증폭

# 제거 후 (upstream pip):
features = image_outputs.pooler_output
```

### 제거된 코드 2: Language embedding scaling

```python
# 제거 전 (로컬 포크 / 학습 시 코드):
lang_emb = self.paligemma_with_expert.embed_language_tokens(tokens)
lang_emb_dim = lang_emb.shape[-1]
return lang_emb * math.sqrt(lang_emb_dim)  # sqrt(2048) ≈ 45.25 배 증폭

# 제거 후 (upstream pip):
lang_emb = self.paligemma_with_expert.embed_language_tokens(tokens)
return lang_emb
```

## 왜 문제가 되는가

PI05는 멀티모달 모델로, attention 내부에서 이미지/언어/액션 임베딩이 경쟁합니다.

- SigLIP `pooler_output`은 정규화된 작은 값
- Gemma 언어/액션 임베딩은 상대적으로 큰 값
- `* sqrt(hidden_size)` 스케일링이 이미지+언어 피처를 모델 내부 스케일에 맞게 정규화

스케일링이 제거되면 이미지+언어 임베딩이 액션/state 임베딩 대비 **45배 약해짐** → attention에서 이미지 신호 무시 → shortcut learning 지속.

```
이미지 처리 파이프라인:
  원본 이미지
      ↓
  리사이즈 (letterbox, 224x224)
      ↓
  SigLIP encoder
      ↓
  pooler_output (작은 정규화 값)
      ↓
  * sqrt(2048)  ← 이 스케일링이 제거되면 이미지가 attention에서 묻힘
      ↓
  모델 내부 attention
```

## 타임라인

| 날짜 | 이벤트 |
|------|--------|
| 2026-05-12 | 로컬 포크 생성 (upstream 분기) — 스케일링 코드 존재 |
| 2026-05-15 | upstream `01dcb4c2` 커밋 — **스케일링 코드 제거** |
| 2026-06-12 | Docker v0.5.2 빌드 시 `pip install upstream` → 스케일링 없는 버전 설치 → ablation 0.05 |
| 2026-06-13 | Dockerfile 변경: upstream pip → 로컬 포크 editable install |
| 2026-06-13 | v0.5.3 서빙 → ablation 9.57 (정상) |

## 결론

fine-tuned 모델들은 스케일링 있는 코드로 학습됐기 때문에 inference도 동일한 스케일링이 있어야 합니다. upstream이 transformers v5.4.0 인터페이스 대응 명목으로 제거했지만, 기존 학습된 모델에는 맞지 않습니다.

**로컬 포크를 유지하거나, upstream 코드를 쓰려면 동일한 스케일링으로 재학습이 필요합니다.**
