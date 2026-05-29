# 데이터셋 포맷 오류 및 수정 내역

학습 실행 중 발견된 문제들과 각 원인, 수정 방법을 정리합니다.

---

## 문제 1: `meta/episodes/` 디렉토리 누락

### 증상

```
FileNotFoundError: Provided directory does not contain any parquet file:
  /data/vla/fin/smolvla_dataset_v1.1.0/meta/episodes
```

### 원인

LeRobot v3.0 포맷에서 `meta/episodes/chunk-000/file-000.parquet`는 **필수 파일**이다.
데이터셋 생성 스크립트가 이 파일을 생성하지 않아서 발생.

### 필요한 파일 구조

```
meta/
├── info.json          ✓ 있었음
├── tasks.parquet      ✓ 있었음
├── stats.json         ✓ 있었음
└── episodes/
    └── chunk-000/
        └── file-000.parquet   ✗ 누락 → 생성 필요
```

### episodes parquet 필수 컬럼

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `episode_index` | int | 에피소드 번호 (0-based) |
| `tasks` | list[str] | 해당 에피소드의 task 지시문 목록 |
| `length` | int | 에피소드 프레임 수 |
| `dataset_from_index` | int | 전체 데이터셋에서 첫 프레임의 절대 index |
| `dataset_to_index` | int | 전체 데이터셋에서 마지막 프레임의 절대 index + 1 |
| `data/chunk_index` | int | 데이터 parquet 파일의 chunk 번호 |
| `data/file_index` | int | 데이터 parquet 파일의 file 번호 |
| `videos/{cam_key}/chunk_index` | int | 해당 카메라 영상 파일의 chunk 번호 |
| `videos/{cam_key}/file_index` | int | 해당 카메라 영상 파일의 file 번호 |
| `videos/{cam_key}/from_timestamp` | float | 영상 파일 내 이 에피소드의 시작 시각 (초) |
| `videos/{cam_key}/to_timestamp` | float | 영상 파일 내 이 에피소드의 종료 시각 (초) |
| `meta/episodes/chunk_index` | int | episodes parquet 자체의 chunk 번호 |
| `meta/episodes/file_index` | int | episodes parquet 자체의 file 번호 |

> 카메라가 여러 개라면 각 카메라 key마다 `videos/{cam_key}/...` 컬럼 세트가 추가된다.

### 수정 방법 (기존 데이터에서 복원)

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

dataset_root = Path("/data/vla/fin/smolvla_dataset_v1.1.0")
fps = 10
vid_key = "observation.images.camera1"

frames = pq.read_table(dataset_root / "data/chunk-000/file-000.parquet").to_pandas()
tasks_df = pq.read_table(dataset_root / "meta/tasks.parquet").to_pandas().reset_index()
task_map = dict(zip(tasks_df["task_index"], tasks_df["task"]))

rows = []
for ep_idx, grp in frames.groupby("episode_index"):
    task_idx = int(grp["task_index"].iloc[0])
    length = len(grp)
    rows.append({
        "episode_index": int(ep_idx),
        "tasks": [task_map[task_idx]],
        "length": length,
        "dataset_from_index": int(grp["index"].min()),
        "dataset_to_index": int(grp["index"].max()) + 1,
        "data/chunk_index": 0,
        "data/file_index": 0,
        f"videos/{vid_key}/chunk_index": 0,
        f"videos/{vid_key}/file_index": int(ep_idx),
        f"videos/{vid_key}/from_timestamp": 0.0,
        f"videos/{vid_key}/to_timestamp": length / fps,
        "meta/episodes/chunk_index": 0,
        "meta/episodes/file_index": 0,
    })

out_path = dataset_root / "meta/episodes/chunk-000/file-000.parquet"
out_path.parent.mkdir(parents=True, exist_ok=True)
pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), out_path, compression="snappy")
```

---

## 문제 2: `videos/{cam_key}/from_timestamp` 컬럼 누락

### 증상

```
KeyError: 'videos/observation.images.camera1/from_timestamp'
```

문제 1에서 episodes parquet를 생성할 때 비디오 타임스탬프 컬럼을 빠뜨려서 발생.

### 원인

`from_timestamp` / `to_timestamp`는 **영상 파일 내에서 이 에피소드가 차지하는 시간 구간**이다.

LeRobot은 여러 에피소드를 하나의 mp4 파일에 이어붙일 수 있다:

```
file-000.mp4 = [에피소드 0 (0.0 ~ 15.5s)] + [에피소드 1 (15.5 ~ 95.5s)] + ...
```

에피소드마다 별도 mp4 파일을 쓰는 경우 (이 데이터셋의 경우):
- `from_timestamp = 0.0`
- `to_timestamp = length / fps`

### 데이터셋 생성 스크립트에서 반드시 채워야 할 값

```python
f"videos/{vid_key}/from_timestamp": 0.0,           # 별도 파일이면 항상 0
f"videos/{vid_key}/to_timestamp":   length / fps,   # 에피소드 전체 길이 (초)
```

---

## 문제 3: LeRobot 코드 버그 (HFValidationError 오해 유발)

### 증상

로컬 경로로 데이터셋을 지정했을 때 `meta/episodes/` 로딩이 실패하면, LeRobot이 그 경로를 HuggingFace Hub repo ID로 오해하고 Hub API를 호출해 아래 오류를 낸다:

```
HFValidationError: Repo id must be in the form 'repo_name' or 'namespace/repo_name':
  '/data/vla/fin/smolvla_dataset_v1.1.0'
```

실제 원인(episodes 파일 누락)이 가려져서 디버깅이 어렵다.

### 수정 위치

`lerobot/src/lerobot/datasets/dataset_metadata.py`, `__init__` 내 except 블록:

```python
# 수정 전
except (FileNotFoundError, NotADirectoryError):
    if is_valid_version(self.revision):
        self.revision = get_safe_version(self.repo_id, self.revision)
    self._pull_from_repo(allow_patterns="meta/")
    self._load_metadata()

# 수정 후
except (FileNotFoundError, NotADirectoryError):
    if Path(self.repo_id).is_absolute():
        raise  # 로컬 절대경로는 Hub 조회 없이 즉시 원래 오류를 전파
    if is_valid_version(self.revision):
        self.revision = get_safe_version(self.repo_id, self.revision)
    self._pull_from_repo(allow_patterns="meta/")
    self._load_metadata()
```

---

## 데이터셋 생성 스크립트 체크리스트

커스텀 데이터셋 생성 스크립트에서 아래 항목이 모두 생성되는지 확인한다.

| 파일 | 필수 여부 | 비고 |
|---|---|---|
| `meta/info.json` | 필수 | `codebase_version`, `fps`, `total_episodes`, `total_frames`, `features` 포함 |
| `meta/tasks.parquet` | 필수 | `task_index` 컬럼, 인덱스는 task 문자열 |
| `meta/stats.json` | 필수 | state/action 정규화에 사용 |
| `meta/episodes/chunk-000/file-000.parquet` | **필수** | 위 표의 컬럼 전부 포함 (이번에 누락됨) |
| `data/chunk-000/file-000.parquet` | 필수 | 프레임별 state/action/timestamp |
| `videos/{cam_key}/chunk-000/file-NNN.mp4` | 필수 | 에피소드별 영상 |

