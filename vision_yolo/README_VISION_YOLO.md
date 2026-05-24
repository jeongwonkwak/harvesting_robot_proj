# vision_yolo — 수확 로봇 모노레포 내 비전 패키지

`harvesting_robot_miniproj/vision_yolo` 는 독립 개발 저장소  
[`yolo_strawberry`](https://github.com/yanggangyiplus/yolo26m_strawberry) 와 동기화된 **딸기 YOLO 검출 + 줄기 그립** 모듈입니다.

---

## 역할

| 기능 | 스크립트 | 가중치 (로컬) |
|---|---|---|
| ripe/unripe 검출 | `realsense_live.py` | `runs/detect/.../yolo26m_unified_832b8/weights/best.pt` |
| **딸기 + 줄기 그립 (권장)** | `realsense_stem_pipeline.py` | detect `best.pt` + stem `yolo26m_stem_roi_128b16/.../best.pt` |
| 팀 배포 zip | `share/strawberry_yolo26m_unified/` | `weights/best.pt`, `weights/stem_best.pt` |

통합 파이프라인은 **한 스크립트**에서 detect → ROI → stem seg → 그립점까지 처리합니다.  
줄기·그립은 기본 **`ripe_strawberry` 만** (`--stem-unripe` 로 unripe 포함 가능).

---

## 빠른 실행 (RealSense)

```bash
cd harvesting_robot_miniproj/vision_yolo
pip install -r requirements.txt

python scripts/realsense_stem_pipeline.py \
  --weights-det runs/detect/runs/strawberry/yolo26m_unified_832b8/weights/best.pt \
  --weights-stem runs/segment/runs/strawberry/yolo26m_stem_roi_128b16/weights/best.pt \
  --imgsz-det 832 --imgsz-stem 128
```

학습·데이터·상세 옵션: [README.md](README.md)

---

## yolo_strawberry 와 동기화

개발은 `~/yolo_strawberry` 에서 하고, 모노레포에 반영할 때:

```bash
cd ~/yolo_strawberry
bash scripts/sync_to_vision_yolo.sh
```

동기화 대상: `scripts/`, `configs/`, `share/strawberry_yolo26m_unified/`, 줄기·seg **라벨** (`datasets/*/labels/all/`), `README.md`, `.gitignore`, `requirements.txt`

이미지·`runs/` 가중치는 복사하지 않습니다. clone 후 `split_dataset.py`·학습 또는 share `weights/` 를 준비하세요.

---

## 폴더 요약

```
vision_yolo/
├── scripts/realsense_stem_pipeline.py   # ★ 통합 실시간
├── configs/strawberry_*.yaml
├── datasets/yolo_unified/               # detect 라벨 (git)
├── datasets/yolo_stem_roi/              # 줄기 ROI 라벨 (git)
├── share/strawberry_yolo26m_unified/    # 배포·메트릭·share 스크립트
└── runs/                                # 학습·추론 (gitignore)
```

---

## 상위 프로젝트

`harvesting_robot_miniproj` 루트 README에서 로봇·제어와의 연동을 확인하세요.
