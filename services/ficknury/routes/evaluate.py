from fastapi import APIRouter
from pydantic import BaseModel
from logic.scorer import score_task
import random
import subprocess

router = APIRouter(prefix="/api/ficknury", tags=["Task Evaluation"])


class EvalInput(BaseModel):
    task_id: str
    task_description: str
    agent: str
    approved: bool = False


@router.post("/evaluate-task")
def evaluate_task(payload: dict):
    """Legacy endpoint for backward compatibility"""
    result = score_task(payload)
    return {
        "score": result["score"],
        "automatable": result["automatable"],
        "agent": result["agent"],
    }


@router.post("/evaluate")
def evaluate_task_with_approval(data: EvalInput):
    """Evaluate task and handle approval/deployment flow"""

    # Score the task
    score = random.uniform(0.0, 1.0)  # TODO: Replace with real scoring logic

    print(f"[FICKNURY] Task: {data.task_description} → Score: {score:.2f}")

    if score >= 0.9:
        # Task is highly automatable
        if data.approved:
            # Deploy the agent
            print(f"[FICKNURY] Deploying agent {data.agent} for task {data.task_id}")

            # Simulated CLI deploy (placeholder)
            try:
                # TODO: Replace with actual deployment logic
                subprocess.run(
                    ["echo", f"Deploying {data.agent} for task {data.task_id}"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                return {
                    "status": "deployed",
                    "agent": data.agent,
                    "task_id": data.task_id,
                    "score": round(score, 2),
                    "message": f"Successfully deployed {data.agent} for task {data.task_id}",
                }
            except Exception as e:
                return {
                    "status": "deployment_failed",
                    "agent": data.agent,
                    "task_id": data.task_id,
                    "score": round(score, 2),
                    "error": str(e),
                    "message": "Deployment failed",
                }
        else:
            # Waiting for approval
            return {
                "status": "awaiting_approval",
                "agent": data.agent,
                "task_id": data.task_id,
                "score": round(score, 2),
                "message": "Task approved for automation, awaiting deployment approval",
            }
    else:
        # Task needs manual review
        return {
            "status": "manual_review",
            "agent": data.agent,
            "task_id": data.task_id,
            "score": round(score, 2),
            "message": "Task requires manual review due to low automation score",
        }
