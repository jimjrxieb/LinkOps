#!/usr/bin/env python3
"""
Test script for ARISE activation functionality
Tests the Shadow Army activation endpoint
"""

import requests
import json
import time
from datetime import datetime

def test_arise_activation():
    """Test the ARISE activation endpoint"""
    
    print("🔥 Testing ARISE Activation...")
    print("=" * 50)
    
    # Test James activation endpoint
    try:
        print("1. Testing James activation endpoint...")
        response = requests.post(
            "http://localhost:8002/api/james/activate",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Activation successful!")
            print(f"Message: {data.get('message', 'No message')}")
            print(f"Status: {data.get('status', 'Unknown')}")
            print(f"Timestamp: {data.get('timestamp', 'Unknown')}")
            
            # Display shadow agents status
            shadow_agents = data.get('shadow_agents', [])
            if shadow_agents:
                print("\nShadow Agents Status:")
                for agent in shadow_agents:
                    status_icon = "🟢" if agent['status'] == 'online' else "🔴"
                    print(f"  {status_icon} {agent['name']} - {agent['role']}")
            
            # Display activation steps
            activation_steps = data.get('activation_steps', [])
            if activation_steps:
                print("\nActivation Steps:")
                for i, step in enumerate(activation_steps, 1):
                    print(f"  {i}. {step}")
            
        else:
            print(f"❌ Activation failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to James service. Is it running?")
        print("   Start with: docker-compose up james_logic")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_health_checks():
    """Test health checks for all shadow agents"""
    
    print("\n🏥 Testing Shadow Agents Health...")
    print("=" * 50)
    
    agents = [
        ("James", "http://localhost:8002/health"),
        ("Whis Logic", "http://localhost:8001/health"),
        ("Whis Data Input", "http://localhost:8004/health"),
        ("Whis Sanitize", "http://localhost:8003/health"),
        ("Whis Smithing", "http://localhost:8005/health"),
        ("Whis Enhance", "http://localhost:8006/health"),
        ("Ficknury", "http://localhost:8007/health"),
        ("WebScraper", "http://localhost:8009/health"),
        ("AuditGuard", "http://localhost:8008/health"),
        ("Igris", "http://localhost:8005/health"),
        ("Katie", "http://localhost:8006/health"),
    ]
    
    for name, url in agents:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Online")
            else:
                print(f"⚠️  {name}: Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"🔴 {name}: Offline")
        except requests.exceptions.Timeout:
            print(f"⏰ {name}: Timeout")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

def main():
    """Main test function"""
    print("🔥 ARISE - Shadow Army Activation Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test activation
    test_arise_activation()
    
    # Test health checks
    test_health_checks()
    
    print("\n" + "=" * 60)
    print("🔥 ARISE test completed!")
    print("If all tests pass, your Shadow Army is ready for deployment.")

if __name__ == "__main__":
    main() 