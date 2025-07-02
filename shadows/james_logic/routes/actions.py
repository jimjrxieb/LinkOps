from fastapi import APIRouter
import subprocess
import shlex
import json
from datetime import datetime

router = APIRouter(prefix="/api/james", tags=["Actions"])


@router.post("/activate")
async def activate_shadow_army():
    """ARISE - Activate the Shadow Army"""
    try:
        # Simulate activation sequence
        activation_steps = [
            "Initializing Shadow Network...",
            "Summoning Core Agents...",
            "Establishing Neural Links...",
            "Activating Command Protocols...",
            "Shadow Army Online",
        ]

        # Log activation
        log_execution(
            f"arise-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            "ARISE",
            "Shadow Army activation sequence completed successfully",
            "success",
        )

        return {
            "message": "ARISE... The LinkOps network is awake.",
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "activation_steps": activation_steps,
            "shadow_agents": [
                {
                    "name": "Whis",
                    "status": "online",
                    "role": "Rune Forger & Shadow Brain",
                },
                {"name": "Igris", "status": "online", "role": "Platform Guardian"},
                {"name": "Katie", "status": "online", "role": "Kubernetes Sentinel"},
                {"name": "Ficknury", "status": "online", "role": "Task Evaluator"},
                {"name": "James", "status": "online", "role": "Voice of the Monarch"},
                {"name": "AuditGuard", "status": "online", "role": "Compliance Warden"},
            ],
        }
    except Exception as e:
        return {
            "message": "Activation failed",
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


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
