import requests

def test_digest_creation():
    resp = requests.post("http://localhost:8001/train/digest")
    assert resp.status_code == 200
    assert "summary" in resp.json() 