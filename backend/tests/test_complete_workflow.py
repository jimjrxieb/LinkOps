#!/usr/bin/env python3
"""
Complete Workflow Test Script
Demonstrates the full task submission → James evaluation → agent routing workflow
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    """Test the complete workflow from task submission to agent routing"""
    print("🔄 Complete Workflow Test")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Submit a task for evaluation
    print("1️⃣ Step 1: Submit Task for James Evaluation")
    print("-" * 40)
    
    task_payload = {
        "task_id": "test/workflow-demo",
        "task_description": "Create a Kubernetes deployment for a machine learning model with GPU support"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/james/evaluate", json=task_payload)
        
        if response.status_code == 200:
            evaluation = response.json()
            print(f"✅ Task evaluated successfully!")
            print(f"   Task ID: {evaluation['task_id']}")
            print(f"   Status: {evaluation['status']}")
            print(f"   Options: {evaluation['options']}")
            print()
            
            # Step 2: Send to Whis agent
            print("2️⃣ Step 2: Send Task to Whis Agent")
            print("-" * 40)
            
            agent_response = requests.post(
                f"{BASE_URL}/api/tasks/send-to-agent",
                params={"task_id": evaluation['task_id'], "agent": "whis"}
            )
            
            if agent_response.status_code == 200:
                agent_result = agent_response.json()
                print(f"✅ Task sent to Whis successfully!")
                print(f"   Status: {agent_result['status']}")
                print(f"   Agent: {agent_result['agent']}")
                print(f"   Task ID: {agent_result['task_id']}")
                print()
                
                # Step 3: Run nightly training to process the task
                print("3️⃣ Step 3: Run Nightly Training")
                print("-" * 40)
                
                training_response = requests.post(f"{BASE_URL}/api/whis/train-nightly")
                
                if training_response.status_code == 200:
                    training_result = training_response.json()
                    print(f"✅ Nightly training completed!")
                    print(f"   Tasks Processed: {training_result['tasks_processed']}")
                    print(f"   Runes Created: {training_result['runes_created']}")
                    print(f"   Orbs Updated: {training_result['orbs_updated']}")
                    print()
                    
                    # Step 4: Check approval queue
                    print("4️⃣ Step 4: Check Approval Queue")
                    print("-" * 40)
                    
                    approvals_response = requests.get(f"{BASE_URL}/api/whis/approvals")
                    
                    if approvals_response.status_code == 200:
                        approvals = approvals_response.json()
                        print(f"✅ Approval queue retrieved!")
                        print(f"   Pending Approvals: {len(approvals)}")
                        
                        if approvals:
                            print("   Recent flagged runes:")
                            for rune in approvals[:3]:  # Show first 3
                                print(f"     - {rune['task_id']} in {rune['orb']}")
                        else:
                            print("   No runes awaiting approval")
                        print()
                        
                        # Step 5: Check training stats
                        print("5️⃣ Step 5: Check Training Statistics")
                        print("-" * 40)
                        
                        stats_response = requests.get(f"{BASE_URL}/api/whis/training-stats")
                        
                        if stats_response.status_code == 200:
                            stats = stats_response.json()
                            print(f"✅ Training statistics retrieved!")
                            print(f"   Logs Today: {stats['logs_today']}")
                            print(f"   Agent Breakdown: {stats['agent_breakdown']}")
                            print(f"   Pending Approvals: {stats['pending_approvals']}")
                            print()
                            
                            print("🎉 Complete Workflow Test Successful!")
                            print("\n📋 Summary:")
                            print("   ✅ Task submitted and evaluated by James")
                            print("   ✅ Task routed to Whis agent")
                            print("   ✅ Nightly training processed the task")
                            print("   ✅ Approval queue system working")
                            print("   ✅ Training statistics available")
                            
                        else:
                            print(f"❌ Failed to get training stats: {stats_response.status_code}")
                    else:
                        print(f"❌ Failed to get approval queue: {approvals_response.status_code}")
                else:
                    print(f"❌ Nightly training failed: {training_response.status_code}")
            else:
                print(f"❌ Failed to send to agent: {agent_response.status_code}")
        else:
            print(f"❌ Task evaluation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_alternative_workflow():
    """Test alternative workflow: complete with James"""
    print("\n🔄 Alternative Workflow: Complete with James")
    print("=" * 50)
    
    # Submit another task
    task_payload = {
        "task_id": "test/james-completion",
        "task_description": "Simple documentation update for API endpoints"
    }
    
    try:
        # Step 1: Evaluate
        response = requests.post(f"{BASE_URL}/api/james/evaluate", json=task_payload)
        
        if response.status_code == 200:
            evaluation = response.json()
            print(f"✅ Task evaluated: {evaluation['task_id']}")
            
            # Step 2: Complete with James
            complete_response = requests.post(
                f"{BASE_URL}/api/tasks/complete-with-james",
                params={"task_id": evaluation['task_id']}
            )
            
            if complete_response.status_code == 200:
                result = complete_response.json()
                print(f"✅ Task completed with James!")
                print(f"   Status: {result['status']}")
                print(f"   Agent: {result['agent']}")
            else:
                print(f"❌ James completion failed: {complete_response.status_code}")
        else:
            print(f"❌ Task evaluation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Alternative workflow failed: {e}")

def main():
    """Run all workflow tests"""
    test_complete_workflow()
    test_alternative_workflow()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Visit http://localhost:8000/gui/task-input for the web interface")
    print("2. Submit tasks and see the complete workflow in action")
    print("3. Check http://localhost:8000/gui/whis-training for approval queue")
    print("4. Monitor logs and training statistics")

if __name__ == "__main__":
    main() 