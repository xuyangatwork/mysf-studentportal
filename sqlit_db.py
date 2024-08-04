import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
def connect_db(db_name="prompts.db"):
    return sqlite3.connect(db_name)

# Create the table if it doesn't exist
def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS prompt_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                prompt_detail TEXT NOT NULL
            )
        ''')

# Update (Insert) record
def upsert_prompt(conn, prompt_detail):
    with conn:
        # Check if a record exists
        cursor = conn.execute('SELECT id FROM prompt_table LIMIT 1')
        record = cursor.fetchone()

        if record:
            # Update the existing record
            conn.execute('''
                UPDATE prompt_table
                SET date = ?, prompt_detail = ?
                WHERE id = ?
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prompt_detail, record[0]))
        else:
            # Insert a new record
            conn.execute('''
                INSERT INTO prompt_table (date, prompt_detail)
                VALUES (?, ?)
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prompt_detail))

# Read the single record
def read_prompt(conn):
    with conn:
        cursor = conn.execute('SELECT id, date, prompt_detail FROM prompt_table LIMIT 1')
        record = cursor.fetchone()
        return record if record else None
