import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_name="points.db"):
    """Context manager for database connection."""
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()

def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dailies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                POINT INTEGER NOT NULL
            )
        ''')
        conn.commit()

