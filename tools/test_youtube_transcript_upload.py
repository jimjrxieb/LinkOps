#!/usr/bin/env python3
"""
Test the /youtube-transcript API using a mock JSON payload.
"""
import json
import requests

with open("tools/mocks/sample_transcript.json") as f:
    payload = json.load(f)

r = requests.post("http://localhost:8000/api/input/youtube-transcript", json=payload)
print("✅ Test upload complete")
print("Status Code:", r.status_code)
print("Response:", r.json())
