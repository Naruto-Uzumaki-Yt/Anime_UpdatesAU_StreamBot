# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

import sqlite3

conn = sqlite3.connect("files.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS files (
    file_key TEXT PRIMARY KEY,
    file_id TEXT,
    file_name TEXT,
    file_size INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS subtitles (
    file_key TEXT,
    lang TEXT,
    content TEXT
)
""")

conn.commit()

def save_file(key, file_id, file_name, file_size):
    cur.execute(
        "INSERT INTO files VALUES (?, ?, ?, ?)",
        (key, file_id, file_name, file_size)
    )
    conn.commit()

def get_file(key):
    cur.execute(
        "SELECT * FROM files WHERE file_key=?",
        (key,)
    )

    row = cur.fetchone()

    if not row:
        return None

    return {
        "file_key": row[0],
        "file_id": row[1],
        "file_name": row[2],
        "file_size": row[3]
    }

def add_subtitle(key, lang, content):
    cur.execute(
        "INSERT INTO subtitles VALUES (?, ?, ?)",
        (key, lang, content)
    )
    conn.commit()

def get_subtitles(key):
    cur.execute(
        "SELECT lang, content FROM subtitles WHERE file_key=?",
        (key,)
    )

    rows = cur.fetchall()

    return {r[0]: r[1] for r in rows}

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
