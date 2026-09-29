# ============================================================
# INFR — Discord Username Checker — WEB EDITION v16.2
# Copyright (c) 2026 INFR. All rights reserved.
# Author: INFR
# ============================================================
# Deploy target: Render (https://render.com)
# Requirements: Python 3.10+
# Install: pip install -r requirements.txt
# Run: python app.py
# ============================================================
# TOKENS: loaded from ENV variable TOKENS="token1,token2"
# PROXIES: hardcoded below in CONFIG["proxies"]
# ============================================================

import asyncio
import aiohttp
import random
import time
import json
import os
import re
import sys
import threading
from datetime import datetime

try:
    from aiohttp_socks import ProxyConnector
except ImportError:
    ProxyConnector = None

try:
    from flask import Flask, render_template_string, jsonify, request
except ImportError:
    print("[!] Install: pip install flask")
    sys.exit(1)

# ==================== TOKENS FROM ENV ====================
def load_tokens_from_env():
    """Load tokens from environment variable TOKENS.
    Format: TOKENS="token1,token2,token3"
    """
    env = os.environ.get("TOKENS", "").strip()
    if not env:
        print("[!] TOKENS environment variable not set")
        print("[!] Set on Render: TOKENS=token1,token2")
        return []
    tokens = [t.strip() for t in env.split(",") if t.strip()]
    return tokens

# ==================== GENERATOR ====================
def generate_usernames(count=10):
    targets = []
    v = "aeiou"
    c = "bcdfghklmnprstv"

    for c1 in c:
        for v1 in v:
            for c2 in c:
                for v2 in v:
                    targets.append(c1 + v1 + c2 + v2)

    for c1 in c:
        for c2 in c:
            for v1 in v:
                for c3 in c:
                    targets.append(c1 + "." + c2 + v1 + c3)
                    targets.append(c1 + "_" + c2 + v1 + c3)

    for c1 in c:
        for v1 in v:
            for c2 in c:
                for v2 in v:
                    targets.append(c1 + v1 + "." + c2 + v2)
                    targets.append(c1 + v1 + "_" + c2 + v2)

    for c1 in c:
        for v1 in v:
            for c2 in c:
                for v2 in v:
                    targets.append(c1 + v1 + c2 + "." + v2)
                    targets.append(c1 + v1 + c2 + "_" + v2)

    seen = set()
    unique = []
    for t in targets:
        if t not in seen:
            seen.add(t)
            unique.append(t)

    random.shuffle(unique)
    return unique[:count]

# ==================== CONFIGURATION ====================
CONFIG = {
    # === TOKENS: loaded from ENV ===
    "tokens": load_tokens_from_env(),
    # === PROXIES: hardcoded ===
    "proxies": [
        "socks5://193.25.215.182:22222",
        "socks5://38.49.210.79:40000",
        "socks5://144.24.111.128:1088",
        "socks5://144.91.121.61:1088",
        "socks5://45.194.33.12:30002",
        "socks5://5.75.133.113:10811",
        "socks5://144.91.111.48:1088",
        "socks5://185.195.71.218:18080",
        "socks5://107.150.41.226:18080",
        "socks5://213.111.146.36:18080",
        "socks5://49.13.22.249:10802",
        "socks5://49.13.22.249:10812",
        "socks5://83.147.217.103:1080",
        "socks5://141.148.206.170:1088",
        "socks5://209.50.255.91:1080",
        "socks5://65.21.252.66:10805",
        "socks5://109.205.182.143:1088",
        "socks5://171.25.158.95:1080",
        "socks5://144.76.61.252:1080",
        "socks5://45.74.31.47:4028",
        "socks5://8.219.245.123:1080",
        "socks5://45.74.31.22:17176",
        "socks5://154.37.218.130:555",
        "socks5://45.74.31.41:10123",
        "socks5://45.74.31.30:14072",
        "socks5://45.74.31.25:11370",
        "socks5://174.138.189.26:2001",
        "socks5://129.153.11.56:1080",
        "socks5://45.74.31.50:9812",
        "socks5://217.142.236.180:1080",
        "socks5://47.238.126.208:1080",
        "socks5://45.74.31.25:16008",
        "socks5://163.5.29.43:1080",
        "socks5://45.74.31.25:5130",
        "socks5://45.74.31.25:4624",
        "socks5://45.74.31.50:20977",
        "socks5://45.74.31.50:6639",
        "socks5://45.74.31.25:6721",
        "socks5://45.74.31.50:4628",
        "socks5://45.74.31.25:7476",
        "socks5://45.74.31.25:6661",
        "socks5://45.74.31.47:5119",
        "socks5://45.74.31.23:15824",
        "socks5://45.74.31.47:7496",
        "socks5://45.74.31.25:9204",
        "socks5://45.74.31.23:13252",
        "socks5://45.74.31.25:4744",
        "socks5://45.74.31.47:4915",
        "socks5://147.45.145.91:443",
        "socks5://45.74.31.47:9367",
        "socks5://45.74.31.50:15520",
        "socks5://45.74.31.41:4187",
        "socks5://45.74.31.25:6812",
        "socks5://45.74.31.47:5900",
        "socks5://45.74.31.50:4150",
        "socks5://45.74.31.47:15727",
        "socks5://45.74.31.50:20780",
        "socks5://45.74.31.47:7837",
        "socks5://45.74.31.30:5249",
        "socks5://111.119.162.248:10919",
        "socks5://45.74.31.22:11756",
        "socks5://111.119.162.248:10948",
        "socks5://45.74.31.40:9868",
        "socks5://45.74.31.23:4154",
        "socks5://45.74.31.22:10176",
        "socks5://45.74.31.23:8552",
        "socks5://45.74.31.30:5524",
        "socks5://45.74.31.22:8438",
        "socks5://45.74.31.40:4300",
    ],
    "delay_min": 10.0,
    "delay_max": 20.0,
    "timeout_total": 20,
    "timeout_connect": 10,
    "check_url": "https://discord.com/api/v9/users/@me",
    "pomelo_url": "https://discord.com/api/v9/users/@me/pomelo-attempt",
    "max_retries": 1,
    "stop_on_429_streak": 3,
    "check_limit": 10,
    "extra_wait_after_429": 60,
    "available_output": os.path.expanduser("~/INFR_available.txt"),
    "web_port": int(os.environ.get("PORT", 5000)),
    "web_host": "0.0.0.0",
}

# ==================== GLOBAL STATE ====================
state = {
    "running": False,
    "checked": 0,
    "available": 0,
    "taken": 0,
    "errors": 0,
    "rate_limits": 0,
    "auth_fails": 0,
    "start_time": None,
    "found": [],
    "logs": [],
    "valid_tokens": 0,
    "total_tokens": len(CONFIG["tokens"]),
    "queue_size": 0,
    "proxies_count": len(CONFIG["proxies"]),
}

# ==================== CHECKER ====================
class UsernameChecker:
    def __init__(self, config):
        self.config = config
        self.tokens = [t.strip() for t in config["tokens"] if t.strip()]
        self.proxies = [p.strip() for p in config["proxies"] if p.strip()]
        self.max_retries = config["max_retries"]
        self.stop_on_429_streak = config["stop_on_429_streak"]
        self.check_limit = config["check_limit"]
        self.extra_wait = config["extra_wait_after_429"]

        self.session = None
        self.connector = None
        self.available_list = []
        self.lock = asyncio.Lock()
        self.running = True
        self.token_valid = []
        self.token_accounts = {}
        self.auth_429_streak = {}
        self.queue = []

    def log(self, msg, level="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        entry = {"time": ts, "msg": msg, "level": level}
        state["logs"].append(entry)
        if len(state["logs"]) > 200:
            state["logs"] = state["logs"][-200:]
        print("[" + ts + "] " + msg)

    async def init_session(self):
        timeout = aiohttp.ClientTimeout(
            total=self.config["timeout_total"],
            connect=self.config["timeout_connect"],
        )
        self.connector = aiohttp.TCPConnector(limit=5, ttl_dns_cache=300, ssl=False)
        self.session = aiohttp.ClientSession(connector=self.connector, timeout=timeout)

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()
        if self.connector and not self.connector.closed:
            await self.connector.close()

    def headers(self, token):
        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

    async def validate_token(self, token):
        try:
            async with self.session.get(
                self.config["check_url"], headers=self.headers(token)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return ("valid", data.get("username", "N/A"))
                elif resp.status == 401:
                    return ("auth_fail", 401)
                elif resp.status == 403:
                    return ("forbidden", 403)
                elif resp.status == 429:
                    try:
                        d = await resp.json()
                        ra = float(d.get("retry_after", 5.0))
                    except Exception:
                        ra = 5.0
                    return ("rate_limit", ra)
                else:
                    return ("unknown", resp.status)
        except asyncio.TimeoutError:
            return ("timeout", 0)
        except Exception as e:
            return ("net_error", str(e)[:100])

    async def validate_all_tokens(self):
        if not self.tokens:
            self.log("No tokens provided in TOKENS env var", "error")
            return []
        self.log("Validating tokens (using only 1st valid) ...")
        for i, token in enumerate(self.tokens, 1):
            status, info = await self.validate_token(token)
            if status == "valid":
                self.token_valid.append(token)
                self.token_accounts[token] = info
                self.log("Token " + str(i) + ": OK — " + str(info), "ok")
                break
            elif status == "auth_fail":
                state["auth_fails"] += 1
                self.log("Token " + str(i) + ": AUTH_FAIL", "error")
            elif status == "rate_limit":
                state["rate_limits"] += 1
                self.log("Token " + str(i) + ": 429 wait " + str(info) + "s", "warn")
                await asyncio.sleep(info)
            elif status == "timeout":
                self.log("Token " + str(i) + ": TIMEOUT", "warn")
            else:
                self.log("Token " + str(i) + ": " + str(status), "error")
        state["valid_tokens"] = len(self.token_valid)
        self.log("Active token: " + str(len(self.token_valid)))
        return self.token_valid

    async def check_username(self, username, token):
        for attempt in range(self.max_retries):
            try:
                async with self.session.post(
                    self.config["pomelo_url"],
                    headers=self.headers(token),
                    json={"username": username},
                ) as resp:
                    status = resp.status
                    data = {}
                    try:
                        data = await resp.json()
                    except Exception:
                        pass

                    if status == 200:
                        taken = data.get("taken", True)
                        if taken is False:
                            return "available"
                        return "taken"
                    elif status == 401:
                        state["auth_fails"] += 1
                        return "auth_fail"
                    elif status == 403:
                        return "forbidden"
                    elif status == 429:
                        state["rate_limits"] += 1
                        self.auth_429_streak[token] = self.auth_429_streak.get(token, 0) + 1
                        ra = float(data.get("retry_after", 5.0))
                        extra = self.extra_wait
                        total_wait = ra + extra
                        self.log("429 — wait " + str(round(total_wait, 1)) + "s (extra " + str(extra) + "s)", "warn")
                        if self.auth_429_streak[token] >= self.stop_on_429_streak:
                            self.log("429 streak — stopping", "error")
                            self.running = False
                            return "rate_limit"
                        await asyncio.sleep(total_wait)
                        continue
                    elif status == 400:
                        return "invalid"
                    else:
                        return "unknown_" + str(status)
            except asyncio.TimeoutError:
                self.log("Timeout for " + username, "warn")
            except Exception as e:
                self.log("Error: " + str(e)[:60], "error")
        return "error"

    async def worker(self, token, worker_id):
        while self.running:
            async with self.lock:
                if state["checked"] >= self.check_limit:
                    self.running = False
                    return
                if not self.queue:
                    return
                username = self.queue.pop(0)
                state["queue_size"] = len(self.queue)

            result = await self.check_username(username, token)

            async with self.lock:
                state["checked"] += 1

                if result == "available":
                    state["available"] += 1
                    self.available_list.append({
                        "username": username,
                        "account": self.token_accounts.get(token, "?")
                    })
                    state["found"].append(username)
                    self.log("AVAILABLE: " + username, "ok")
                    self.save_available(username)
                elif result == "taken":
                    state["taken"] += 1
                    self.log("taken: " + username, "dim")
                else:
                    state["errors"] += 1

            delay = random.uniform(self.config["delay_min"], self.config["delay_max"])
            self.log("waiting " + str(round(delay, 1)) + "s before next ...", "dim")
            await asyncio.sleep(delay)

    def save_available(self, username):
        try:
            with open(self.config["available_output"], "a", encoding="utf-8") as f:
                f.write(username + "\n")
        except Exception:
            pass

    async def run(self):
        state["start_time"] = time.time()
        state["running"] = True
        await self.init_session()
        try:
            await self.validate_all_tokens()
            if not self.token_valid:
                self.log("No valid tokens — exiting", "error")
                state["running"] = False
                return

            self.log("Generating " + str(self.check_limit) + " beautiful 4L usernames ...")
            all_names = generate_usernames(count=self.check_limit)
            self.queue = all_names
            state["queue_size"] = len(self.queue)
            self.log("Queue size: " + str(len(self.queue)))
            self.log("Proxies loaded: " + str(len(self.proxies)))
            self.log("Active workers: 1")

            workers = []
            token = self.token_valid[0]
            w = asyncio.create_task(self.worker(token, 0))
            workers.append(w)

            try:
                await asyncio.gather(*workers, return_exceptions=True)
            except KeyboardInterrupt:
                pass

        finally:
            state["running"] = False
            await self.close_session()
            self.log("Done. Available: " + str(state["available"]) + " / " + str(state["checked"]))
            self.save_report()

    def save_report(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = os.path.expanduser("~/INFR_check_report_" + ts + ".json")
        report = {
            "stats": dict(state),
            "available": self.available_list,
            "author": "INFR",
            "version": "16.2",
        }
        try:
            with open(outfile, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

# ==================== FLASK APP ====================
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>INFR — Username Checker</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
body { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; min-height: 100vh; padding: 20px; }
.container { max-width: 1100px; margin: 0 auto; }
.header { text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 16px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }
.header h1 { color: #fff; font-size: 36px; font-weight: 700; letter-spacing: 4px; }
.header p { color: rgba(255,255,255,0.85); font-size: 13px; margin-top: 6px; }
.info-bar { background: rgba(74, 222, 128, 0.1); border: 1px solid rgba(74, 222, 128, 0.3); border-radius: 12px; padding: 12px 20px; margin-bottom: 20px; color: #4ade80; font-size: 13px; text-align: center; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
.card { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 20px; transition: transform 0.2s; }
.card:hover { transform: translateY(-3px); border-color: rgba(102, 126, 234, 0.5); }
.card .label { color: #8888aa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.card .value { color: #fff; font-size: 30px; font-weight: 700; }
.card .value.green { color: #4ade80; }
.card .value.yellow { color: #fbbf24; }
.card .value.red { color: #f87171; }
.card .value.blue { color: #60a5fa; }
.controls { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
button { padding: 14px 30px; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-start { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
.btn-start:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6); }
.btn-stop { background: linear-gradient(135deg, #f87171, #dc2626); color: #fff; }
.btn-stop:hover { transform: translateY(-2px); }
button:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.panel { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 20px; margin-bottom: 20px; }
.panel h2 { color: #a78bfa; font-size: 15px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.found-list { max-height: 300px; overflow-y: auto; }
.found-item { padding: 12px 15px; background: linear-gradient(90deg, rgba(74, 222, 128, 0.15), rgba(74, 222, 128, 0.05)); border-left: 4px solid #4ade80; border-radius: 8px; margin-bottom: 8px; color: #4ade80; font-weight: 600; font-size: 15px; }
.log-box { background: rgba(0,0,0,0.3); border-radius: 10px; padding: 12px; max-height: 350px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 12px; }
.log-line { padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.log-time { color: #6b7280; margin-right: 8px; }
.log-ok { color: #4ade80; }
.log-warn { color: #fbbf24; }
.log-error { color: #f87171; }
.log-info { color: #a78bfa; }
.log-dim { color: #6b7280; }
.status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #f87171; margin-right: 8px; }
.status-dot.on { background: #4ade80; box-shadow: 0 0 12px #4ade80; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.empty { color: #6b7280; text-align: center; padding: 30px; font-style: italic; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 10px; }
::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>INFR</h1>
    <p>DISCORD USERNAME CHECKER — WEB v16.2</p>
  </div>

  <div class="info-bar">
    SAFE MODE: 1 token, 10 usernames, 10-20s delay, extra 60s after 429
  </div>

  <div class="controls">
    <button class="btn-start" id="startBtn" onclick="startChecker()">START CHECK</button>
    <button class="btn-stop" id="stopBtn" onclick="stopChecker()" disabled>STOP</button>
    <div style="display:flex;align-items:center;color:#a78bfa;font-size:14px;">
      <span class="status-dot" id="statusDot"></span>
      <span id="statusText">Idle</span>
    </div>
  </div>

  <div class="grid">
    <div class="card"><div class="label">Checked</div><div class="value" id="vChecked">0</div></div>
    <div class="card"><div class="label">Available</div><div class="value green" id="vAvailable">0</div></div>
    <div class="card"><div class="label">Taken</div><div class="value" id="vTaken">0</div></div>
    <div class="card"><div class="label">Queue</div><div class="value blue" id="vQueue">0</div></div>
    <div class="card"><div class="label">Valid Tokens</div><div class="value yellow" id="vTokens">0</div></div>
    <div class="card"><div class="label">Rate Limits</div><div class="value red" id="v429">0</div></div>
  </div>

  <div class="panel">
    <h2>AVAILABLE USERNAMES</h2>
    <div class="found-list" id="foundList">
      <div class="empty">No usernames found yet...</div>
    </div>
  </div>

  <div class="panel">
    <h2>LIVE LOGS</h2>
    <div class="log-box" id="logBox">
      <div class="log-line"><span class="log-time">[--:--:--]</span> <span class="log-info">Waiting to start...</span></div>
    </div>
  </div>
</div>

<script>
let running = false;
let lastLogCount = 0;
let lastFoundCount = 0;

async function startChecker() {
  const r = await fetch('/api/start', {method: 'POST'});
  const d = await r.json();
  if (d.status === 'started') { running = true; updateButtons(); }
}

async function stopChecker() {
  await fetch('/api/stop', {method: 'POST'});
  running = false;
  updateButtons();
}

function updateButtons() {
  document.getElementById('startBtn').disabled = running;
  document.getElementById('stopBtn').disabled = !running;
  const dot = document.getElementById('statusDot');
  const txt = document.getElementById('statusText');
  if (running) { dot.className = 'status-dot on'; txt.textContent = 'Running'; }
  else { dot.className = 'status-dot'; txt.textContent = 'Idle'; }
}

async function poll() {
  try {
    const r = await fetch('/api/status');
    const d = await r.json();
    running = d.running;
    updateButtons();
    document.getElementById('vChecked').textContent = d.checked || 0;
    document.getElementById('vAvailable').textContent = d.available || 0;
    document.getElementById('vTaken').textContent = d.taken || 0;
    document.getElementById('vQueue').textContent = d.queue_size || 0;
    document.getElementById('vTokens').textContent = d.valid_tokens || 0;
    document.getElementById('v429').textContent = d.rate_limits || 0;

    if (d.found && d.found.length !== lastFoundCount) {
      const list = document.getElementById('foundList');
      if (d.found.length === 0) {
        list.innerHTML = '<div class="empty">No usernames found yet...</div>';
      } else {
        list.innerHTML = d.found.slice().reverse().map(u => '<div class="found-item">' + u + '</div>').join('');
      }
      lastFoundCount = d.found.length;
    }

    if (d.logs && d.logs.length !== lastLogCount) {
      const box = document.getElementById('logBox');
      box.innerHTML = d.logs.slice(-50).map(l => {
        let cls = 'log-info';
        if (l.level === 'ok') cls = 'log-ok';
        else if (l.level === 'warn') cls = 'log-warn';
        else if (l.level === 'error') cls = 'log-error';
        else if (l.level === 'dim') cls = 'log-dim';
        return '<div class="log-line"><span class="log-time">[' + l.time + ']</span> <span class="' + cls + '">' + l.msg + '</span></div>';
      }).join('');
      box.scrollTop = box.scrollHeight;
      lastLogCount = d.logs.length;
    }
  } catch(e) {}
  setTimeout(poll, 1000);
}

poll();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/start', methods=['POST'])
def api_start():
    if state["running"]:
        return jsonify({"status": "already_running"})

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        checker = UsernameChecker(CONFIG)
        try:
            loop.run_until_complete(checker.run())
        except Exception as e:
            state["logs"].append({"time": datetime.now().strftime("%H:%M:%S"), "msg": "Error: " + str(e)[:100], "level": "error"})
        finally:
            state["running"] = False

    threading.Thread(target=run_async, daemon=True).start()
    return jsonify({"status": "started"})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    state["running"] = False
    return jsonify({"status": "stopping"})

@app.route('/api/status')
def api_status():
    return jsonify({
        "running": state["running"],
        "checked": state["checked"],
        "available": state["available"],
        "taken": state["taken"],
        "errors": state["errors"],
        "rate_limits": state["rate_limits"],
        "queue_size": state["queue_size"],
        "valid_tokens": state["valid_tokens"],
        "found": state["found"],
        "logs": state["logs"][-50:],
        "proxies_count": state.get("proxies_count", 0),
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# ==================== MAIN ====================
def main():
    port = int(os.environ.get("PORT", CONFIG["web_port"]))
    print("")
    print("=" * 60)
    print("  INFR — USERNAME CHECKER — WEB v16.2")
    print("  made by INFR — 2026")
    print("=" * 60)
    print("")
    print("  Tokens from env:  " + str(len(CONFIG['tokens'])))
    print("  Proxies in code:  " + str(len(CONFIG['proxies'])))
    print("  Limit:            " + str(CONFIG['check_limit']))
    print("  Port:             " + str(port))
    print("")
    print("=" * 60)
    print("")

    app.run(host=CONFIG["web_host"], port=port, debug=False, threaded=True)

if __name__ == "__main__":
    main()
