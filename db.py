import sqlite3

DB_NAME = "events.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_event(timestamp, event_type, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (timestamp, event_type, value) VALUES (?, ?, ?)",
        (timestamp, event_type, value)
    )
    conn.commit()
    conn.close()


def fetch_events():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, event_type, value FROM events ORDER BY timestamp DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
