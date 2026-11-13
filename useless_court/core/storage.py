"""판례 데이터를 로컬 SQLite에 저장한다."""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'data' / 'court.db'


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        side TEXT NOT NULL,
        verdict TEXT NOT NULL,
        won INTEGER NOT NULL,
        record_json TEXT NOT NULL,
        verdict_text TEXT NOT NULL
    )''')
    conn.commit()
    return conn


def save_case(trial, result, document):
    with connect() as conn:
        cursor = conn.execute('''INSERT INTO cases
            (created_at,name,category,side,verdict,won,record_json,verdict_text)
            VALUES (?,?,?,?,?,?,?,?)''',
            (datetime.now().strftime('%Y-%m-%d %H:%M'), trial['case']['name'], trial['case']['category'],
             trial['side'], result['verdict'], int(result['won']), json.dumps(trial, ensure_ascii=False), document['text']))
        conn.commit()
        return cursor.lastrowid


def history(search=''):
    with connect() as conn:
        return conn.execute('''SELECT id,created_at,name,category,side,verdict,won,verdict_text
                               FROM cases WHERE name LIKE ? ORDER BY id DESC''', (f'%{search}%',)).fetchall()
