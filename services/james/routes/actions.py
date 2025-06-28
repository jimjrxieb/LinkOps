from fastapi import APIRouter
import subprocess
import shlex
import json
from datetime import datetime

router = APIRouter(prefix="/api/james", tags=["Actions"])


@router.post("/run")
def run_manual_command(payload: dict):
    script = payload.get("rune", "")
    task_id = payload.get(
        "task_id", f"james-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    )

    try:
        # Safely parse the script command using shlex.split
        cmd = shlex.split(script)
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        output = result.decode()

        # Log the successful execution
        log_execution(task_id, script, output, "success")

        return {"output": output, "status": "success", "task_id": task_id}
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode()

        # Log the failed execution
        log_execution(task_id, script, error_output, "failed")

        return {"error": error_output, "status": "failed", "task_id": task_id}
    except ValueError as e:
        # Handle invalid command string
        error_msg = f"Invalid command format: {str(e)}"
        log_execution(task_id, script, error_msg, "failed")
        return {"error": error_msg, "status": "failed", "task_id": task_id}


def log_execution(task_id: str, script: str, output: str, status: str):
    """Log James' manual executions"""
    log_entry = {
        "task_id": task_id,
        "agent": "james",
        "script": script,
        "output": output,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "execution_type": "manual",
    }

    # Save to storage/logs
    import os

    os.makedirs("storage/logs", exist_ok=True)

    with open(f"storage/logs/{task_id}_{status}.json", "w") as f:
        json.dump(log_entry, f, indent=2)
