#!/usr/bin/env python3
"""
Stub: Run the full pipeline (input → sanitize → train) for testing.
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run the full pipeline: input → sanitize → train.")
    parser.add_argument('--input', required=True, help='Input file or URL')
    parser.add_argument('--topic', required=True, help='Topic for the run')
    args = parser.parse_args()

    print(f"[STUB] Would submit input: {args.input} with topic: {args.topic}")
    print("[STUB] Would call sanitize service...")
    print("[STUB] Would call train service...")
    print("[STUB] Pipeline complete.")

if __name__ == "__main__":
    main() 