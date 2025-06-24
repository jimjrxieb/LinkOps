import psycopg
import os

DB_URL = os.getenv("DB_URL", "postgresql://linkops:secret@db:5432/linkops_core")

def get_conn():
    return psycopg.connect(DB_URL)

def save_orb(title, category, agent, content, recurrence="low"):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO orbs (title, category, agent, content, recurrence) VALUES (%s, %s, %s, %s, %s)",
            (title, category, agent, content, recurrence)
        )

def save_rune(orb_id, script):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO runes (orb_id, script) VALUES (%s, %s)",
            (orb_id, script)
        )
# Add more functions like save_log(), get_agent_capabilities(), etc. 