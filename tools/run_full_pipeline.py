#!/usr/bin/env python3
"""
Simulate a full Whis data flow: Manual or YouTube input → Sanitizer → (simulated) Smithing → Log Output
"""
import argparse
import requests
import json
import time

MANUAL_ENDPOINT = "http://localhost:8000/api/input/manual"
YOUTUBE_ENDPOINT = "http://localhost:8000/api/input/youtube-transcript"
SMITHING_ENDPOINT = "http://localhost:8002/api/whis/smith-orbs"  # Example future endpoint

def submit_manual():
    with open("tools/mocks/sample_task.json") as f:
        payload = json.load(f)
    print("🟢 Submitting manual task to Whis...")
    res = requests.post(MANUAL_ENDPOINT, json=payload)
    print("✅ Submission Response:", res.status_code, res.json())
    return res.ok

def submit_youtube():
    with open("tools/mocks/sample_transcript.json") as f:
        payload = json.load(f)
    print("🟢 Submitting YouTube transcript to Whis...")
    res = requests.post(YOUTUBE_ENDPOINT, json=payload)
    print("✅ Submission Response:", res.status_code, res.json())
    return res.ok

def simulate_smithing():
    print("🛠️  Simulating Orb & Rune Smithing... (stubbed for now)")
    time.sleep(1.5)
    print("✨ Orbs & Runes generated successfully.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Simulate full Whis MLOps pipeline.")
    parser.add_argument("--type", choices=["manual", "youtube"], required=True, help="Type of input to simulate")

    args = parser.parse_args()

    if args.type == "manual":
        success = submit_manual()
    elif args.type == "youtube":
        success = submit_youtube()
    else:
        print("❌ Invalid input type.")
        return

    if success:
        print("⏳ Waiting for sanitizer to process...")
        time.sleep(2.5)  # Replace with queue check if desired

        smith_result = simulate_smithing()
        if smith_result:
            print("✅ Whis pipeline simulation complete.")
        else:
            print("⚠️  Smithing failed.")
    else:
        print("❌ Input submission failed.")

if __name__ == "__main__":
    main() 