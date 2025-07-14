import psycopg2
import os
from datetime import datetime, timedelta

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posted_deals (
            asin TEXT PRIMARY KEY,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def was_recently_posted(asin, hours=24):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT posted_at FROM posted_deals WHERE asin = %s", (asin,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        posted_at = result[0]
        return datetime.utcnow() - posted_at < timedelta(hours=hours)
    return False

def mark_as_posted(asin):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO posted_deals (asin, posted_at) VALUES (%s, %s) ON CONFLICT (asin) DO UPDATE SET posted_at = EXCLUDED.posted_at",
        (asin, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()
