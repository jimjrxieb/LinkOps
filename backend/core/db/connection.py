"""
Database connection management and utilities
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging
from contextlib import contextmanager
from typing import Generator

from config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database connection manager with connection pooling"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._setup_engine()

    def _setup_engine(self):
        """Setup SQLAlchemy engine with connection pooling"""
        self.engine = create_engine(
            settings.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=settings.DEBUG,
        )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Add engine event listeners
        self._setup_engine_events()

    def _setup_engine_events(self):
        """Setup engine event listeners for logging and monitoring"""

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Set SQLite pragmas for better performance"""
            if "sqlite" in settings.DATABASE_URL:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()

        @event.listens_for(self.engine, "before_cursor_execute")
        def before_cursor_execute(
            conn, cursor, statement, parameters, context, executemany
        ):
            """Log SQL queries in debug mode"""
            if settings.DEBUG:
                logger.debug(f"Executing SQL: {statement}")

    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    @contextmanager
    def get_session_context(self) -> Generator[Session, None, None]:
        """Context manager for database sessions"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_session_context() as session:
                session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    def close(self):
        """Close all database connections"""
        if self.engine:
            self.engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()


def get_db_manager() -> DatabaseManager:
    """Get database manager instance"""
    return db_manager
