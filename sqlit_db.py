import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

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
            ''', (get_singapore_time(), prompt_detail, record[0]))
        else:
            # Insert a new record
            conn.execute('''
                INSERT INTO prompt_table (date, prompt_detail)
                VALUES (?, ?)
            ''', (get_singapore_time(), prompt_detail))

# Read the single record
def read_prompt(conn):
    with conn:
        cursor = conn.execute('SELECT id, date, prompt_detail FROM prompt_table LIMIT 1')
        record = cursor.fetchone()
        return record if record else None
    
# Function to get current time in Singapore timezone
def get_singapore_time():
    utc_time = datetime.utcnow().replace(tzinfo=ZoneInfo('UTC'))
    singapore_time = utc_time.astimezone(ZoneInfo('Asia/Singapore'))
    return singapore_time.strftime("%Y-%m-%d %H:%M:%S")

