# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import sqlite3
import threading

# =========================
# DATABASE CONNECT
# =========================

conn = sqlite3.connect(
    "files.db",
    check_same_thread=False
)

cur = conn.cursor()

lock = threading.Lock()

# =========================
# FILES TABLE
# =========================

cur.execute("""

CREATE TABLE IF NOT EXISTS files (

    file_key TEXT PRIMARY KEY,
    file_id TEXT,
    file_name TEXT,
    file_size INTEGER

)

""")

# =========================
# SUBTITLE TABLE
# =========================

cur.execute("""

CREATE TABLE IF NOT EXISTS subtitles (

    file_key TEXT,
    lang TEXT,
    content TEXT

)

""")

conn.commit()

# =========================
# SAVE FILE
# =========================

def save_file(
    key,
    file_id,
    file_name,
    file_size
):

    with lock:

        cur.execute(
            """
            INSERT OR REPLACE INTO files
            VALUES (?, ?, ?, ?)
            """,
            (
                key,
                file_id,
                file_name,
                file_size
            )
        )

        conn.commit()

# =========================
# GET FILE
# =========================

def get_file(key):

    with lock:

        cur.execute(
            """
            SELECT * FROM files
            WHERE file_key=?
            """,
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

# =========================
# ADD SUBTITLE
# =========================

def add_subtitle(
    key,
    lang,
    content
):

    with lock:

        cur.execute(
            """
            INSERT INTO subtitles
            VALUES (?, ?, ?)
            """,
            (
                key,
                lang,
                content
            )
        )

        conn.commit()

# =========================
# GET SUBTITLES
# =========================

def get_subtitles(key):

    with lock:

        cur.execute(
            """
            SELECT lang, content
            FROM subtitles
            WHERE file_key=?
            """,
            (key,)
        )

        rows = cur.fetchall()

    return {

        row[0]: row[1]
        for row in rows

    }

# =========================
# DELETE FILE
# =========================

def delete_file(key):

    with lock:

        cur.execute(
            """
            DELETE FROM files
            WHERE file_key=?
            """,
            (key,)
        )

        cur.execute(
            """
            DELETE FROM subtitles
            WHERE file_key=?
            """,
            (key,)
        )

        conn.commit()

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
