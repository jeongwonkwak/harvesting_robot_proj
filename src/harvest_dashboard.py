#!/usr/bin/env python3
"""
harvest_dashboard.py — 딸기 수확 로봇 웹 대시보드

실행:
  python3 src/harvest_dashboard.py            # http://localhost:8765
  python3 src/harvest_dashboard.py --demo     # 데모 모드 (시뮬레이션 자동 진행)
  python3 src/harvest_dashboard.py --port 9000

상태 업데이트 (별도 터미널 / 로봇 스크립트에서):
  python3 src/harvest_dashboard.py --update start_harvest
  python3 src/harvest_dashboard.py --update harvest_success
  python3 src/harvest_dashboard.py --update harvest_fail
  python3 src/harvest_dashboard.py --update damage
  python3 src/harvest_dashboard.py --update reset
  python3 src/harvest_dashboard.py --msg "꼭지 가림 — 방향 변경" --level warning
  python3 src/harvest_dashboard.py --status grasping
"""

import argparse
import asyncio
import json
import os
import random
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 상태 파일 ─────────────────────────────────────────────────────────────────
STATE_FILE   = Path(os.environ.get('HARVEST_STATE_FILE', '/tmp/harvest_state.json'))
MAX_MESSAGES = 40

DEFAULT_STATE: dict = {
    "session_start":         None,
    "total_attempts":        0,
    "success_count":         0,
    "damage_count":          0,
    "grasp_times":           [],
    "current_harvest_start": None,
    "messages":              [],
    "status":                "idle",
}

def _load() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                s = json.load(f)
            for k, v in DEFAULT_STATE.items():
                s.setdefault(k, v)
            return s
        except Exception:
            pass
    return DEFAULT_STATE.copy()

def _save(s: dict) -> None:
    tmp = STATE_FILE.with_suffix('.tmp')
    with open(tmp, 'w') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)

def _push_msg(s: dict, text: str, level: str = "info") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    s["messages"].append({"time": ts, "level": level, "text": text})
    if len(s["messages"]) > MAX_MESSAGES:
        s["messages"] = s["messages"][-MAX_MESSAGES:]

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🍓 딸기 수확 대시보드</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* ── 헤더 ── */
  .header {
    background: linear-gradient(135deg, #161b22 0%, #1c1033 100%);
    border-bottom: 1px solid #30363d;
    padding: 14px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }
  .header-title { font-size: 1.35rem; font-weight: 700; letter-spacing: .5px; }
  .header-title span { color: #ff6b6b; }
  .header-meta { font-size: .8rem; color: #8b949e; text-align: right; line-height: 1.6; }
  .header-time { font-size: .9rem; color: #58a6ff; font-weight: 600; }

  /* ── 메인 ── */
  .main {
    flex: 1;
    display: grid;
    grid-template-rows: auto 1fr;
    gap: 0;
    padding: 20px 24px;
    gap: 20px;
    overflow: hidden;
  }

  /* ── 통계 카드 행 ── */
  .stats-row {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 14px;
  }

  .card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
    transition: border-color .3s, box-shadow .3s;
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
  }
  .card.green::before  { background: linear-gradient(90deg, #238636, #2ea043); }
  .card.blue::before   { background: linear-gradient(90deg, #1f6feb, #388bfd); }
  .card.yellow::before { background: linear-gradient(90deg, #9e6a03, #d29922); }
  .card.red::before    { background: linear-gradient(90deg, #b62324, #f85149); }
  .card.cyan::before   { background: linear-gradient(90deg, #0e7490, #22d3ee); }
  .card.purple::before { background: linear-gradient(90deg, #6e40c9, #a371f7); }

  .card-label {
    font-size: .7rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-bottom: 10px;
  }
  .card-value {
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1;
    transition: color .4s;
  }
  .card-unit { font-size: .85rem; font-weight: 400; color: #8b949e; margin-left: 2px; }

  .val-green  { color: #3fb950; }
  .val-yellow { color: #d29922; }
  .val-red    { color: #f85149; }
  .val-blue   { color: #58a6ff; }
  .val-cyan   { color: #22d3ee; }
  .val-white  { color: #e6edf3; }

  /* ── 하단 행 ── */
  .bottom-row {
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 14px;
    min-height: 0;
  }

  /* ── 상태 패널 ── */
  .status-panel {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    gap: 14px;
  }
  .status-label-text {
    font-size: .7rem; color: #8b949e;
    text-transform: uppercase; letter-spacing: .8px;
  }
  .status-dot-wrap { position: relative; display: flex; align-items: center; justify-content: center; }
  .status-dot {
    width: 56px; height: 56px;
    border-radius: 50%;
    background: #21262d;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    transition: background .4s;
  }
  .pulse-ring {
    position: absolute;
    width: 56px; height: 56px;
    border-radius: 50%;
    border: 2px solid transparent;
    animation: none;
  }
  @keyframes pulse {
    0%   { transform: scale(1);   opacity: .8; }
    100% { transform: scale(1.9); opacity: 0;  }
  }
  .status-name {
    font-size: 1.05rem;
    font-weight: 700;
    transition: color .4s;
  }
  .status-timer {
    font-size: 1.5rem; font-weight: 700;
    color: #d29922; letter-spacing: 1px;
    min-height: 1.8rem;
  }

  /* ── 메시지 로그 ── */
  .msg-panel {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .msg-header {
    padding: 12px 16px;
    border-bottom: 1px solid #21262d;
    font-size: .75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .8px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }
  .msg-dot { width: 6px; height: 6px; border-radius: 50%; background: #3fb950; animation: blink 1.5s ease-in-out infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

  .msg-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
    display: flex;
    flex-direction: column-reverse;   /* 최신이 아래 */
  }
  .msg-list::-webkit-scrollbar { width: 4px; }
  .msg-list::-webkit-scrollbar-track { background: transparent; }
  .msg-list::-webkit-scrollbar-thumb { background: #30363d; border-radius: 2px; }

  .msg-item {
    display: flex;
    align-items: baseline;
    gap: 8px;
    padding: 5px 16px;
    border-bottom: 1px solid #0d1117;
    font-size: .82rem;
    animation: fadeIn .3s ease;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; } }

  .msg-time  { color: #484f58; font-size: .73rem; white-space: nowrap; flex-shrink: 0; font-family: monospace; }
  .msg-icon  { flex-shrink: 0; font-size: .8rem; }
  .msg-text  { color: #c9d1d9; flex: 1; }

  .msg-info    .msg-icon { color: #58a6ff; }
  .msg-info    .msg-text { color: #c9d1d9; }
  .msg-success .msg-icon { color: #3fb950; }
  .msg-success .msg-text { color: #56d364; }
  .msg-warning .msg-icon { color: #d29922; }
  .msg-warning .msg-text { color: #e3b341; }
  .msg-error   .msg-icon { color: #f85149; }
  .msg-error   .msg-text { color: #ff7b72; }

  /* ── 연결 상태 ── */
  .ws-badge {
    position: fixed; bottom: 14px; right: 18px;
    font-size: .7rem; padding: 4px 10px;
    border-radius: 20px; border: 1px solid #30363d;
    background: #161b22; color: #8b949e;
    display: flex; align-items: center; gap: 5px;
  }
  .ws-dot { width: 6px; height: 6px; border-radius: 50%; background: #3fb950; }
  .ws-badge.disconnected .ws-dot { background: #f85149; }
  .ws-badge.disconnected { color: #f85149; }
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="header-title"><span>🍓</span> 딸기 수확 로봇 대시보드</div>
  </div>
  <div class="header-meta">
    <div id="session-info">세션 시작 전</div>
    <div class="header-time" id="clock">—</div>
  </div>
</div>

<div class="main">
  <!-- 통계 카드 -->
  <div class="stats-row">
    <div class="card green">
      <div class="card-label">총 수확량</div>
      <div class="card-value val-green" id="v-harvest">0<span class="card-unit">개</span></div>
    </div>
    <div class="card blue">
      <div class="card-label">수확 성공률</div>
      <div class="card-value" id="v-rate">—</div>
    </div>
    <div class="card cyan">
      <div class="card-label">평균 파지 시간</div>
      <div class="card-value val-cyan" id="v-avg">—</div>
    </div>
    <div class="card yellow">
      <div class="card-label">현재 수확 시간</div>
      <div class="card-value val-yellow" id="v-cur">—</div>
    </div>
    <div class="card red">
      <div class="card-label">손상률</div>
      <div class="card-value" id="v-dmg">—</div>
    </div>
    <div class="card purple">
      <div class="card-label">총 시도 횟수</div>
      <div class="card-value val-white" id="v-attempts">0<span class="card-unit">회</span></div>
    </div>
  </div>

  <!-- 하단 -->
  <div class="bottom-row">
    <!-- 상태 -->
    <div class="status-panel">
      <div class="status-label-text">로봇 상태</div>
      <div class="status-dot-wrap">
        <div class="pulse-ring" id="pulse-ring"></div>
        <div class="status-dot" id="status-dot">🤖</div>
      </div>
      <div class="status-name" id="status-name">대기 중</div>
      <div class="status-timer" id="status-timer"></div>
    </div>

    <!-- 메시지 -->
    <div class="msg-panel">
      <div class="msg-header">
        <div class="msg-dot"></div>
        실시간 메시지
      </div>
      <div class="msg-list" id="msg-list">
        <div class="msg-item msg-info">
          <span class="msg-time">—</span>
          <span class="msg-icon">●</span>
          <span class="msg-text">대시보드 연결 대기 중...</span>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="ws-badge disconnected" id="ws-badge">
  <div class="ws-dot"></div>
  연결 중...
</div>

<script>
// ── 상수 ──
const STATUS_LABEL = {idle:'대기 중', approaching:'접근 중', grasping:'파지 중', returning:'복귀 중', error:'오류'};
const STATUS_ICON  = {idle:'🤖', approaching:'🦾', grasping:'✊', returning:'↩️', error:'⚠️'};
const STATUS_COLOR = {idle:'#8b949e', approaching:'#22d3ee', grasping:'#d29922', returning:'#3fb950', error:'#f85149'};
const LEVEL_ICON   = {info:'●', success:'✔', warning:'⚠', error:'✖'};

// ── 시계 ──
setInterval(() => {
  document.getElementById('clock').textContent =
    new Date().toLocaleString('ko-KR', {year:'numeric',month:'2-digit',day:'2-digit',
      hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});
}, 500);

// ── 현재 수확 타이머 (로컬 업데이트) ──
let harvestStart = null;
setInterval(() => {
  const el = document.getElementById('v-cur');
  const st = document.getElementById('status-timer');
  if (!harvestStart) { el.textContent = '—'; st.textContent = ''; return; }
  const sec = (Date.now() - harvestStart) / 1000;
  const s   = fmtSec(sec);
  el.textContent = s;
  st.textContent = s;
}, 200);

function fmtSec(sec) {
  const m = String(Math.floor(sec / 60)).padStart(2, '0');
  const s = String(Math.floor(sec % 60)).padStart(2, '0');
  return `${m}:${s}`;
}

// ── 렌더링 ──
let prevMsgCount = 0;

function render(s) {
  // 세션 정보
  if (s.session_start) {
    const start   = new Date(s.session_start);
    const elapsed = (Date.now() - start) / 1000;
    document.getElementById('session-info').textContent =
      `세션 시작  ${start.toLocaleTimeString('ko-KR')}  ( ${fmtSec(elapsed)} 경과 )`;
  }

  // 수확량
  document.getElementById('v-harvest').innerHTML =
    `${s.success_count}<span class="card-unit">개</span>`;
  document.getElementById('v-attempts').innerHTML =
    `${s.total_attempts}<span class="card-unit">회</span>`;

  // 성공률
  const rateEl = document.getElementById('v-rate');
  if (s.total_attempts > 0) {
    const r = (s.success_count / s.total_attempts * 100).toFixed(1);
    rateEl.textContent = r + ' %';
    rateEl.className = 'card-value ' + (r >= 80 ? 'val-green' : r >= 50 ? 'val-yellow' : 'val-red');
  } else {
    rateEl.textContent = '—'; rateEl.className = 'card-value val-white';
  }

  // 평균 파지
  const avgEl = document.getElementById('v-avg');
  if (s.grasp_times && s.grasp_times.length > 0) {
    const avg = s.grasp_times.reduce((a,b)=>a+b,0) / s.grasp_times.length;
    avgEl.innerHTML = avg.toFixed(1) + '<span class="card-unit">초</span>';
  } else {
    avgEl.textContent = '—';
  }

  // 손상률
  const dmgEl = document.getElementById('v-dmg');
  if (s.success_count > 0) {
    const d = (s.damage_count / s.success_count * 100).toFixed(1);
    dmgEl.textContent = d + ' %';
    dmgEl.className = 'card-value ' + (d <= 5 ? 'val-green' : d <= 15 ? 'val-yellow' : 'val-red');
  } else {
    dmgEl.textContent = '—'; dmgEl.className = 'card-value val-white';
  }

  // 수확 타이머 기준시각
  harvestStart = s.current_harvest_start ? new Date(s.current_harvest_start) : null;

  // 로봇 상태
  const st    = s.status || 'idle';
  const color = STATUS_COLOR[st] || '#8b949e';
  document.getElementById('status-dot').textContent = STATUS_ICON[st] || '🤖';
  document.getElementById('status-dot').style.background = color + '22';
  document.getElementById('status-name').textContent = STATUS_LABEL[st] || st;
  document.getElementById('status-name').style.color = color;
  const ring = document.getElementById('pulse-ring');
  ring.style.borderColor = color;
  ring.style.animation = (st !== 'idle' && st !== 'error')
    ? 'pulse 1.2s ease-out infinite' : 'none';

  // 메시지
  const msgs = s.messages || [];
  if (msgs.length !== prevMsgCount) {
    prevMsgCount = msgs.length;
    const list = document.getElementById('msg-list');
    list.innerHTML = [...msgs].reverse().map(m => {
      const lvl  = m.level || 'info';
      const icon = LEVEL_ICON[lvl] || '●';
      return `<div class="msg-item msg-${lvl}">
        <span class="msg-time">[${m.time}]</span>
        <span class="msg-icon">${icon}</span>
        <span class="msg-text">${m.text}</span>
      </div>`;
    }).join('');
  }
}

// ── WebSocket ──
let ws, wsRetry = 0;

function connect() {
  ws = new WebSocket(`ws://${location.host}/ws`);
  const badge = document.getElementById('ws-badge');

  ws.onopen = () => {
    wsRetry = 0;
    badge.className = 'ws-badge';
    badge.querySelector('.ws-dot').style.background = '#3fb950';
    badge.lastChild.textContent = ' 연결됨';
  };
  ws.onmessage = (e) => {
    try { render(JSON.parse(e.data)); } catch {}
  };
  ws.onclose = () => {
    badge.className = 'ws-badge disconnected';
    badge.lastChild.textContent = ' 연결 끊김';
    wsRetry++;
    setTimeout(connect, Math.min(1000 * wsRetry, 5000));
  };
  ws.onerror = () => ws.close();
}
connect();
</script>
</body>
</html>
"""

# ── FastAPI 서버 ──────────────────────────────────────────────────────────────

def make_app(demo: bool = False):
    try:
        from fastapi import FastAPI, WebSocket, WebSocketDisconnect
        from fastapi.responses import HTMLResponse
    except ImportError:
        print("fastapi/uvicorn이 필요합니다: pip install fastapi uvicorn")
        sys.exit(1)

    app = FastAPI()

    @app.get("/")
    async def index():
        return HTMLResponse(HTML)

    @app.websocket("/ws")
    async def ws_endpoint(ws: WebSocket):
        await ws.accept()
        try:
            while True:
                state = _load()
                await ws.send_json(state)
                await asyncio.sleep(0.4)
        except (WebSocketDisconnect, Exception):
            pass

    if demo:
        t = threading.Thread(target=_run_demo, daemon=True)
        t.start()

    return app


# ── 데모 시뮬레이션 ───────────────────────────────────────────────────────────
_DEMO_MSGS = [
    ("딸기 감지됨 — 파지 접근 시작",                           "info"),
    ("현재 딸기 꼭지가 가려져 있으므로 접근 방향을 변경합니다", "warning"),
    ("잎 장애물 감지 — 우회 경로 재계획 중",                   "warning"),
    ("미성숙 딸기 감지 — 건너뜀",                              "warning"),
    ("그리퍼 작동 — 줄기 파지 시도",                           "info"),
    ("그리퍼 닫힘 확인 — 줄기 파지 완료",                      "success"),
    ("클러스터 내 목표 딸기 위치 계산 중",                      "info"),
    ("홈 포즈 복귀 중",                                        "info"),
    ("폐색률 68 % — Heavy 카테고리 진입",                       "warning"),
    ("IK 재계획 — 관절 한계 회피",                             "warning"),
    ("손상 없이 수확 완료",                                     "success"),
]

def _run_demo():
    s = DEFAULT_STATE.copy()
    s["session_start"] = datetime.now().isoformat()
    _push_msg(s, "대시보드 시작 — 딸기 수확 로봇 연결됨", "info")
    _save(s)
    step = 0
    while True:
        phase = step % 28
        if phase == 0:
            s["status"] = "approaching"
            s["current_harvest_start"] = datetime.now().isoformat()
            m = random.choice(_DEMO_MSGS[:4])
            _push_msg(s, m[0], m[1])
        elif phase == 10:
            s["status"] = "grasping"
            _push_msg(s, "그리퍼 작동 — 파지 시도", "info")
        elif phase == 20:
            ok = random.random() > 0.15
            gt = round(random.uniform(2.8, 9.5), 1)
            s["total_attempts"] += 1
            if ok:
                s["success_count"] += 1
                s["grasp_times"].append(gt)
                if random.random() < 0.09:
                    s["damage_count"] += 1
                    _push_msg(s, f"수확 완료 — 손상 감지 ({gt}초)", "warning")
                else:
                    _push_msg(s, f"수확 성공  ({gt}초)", "success")
            else:
                _push_msg(s, "파지 실패 — 다음 딸기로 이동", "error")
            s["status"] = "returning"
            s["current_harvest_start"] = None
        elif phase == 24:
            s["status"] = "idle"
            if random.random() < 0.35:
                m = random.choice(_DEMO_MSGS[4:])
                _push_msg(s, m[0], m[1])
        _save(s)
        time.sleep(0.3)
        step += 1


# ── CLI 업데이트 ──────────────────────────────────────────────────────────────
def cmd_update(action: str) -> None:
    s = _load()
    if not s.get("session_start"):
        s["session_start"] = datetime.now().isoformat()

    if action == "start_harvest":
        s["current_harvest_start"] = datetime.now().isoformat()
        s["status"] = "approaching"
        _push_msg(s, "수확 시작 — 딸기 접근 중", "info")
    elif action == "harvest_success":
        gt = None
        if s.get("current_harvest_start"):
            gt = round((datetime.now() - datetime.fromisoformat(
                s["current_harvest_start"])).total_seconds(), 2)
            s["grasp_times"].append(gt)
        s["total_attempts"] += 1
        s["success_count"]  += 1
        s["current_harvest_start"] = None
        s["status"] = "returning"
        _push_msg(s, f"수확 성공{f'  ({gt}초)' if gt else ''}", "success")
    elif action == "harvest_fail":
        s["total_attempts"] += 1
        s["current_harvest_start"] = None
        s["status"] = "idle"
        _push_msg(s, "파지 실패", "error")
    elif action == "damage":
        s["damage_count"] += 1
        _push_msg(s, "손상 감지", "warning")
    elif action == "reset":
        s = DEFAULT_STATE.copy()
        s["session_start"] = datetime.now().isoformat()
        _push_msg(s, "대시보드 리셋", "info")
    _save(s)


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="딸기 수확 로봇 웹 대시보드")
    parser.add_argument('--demo',   action='store_true', help='시뮬레이션 데모 모드')
    parser.add_argument('--port',   type=int, default=8765, help='포트 (기본: 8765)')
    parser.add_argument('--host',   default='0.0.0.0',      help='호스트 (기본: 0.0.0.0)')
    parser.add_argument('--update', metavar='ACTION',
                        choices=['start_harvest','harvest_success',
                                 'harvest_fail','damage','reset'])
    parser.add_argument('--msg',    metavar='TEXT')
    parser.add_argument('--level',  default='info',
                        choices=['info','success','warning','error'])
    parser.add_argument('--status', metavar='STATUS',
                        choices=['idle','approaching','grasping','returning','error'])
    args = parser.parse_args()

    # 업데이트 명령 모드 (서버 없이)
    if args.update:
        cmd_update(args.update); return
    if args.msg:
        s = _load()
        if not s.get("session_start"): s["session_start"] = datetime.now().isoformat()
        _push_msg(s, args.msg, args.level); _save(s); return
    if args.status:
        s = _load(); s["status"] = args.status; _save(s); return

    # 서버 실행
    try:
        import uvicorn
    except ImportError:
        print("uvicorn이 필요합니다: pip install uvicorn")
        sys.exit(1)

    app = make_app(demo=args.demo)
    print(f"\n  🍓  딸기 수확 대시보드")
    print(f"  →  http://localhost:{args.port}\n")
    if args.demo:
        print("  [데모 모드] 시뮬레이션이 자동으로 진행됩니다.\n")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == '__main__':
    main()
