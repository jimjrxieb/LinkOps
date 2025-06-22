#!/usr/bin/env python3
"""
Simple test to verify backend functionality
"""

import requests
import json
import time
import sys

def test_backend():
    """Test the backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing LinkOps James Workflow Backend...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        data = response.json()
        print(f"   Message: {data.get('message', 'N/A')}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test task creation
    try:
        task_data = {
            "task_input": "How do I restart a Kubernetes pod?",
            "origin": "manager",
            "priority": "medium",
            "tags": ["kubernetes", "troubleshooting"]
        }
        response = requests.post(f"{base_url}/api/tasks", json=task_data, timeout=10)
        print(f"✅ Task creation: {response.status_code}")
        result = response.json()
        task_id = result.get("task_id")
        print(f"   Task ID: {task_id}")
        
        # Test James solve
        if task_id:
            response = requests.post(f"{base_url}/api/tasks/{task_id}/james/solve", timeout=10)
            print(f"✅ James solve: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False
    
    print("🎉 All tests passed!")
    return True

if __name__ == "__main__":
    # Wait a bit for the server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    success = test_backend()
    sys.exit(0 if success else 1) 