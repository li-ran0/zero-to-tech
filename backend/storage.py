# backend/storage.py
import sqlite3
from pathlib import Path


# 用 __file__ 定位，不依赖进程的工作目录：
# 从 backend/ 启动和从项目根用 --app-dir 启动，都会落到同一个文件上。
DB_FILE = Path(__file__).with_name("history.db")

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)
    # 老库是上一版建的，没有 session_id 列；CREATE TABLE IF NOT EXISTS 不会补列，
    # 所以这里对已存在的表做一次迁移，否则 INSERT 会报 no such column。
    columns = {row["name"] for row in cur.execute("PRAGMA table_info(history)")}
    if "session_id" not in columns:
        cur.execute("ALTER TABLE history ADD COLUMN session_id TEXT")
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_history_session_created "
        "ON history(session_id, created_at)"
    )
    conn.commit()
    conn.close()


def save_record(session_id, record):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (session_id, text, score, label, pinyin, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        [session_id, record["text"], record["score"],
         record["label"], record["pinyin"], record["created_at"]],
    )
    conn.commit()
    conn.close()

def get_history(session_id, limit):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM history WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
        [session_id, limit],
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(dict(row))
    return records
