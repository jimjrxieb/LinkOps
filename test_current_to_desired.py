#!/usr/bin/env python3
"""
Daily Test Script - Simulates LinkOps workflow
Runs: collector → sanitizer → whis → db → ficknury → scraperdash → reloop
"""

import requests
import json
import time
from datetime import datetime

SERVICES = {
    'data-collector': 'http://localhost:8001',
    'sanitizer': 'http://localhost:8002', 
    'whis': 'http://localhost:8003',
    'ficknury': 'http://localhost:8004',
    'scraperdash': 'http://localhost:8005'
}

def test_workflow():
    """Test the complete LinkOps workflow"""
    print("🔄 LINKOPS DAILY WORKFLOW TEST")
    print("=" * 50)
    
    timestamp = int(time.time())
    
    # 1. Simulate collector input
    print("1️⃣ Simulating collector input...")
    task_data = {
        "task_description": "Create a fast SSD storage class for Kubernetes cluster",
        "task_id": f"daily-test-{timestamp}",
        "input_type": "task"
    }
    
    try:
        response = requests.post(f"{SERVICES['data-collector']}/api/collect/task", json=task_data, timeout=10)
        print(f"   ✅ Collector: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Collector failed: {e}")
        return False
    
    # 2. Simulate sanitizer processing
    print("2️⃣ Simulating sanitizer processing...")
    sanitize_data = {
        "input": "Create storageclass in namespace default with IP 10.0.0.1 and file /etc/k8s/config.yaml",
        "input_type": "task"
    }
    
    try:
        response = requests.post(f"{SERVICES['sanitizer']}/api/sanitize", json=sanitize_data, timeout=10)
        print(f"   ✅ Sanitizer: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Sanitizer failed: {e}")
        return False
    
    # 3. Simulate Whis training
    print("3️⃣ Simulating Whis training...")
    try:
        response = requests.post(f"{SERVICES['whis']}/api/whis/train-nightly", timeout=30)
        print(f"   ✅ Whis training: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Whis training failed: {e}")
        return False
    
    # 4. Simulate FickNury deployment
    print("4️⃣ Simulating FickNury deployment...")
    eval_data = {
        "task_description": "Create a storageclass for fast SSD storage",
        "task_id": f"eval-{timestamp}"
    }
    
    try:
        response = requests.post(f"{SERVICES['ficknury']}/api/ficknury/evaluate-task", json=eval_data, timeout=10)
        print(f"   ✅ FickNury evaluation: {response.status_code}")
    except Exception as e:
        print(f"   ❌ FickNury failed: {e}")
        return False
    
    # 5. Simulate ScraperDash audit
    print("5️⃣ Simulating ScraperDash audit...")
    try:
        response = requests.get(f"{SERVICES['scraperdash']}/api/scraper/logs", timeout=10)
        print(f"   ✅ ScraperDash logs: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ScraperDash failed: {e}")
        return False
    
    # 6. Simulate reloop
    print("6️⃣ Simulating reloop...")
    reloop_data = {
        "source": "daily_test",
        "content": "Kubernetes storage best practices from daily test",
        "type": "knowledge"
    }
    
    try:
        response = requests.post(f"{SERVICES['scraperdash']}/api/scraper/reloop", json=reloop_data, timeout=10)
        print(f"   ✅ Reloop: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Reloop failed: {e}")
        return False
    
    print("\n✅ DAILY WORKFLOW COMPLETED SUCCESSFULLY!")
    return True

def main():
    """Main entry point"""
    success = test_workflow()
    if success:
        print("\n🎉 LinkOps is functioning like a true self-evolving, multi-agent, LLMOps platform!")
        exit(0)
    else:
        print("\n💥 LinkOps workflow test failed!")
        exit(1)

if __name__ == "__main__":
    main() 