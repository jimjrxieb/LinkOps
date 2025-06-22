"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL should be set via DATABASE_URL environment variable
# Default is a placeholder - replace with actual credentials in .env file
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/linkops")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 