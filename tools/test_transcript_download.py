#!/usr/bin/env python3
"""
Test direct transcript download from YouTube (no API call).
"""
from services.whis_data_input.utils.youtube_transcript import download_transcript

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
transcript = download_transcript(url)

if transcript:
    print("✅ Transcript Downloaded:\n")
    print(transcript[:300] + "...")
else:
    print("❌ No transcript found.")
