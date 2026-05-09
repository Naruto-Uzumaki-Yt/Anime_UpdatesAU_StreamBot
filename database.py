
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

conn.row_factory = sqlite3.Row

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
    file_size INTEGER,
    mime_type TEXT DEFAULT 'video/x-matroska'

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

# =========================
# USER LAST FILE TABLE
# =========================

cur.execute("""

CREATE TABLE IF NOT EXISTS users (

    user_id INTEGER PRIMARY KEY,
    last_file_key TEXT

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
    file_size,
    mime_type="video/x-matroska"
):

    with lock:

        cur.execute(
            """
            INSERT OR REPLACE INTO files
            (
                file_key,
                file_id,
                file_name,
                file_size,
                mime_type
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                key,
                file_id,
                file_name,
                file_size,
                mime_type
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
            SELECT *
            FROM files
            WHERE file_key=?
            """,
            (key,)
        )

        row = cur.fetchone()

    if not row:
        return None

    return {

        "file_key": row["file_key"],
        "file_id": row["file_id"],
        "file_name": row["file_name"],
        "file_size": row["file_size"],
        "mime_type": row["mime_type"]

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

        row["lang"]: row["content"]
        for row in rows

    }

# =========================
# SAVE USER LAST FILE
# =========================

def set_user_last(
    user_id,
    key
):

    with lock:

        cur.execute(
            """
            INSERT OR REPLACE INTO users
            VALUES (?, ?)
            """,
            (
                user_id,
                key
            )
        )

        conn.commit()

# =========================
# GET USER LAST FILE
# =========================

def get_user_last(user_id):

    with lock:

        cur.execute(
            """
            SELECT last_file_key
            FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )

        row = cur.fetchone()

    if not row:
        return None

    return row["last_file_key"]

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
