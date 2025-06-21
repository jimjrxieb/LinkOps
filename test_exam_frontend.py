#!/usr/bin/env python3
"""
Test the exam form frontend functionality
"""
import requests
import json

def test_exam_endpoint():
    """Test the exam submission endpoint"""
    print("🧪 Testing Exam Form Frontend...")
    
    # Test data
    test_data = {
        "task_id": "terraform/local-exec",
        "question": "Which provisioner type runs on the machine executing Terraform?",
        "answer": "local-exec provisioner"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/james/submit-answer",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"✅ Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server might not be running")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_exam_endpoint() 