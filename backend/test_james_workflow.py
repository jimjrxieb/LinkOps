#!/usr/bin/env python3
"""
Test script for LinkOps James Workflow System
Demonstrates all the main functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Test root endpoint"""
    print("🏠 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_task():
    """Test task creation"""
    print("📝 Testing task creation...")
    
    task_data = {
        "task_input": "How do I restart a pod in Kubernetes?",
        "origin": "manager",
        "priority": "medium",
        "tags": ["kubernetes", "troubleshooting"]
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    task_id = result.get("task_id")
    print(f"Created task ID: {task_id}")
    print()
    
    return task_id

def test_get_tasks():
    """Test getting all tasks"""
    print("📋 Testing get all tasks...")
    response = requests.get(f"{BASE_URL}/api/tasks")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {result.get('count', 0)} tasks")
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_task_analysis(task_id):
    """Test task analysis"""
    print(f"🔍 Testing task analysis for {task_id}...")
    response = requests.get(f"{BASE_URL}/api/tasks/{task_id}/analysis")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_james_solve(task_id):
    """Test James solving a task"""
    print(f"🧠 Testing James solve for task {task_id}...")
    response = requests.post(f"{BASE_URL}/api/tasks/{task_id}/james/solve")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_agent_dispatch(task_id):
    """Test agent dispatch"""
    print(f"⚡ Testing agent dispatch for task {task_id}...")
    
    dispatch_data = {
        "task_id": task_id,
        "agent_id": "katie"
    }
    
    response = requests.post(f"{BASE_URL}/api/tasks/{task_id}/agent-dispatch", json=dispatch_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_chat():
    """Test chat with James"""
    print("💬 Testing chat with James...")
    
    chat_data = {
        "message": "What is the best way to deploy a microservice?",
        "context": "deployment"
    }
    
    response = requests.post(f"{BASE_URL}/api/chat", json=chat_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_qa_training():
    """Test Q&A training"""
    print("🎓 Testing Q&A training...")
    
    qa_data = {
        "task_id": "training-001",
        "question": "How do you scale a Kubernetes deployment?",
        "answer": "Use kubectl scale deployment <name> --replicas=<number>",
        "category": "kubernetes"
    }
    
    response = requests.post(f"{BASE_URL}/api/qa", json=qa_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_info_dump():
    """Test info dump"""
    print("📚 Testing info dump...")
    
    info_data = {
        "content": "Kubernetes best practices: Always set resource limits and requests for your pods. Use namespaces to organize your resources. Implement health checks with readiness and liveness probes.",
        "source": "blog",
        "category": "kubernetes"
    }
    
    response = requests.post(f"{BASE_URL}/api/info-dump", json=info_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def test_chat_history():
    """Test chat history"""
    print("📜 Testing chat history...")
    response = requests.get(f"{BASE_URL}/api/chat/history")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting LinkOps James Workflow Tests")
    print("=" * 50)
    
    try:
        # Test basic endpoints
        test_health()
        test_root()
        
        # Test task workflow
        task_id = test_create_task()
        test_get_tasks()
        test_task_analysis(task_id)
        
        # Test James solutions
        test_james_solve(task_id)
        test_agent_dispatch(task_id)
        
        # Test other features
        test_chat()
        test_qa_training()
        test_info_dump()
        test_chat_history()
        
        print("✅ All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main() 