import os
import json

def verify_task_completion(task_id: str):
    # Check if task log exists and verify completion
    log_files = [f for f in os.listdir("storage/logs") if f.startswith(task_id)]
    
    if not log_files:
        return {"status": "not_found", "task_id": task_id}
    
    # Get the most recent log
    latest_log = sorted(log_files)[-1]
    
    with open(f"storage/logs/{latest_log}", "r") as f:
        log_data = json.load(f)
    
    return {
        "status": log_data["status"],
        "task_id": task_id,
        "agent": log_data["agent"],
        "timestamp": log_data["timestamp"],
        "output": log_data["output"][:200] + "..." if len(log_data["output"]) > 200 else log_data["output"]
    } 