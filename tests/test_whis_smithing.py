from fastapi.testclient import TestClient

try:
    from services.whis_smithing.main import app
except ImportError:
    import sys

    sys.path.append("shadows/whis_smithing")
    from main import app

client = TestClient(app)


def test_generate_rune():
    payload = {"input_data": {"test": "data"}, "rune_type": "standard"}
    response = client.post("/api/v1/smithing/generate-rune", json=payload)
    assert response.status_code in [200, 201]
    assert "rune" in response.json() or "result" in response.json()
