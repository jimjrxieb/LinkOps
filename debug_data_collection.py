#!/usr/bin/env python3
"""
Debug script to test data collection without database dependencies
"""

import requests
import json

def test_data_collection():
    """Test the data collection endpoints"""
    
    # Test Q&A submission
    qna_data = {
        "type": "qna",
        "content": {
            "question": "What is Kubernetes?",
            "answer": "Kubernetes is a container orchestration platform."
        }
    }
    
    print("🧪 Testing Q&A submission...")
    try:
        response = requests.post(
            "http://localhost:8000/api/data-collect/sanitize",
            json=qna_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test task submission
    task_data = {
        "type": "task",
        "content": "Deploy a Kubernetes pod"
    }
    
    print("\n🧪 Testing task submission...")
    try:
        response = requests.post(
            "http://localhost:8000/api/data-collect/sanitize",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Whis nightly training
    print("\n🧪 Testing Whis nightly training...")
    try:
        response = requests.post("http://localhost:8000/api/whis/train-nightly")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_data_collection() 