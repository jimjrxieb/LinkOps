from fastapi.testclient import TestClient

try:
    from services.whis_sanitize.main import app
except ImportError:
    import sys

    sys.path.append("services/whis_sanitize")
    from main import app

client = TestClient(app)


def test_clean_fixlog():
    payload = {
        "input_type": "fixlog",
        "content": {"log_entry": "Failed to connect to pod"},
    }
    response = client.post("/api/sanitize", json=payload)
    assert response.status_code == 200
    assert "sanitized" in response.json()


def test_invalid_payload():
    payload = {"input_type": "fixlog"}  # missing content
    response = client.post("/api/sanitize", json=payload)
    assert response.status_code == 422
