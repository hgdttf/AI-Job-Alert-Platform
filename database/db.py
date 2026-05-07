import sqlite3
import os

# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "..",
    "platform.db"
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

# Allows dictionary-style row access
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        send_time TEXT,
        btech INTEGER,
        mtech INTEGER,
        life_science INTEGER,
        ms_research INTEGER,
        last_sent TEXT
    )
    """
)

# ==========================================
# SENT JOBS TABLE
# ==========================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sent_jobs (

        job_link TEXT PRIMARY KEY

    )
    """
)

# ==========================================
# SAVE CHANGES
# ==========================================

conn.commit()