#!/usr/bin/env python3
"""
Test the /manual API using a mock JSON payload.
"""
import json
import requests

with open("tools/mocks/sample_task.json") as f:
    payload = json.load(f)

r = requests.post("http://localhost:8000/api/input/manual", json=payload)
print("✅ Manual task upload test complete")
print("Status Code:", r.status_code)
print("Response:", r.json())
