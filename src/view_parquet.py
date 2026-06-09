#!/usr/bin/env python3
"""
Parquet 파일 뷰어
사용법: python3 src/view_parquet.py [파일 경로] [행 수]
예시: python3 src/view_parquet.py data/mid/vla_dataset_v0.4.0/data/chunk-000/file-000.parquet 5
"""

import pandas as pd
import sys
from pathlib import Path

def view_parquet(file_path, num_rows=5):
    """Parquet 파일 보기"""

    path = Path(file_path)
    if not path.exists():
        print(f"❌ 파일 없음: {file_path}")
        return

    df = pd.read_parquet(file_path)

    print("\n" + "=" * 80)
    print(f"📊 파일: {path.name}")
    print("=" * 80)

    # 기본 정보
    print(f"\n크기: {df.shape[0]:,}개 행 × {df.shape[1]:,}개 칼럼")
    print(f"\n칼럼 목록:")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        print(f"  {i}. {col} ({dtype})")

    # 샘플 데이터
    print(f"\n처음 {num_rows}개 행:")
    print(df.head(num_rows).to_string())

    # 첫 번째 행 자세히
    print(f"\n첫 번째 행 자세히:")
    row = df.iloc[0]
    for col, val in row.items():
        print(f"  {col}: {val}")

    # 에피소드별 통계
    if 'episode_index' in df.columns:
        print(f"\n에피소드별 프레임 수:")
        ep_counts = df.groupby('episode_index').size()
        for ep, count in ep_counts.items():
            print(f"  에피소드 {ep}: {count}개 프레임")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # 기본 경로
        default_path = '/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.0/data/chunk-000/file-000.parquet'
        num_rows = 5
        save_output = True
    else:
        default_path = sys.argv[1]
        num_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        save_output = '--save' in sys.argv or '-s' in sys.argv

    # 출력을 파일에 저장
    if save_output:
        dataset_dir = Path('/home/user/robot_workspace/vla_ws/data/mid/vla_dataset_v0.4.0')
        output_file = dataset_dir / 'PARQUET_INFO.txt'

        # 출력을 문자열로 캡처
        from io import StringIO
        import contextlib

        output = StringIO()
        with contextlib.redirect_stdout(output):
            view_parquet(default_path, num_rows)

        content = output.getvalue()
        output_file.write_text(content, encoding='utf-8')
        print(f"✅ 저장됨: {output_file}")
        print(content)
    else:
        view_parquet(default_path, num_rows)
