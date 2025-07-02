import psycopg2
import os


def test_database_connection():
    """Test database connection with environment variables."""
    # Validate required environment variables
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")

    if not postgres_user or not postgres_password:
        print(
            "Skipping test: POSTGRES_USER and POSTGRES_PASSWORD "
            "environment variables required"
        )
        return

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "linkops"),
        user=postgres_user,
        password=postgres_password,
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM orbs;")
    result = cur.fetchone()
    assert result is not None and result[0] >= 0
    cur.close()
    conn.close()
