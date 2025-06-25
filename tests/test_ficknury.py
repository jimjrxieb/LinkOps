import requests

def test_ficknury_autonomous_task():
    task = {"task": "Restart kubelet", "confidence": 1.0}
    resp = requests.post("http://localhost:8003/evaluate", json=task)
    assert resp.status_code == 200
    assert resp.json().get("action") == "deploy" 