#!/usr/bin/env python3
"""
Quick Health Check for LinkOps Services
"""

import requests
import psycopg
import os

SERVICES = {
    'data-collector': 'http://localhost:8001',
    'sanitizer': 'http://localhost:8002', 
    'whis': 'http://localhost:8003',
    'ficknury': 'http://localhost:8004',
    'scraperdash': 'http://localhost:8005',
    'james': 'http://localhost:8006'
}

DB_URL = "postgresql://linkops:secret@localhost:5432/linkops_core"

def check_service(service_name, base_url):
    """Check if a service is responding"""
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        return response.status_code in [200, 404]  # 404 is OK for root endpoint
    except:
        return False

def check_database():
    """Check database connection"""
    try:
        conn = psycopg.connect(DB_URL)
        conn.close()
        return True
    except:
        return False

def main():
    print("🏥 LINKOPS HEALTH CHECK")
    print("=" * 30)
    
    all_healthy = True
    
    # Check services
    for service_name, base_url in SERVICES.items():
        healthy = check_service(service_name, base_url)
        status = "✅" if healthy else "❌"
        print(f"{status} {service_name}: {base_url}")
        if not healthy:
            all_healthy = False
    
    # Check database
    db_healthy = check_database()
    status = "✅" if db_healthy else "❌"
    print(f"{status} database: {DB_URL}")
    if not db_healthy:
        all_healthy = False
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    key_healthy = bool(api_key and api_key.startswith("sk-"))
    status = "✅" if key_healthy else "❌"
    print(f"{status} OpenAI API Key: {'Configured' if key_healthy else 'Missing'}")
    if not key_healthy:
        all_healthy = False
    
    print("\n" + "=" * 30)
    if all_healthy:
        print("🎉 ALL SYSTEMS HEALTHY!")
        exit(0)
    else:
        print("💥 SOME SYSTEMS UNHEALTHY!")
        exit(1)

if __name__ == "__main__":
    main() 