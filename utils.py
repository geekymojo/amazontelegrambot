import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS posted_deals (
                    asin TEXT PRIMARY KEY,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

def is_posted_recently(asin, hours=24):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT posted_at FROM posted_deals WHERE asin = %s AND posted_at > NOW() - INTERVAL '%s hours'",
                (asin, hours)
            )
            return cur.fetchone() is not None

def save_posted(asin):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO posted_deals (asin) VALUES (%s) ON CONFLICT (asin) DO UPDATE SET posted_at = CURRENT_TIMESTAMP",
                (asin,)
            )
            conn.commit()
