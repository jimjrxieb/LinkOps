import requests

def test_orb_rune_creation():
    task = {"input_type": "task", "payload": {"text": "Fix kubectl command"}}
    resp = requests.post("http://localhost:8002/sanitize", json=task)
    assert resp.status_code == 200
    # Optionally, check Whis queue or DB for new orb/rune 