import sqlite3
import os
from datetime import datetime, timedelta

def get_db():
    conn = sqlite3.connect("jaseb.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists("jaseb.db"):
        conn = get_db()
        c = conn.cursor()
        # Tabel akun userbot
        c.execute('''CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            session_file TEXT,
            status TEXT,
            masa_sewa INTEGER,
            expired_at TEXT
        )''')
        # Tabel konfigurasi per akun
        c.execute('''CREATE TABLE configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            teks_forward TEXT,
            watermark TEXT,
            auto_respon TEXT,
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )''')
        # Tabel log
        c.execute('''CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            time TEXT,
            group_name TEXT,
            status TEXT,
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )''')
        conn.commit()
        conn.close()

init_db() 