#!/usr/bin/env python3
"""
Health check script for LinkOps services
"""

import requests
import time
from typing import Dict, List

# Updated service URLs with new names
SERVICES = {
    "whis_data_input": "http://localhost:8001",
    "whis_sanitize": "http://localhost:8002",
    "whis": "http://localhost:8003",
    "whis_smithing": "http://localhost:8004",
    "whis_enhance": "http://localhost:8005",
    "james": "http://localhost:8006",
    "igris": "http://localhost:8007",
    "katie": "http://localhost:8008",
    "auditguard": "http://localhost:8009",
    "ficknury": "http://localhost:8010",
    "scraperdash": "http://localhost:8011",
}


def check_service_health(service_name: str, base_url: str) -> Dict:
    """Check health of a single service"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            return {
                "service": service_name,
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "data": response.json(),
            }
        else:
            return {
                "service": service_name,
                "status": "unhealthy",
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
            }
    except requests.exceptions.RequestException as e:
        return {"service": service_name, "status": "unreachable", "error": str(e)}


def main():
    """Main health check function"""
    print("🏥 LinkOps Services Health Check")
    print("=" * 50)

    results = []
    for service_name, base_url in SERVICES.items():
        print(f"Checking {service_name}...", end=" ")
        result = check_service_health(service_name, base_url)
        results.append(result)

        if result["status"] == "healthy":
            print("✅")
        elif result["status"] == "unhealthy":
            print("⚠️")
        else:
            print("❌")

    print("\n📊 Health Summary:")
    print("-" * 30)

    healthy_count = sum(1 for r in results if r["status"] == "healthy")
    total_count = len(results)

    for result in results:
        status_icon = (
            "✅"
            if result["status"] == "healthy"
            else "⚠️" if result["status"] == "unhealthy" else "❌"
        )
        print(f"{status_icon} {result['service']}: {result['status']}")

    print(f"\nOverall: {healthy_count}/{total_count} services healthy")

    if healthy_count == total_count:
        print("🎉 All services are healthy!")
        return 0
    else:
        print("⚠️  Some services are not healthy")
        return 1


if __name__ == "__main__":
    exit(main())
