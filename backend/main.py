import os
import sqlite3
from fastapi import FastAPI, WebSocket, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import datetime
import asyncio
from typing import Optional
from .models import add_account, get_accounts, get_account, update_account_status, get_config, update_config, add_log, get_logs

app = FastAPI()

# CORS agar frontend bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi DB
if not os.path.exists("logs.db"):
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        group_name TEXT,
        status TEXT
    )
    """)
    conn.commit()
    conn.close()

@app.get("/logs")
def get_logs_api(account_id: Optional[int] = None):
    return {"logs": get_logs(account_id)}

@app.post("/log")
async def log(request: Request):
    data = await request.json()
    add_log(data.get("account_id"), data["time"], data["group_name"], data["status"])
    # Kirim ke websocket
    for ws in websockets:
        await ws.send_json(data)
    return {"ok": True}

websockets = set()

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websockets.add(websocket)
    try:
        while True:
            await asyncio.sleep(60)  # keep alive
    except Exception:
        pass
    finally:
        websockets.remove(websocket)

@app.get("/", response_class=HTMLResponse)
def index():
    return "<h1>JASEB Backend Running</h1>"

@app.post("/accounts")
def create_account(phone: str = Form(...), masa_sewa: int = Form(...), session_file: UploadFile = File(...)):
    # Simpan session file
    session_path = f"sessions/{phone}.session"
    os.makedirs("sessions", exist_ok=True)
    with open(session_path, "wb") as f:
        f.write(session_file.file.read())
    account_id = add_account(phone, session_path, masa_sewa)
    return {"ok": True, "account_id": account_id}

@app.get("/accounts")
def list_accounts():
    return {"accounts": get_accounts()}

@app.get("/accounts/{account_id}")
def get_account_detail(account_id: int):
    return get_account(account_id)

@app.post("/accounts/{account_id}/status")
def set_account_status(account_id: int, status: str = Form(...)):
    update_account_status(account_id, status)
    return {"ok": True}

@app.get("/accounts/{account_id}/config")
def get_account_config(account_id: int):
    return get_config(account_id)

@app.post("/accounts/{account_id}/config")
def set_account_config(account_id: int, teks_forward: str = Form(...), watermark: str = Form(...), auto_respon: str = Form(...)):
    update_config(account_id, teks_forward, watermark, auto_respon)
    return {"ok": True}

@app.get("/sync")
def sync_for_daemon():
    # Endpoint untuk daemon: ambil semua akun aktif & config
    accounts = get_accounts()
    configs = {a['id']: get_config(a['id']) for a in accounts}
    return {"accounts": accounts, "configs": configs} 