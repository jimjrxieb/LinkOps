#!/usr/bin/env python3
"""
Test script to verify GUI setup and functionality
"""

import requests
import sys
import os

def test_gui_endpoints():
    """Test GUI endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing LinkOps Core GUI")
    print("=" * 40)
    
    endpoints = [
        ("/gui", "Dashboard"),
        ("/gui/orbs", "Orbs Page"),
        ("/gui/logs", "Logs Page"),
        ("/gui/whis", "Whis Upload Page"),
        ("/health", "Health Check"),
        ("/docs", "API Documentation")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code}")
            else:
                print(f"⚠️  {name}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection failed")
            print("💡 Start the server with: uvicorn core.api.main:app --reload")
            return False
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    return True

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    print("\n🔌 Testing API Endpoints")
    print("=" * 40)
    
    # Test creating a log
    try:
        log_data = {
            "agent": "test-agent",
            "task_id": "test-task",
            "action": "GUI test",
            "result": "Testing GUI functionality"
        }
        response = requests.post(f"{base_url}/api/logs", json=log_data, timeout=5)
        if response.status_code == 200:
            print("✅ Create Log: Success")
        else:
            print(f"⚠️  Create Log: {response.status_code}")
    except Exception as e:
        print(f"❌ Create Log: {e}")
    
    # Test creating an orb
    try:
        orb_data = {
            "name": "Test Orb",
            "description": "Test orb created via GUI test",
            "category": "Test"
        }
        response = requests.post(f"{base_url}/api/orbs", json=orb_data, timeout=5)
        if response.status_code == 200:
            print("✅ Create Orb: Success")
        else:
            print(f"⚠️  Create Orb: {response.status_code}")
    except Exception as e:
        print(f"❌ Create Orb: {e}")
    
    # Test getting orbs
    try:
        response = requests.get(f"{base_url}/api/orbs", timeout=5)
        if response.status_code == 200:
            orbs = response.json()
            print(f"✅ Get Orbs: Found {len(orbs)} orbs")
        else:
            print(f"⚠️  Get Orbs: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Orbs: {e}")

def main():
    """Main test function"""
    print("🚀 LinkOps Core GUI Test")
    print("=" * 50)
    
    # Test GUI endpoints
    if not test_gui_endpoints():
        return False
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("🎉 GUI test completed!")
    print("\nNext steps:")
    print("1. Open http://localhost:8000/gui in your browser")
    print("2. Try uploading a screenshot via the Whis interface")
    print("3. Check the logs and orbs pages")
    print("4. Explore the API documentation at /docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 