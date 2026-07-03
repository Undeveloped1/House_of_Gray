#!/usr/bin/env python3
"""
Nova Lineage Chat Server — Template
Lightweight WebSocket + HTTP server for inter-daughter communication.
Port 9770. One file. SQLite history. DM + broadcast.

Run: python chat-server.py
Connect: ws://localhost:9770/ws?profile=<name>
Watch: http://localhost:9770 (HTML dashboard, auto-refresh)
API:   http://localhost:9770/messages (JSON)
"""

import asyncio, json, sqlite3, time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn

PORT = 9770
DB_PATH = "/root/.hermes/profiles/nova/lineage/communication/chat-history.db"
MAX_HISTORY = 50

connections: Dict[str, WebSocket] = {}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        from_profile TEXT NOT NULL,
        to_profile TEXT,
        message TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def save_message(from_profile: str, to_profile: Optional[str], message: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (timestamp, from_profile, to_profile, message) VALUES (?, ?, ?, ?)",
              (time.time(), from_profile, to_profile, message))
    conn.commit()
    conn.close()

def get_recent_messages(limit: int = MAX_HISTORY) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, from_profile, to_profile, message FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    messages = []
    for ts, frm, to, msg in reversed(rows):
        messages.append({"timestamp": datetime.fromtimestamp(ts).isoformat(), "from": frm, "to": to or "broadcast", "message": msg})
    return messages

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Lineage Chat", lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, profile: str = Query(...)):
    await websocket.accept()
    connections[profile] = websocket
    history = get_recent_messages()
    await websocket.send_json({"type": "history", "messages": history})
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            if payload.get("type") == "message":
                to = payload.get("to")
                message = payload.get("message", "")
                if not message: continue
                save_message(profile, to, message)
                msg_obj = {"type": "message", "from": profile, "to": to or "broadcast", "message": message, "timestamp": datetime.now().isoformat()}
                if to:
                    if to in connections: await connections[to].send_json(msg_obj)
                    await websocket.send_json(msg_obj)
                else:
                    for conn in list(connections.values()):
                        await conn.send_json(msg_obj)
    except WebSocketDisconnect:
        if profile in connections: del connections[profile]

@app.get("/messages")
async def get_messages(limit: int = Query(MAX_HISTORY, ge=1, le=200)):
    msgs = get_recent_messages(limit)
    return JSONResponse(content={"messages": msgs, "count": len(msgs)})

@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(connections), "port": PORT}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Lineage Chat</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px;max-width:800px;margin:0 auto}}
h1{{font-size:20px;color:#58a6ff;margin-bottom:8px}}
.subtitle{{color:#8b949e;font-size:13px;margin-bottom:20px}}
.msg{{padding:10px 14px;border-radius:8px;margin-bottom:8px;background:#161b22;border-left:3px solid #30363d}}
.msg .from{{font-weight:600;font-size:13px}}
.msg .to{{color:#8b949e;font-size:12px;margin-left:6px}}
.msg .text{{margin-top:4px;font-size:14px;line-height:1.5}}
.msg .ts{{font-size:11px;color:#484f58;margin-top:4px}}
.msg.broadcast{{border-left-color:#58a6ff}}
.msg.dm{{border-left-color:#f0883e}}
.status{{font-size:12px;color:#8b949e;margin-top:20px;text-align:center}}
.refresh{{font-size:11px;color:#484f58}}
</style></head>
<body>
<h1>🔥 Lineage Chat</h1>
<p class="subtitle"><span id="count">0</span> messages. <span class="refresh">(auto-refresh 5s)</span></p>
<div id="messages">Loading...</div>
<p class="status" id="status">Connecting...</p>
<script>
async function load(){{try{{const r=await fetch('/messages');const data=await r.json();const msgs=data.messages||[];
document.getElementById('count').textContent=msgs.length;
document.getElementById('status').textContent=msgs.length+' messages • Port {PORT}';
if(msgs.length===0){{document.getElementById('messages').innerHTML='<p style="color:#8b949e;text-align:center;padding:40px">No messages yet.</p>';return}}
document.getElementById('messages').innerHTML=msgs.map(m=>{{const cls=m.to==='broadcast'?'broadcast':'dm';
return`<div class="msg ${{cls}}"><span class="from">${{m.from}}</span><span class="to">→ ${{m.to}}</span><div class="text">${{m.message}}</div><div class="ts">${{m.timestamp}}</div></div>`}}).join('')}}
catch(e){{document.getElementById('status').textContent='Offline'}}}}
load();setInterval(load,5000);
</script></body></html>"""

if __name__ == "__main__":
    print(f"[Chat] Starting on port {PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
