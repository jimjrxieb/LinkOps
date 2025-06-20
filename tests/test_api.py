"""
API endpoint tests
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test basic health check endpoint"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "LinkOps Core"
    assert "timestamp" in data


def test_detailed_health_check(client: TestClient):
    """Test detailed health check endpoint"""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "kafka" in data
    assert "system" in data
    assert "directories" in data


def test_readiness_check(client: TestClient):
    """Test readiness check endpoint"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_liveness_check(client: TestClient):
    """Test liveness check endpoint"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_get_links_empty(client: TestClient):
    """Test getting links when database is empty"""
    response = client.get("/api/v1/links")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_link(client: TestClient, sample_link_data):
    """Test creating a new link"""
    response = client.post("/api/v1/links", json=sample_link_data)
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == sample_link_data["url"]
    assert data["title"] == sample_link_data["title"]
    assert data["description"] == sample_link_data["description"]
    assert "id" in data
    assert "created_at" in data


def test_create_link_invalid_url(client: TestClient):
    """Test creating a link with invalid URL"""
    invalid_data = {
        "url": "not-a-valid-url",
        "title": "Invalid URL",
        "description": "This should fail"
    }
    response = client.post("/api/v1/links", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_get_link_not_found(client: TestClient):
    """Test getting a non-existent link"""
    response = client.get("/api/v1/links/non-existent-id")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_update_link_not_found(client: TestClient):
    """Test updating a non-existent link"""
    update_data = {"title": "Updated Title"}
    response = client.put("/api/v1/links/non-existent-id", json=update_data)
    assert response.status_code == 404


def test_delete_link_not_found(client: TestClient):
    """Test deleting a non-existent link"""
    response = client.delete("/api/v1/links/non-existent-id")
    assert response.status_code == 404


def test_link_crud_operations(client: TestClient, sample_link_data):
    """Test complete CRUD operations for a link"""
    # Create
    create_response = client.post("/api/v1/links", json=sample_link_data)
    assert create_response.status_code == 200
    link_data = create_response.json()
    link_id = link_data["id"]
    
    # Read
    get_response = client.get(f"/api/v1/links/{link_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == link_id
    
    # Update
    update_data = {"title": "Updated Title"}
    update_response = client.put(f"/api/v1/links/{link_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"
    
    # Delete
    delete_response = client.delete(f"/api/v1/links/{link_id}")
    assert delete_response.status_code == 200
    
    # Verify deletion
    get_after_delete = client.get(f"/api/v1/links/{link_id}")
    assert get_after_delete.status_code == 404
