from fastapi.testclient import TestClient

try:
    from services.whis_enhance.main import app
except ImportError:
    import sys

    sys.path.append("services/whis_enhance")
    from main import app

client = TestClient(app)


def test_enhancement_status():
    response = client.get("/api/v1/enhance/enhancement-status")
    assert response.status_code in [200, 201]
    assert "status" in response.json() or "result" in response.json()
