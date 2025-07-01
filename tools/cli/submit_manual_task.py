#!/usr/bin/env python3
"""
Submit a manual task (from JSON file) to the whis_data_input API.
"""
import argparse
import requests
import json


def main():
    parser = argparse.ArgumentParser(
        description="Submit manual task JSON to data input API."
    )
    parser.add_argument("--file", required=True, help="Path to sample_task.json")
    parser.add_argument(
        "--api",
        default="http://localhost:8001/api/input/manual-task",
        help="Data input API endpoint",
    )
    args = parser.parse_args()

    with open(args.file, "r") as f:
        payload = json.load(f)
    try:
        resp = requests.post(args.api, json=payload)
        print(f"Status: {resp.status_code}")
        print(resp.json())
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
