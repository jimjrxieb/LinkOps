#!/usr/bin/env python3
"""
LinkOps Microservices Test & Integration Harness
Run this checklist in Cursor or CI after major updates or before deployment.
"""

import requests
import json
import time
import subprocess
import os
import psycopg
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration
SERVICES = {
    'data-collector': 'http://localhost:8001',
    'sanitizer': 'http://localhost:8002', 
    'whis': 'http://localhost:8003',
    'ficknury': 'http://localhost:8004',
    'scraperdash': 'http://localhost:8005',
    'james': 'http://localhost:8006',
    'db': 'localhost:5432'
}

DB_URL = "postgresql://linkops:secret@localhost:5432/linkops_core"

class TestResult:
    def __init__(self, test_name: str, success: bool, message: str = "", data: dict = None):
        self.test_name = test_name
        self.success = success
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()

    def __str__(self):
        status = "✅ PASS" if self.success else "❌ FAIL"
        return f"{status} {self.test_name}: {self.message}"

class LinkOpsTestHarness:
    def __init__(self):
        self.results: List[TestResult] = []
        self.test_data = {}
        
    def log_result(self, test_name: str, success: bool, message: str = "", data: dict = None):
        result = TestResult(test_name, success, message, data)
        self.results.append(result)
        print(result)
        return result

    def test_service_health(self, service_name: str, base_url: str) -> bool:
        """Test if a microservice is responding"""
        try:
            if service_name == 'db':
                # Test PostgreSQL connection
                conn = psycopg.connect(DB_URL)
                conn.close()
                return True
            else:
                # Test HTTP endpoint
                response = requests.get(f"{base_url}/", timeout=5)
                return response.status_code in [200, 404]  # 404 is OK for root endpoint
        except Exception as e:
            return False

    def test_1_microservices_up_and_healthy(self):
        """1️⃣ Test all microservices are running and healthy"""
        print("\n🔧 1️⃣ MICROSERVICES UP & HEALTHY")
        print("=" * 50)
        
        all_healthy = True
        
        for service_name, base_url in SERVICES.items():
            healthy = self.test_service_health(service_name, base_url)
            self.log_result(
                f"Service {service_name} healthy",
                healthy,
                f"Response from {base_url}" if healthy else f"Failed to connect to {base_url}"
            )
            if not healthy:
                all_healthy = False
        
        # Test .env file
        env_key = os.getenv("OPENAI_API_KEY")
        self.log_result(
            "OpenAI API Key configured",
            bool(env_key and env_key.startswith("sk-")),
            "API key found" if env_key else "No API key found"
        )
        
        return all_healthy

    def test_2_data_collector(self):
        """2️⃣ Test Data Collector functionality"""
        print("\n🧩 2️⃣ DATA COLLECTOR TEST")
        print("=" * 50)
        
        base_url = SERVICES['data-collector']
        
        # Test task collection
        task_data = {
            "task_description": "Create a storageclass for fast SSD storage",
            "task_id": f"test-{int(time.time())}",
            "input_type": "task"
        }
        
        try:
            response = requests.post(f"{base_url}/api/collect/task", json=task_data, timeout=10)
            success = response.status_code == 200
            self.log_result(
                "POST /api/collect/task",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("POST /api/collect/task", False, f"Exception: {str(e)}")
        
        # Test Q&A collection
        qna_data = {
            "question": "How do I create a Kubernetes storage class?",
            "answer": "Use kubectl create -f storageclass.yaml",
            "task_id": f"qna-{int(time.time())}"
        }
        
        try:
            response = requests.post(f"{base_url}/api/collect/qna", json=qna_data, timeout=10)
            success = response.status_code == 200
            self.log_result(
                "POST /api/collect/qna",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("POST /api/collect/qna", False, f"Exception: {str(e)}")

    def test_3_sanitizer(self):
        """3️⃣ Test Sanitizer functionality"""
        print("\n🧼 3️⃣ SANITIZER TEST")
        print("=" * 50)
        
        base_url = SERVICES['sanitizer']
        
        # Test sanitization
        test_data = {
            "input": "Create storageclass in namespace default with IP 192.168.1.100 and file /etc/kubernetes/config.yaml",
            "input_type": "task"
        }
        
        try:
            response = requests.post(f"{base_url}/api/sanitize", json=test_data, timeout=10)
            success = response.status_code == 200
            if success:
                sanitized = response.json()
                contains_placeholders = any(placeholder in sanitized.get('sanitized_input', '') 
                                          for placeholder in ['<IP_ADDR>', '<FILENAME>', '<NAMESPACE>'])
                self.log_result(
                    "POST /api/sanitize",
                    contains_placeholders,
                    f"Sanitized: {sanitized.get('sanitized_input', '')[:100]}..."
                )
            else:
                self.log_result("POST /api/sanitize", False, f"Failed: {response.text}")
        except Exception as e:
            self.log_result("POST /api/sanitize", False, f"Exception: {str(e)}")

    def test_4_whis_functionality(self):
        """4️⃣ Test Whis functionality"""
        print("\n🧠 4️⃣ WHIS FUNCTIONALITY")
        print("=" * 50)
        
        base_url = SERVICES['whis']
        
        # Test nightly training
        try:
            response = requests.post(f"{base_url}/api/whis/train-nightly", timeout=30)
            success = response.status_code == 200
            self.log_result(
                "POST /api/whis/train-nightly",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("POST /api/whis/train-nightly", False, f"Exception: {str(e)}")
        
        # Test digest
        try:
            response = requests.get(f"{base_url}/api/whis/digest", timeout=10)
            success = response.status_code == 200
            self.log_result(
                "GET /api/whis/digest",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("GET /api/whis/digest", False, f"Exception: {str(e)}")
        
        # Test approvals
        try:
            response = requests.get(f"{base_url}/api/whis/approvals", timeout=10)
            success = response.status_code == 200
            self.log_result(
                "GET /api/whis/approvals",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("GET /api/whis/approvals", False, f"Exception: {str(e)}")

    def test_5_ficknury_deployment(self):
        """5️⃣ Test FickNury deployment logic"""
        print("\n🦾 5️⃣ FICKNURY DEPLOYMENT LOGIC")
        print("=" * 50)
        
        base_url = SERVICES['ficknury']
        
        # Test task evaluation
        task_data = {
            "task_description": "Create a storageclass for fast SSD storage",
            "task_id": f"eval-{int(time.time())}"
        }
        
        try:
            response = requests.post(f"{base_url}/api/ficknury/evaluate-task", json=task_data, timeout=10)
            success = response.status_code == 200
            if success:
                result = response.json()
                self.log_result(
                    "POST /api/ficknury/evaluate-task",
                    True,
                    f"Score: {result.get('score', 'N/A')}, Agent: {result.get('agent', 'N/A')}"
                )
            else:
                self.log_result("POST /api/ficknury/evaluate-task", False, f"Failed: {response.text}")
        except Exception as e:
            self.log_result("POST /api/ficknury/evaluate-task", False, f"Exception: {str(e)}")

    def test_6_scraperdash_feedback(self):
        """6️⃣ Test ScraperDash feedback loop"""
        print("\n👁️ 6️⃣ SCRAPERDASH FEEDBACK LOOP")
        print("=" * 50)
        
        base_url = SERVICES['scraperdash']
        
        # Test logs endpoint
        try:
            response = requests.get(f"{base_url}/api/scraper/logs", timeout=10)
            success = response.status_code == 200
            self.log_result(
                "GET /api/scraper/logs",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("GET /api/scraper/logs", False, f"Exception: {str(e)}")
        
        # Test agents endpoint
        try:
            response = requests.get(f"{base_url}/api/scraper/agents", timeout=10)
            success = response.status_code == 200
            self.log_result(
                "GET /api/scraper/agents",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("GET /api/scraper/agents", False, f"Exception: {str(e)}")
        
        # Test external sources
        try:
            response = requests.get(f"{base_url}/api/scraper/external", timeout=10)
            success = response.status_code == 200
            self.log_result(
                "GET /api/scraper/external",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("GET /api/scraper/external", False, f"Exception: {str(e)}")

    def test_7_james_assistant(self):
        """7️⃣ Test James Assistant"""
        print("\n👑 7️⃣ JAMES ASSISTANT")
        print("=" * 50)
        
        base_url = SERVICES['james']
        
        # Test chat
        chat_data = {
            "message": "Can you explain what a Kubernetes storage class is?"
        }
        
        try:
            response = requests.post(f"{base_url}/api/james/chat", json=chat_data, timeout=15)
            success = response.status_code == 200
            if success:
                result = response.json()
                self.log_result(
                    "POST /api/james/chat",
                    True,
                    f"Response: {result.get('james_response', '')[:100]}..."
                )
            else:
                self.log_result("POST /api/james/chat", False, f"Failed: {response.text}")
        except Exception as e:
            self.log_result("POST /api/james/chat", False, f"Exception: {str(e)}")
        
        # Test explain
        explain_data = {
            "text": "A StorageClass provides a way for administrators to describe the classes of storage they offer."
        }
        
        try:
            response = requests.post(f"{base_url}/api/james/explain", json=explain_data, timeout=15)
            success = response.status_code == 200
            if success:
                result = response.json()
                self.log_result(
                    "POST /api/james/explain",
                    True,
                    f"Explanation: {result.get('explanation', '')[:100]}..."
                )
            else:
                self.log_result("POST /api/james/explain", False, f"Failed: {response.text}")
        except Exception as e:
            self.log_result("POST /api/james/explain", False, f"Exception: {str(e)}")

    def test_8_database_microservice(self):
        """8️⃣ Test Database microservice"""
        print("\n🧠 8️⃣ DATABASE MICROSERVICE")
        print("=" * 50)
        
        try:
            conn = psycopg.connect(DB_URL)
            cur = conn.cursor()
            
            # Test table existence
            tables = ['orbs', 'runes', 'logs', 'capabilities', 'approvals']
            for table in tables:
                cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
                exists = cur.fetchone()[0]
                self.log_result(
                    f"Table {table} exists",
                    exists,
                    f"Table {'found' if exists else 'not found'}"
                )
            
            # Test data insertion (if tables exist)
            cur.execute("SELECT COUNT(*) FROM orbs")
            orb_count = cur.fetchone()[0]
            self.log_result(
                "Database accessible",
                True,
                f"Found {orb_count} orbs in database"
            )
            
            cur.close()
            conn.close()
            
        except Exception as e:
            self.log_result("Database accessible", False, f"Exception: {str(e)}")

    def test_9_mlops_feedback_loop(self):
        """9️⃣ Test MLOps feedback loop"""
        print("\n🔁 9️⃣ MLOPS FEEDBACK LOOP")
        print("=" * 50)
        
        # Test reloop functionality
        base_url = SERVICES['scraperdash']
        reloop_data = {
            "source": "test_harness",
            "content": "Kubernetes best practices for storage management",
            "type": "knowledge"
        }
        
        try:
            response = requests.post(f"{base_url}/api/scraper/reloop", json=reloop_data, timeout=10)
            success = response.status_code == 200
            self.log_result(
                "POST /api/scraper/reloop",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.text}"
            )
        except Exception as e:
            self.log_result("POST /api/scraper/reloop", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 LINKOPS MICROSERVICES TEST HARNESS")
        print("=" * 60)
        print(f"Started at: {datetime.now()}")
        print("=" * 60)
        
        # Run all test suites
        self.test_1_microservices_up_and_healthy()
        self.test_2_data_collector()
        self.test_3_sanitizer()
        self.test_4_whis_functionality()
        self.test_5_ficknury_deployment()
        self.test_6_scraperdash_feedback()
        self.test_7_james_assistant()
        self.test_8_database_microservice()
        self.test_9_mlops_feedback_loop()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if not result.success:
                    print(f"  - {result.test_name}: {result.message}")
        
        print(f"\nCompleted at: {datetime.now()}")
        
        # Return exit code for CI
        return 0 if failed_tests == 0 else 1

def main():
    """Main entry point"""
    harness = LinkOpsTestHarness()
    exit_code = harness.run_all_tests()
    exit(exit_code)

if __name__ == "__main__":
    main() 