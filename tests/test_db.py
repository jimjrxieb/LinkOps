import psycopg2
import os

def test_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "linkops"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM orbs;")
    assert cur.fetchone()[0] >= 0
    cur.close()
    conn.close() 