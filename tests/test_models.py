"""
Model validation tests
"""

import pytest
from pydantic import ValidationError

from core.models.schemas import LinkCreate, LinkUpdate, LinkResponse


def test_link_create_valid():
    """Test valid link creation"""
    data = {
        "url": "https://example.com",
        "title": "Example Website",
        "description": "A sample website",
    }
    link = LinkCreate(**data)
    assert link.url == "https://example.com"
    assert link.title == "Example Website"
    assert link.description == "A sample website"


def test_link_create_invalid_url():
    """Test link creation with invalid URL"""
    data = {"url": "not-a-valid-url", "title": "Example Website"}
    with pytest.raises(ValidationError):
        LinkCreate(**data)


def test_link_create_minimal():
    """Test link creation with minimal data"""
    data = {"url": "https://example.com"}
    link = LinkCreate(**data)
    assert link.url == "https://example.com"
    assert link.title is None
    assert link.description is None


def test_link_update_partial():
    """Test partial link update"""
    data = {"title": "Updated Title"}
    link_update = LinkUpdate(**data)
    assert link_update.title == "Updated Title"
    assert link_update.url is None
    assert link_update.description is None


def test_link_update_invalid_url():
    """Test link update with invalid URL"""
    data = {"url": "not-a-valid-url"}
    with pytest.raises(ValidationError):
        LinkUpdate(**data)


def test_link_response_valid():
    """Test valid link response"""
    data = {
        "id": "test-id-123",
        "url": "https://example.com",
        "title": "Example Website",
        "description": "A sample website",
        "screenshot_path": None,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None,
    }
    link_response = LinkResponse(**data)
    assert link_response.id == "test-id-123"
    assert link_response.url == "https://example.com"
    assert link_response.created_at == "2023-01-01T00:00:00"


def test_link_create_title_too_long():
    """Test link creation with title too long"""
    data = {
        "url": "https://example.com",
        "title": "A" * 256,  # Exceeds max_length=255
        "description": "A sample website",
    }
    with pytest.raises(ValidationError):
        LinkCreate(**data)


def test_link_create_description_too_long():
    """Test link creation with description too long"""
    data = {
        "url": "https://example.com",
        "title": "Example Website",
        "description": "A" * 1001,  # Exceeds max_length=1000
    }
    with pytest.raises(ValidationError):
        LinkCreate(**data)
