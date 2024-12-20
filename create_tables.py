from rich import print
import sqlite3

from db import get_db_connection

def create_writers_table(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS writers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                total_points INTEGER DEFAULT 0 CHECK (total_points >= 0)
            );
        ''')
        print("[green]✅ writers table created successfully")
    except sqlite3.OperationalError as ex:
        print(f"[red]⚠️ Database operation error: {ex}")
        raise
    except Exception as ex:
        print(f"[red]⚠️ Unexpected error: {ex}")
        raise

def create_dailies_table(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dailies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                writer_id INTEGER NOT NULL,
                date DATE NOT NULL DEFAULT (DATE('now')),
                points INTEGER NOT NULL DEFAULT 0 CHECK (points >= 0),
                FOREIGN KEY (writer_id) REFERENCES writers(id) ON DELETE CASCADE
            );
        ''')
        print("[green]✅ dailies table created successfully")
    except sqlite3.OperationalError as ex:
        print(f"[red]⚠️ Database operation error: {ex}")
        raise
    except Exception as ex:
        print(f"[red]⚠️ Unexpected error: {ex}")
        raise

def create_short_stories_table(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS short_stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                writer_id INTEGER NOT NULL,
                date DATE NOT NULL DEFAULT (DATE('now')),
                points INTEGER NOT NULL DEFAULT 0 CHECK (points >= 0),
                FOREIGN KEY (writer_id) REFERENCES writers(id) ON DELETE CASCADE
            );
        ''')
        print("[green]✅ short_stories table created successfully")
    except sqlite3.OperationalError as ex:
        print(f"[red]⚠️ Database operation error: {ex}")
        raise
    except Exception as ex:
        print(f"[red]⚠️ Unexpected error: {ex}")
        raise

def create_tournaments_table(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                writer_id INTEGER NOT NULL,
                date DATE NOT NULL DEFAULT (DATE('now')),
                points INTEGER NOT NULL DEFAULT 0 CHECK (points >= 0),
                FOREIGN KEY (writer_id) REFERENCES writers(id) ON DELETE CASCADE
            );
        ''')
        print("[green]✅ tournaments table created successfully")
    except sqlite3.OperationalError as ex:
        print(f"[red]⚠️ Database operation error: {ex}")
        raise
    except Exception as ex:
        print(f"[red]⚠️ Unexpected error: {ex}")
        raise

def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        create_writers_table(cursor)
        create_dailies_table(cursor)
        create_short_stories_table(cursor)
        create_tournaments_table(cursor)
        try:
            conn.commit()
            print("[green]💯 all tables created successfully")
        except Exception as ex:
            print(f"[red]❌ error : {ex}")


def main():
    try:
        create_tables()
    except Exception as ex:
        print(f"⚠️ Error in creating tables : {ex}")

if __name__ == "__main__":
    main()
