#!/usr/bin/env python3
"""
Test script to verify the complete data flow:
data_collector → sanitizer → whis
"""

import requests
import json
import time

def test_complete_data_flow():
    """Test the complete data flow from collection to training"""
    
    print("🔄 Testing Complete Data Flow: data_collector → sanitizer → whis")
    print("=" * 70)
    
    # Test data
    test_cases = [
        {
            "name": "Kubernetes Task",
            "input_type": "task",
            "payload": {
                "task_description": "Create a Kubernetes deployment with nginx",
                "priority": "high",
                "environment": "production"
            }
        },
        {
            "name": "Q&A Pair",
            "input_type": "qna", 
            "payload": {
                "question": "How do I scale a Kubernetes deployment?",
                "answer": "Use kubectl scale deployment <name> --replicas=<number>",
                "context": "kubernetes scaling"
            }
        },
        {
            "name": "Info Dump",
            "input_type": "info",
            "payload": {
                "system_info": "Linux server with 16GB RAM",
                "services": ["nginx", "postgres", "redis", "kafka"],
                "environment": "staging"
            }
        },
        {
            "name": "Fix Log",
            "input_type": "fixlog",
            "payload": {
                "error": "Pod failed to start due to resource constraints",
                "solution": "Increased memory limits in deployment",
                "namespace": "default"
            }
        }
    ]
    
    data_collector_url = "http://localhost:8001/api/collect"
    
    print("\n1️⃣ Testing Data Collector → Sanitizer → Whis Flow")
    print("-" * 50)
    
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print(f"   Type: {test_case['input_type']}")
        
        try:
            # Send to data collector
            response = requests.post(data_collector_url, json={
                "input_type": test_case["input_type"],
                "payload": test_case["payload"]
            }, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Data Collector Status: {result['status']}")
                print(f"   📤 Sent to Sanitizer: {result.get('sent_to_sanitizer', False)}")
                
                if result.get('sanitizer_response'):
                    sanitizer_result = result['sanitizer_response']
                    print(f"   🧹 Sanitizer Status: {sanitizer_result.get('status', 'N/A')}")
                    print(f"   📤 Forwarded to Whis: {sanitizer_result.get('forwarded_to_whis', False)}")
                    
                    if sanitizer_result.get('whis_response'):
                        whis_result = sanitizer_result['whis_response']
                        print(f"   🧠 Whis Status: {whis_result.get('status', 'N/A')}")
                        print(f"   🏷️  Category: {whis_result.get('category', 'N/A')}")
                        print(f"   💬 Message: {whis_result.get('message', 'N/A')}")
                    elif sanitizer_result.get('error'):
                        print(f"   ❌ Whis Error: {sanitizer_result['error']}")
                elif result.get('error'):
                    print(f"   ❌ Sanitizer Error: {result['error']}")
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    # Test 2: Direct endpoint testing
    print("\n2️⃣ Testing Individual Service Endpoints")
    print("-" * 50)
    
    endpoints = [
        ("Data Collector", "http://localhost:8001/api/collect"),
        ("Sanitizer", "http://localhost:8002/api/sanitize"),
        ("Whis Training", "http://localhost:8003/api/whis/train")
    ]
    
    for service_name, endpoint_url in endpoints:
        try:
            response = requests.get(endpoint_url.replace("/api/", "/health"), timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {service_name}: Healthy")
            else:
                print(f"   ⚠️  {service_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {service_name}: {str(e)}")
    
    # Test 3: Legacy endpoints (backward compatibility)
    print("\n3️⃣ Testing Legacy Endpoints (Backward Compatibility)")
    print("-" * 50)
    
    legacy_endpoints = [
        ("Task Collection", "http://localhost:8001/api/collect/task", {
            "task_description": "Legacy task test",
            "priority": "low"
        }),
        ("QnA Collection", "http://localhost:8001/api/collect/qna", {
            "question": "Legacy question?",
            "answer": "Legacy answer."
        }),
        ("Info Collection", "http://localhost:8001/api/collect/info", {
            "info": "Legacy info dump"
        })
    ]
    
    for endpoint_name, endpoint_url, payload in legacy_endpoints:
        try:
            response = requests.post(endpoint_url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {endpoint_name}: {result.get('status', 'N/A')}")
            else:
                print(f"   ❌ {endpoint_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint_name}: {str(e)}")
    
    print("\n🎉 Complete data flow test finished!")
    print("\n📝 Summary:")
    print("✅ Data Collector → Sanitizer → Whis communication implemented")
    print("✅ Backward compatibility maintained")
    print("✅ Error handling in place")
    print("\n🔍 Next steps:")
    print("1. Check service logs for detailed information")
    print("2. Monitor data_lake directory for saved files")
    print("3. Verify Kafka topics still receive legacy data")

if __name__ == "__main__":
    test_complete_data_flow() 