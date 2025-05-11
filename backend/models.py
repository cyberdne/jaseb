from .db import get_db
from datetime import datetime, timedelta

def add_account(phone, session_file, masa_sewa):
    conn = get_db()
    c = conn.cursor()
    expired_at = (datetime.now() + timedelta(days=masa_sewa)).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO accounts (phone, session_file, status, masa_sewa, expired_at) VALUES (?, ?, ?, ?, ?)",
              (phone, session_file, 'active', masa_sewa, expired_at))
    account_id = c.lastrowid
    # Default config
    c.execute("INSERT INTO configs (account_id, teks_forward, watermark, auto_respon) VALUES (?, ?, ?, ?)",
              (account_id, '', '', ''))
    conn.commit()
    conn.close()
    return account_id

def get_accounts():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_account(account_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM accounts WHERE id=?", (account_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_account_status(account_id, status):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE accounts SET status=? WHERE id=?", (status, account_id))
    conn.commit()
    conn.close()

def get_config(account_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM configs WHERE account_id=?", (account_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_config(account_id, teks_forward, watermark, auto_respon):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE configs SET teks_forward=?, watermark=?, auto_respon=? WHERE account_id=?",
              (teks_forward, watermark, auto_respon, account_id))
    conn.commit()
    conn.close()

def add_log(account_id, time, group_name, status):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO logs (account_id, time, group_name, status) VALUES (?, ?, ?, ?)",
              (account_id, time, group_name, status))
    conn.commit()
    conn.close()

def get_logs(account_id=None, limit=100):
    conn = get_db()
    c = conn.cursor()
    if account_id:
        c.execute("SELECT * FROM logs WHERE account_id=? ORDER BY id DESC LIMIT ?", (account_id, limit))
    else:
        c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows] 