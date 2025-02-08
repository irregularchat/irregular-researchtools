import sqlite3
import time

DATABASE = "session_data.db"

def create_session_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                account_number TEXT PRIMARY KEY,
                session_data TEXT,
                last_accessed INTEGER
            )
        """)
        conn.commit()

def store_session_data(account_number, session_data):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (account_number, session_data, last_accessed)
            VALUES (?, ?, ?)
        """, (account_number, session_data, int(time.time())))
        conn.commit()

def retrieve_session_data(account_number):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT session_data FROM sessions WHERE account_number = ?
        """, (account_number,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

def delete_expired_sessions(expiration_time):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM sessions WHERE last_accessed < ?
        """, (int(time.time()) - expiration_time,))
        conn.commit()

create_session_table()
