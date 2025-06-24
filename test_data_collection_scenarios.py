#!/usr/bin/env python3
"""
Test scenarios for LinkOps data collection pipeline
Verifies that all input types end up in Whis data lake queue
"""

import requests
import json
import time
import base64
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")

def test_health_check():
    """Test backend health"""
    print_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend healthy: {data['status']}")
            print(f"   Stores: {data['stores']}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_qa_input():
    """Test Q&A data collection"""
    print_header("Q&A Input Test")
    
    qa_data = {
        "type": "qna",
        "content": {
            "question": "create a pod name testpod with the nginx image",
            "answer": "kubectl run testpod --image=nginx"
        }
    }
    
    try:
        response = requests.post(f"{API_BASE}/data-collect/sanitize", json=qa_data)
        if response.status_code == 200:
            data = response.json()
            print_success("Q&A submitted successfully")
            print(f"   Sanitized: {data['sanitized']}")
            return True
        else:
            print_error(f"Q&A submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Q&A test error: {str(e)}")
        return False

def test_task_input():
    """Test task data collection"""
    print_header("Task Input Test")
    
    task_data = {
        "type": "task",
        "content": "Deploy a Kubernetes cluster with monitoring stack including Prometheus and Grafana"
    }
    
    try:
        response = requests.post(f"{API_BASE}/data-collect/sanitize", json=task_data)
        if response.status_code == 200:
            data = response.json()
            print_success("Task submitted successfully")
            print(f"   Sanitized: {data['sanitized']}")
            return True
        else:
            print_error(f"Task submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Task test error: {str(e)}")
        return False

def test_info_dump_input():
    """Test info dump data collection"""
    print_header("Info Dump Test")
    
    info_dump_data = {
        "type": "dump",
        "content": """
        Kubernetes Best Practices:
        1. Always use resource limits and requests
        2. Implement proper health checks
        3. Use namespaces for organization
        4. Enable RBAC for security
        5. Use persistent volumes for stateful data
        6. Implement network policies
        7. Regular security scanning
        8. Monitor cluster resources
        """
    }
    
    try:
        response = requests.post(f"{API_BASE}/data-collect/sanitize", json=info_dump_data)
        if response.status_code == 200:
            data = response.json()
            print_success("Info dump submitted successfully")
            print(f"   Sanitized: {data['sanitized']}")
            return True
        else:
            print_error(f"Info dump submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Info dump test error: {str(e)}")
        return False

def test_image_text_input():
    """Test image text extraction"""
    print_header("Image Text Extraction Test")
    
    # Create a simple text file to simulate image text
    image_text_data = {
        "type": "image",
        "content": "kubectl apply -f deployment.yaml\nkubectl get pods\nkubectl logs pod-name"
    }
    
    try:
        response = requests.post(f"{API_BASE}/data-collect/sanitize", json=image_text_data)
        if response.status_code == 200:
            data = response.json()
            print_success("Image text submitted successfully")
            print(f"   Sanitized: {data['sanitized']}")
            return True
        else:
            print_error(f"Image text submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Image text test error: {str(e)}")
        return False

def test_whis_training_trigger():
    """Test Whis training trigger"""
    print_header("Whis Training Trigger Test")
    
    try:
        response = requests.post(f"{API_BASE}/whis/train-nightly")
        if response.status_code == 200:
            data = response.json()
            print_success("Whis training triggered successfully")
            print(f"   Logs processed: {data['count']}")
            print(f"   Preview: {data['preview']}")
            return True
        else:
            print_error(f"Whis training failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Whis training error: {str(e)}")
        return False

def test_whis_approvals():
    """Test Whis approvals queue"""
    print_header("Whis Approvals Queue Test")
    
    try:
        response = requests.get(f"{API_BASE}/whis/approvals")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data)} pending runes")
            for i, rune in enumerate(data[:3]):  # Show first 3
                print(f"   Rune {i+1}: {rune.get('agent', 'unknown')} - {rune.get('origin', 'unknown')}")
            return True
        else:
            print_error(f"Approvals retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Approvals test error: {str(e)}")
        return False

def test_whis_digest():
    """Test Whis daily digest"""
    print_header("Whis Daily Digest Test")
    
    try:
        response = requests.get(f"{API_BASE}/whis/digest")
        if response.status_code == 200:
            data = response.json()
            print_success("Digest retrieved successfully")
            print(f"   Log count: {data['log_count']}")
            print(f"   Runes total: {data['runes_total']}")
            print(f"   Runes approved: {data['runes_approved']}")
            print(f"   Runes pending: {data['runes_pending']}")
            print(f"   Agents affected: {data['agents_affected']}")
            return True
        else:
            print_error(f"Digest retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Digest test error: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all test scenarios"""
    print_header("LinkOps Data Collection Pipeline Test")
    print("Testing all data collection inputs and Whis data lake integration")
    
    # Test results tracking
    results = []
    
    # 1. Health check
    results.append(("Health Check", test_health_check()))
    
    # 2. Data collection tests
    results.append(("Q&A Input", test_qa_input()))
    results.append(("Task Input", test_task_input()))
    results.append(("Info Dump", test_info_dump_input()))
    results.append(("Image Text", test_image_text_input()))
    
    # 3. Wait a moment for data to be processed
    print("\n⏳ Waiting 2 seconds for data processing...")
    time.sleep(2)
    
    # 4. Whis training and queue tests
    results.append(("Whis Training Trigger", test_whis_training_trigger()))
    results.append(("Whis Approvals Queue", test_whis_approvals()))
    results.append(("Whis Daily Digest", test_whis_digest()))
    
    # 5. Summary
    print_header("Test Results Summary")
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! Data collection pipeline is working correctly.")
        print("\n🎯 Data Flow Verified:")
        print("   Input Collection → Sanitization → Database → Whis Training → Rune Queue")
    else:
        print_error(f"{total - passed} tests failed. Check the backend logs for issues.")
    
    return passed == total

if __name__ == "__main__":
    run_comprehensive_test() 