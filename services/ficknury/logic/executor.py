import subprocess
import json
from datetime import datetime

def deploy_agent(task):
    script = task.get("rune_script")
    agent = task.get("agent")
    task_id = task.get("task_id", "unknown")
    
    try:
        output = subprocess.check_output(script, shell=True, stderr=subprocess.STDOUT)
        
        # Log the successful execution
        log_execution(task_id, agent, script, output.decode(), "success")
        
        return {"status": "completed", "agent": agent, "output": output.decode()}
    except subprocess.CalledProcessError as e:
        # Log the failed execution
        log_execution(task_id, agent, script, e.output.decode(), "failed")
        
        return {"status": "failed", "error": e.output.decode()}

def log_execution(task_id, agent, script, output, status):
    log_entry = {
        "task_id": task_id,
        "agent": agent,
        "script": script,
        "output": output,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Save to storage/logs
    import os
    os.makedirs("storage/logs", exist_ok=True)
    
    with open(f"storage/logs/{task_id}_{status}.json", "w") as f:
        json.dump(log_entry, f, indent=2) 