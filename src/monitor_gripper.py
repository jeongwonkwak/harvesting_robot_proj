#!/usr/bin/env python3
"""
실시간 Gripper 값 모니터링 도구
- 수집 중인 최신 bag 파일의 /gripper/position 토픽 모니터링
- 프레임마다 gripper 값이 올바르게 기록되는지 확인

실행:
  python3 monitor_gripper.py
  python3 monitor_gripper.py --episode-dir /path/to/episode_dir
"""

import argparse
import sqlite3
import struct
import time
from pathlib import Path
from datetime import datetime

def parse_float32_msg(raw: bytes) -> float:
    """CDR format float32 파싱"""
    buf = raw[4:]  # 첫 4바이트 헤더 스킵
    return struct.unpack('<f', buf[:4])[0] if len(buf) >= 4 else 0.0

def monitor_gripper(db_path: Path, update_interval: float = 0.5):
    """
    Bag 파일의 gripper 값을 실시간으로 모니터링

    Args:
        db_path: ROS 2 bag 파일 (.db3)
        update_interval: 업데이트 간격 (초)
    """

    if not db_path.exists():
        print(f"❌ 파일을 찾을 수 없음: {db_path}")
        return

    print(f"📊 Gripper 모니터링 시작: {db_path.name}")
    print(f"{'='*70}")
    print(f"{'Frame':<6} {'Gripper':<12} {'Status':<15} {'Timestamp':<20}")
    print(f"{'-'*70}")

    last_count = 0
    gripper_values = []

    try:
        while True:
            try:
                conn = sqlite3.connect(str(db_path))
                cur = conn.cursor()

                # /gripper/position 토픽 찾기
                cur.execute("SELECT id FROM topics WHERE name = '/gripper/position'")
                result = cur.fetchone()

                if not result:
                    print("❌ /gripper/position 토픽을 찾을 수 없음")
                    conn.close()
                    break

                topic_id = result[0]

                # 모든 메시지 가져오기
                cur.execute(
                    'SELECT timestamp, data FROM messages WHERE topic_id = ? ORDER BY timestamp',
                    (topic_id,)
                )
                messages = cur.fetchall()
                conn.close()

                # 새로운 메시지만 처리
                if len(messages) > last_count:
                    new_messages = messages[last_count:]

                    for frame_idx, (ts, raw) in enumerate(new_messages, start=last_count):
                        try:
                            gripper_val = parse_float32_msg(bytes(raw))
                            gripper_values.append(gripper_val)

                            # 상태 판단
                            if gripper_val < 0.1:
                                status = "🔓 열림"
                                color = "✅"
                            elif gripper_val > 0.9:
                                status = "🔒 닫힘"
                                color = "✅"
                            else:
                                status = "⚠️  중간값"
                                color = "⚠️ "

                            # 타임스탐프 변환
                            ts_sec = ts / 1e9
                            ts_str = datetime.fromtimestamp(ts_sec).strftime("%H:%M:%S.%f")[:-3]

                            print(f"{frame_idx:<6} {gripper_val:<12.6f} {status:<15} {ts_str:<20}")

                        except Exception as e:
                            print(f"{frame_idx:<6} {'[Error]':<12} {str(e):<15}")

                    last_count = len(messages)

                    # 통계
                    print(f"\n📈 통계 (총 {len(gripper_values)}개 프레임):")
                    print(f"  Min: {min(gripper_values):.6f}")
                    print(f"  Max: {max(gripper_values):.6f}")
                    print(f"  Mean: {sum(gripper_values)/len(gripper_values):.6f}")

                    # 문제 감지
                    unique_vals = set(f"{v:.6f}" for v in gripper_values)
                    if len(unique_vals) == 1:
                        print(f"  ⚠️ 경고: 모든 값이 동일함 (센서 오류?)")
                    print(f"{'-'*70}\n")

                time.sleep(update_interval)

            except sqlite3.DatabaseError:
                # DB가 잠긴 경우 재시도
                time.sleep(update_interval)
                continue
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 오류: {e}")
                time.sleep(update_interval)

    except KeyboardInterrupt:
        print("\n\n📊 모니터링 종료")
        if gripper_values:
            print(f"\n최종 통계:")
            print(f"  총 프레임: {len(gripper_values)}")
            print(f"  범위: {min(gripper_values):.6f} ~ {max(gripper_values):.6f}")
            print(f"  평균: {sum(gripper_values)/len(gripper_values):.6f}")


def main():
    parser = argparse.ArgumentParser(
        description="수집 중인 bag 파일의 gripper 값 실시간 모니터링"
    )
    parser.add_argument(
        '--episode-dir',
        type=Path,
        help='Episode 디렉토리 (자동으로 최신 bag 파일 찾음)'
    )
    parser.add_argument(
        '--db',
        type=Path,
        help='Bag 파일 경로 (.db3)'
    )
    parser.add_argument(
        '--interval',
        type=float,
        default=0.5,
        help='업데이트 간격 (초, 기본값: 0.5)'
    )

    args = parser.parse_args()

    # 경로 결정
    db_path = None

    if args.db:
        db_path = args.db
    elif args.episode_dir:
        db_files = list(args.episode_dir.glob("*.db3"))
        if db_files:
            db_path = db_files[0]
    else:
        # 최신 episode 자동 감지
        raw_dir = Path("/home/user/robot_workspace/vla_ws/data/raw/final_project/vla_dataset_v0.4.0")
        episode_dirs = sorted(raw_dir.glob("episode_*_eef"), reverse=True)
        if episode_dirs:
            db_files = list(episode_dirs[0].glob("*.db3"))
            if db_files:
                db_path = db_files[0]

    if not db_path:
        print("❌ Bag 파일을 찾을 수 없음")
        parser.print_help()
        return

    monitor_gripper(db_path, args.interval)


if __name__ == "__main__":
    main()
