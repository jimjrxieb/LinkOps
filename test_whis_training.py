#!/usr/bin/env python3
"""
Test script for Whis Training System
Demonstrates both manual training and nightly batch processing
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_manual_training():
    """Test manual training endpoint"""
    print("🎓 Testing Manual Training...")
    
    payload = {
        "task_id": "test/manual-training",
        "content": "This is a test manual training entry for Whis. It demonstrates how to manually add knowledge to Whis's orb.",
        "source": "manual"
    }
    
    response = requests.post(f"{BASE_URL}/api/whis/train", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Manual training successful!")
        print(f"   Rune ID: {data.get('rune_id')}")
        print(f"   Task ID: {data.get('task_id')}")
        print(f"   Status: {data.get('status')}")
    else:
        print(f"❌ Manual training failed: {response.status_code}")
        print(f"   Error: {response.text}")

def test_nightly_training():
    """Test nightly training endpoint"""
    print("\n🌙 Testing Night Training...")
    
    response = requests.post(f"{BASE_URL}/api/whis/train-nightly")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Night training successful!")
        print(f"   Tasks Processed: {data.get('tasks_processed')}")
        print(f"   Runes Created: {data.get('runes_created')}")
        print(f"   Orbs Updated: {', '.join(data.get('orbs_updated', []))}")
        print(f"   Repeated Tasks: {len(data.get('repeated_tasks', []))}")
        
        if data.get('repeated_tasks'):
            print("   Repeated Task Details:")
            for task in data['repeated_tasks']:
                print(f"     - {task['agent']}: {task['task_id']} (count: {task['count']})")
    else:
        print(f"❌ Night training failed: {response.status_code}")
        print(f"   Error: {response.text}")

def test_training_stats():
    """Test training statistics endpoint"""
    print("\n📊 Testing Training Statistics...")
    
    response = requests.get(f"{BASE_URL}/api/whis/training-stats")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Training stats retrieved!")
        print(f"   Logs Today: {data.get('logs_today')}")
        print(f"   Agent Breakdown: {data.get('agent_breakdown')}")
        print(f"   Orb Rune Counts: {data.get('orb_rune_counts')}")
    else:
        print(f"❌ Training stats failed: {response.status_code}")
        print(f"   Error: {response.text}")

def test_whis_stats():
    """Test Whis statistics endpoint"""
    print("\n🧠 Testing Whis Statistics...")
    
    response = requests.get(f"{BASE_URL}/api/whis/stats")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Whis stats retrieved!")
        print(f"   Orb Name: {data.get('orb_name')}")
        print(f"   Total Runes: {data.get('total_runes')}")
        print(f"   Total Logs: {data.get('total_logs')}")
        print(f"   Recent Runes: {data.get('recent_runes')}")
        print(f"   Recent Logs: {data.get('recent_logs')}")
    else:
        print(f"❌ Whis stats failed: {response.status_code}")
        print(f"   Error: {response.text}")

def test_digest():
    """Test daily digest endpoint"""
    print("\n📋 Testing Daily Digest...")
    
    response = requests.get(f"{BASE_URL}/api/whis/digest")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Daily digest retrieved!")
        print(f"   Orbs Updated: {', '.join(data.get('orbs_updated', []))}")
        print(f"   Runes Created: {data.get('runes_created')}")
        print(f"   Logs Processed: {data.get('logs_processed')}")
    else:
        print(f"❌ Daily digest failed: {response.status_code}")
        print(f"   Error: {response.text}")

def main():
    """Run all tests"""
    print("🧠 Whis Training System Test Suite")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Test all endpoints
        test_manual_training()
        test_nightly_training()
        test_training_stats()
        test_whis_stats()
        test_digest()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("\n🎯 Next Steps:")
        print("1. Visit http://localhost:8000/gui/whis-training for the web interface")
        print("2. Use the '🎓 Train Now' button for manual training")
        print("3. Use the '🌙 Night Training' button for batch processing")
        print("4. Check the '📊 Training Stats' button for statistics")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main() 