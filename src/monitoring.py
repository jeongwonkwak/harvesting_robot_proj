#!/usr/bin/env python3
"""
🤖 통합 모니터링 런처
- harvest_dashboard.py (포트 8765) - 로봇 제어
- bag_monitor.py (포트 8501, Streamlit) - 센서 모니터링
- integrated_dashboard.py (포트 8080) - 통합 대시보드

이 3개를 하나의 명령어로 시작

실행:
  python3 src/monitoring.py

또는:
  python3 monitoring.py
"""

import subprocess
import time
import sys
import os
import signal
from pathlib import Path

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent

SERVICES = [
    {
        'name': '🎮 Harvest Dashboard',
        'cmd': ['python3', 'src/dashboard/harvest_dashboard.py'],
        'port': 8765,
        'startup_time': 3,
    },
    {
        'name': '📊 Bag Monitor',
        'cmd': ['streamlit', 'run', 'src/bag_monitor.py', '--logger.level=error', '--client.showErrorDetails=false'],
        'port': 8501,
        'startup_time': 4,
    },
    {
        'name': '📈 Integrated Dashboard',
        'cmd': ['python3', 'src/integrated_dashboard.py'],
        'port': 8080,
        'startup_time': 1,
    },
]

processes = []


def print_header():
    """시작 메시지 출력"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           🤖 통합 로봇 대시보드 (올인원)                  ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║                                                            ║")
    print("║  ✅ 다음 3개 서비스를 자동으로 시작합니다:              ║")
    print("║                                                            ║")
    print("║  1️⃣  🎮 Harvest Dashboard (포트 8765)                  ║")
    print("║     → 로봇 제어, 데이터 수집                           ║")
    print("║                                                            ║")
    print("║  2️⃣  📊 Bag Monitor (포트 8501)                        ║")
    print("║     → 센서 모니터링, 실시간 그래프                    ║")
    print("║                                                            ║")
    print("║  3️⃣  📈 Integrated Dashboard (포트 8080)               ║")
    print("║     → 3개 뷰 통합 (제어 / 모니터링 / 듀얼)            ║")
    print("║                                                            ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print("║  🌐 접속 주소:                                           ║")
    print("║                                                            ║")
    print("║     http://localhost:8080                                 ║")
    print("║                                                            ║")
    print("║  📌 3가지 뷰 사용 가능:                                  ║")
    print("║     • 🎮 로봇 제어                                      ║")
    print("║     • 📊 센서 모니터링                                  ║")
    print("║     • 📈 듀얼 뷰 (좌우 분할)                            ║")
    print("║                                                            ║")
    print("║  ⏱️  서비스 시작 중... (약 10초 소요)                   ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()


def start_services():
    """모든 서비스 시작"""
    os.chdir(PROJECT_ROOT)

    for service in SERVICES:
        print(f"⏳ {service['name']} 시작 중...", end=" ", flush=True)

        try:
            # Streamlit은 특별 처리
            if "streamlit" in service['cmd']:
                # Streamlit 출력 억제
                process = subprocess.Popen(
                    service['cmd'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
            else:
                process = subprocess.Popen(
                    service['cmd'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                )

            processes.append({
                'name': service['name'],
                'process': process,
                'port': service['port'],
            })

            time.sleep(service['startup_time'])
            print(f"✅ (포트 {service['port']})")

        except Exception as e:
            print(f"❌ 오류: {e}")
            stop_all_services()
            sys.exit(1)

    # 모든 서비스가 시작됨
    print("\n" + "=" * 60)
    print("✨ 모든 서비스가 정상 실행 중입니다!")
    print("=" * 60)
    print("\n🌐 브라우저에서 열기:")
    print("   http://localhost:8080\n")
    print("📝 상태:")
    for p in processes:
        status = "🟢 실행 중" if p['process'].poll() is None else "🔴 중지됨"
        print(f"   {p['name']:<30} {status}")
    print("\n⌨️  Ctrl+C를 눌러서 모든 서비스 종료\n")


def monitor_services():
    """서비스 모니터링"""
    try:
        while True:
            # 프로세스 상태 확인
            for p in processes:
                if p['process'].poll() is not None:
                    print(f"\n⚠️  {p['name']}이(가) 종료되었습니다!")
                    print("❌ 모든 서비스를 종료합니다...")
                    stop_all_services()
                    sys.exit(1)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n🛑 Ctrl+C 감지됨. 모든 서비스를 종료 중...\n")
        stop_all_services()
        sys.exit(0)


def stop_all_services():
    """모든 서비스 종료"""
    print("⏹️  서비스 종료 중...")

    for p in processes:
        try:
            p['process'].terminate()
            p['process'].wait(timeout=3)
            print(f"   ✅ {p['name']} 종료됨")
        except subprocess.TimeoutExpired:
            p['process'].kill()
            print(f"   ⚠️  {p['name']} 강제 종료됨")
        except Exception as e:
            print(f"   ❌ {p['name']} 종료 오류: {e}")

    print("\n✨ 모든 서비스가 종료되었습니다.")


def signal_handler(sig, frame):
    """신호 처리"""
    stop_all_services()
    sys.exit(0)


if __name__ == '__main__':
    # 신호 처리
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        print_header()
        start_services()
        monitor_services()

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        stop_all_services()
        sys.exit(1)
