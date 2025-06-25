#!/usr/bin/env python3
"""
Test script to verify sanitizer → whis communication
"""

import requests
import json
import time

def test_sanitizer_whis_communication():
    """Test the communication flow between sanitizer and whis"""
    
    print("🧪 Testing Sanitizer → Whis Communication")
    print("=" * 50)
    
    # Test data
    test_cases = [
        {
            "name": "Kubernetes Task",
            "input_type": "task",
            "payload": {
                "task_description": "Create a Kubernetes pod with nginx image",
                "priority": "high"
            }
        },
        {
            "name": "Q&A Pair",
            "input_type": "qna", 
            "payload": {
                "question": "How do I deploy to Kubernetes?",
                "answer": "Use kubectl apply -f deployment.yaml"
            }
        },
        {
            "name": "Info Dump",
            "input_type": "info",
            "payload": {
                "system_info": "Linux server with 8GB RAM",
                "services": ["nginx", "postgres", "redis"]
            }
        }
    ]
    
    sanitizer_url = "http://localhost:8002/api/sanitize"
    whis_url = "http://localhost:8003/api/whis/train"
    
    # Test 1: Direct sanitizer call
    print("\n1️⃣ Testing Sanitizer Endpoint")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        
        try:
            response = requests.post(sanitizer_url, json={
                "input_type": test_case["input_type"],
                "payload": test_case["payload"]
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: {result['status']}")
                print(f"   📤 Forwarded to Whis: {result.get('forwarded_to_whis', False)}")
                
                if result.get('whis_response'):
                    print(f"   🧠 Whis Response: {result['whis_response']}")
                elif result.get('error'):
                    print(f"   ❌ Error: {result['error']}")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    # Test 2: Direct whis call
    print("\n2️⃣ Testing Whis Training Endpoint")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        
        try:
            response = requests.post(whis_url, json={
                "input_type": test_case["input_type"],
                "payload": test_case["payload"]
            }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: {result['status']}")
                print(f"   🏷️  Category: {result.get('category', 'N/A')}")
                print(f"   💬 Message: {result.get('message', 'N/A')}")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    # Test 3: Service health check
    print("\n3️⃣ Service Health Check")
    print("-" * 30)
    
    services = [
        ("Sanitizer", "http://localhost:8002/health"),
        ("Whis", "http://localhost:8003/health")
    ]
    
    for service_name, health_url in services:
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {service_name}: Healthy")
            else:
                print(f"   ⚠️  {service_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {service_name}: {str(e)}")
    
    print("\n🎉 Communication test complete!")
    print("\n📝 Next steps:")
    print("1. Check service logs for detailed information")
    print("2. Verify data is being processed correctly")
    print("3. Monitor the data_lake directory for saved files")

if __name__ == "__main__":
    test_sanitizer_whis_communication() 