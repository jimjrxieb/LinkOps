"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.api.app import create_app
from config.database import Base, get_db
from config.settings import get_settings


@pytest.fixture
def settings():
    """Get test settings"""
    return get_settings()


@pytest.fixture
def test_db():
    """Create test database"""
    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, TestingSessionLocal


@pytest.fixture
def db_session(test_db):
    """Get database session for testing"""
    engine, TestingSessionLocal = test_db

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    return override_get_db


@pytest.fixture
def client(db_session):
    """Create test client"""
    app = create_app()

    # Override database dependency
    app.dependency_overrides[get_db] = db_session

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_link_data():
    """Sample link data for testing"""
    return {
        "url": "https://example.com",
        "title": "Example Website",
        "description": "A sample website for testing",
    }


@pytest.fixture
def sample_link_response():
    """Sample link response data for testing"""
    return {
        "id": "test-id-123",
        "url": "https://example.com",
        "title": "Example Website",
        "description": "A sample website for testing",
        "screenshot_path": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None,
    }
