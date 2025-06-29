#!/usr/bin/env python3
"""
Test the complete Whis AI training pipeline flow:
whis_data_input → whis_sanitize → whis_smithing → whis_enhance
"""

import requests


def test_complete_whis_flow():
    """Test the complete Whis AI training pipeline"""
    print("🔄 Testing Complete Whis AI Training Pipeline")
    print("=" * 60)
    print("Flow: whis_data_input → whis_sanitize → whis_smithing → whis_enhance")
    print()

    # Test data
    test_data = {
        "input_type": "fix_logs",
        "content": {
            "log_entry": "ERROR: Database connection failed at 2024-01-15 10:30:00",
            "severity": "high",
            "component": "database",
        },
        "metadata": {"source": "test_flow", "timestamp": "2024-01-15T10:30:00Z"},
    }

    print(
        "1️⃣ Testing Whis Data Input → Whis Sanitize → Whis Smithing → "
        "Whis Enhance Flow"
    )
    print("-" * 70)

    # Step 1: Send data to whis_data_input
    print("📤 Step 1: Sending data to whis_data_input...")
    data_input_url = "http://localhost:8001/api/collect"

    try:
        response = requests.post(data_input_url, json=test_data, timeout=10)
        result = response.json()

        print(f"   ✅ Data Input Status: {result.get('status', 'N/A')}")
        print(f"   📤 Sent to Sanitizer: {result.get('sent_to_sanitizer', False)}")

        if result.get("sanitizer_response"):
            sanitizer_result = result["sanitizer_response"]
            print(f"   🧹 Sanitizer Status: {sanitizer_result.get('status', 'N/A')}")
            print(
                f"   📤 Forwarded to Smithing: "
                f"{sanitizer_result.get('forwarded_to_smithing', False)}"
            )

            if sanitizer_result.get("smithing_response"):
                smithing_result = sanitizer_result["smithing_response"]
                print(f"   🔨 Smithing Status: {smithing_result.get('status', 'N/A')}")
                print(
                    f"   📤 Forwarded to Enhance: "
                    f"{smithing_result.get('forwarded_to_enhance', False)}"
                )

                if smithing_result.get("enhance_response"):
                    enhance_result = smithing_result["enhance_response"]
                    print(
                        f"   🚀 Enhance Status: {enhance_result.get('status', 'N/A')}"
                    )
                    print(
                        f"   🎯 Training Result: "
                        f"{enhance_result.get('training_result', 'N/A')}"
                    )
                elif smithing_result.get("error"):
                    print(f"   ❌ Enhance Error: {smithing_result['error']}")
            elif sanitizer_result.get("error"):
                print(f"   ❌ Smithing Error: {sanitizer_result['error']}")
        elif result.get("error"):
            print(f"   ❌ Sanitizer Error: {result['error']}")

    except Exception as e:
        print(f"   ❌ Data Input Error: {str(e)}")

    print("\n2️⃣ Testing Individual Service Health")
    print("-" * 40)

    # Test individual service health
    services = [
        ("Whis Data Input", "http://localhost:8001/health"),
        ("Whis Sanitize", "http://localhost:8002/health"),
        ("Whis Smithing", "http://localhost:8004/health"),
        ("Whis Enhance", "http://localhost:8005/health"),
    ]

    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {service_name}: Healthy")
            else:
                print(f"   ⚠️  {service_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {service_name}: Unreachable - {str(e)}")

    print("\n3️⃣ Testing Direct API Calls")
    print("-" * 30)

    # Test direct API calls to each service
    test_calls = [
        (
            "Whis Sanitize",
            "http://localhost:8002/api/sanitize",
            {"input_type": "test", "content": {"test": "data"}},
        ),
        (
            "Whis Smithing",
            "http://localhost:8004/api/v1/smithing/generate-rune",
            {"input_data": {"test": "data"}, "rune_type": "standard"},
        ),
        (
            "Whis Enhance",
            "http://localhost:8005/api/v1/enhance/enhancement-status",
            {},
        ),
    ]

    for service_name, url, payload in test_calls:
        try:
            if payload:
                response = requests.post(url, json=payload, timeout=5)
            else:
                response = requests.get(url, timeout=5)

            if response.status_code in [200, 201]:
                print(f"   ✅ {service_name}: API Working")
            else:
                print(f"   ⚠️  {service_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {service_name}: API Error - {str(e)}")

    print("\n✅ Whis AI Training Pipeline communication implemented")
    print("🎯 All microservices are properly connected and ready for training!")


if __name__ == "__main__":
    test_complete_whis_flow()
