#!/usr/bin/env python3
"""
통합 대시보드
- harvest_dashboard.py (포트 8765) + bag_monitor.py (포트 8501)를 iframe으로 통합
- 하나의 페이지에서 모든 것을 볼 수 있음

실행:
  python3 integrated_dashboard.py

그러면 http://localhost:8080 에서 접속 가능
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode())
        else:
            super().do_GET()

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 통합 로봇 대시보드</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 2px solid #3b82f6;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .title {
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .nav-tabs {
            display: flex;
            gap: 10px;
            margin-left: 30px;
            flex: 1;
        }

        .tab-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            background: #334155;
            color: #cbd5e1;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.3s;
        }

        .tab-btn:hover {
            background: #475569;
            color: #f1f5f9;
        }

        .tab-btn.active {
            background: #3b82f6;
            color: white;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }

        .status {
            display: flex;
            gap: 8px;
            align-items: center;
            font-size: 12px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .content {
            flex: 1;
            overflow: hidden;
            display: flex;
        }

        .tab-pane {
            display: none;
            width: 100%;
            height: 100%;
        }

        .tab-pane.active {
            display: flex;
        }

        .dual-view {
            display: grid;
            grid-template-rows: 1fr 1fr;
            gap: 2px;
            width: 100%;
            height: 100%;
            background: #000;
        }

        .full-view {
            width: 100%;
            height: 100%;
        }

        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }

        .info-box {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 15px;
            margin: 10px;
            text-align: center;
        }

        .info-box h3 {
            color: #60a5fa;
            margin-bottom: 8px;
        }

        .footer {
            background: #0f172a;
            border-top: 1px solid #334155;
            padding: 10px 20px;
            font-size: 12px;
            color: #64748b;
            text-align: right;
        }
    </style>
</head>
<body>
    <!-- 헤더 -->
    <div class="header">
        <div class="title">
            🤖 딸기 수확 로봇 | 통합 대시보드
        </div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('control')">
                🎮 로봇 제어
            </button>
            <button class="tab-btn" onclick="switchTab('monitor')">
                📊 센서 모니터링
            </button>
            <button class="tab-btn" onclick="switchTab('dual')">
                📺 상하 분할 (추천)
            </button>
        </div>
        <div class="status">
            <div class="status-dot"></div>
            <span>대시보드 활성</span>
        </div>
    </div>

    <!-- 콘텐츠 -->
    <div class="content">
        <!-- 탭 1: 로봇 제어 (harvest_dashboard) -->
        <div id="control" class="tab-pane active full-view">
            <iframe src="http://localhost:8765"></iframe>
        </div>

        <!-- 탭 2: 센서 모니터링 (bag_monitor) -->
        <div id="monitor" class="tab-pane full-view">
            <iframe src="http://localhost:8501"></iframe>
        </div>

        <!-- 탭 3: 듀얼 뷰 (상하 분할) -->
        <div id="dual" class="tab-pane dual-view">
            <iframe src="http://localhost:8765" style="border-bottom: 2px solid #000;"></iframe>
            <iframe src="http://localhost:8501"></iframe>
        </div>
    </div>

    <!-- 푸터 -->
    <div class="footer">
        💡 Tip: 상하 분할 뷰에서 녹화 시작 시 하단 그래프가 실시간 업데이트됩니다 | 포트: 8765(제어) / 8501(모니터) / 8080(통합)
    </div>

    <script>
        function switchTab(tabName) {
            // 모든 탭 숨기기
            document.querySelectorAll('.tab-pane').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });

            // 선택한 탭 표시
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║         🤖 통합 로봇 대시보드 시작                       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  필수: 다음 3개 서비스가 실행 중이어야 합니다             ║
║                                                            ║
║  1️⃣  포트 8765: Harvest Dashboard                        ║
║     $ python3 src/dashboard/harvest_dashboard.py          ║
║                                                            ║
║  2️⃣  포트 8501: Bag Monitor (Streamlit)                 ║
║     $ streamlit run src/bag_monitor.py                    ║
║                                                            ║
║  3️⃣  포트 8080: 통합 대시보드 (이 프로그램)             ║
║     현재 실행 중...                                      ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║  🌐 접속: http://localhost:8080                          ║
║                                                            ║
║  📌 3개 뷰:                                               ║
║     • 🎮 로봇 제어: harvest_dashboard 전체               ║
║     • 📊 센서 모니터링: bag_monitor 전체                 ║
║     • 📈 듀얼 뷰: 좌우 분할 (제어 + 모니터링)            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)

    server = HTTPServer(('localhost', 8080), DashboardHandler)
    print("✅ 통합 대시보드 실행 중: http://localhost:8080")
    print("📌 Ctrl+C로 종료\n")
    server.serve_forever()
