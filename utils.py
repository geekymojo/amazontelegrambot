import sqlite3

DB_NAME = 'posted_deals.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posted (
            asin TEXT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_posted_recently(asin):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT timestamp FROM posted WHERE asin = ?', (asin,))
    row = c.fetchone()
    conn.close()
    return row is not None

def save_posted(asin):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO posted (asin) VALUES (?)', (asin,))
    conn.commit()
    conn.close()
