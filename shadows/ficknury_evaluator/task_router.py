from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import requests
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FickNury Task Router", version="1.0.0")


class Task(BaseModel):
    task_id: str
    title: str
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = "general"
    tags: Optional[list] = []


class TaskEvaluation(BaseModel):
    task_id: str
    confidence: float
    agent: str
    status: str
    reasoning: str


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ficknury-evaluator"}


@app.post("/evaluate")
async def evaluate_task(task: Task) -> TaskEvaluation:
    """
    Evaluate task and route to appropriate agent based on confidence score.
    """
    logger.info(f"Evaluating task: {task.task_id} - {task.title}")

    # Calculate confidence based on task content and keywords
    confidence = calculate_confidence(task)
    agent, status, reasoning = determine_agent_and_status(task, confidence)

    evaluation = TaskEvaluation(
        task_id=task.task_id,
        confidence=confidence,
        agent=agent,
        status=status,
        reasoning=reasoning,
    )

    # Route task to appropriate agent
    try:
        await route_task(task, evaluation)
        logger.info(
            f"Task {task.task_id} routed to {agent} with confidence {confidence}"
        )
    except Exception as e:
        logger.error(f"Failed to route task {task.task_id}: {str(e)}")
        # Fallback to manual review
        evaluation.agent = "james_logic"
        evaluation.status = "manual_review"
        evaluation.reasoning = f"Routing failed: {str(e)}"

    return evaluation


def calculate_confidence(task: Task) -> float:
    """
    Calculate confidence score based on task content analysis.
    """
    description_lower = task.description.lower()
    title_lower = task.title.lower()

    # High confidence keywords (infrastructure, deployment, security)
    high_confidence_keywords = [
        "helm",
        "terraform",
        "kubernetes",
        "k8s",
        "docker",
        "deployment",
        "security",
        "audit",
        "compliance",
        "migration",
        "infrastructure",
        "aws",
        "azure",
        "gcp",
        "cloud",
        "ci/cd",
        "pipeline",
    ]

    # Medium confidence keywords (development, testing, monitoring)
    medium_confidence_keywords = [
        "test",
        "testing",
        "monitor",
        "logging",
        "debug",
        "fix",
        "update",
        "upgrade",
        "install",
        "configure",
        "setup",
    ]

    # Count keyword matches
    high_matches = sum(
        1
        for keyword in high_confidence_keywords
        if keyword in description_lower or keyword in title_lower
    )
    medium_matches = sum(
        1
        for keyword in medium_confidence_keywords
        if keyword in description_lower or keyword in title_lower
    )

    # Calculate base confidence
    base_confidence = min(0.9, (high_matches * 0.3) + (medium_matches * 0.1))

    # Adjust based on task category
    if task.category in ["infrastructure", "security", "deployment"]:
        base_confidence += 0.1
    elif task.category in ["development", "testing"]:
        base_confidence += 0.05

    # Priority adjustment
    if task.priority == "high":
        base_confidence -= 0.1  # More careful with high priority tasks

    return min(1.0, max(0.0, base_confidence))


def determine_agent_and_status(task: Task, confidence: float) -> tuple[str, str, str]:
    """
    Determine which agent should handle the task and the status.
    """
    if confidence >= 0.95:
        # Route to specialized agents based on task type
        if any(
            keyword in task.description.lower()
            for keyword in ["helm", "kubernetes", "k8s", "deployment"]
        ):
            return "katie_logic", "assigned", "High confidence Kubernetes/Helm task"
        elif any(
            keyword in task.description.lower()
            for keyword in ["aws", "azure", "gcp", "cloud", "infrastructure"]
        ):
            return (
                "igris_logic",
                "assigned",
                "High confidence cloud infrastructure task",
            )
        elif any(
            keyword in task.description.lower()
            for keyword in ["security", "audit", "compliance"]
        ):
            return "audit_logic", "assigned", "High confidence security/audit task"
        else:
            return "whis_logic", "assigned", "High confidence general task"

    elif confidence >= 0.7:
        # Send to Whis for learning and processing
        return (
            "whis_logic",
            "learning",
            "Medium confidence - sending to Whis for processing",
        )

    elif confidence >= 0.4:
        # Send to data input for training
        return "whis_data_input", "training", "Low confidence - queued for training"

    else:
        # Manual intervention required
        return (
            "james_logic",
            "manual_review",
            "Very low confidence - requires manual review",
        )


async def route_task(task: Task, evaluation: TaskEvaluation):
    """
    Route the task to the appropriate agent service.
    """
    task_data = {
        "task_id": task.task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "category": task.category,
        "tags": task.tags,
        "evaluation": evaluation.dict(),
    }

    # Route based on agent
    if evaluation.agent == "whis_logic":
        response = requests.post(
            "http://whis_logic:8000/process_task", json=task_data, timeout=30
        )
    elif evaluation.agent == "whis_data_input":
        response = requests.post(
            "http://whis_data_input:8000/learn", json=task_data, timeout=30
        )
    elif evaluation.agent == "james_logic":
        response = requests.post(
            "http://james_logic:8000/manual-review", json=task_data, timeout=30
        )
    elif evaluation.agent == "katie_logic":
        response = requests.post(
            "http://katie_logic:8000/kubernetes-task", json=task_data, timeout=30
        )
    elif evaluation.agent == "igris_logic":
        response = requests.post(
            "http://igris_logic:8000/platform-task", json=task_data, timeout=30
        )
    elif evaluation.agent == "audit_logic":
        response = requests.post(
            "http://audit_logic:8000/security-task", json=task_data, timeout=30
        )
    else:
        # Default fallback
        response = requests.post(
            "http://james_logic:8000/manual-review", json=task_data, timeout=30
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to route to {evaluation.agent}",
        )


@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """
    Get the status of a specific task.
    """
    # This would typically query a database or task store
    # For now, return a placeholder
    return {
        "task_id": task_id,
        "status": "unknown",
        "message": "Task status tracking not implemented yet",
    }


@app.get("/metrics")
async def get_metrics():
    """
    Get routing metrics and statistics.
    """
    # This would typically return actual metrics
    return {
        "total_tasks_processed": 0,
        "tasks_by_agent": {},
        "average_confidence": 0.0,
        "success_rate": 0.0,
    }
