import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_name="points.db"):
    """Context manager for database connection."""
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()
