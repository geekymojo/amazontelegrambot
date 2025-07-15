import sqlite3
import os

DB_FILE = "posted_deals.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posted_deals (
            asin TEXT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_posted_recently(asin):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT asin FROM posted_deals WHERE asin = ?', (asin,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_posted(asin):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO posted_deals (asin) VALUES (?)', (asin,))
    conn.commit()
    conn.close()
