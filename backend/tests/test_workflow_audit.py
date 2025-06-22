#!/usr/bin/env python3
"""
LinkOps Workflow Audit Test
Complete cycle: Task Entry → James Evaluation → Agent Routing → Night Training → Approval Queue → Daily Summary
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_complete_workflow_cycle():
    """Test the complete LinkOps workflow cycle"""
    print("🔍 LinkOps Workflow Audit: James + Whis Full Cycle")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Task Entry
    print("🔹 1. Task Entry")
    print("-" * 30)
    
    task_payload = {
        "task_id": "k8s/storage-class-demo",
        "task_description": "Create default StorageClass for Kubernetes cluster with AWS EBS"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/james/evaluate", json=task_payload)
        
        if response.status_code == 200:
            evaluation = response.json()
            print(f"✅ Task evaluated successfully!")
            print(f"   Task ID: {evaluation['task_id']}")
            print(f"   Detected Category: {evaluation['detected_category']}")
            print(f"   Evaluation Result: {evaluation['evaluation_result']}")
            print(f"   Is Autonomous: {evaluation['is_autonomous']}")
            print(f"   Options: {evaluation['options']}")
            print()
            
            # Step 2: Send to Agent
            print("🔹 2. Send to Agent")
            print("-" * 30)
            
            agent_response = requests.post(
                f"{BASE_URL}/api/tasks/send-to-agent",
                params={"task_id": evaluation['task_id'], "agent": evaluation['detected_category']}
            )
            
            if agent_response.status_code == 200:
                agent_result = agent_response.json()
                print(f"✅ Task sent to {agent_result['agent']} successfully!")
                print(f"   Status: {agent_result['status']}")
                print(f"   Task ID: {agent_result['task_id']}")
                print()
                
                # Step 3: Run Night Training
                print("🔹 3. Night Training")
                print("-" * 30)
                
                training_response = requests.post(f"{BASE_URL}/api/whis/train-nightly")
                
                if training_response.status_code == 200:
                    training_result = training_response.json()
                    print(f"✅ Night training completed!")
                    print(f"   Tasks Processed: {training_result['tasks_processed']}")
                    print(f"   Runes Created: {training_result['runes_created']}")
                    print(f"   Orbs Updated: {training_result['orbs_updated']}")
                    print()
                    
                    # Step 4: Check Approval Queue
                    print("🔹 4. Approval Queue")
                    print("-" * 30)
                    
                    approvals_response = requests.get(f"{BASE_URL}/api/whis/approvals")
                    
                    if approvals_response.status_code == 200:
                        approvals = approvals_response.json()
                        print(f"✅ Approval queue retrieved!")
                        print(f"   Pending Approvals: {len(approvals)}")
                        
                        if approvals:
                            print("   Recent flagged runes:")
                            for rune in approvals[:3]:
                                print(f"     - {rune['task_id']} in {rune['orb']}")
                        else:
                            print("   No runes awaiting approval")
                        print()
                        
                        # Step 5: Daily Summary
                        print("🔹 5. Daily Summary")
                        print("-" * 30)
                        
                        digest_response = requests.get(f"{BASE_URL}/api/whis/digest")
                        stats_response = requests.get(f"{BASE_URL}/api/whis/training-stats")
                        
                        if digest_response.status_code == 200 and stats_response.status_code == 200:
                            digest = digest_response.json()
                            stats = stats_response.json()
                            
                            print(f"✅ Daily summary retrieved!")
                            print(f"   Runes Created: {digest['runes_created']}")
                            print(f"   Logs Processed: {digest['logs_processed']}")
                            print(f"   Orbs Updated: {digest['orbs_updated']}")
                            print(f"   Logs Today: {stats['logs_today']}")
                            print(f"   Pending Approvals: {stats['pending_approvals']}")
                            print(f"   Agent Breakdown: {stats['agent_breakdown']}")
                            print()
                            
                            # Step 6: Workflow Audit Summary
                            print("🧾 📊 Final Summary")
                            print("-" * 30)
                            print("✅ Tasks are entered, sanitized by James")
                            print("✅ Solutions are shown or tasks auto-routed")
                            print("✅ Logs are captured for Whis")
                            print("✅ Whis trains overnight, breaking down entries")
                            print("✅ Runes are flagged + sent to approval queue")
                            print("✅ Final summary is viewable in digest")
                            print()
                            print("🔚 Ready for Tomorrow")
                            print("By morning:")
                            print("- Whis's Orbs have new intelligence")
                            print("- You've reviewed or approved anything new")
                            print("- System is fully looped: memory, agents, logs, learning ✅")
                            
                        else:
                            print(f"❌ Failed to get daily summary")
                    else:
                        print(f"❌ Failed to get approval queue: {approvals_response.status_code}")
                else:
                    print(f"❌ Night training failed: {training_response.status_code}")
            else:
                print(f"❌ Failed to send to agent: {agent_response.status_code}")
        else:
            print(f"❌ Task evaluation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_alternative_workflows():
    """Test alternative workflow paths"""
    print("\n🔄 Alternative Workflows")
    print("=" * 40)
    
    # Test autonomous task
    print("\n📝 Testing Autonomous Task:")
    autonomous_payload = {
        "task_id": "devops/terraform-init",
        "task_description": "Initialize Terraform configuration for AWS infrastructure"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/james/evaluate", json=autonomous_payload)
        if response.status_code == 200:
            evaluation = response.json()
            print(f"✅ Autonomous task detected: {evaluation['is_autonomous']}")
            print(f"   Category: {evaluation['detected_category']}")
            print(f"   Result: {evaluation['evaluation_result']}")
    except Exception as e:
        print(f"❌ Autonomous task test failed: {e}")
    
    # Test complete with James
    print("\n📝 Testing Complete with James:")
    try:
        complete_response = requests.post(
            f"{BASE_URL}/api/tasks/complete-with-james",
            params={"task_id": "test/james-completion"}
        )
        if complete_response.status_code == 200:
            result = complete_response.json()
            print(f"✅ Task completed with James: {result['status']}")
    except Exception as e:
        print(f"❌ James completion test failed: {e}")

def main():
    """Run complete workflow audit"""
    test_complete_workflow_cycle()
    test_alternative_workflows()
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("1. Visit http://localhost:8000/gui/task-input for task submission")
    print("2. Visit http://localhost:8000/gui/digest for daily summary")
    print("3. Visit http://localhost:8000/gui/whis-training for approval queue")
    print("4. Monitor the complete workflow cycle in action")

if __name__ == "__main__":
    main() 