from fastapi import FastAPI, Request
from pydantic import BaseModel
import csv
import json
import requests
from datetime import datetime
from routes import collect, qna, info_dump, image_input, fixlog, youtube
import os

app = FastAPI(title="Data Collector Service")

app.include_router(collect.router)
app.include_router(qna.router)
app.include_router(info_dump.router)
app.include_router(image_input.router)
app.include_router(fixlog.router)
app.include_router(youtube.router)

TRAINING_CSV_PATH = "/app/training_queue.csv"


class LearningTask(BaseModel):
    task_id: str
    title: str
    description: str
    priority: str = "medium"
    category: str = "general"
    tags: list = []
    evaluation: dict = {}


@app.post("/task")
async def receive_task(request: Request):
    """
    Receive tasks from James and add to training queue.
    """
    data = await request.json()

    try:
        # Sanitize the task first
        sanitized_response = requests.post(
            "http://whis_sanitize:8000/sanitize", json=data, timeout=10
        )

        if sanitized_response.status_code == 200:
            sanitized_data = sanitized_response.json()["sanitized"]
        else:
            # Fallback to original data if sanitization fails
            sanitized_data = data

        # Add to training queue CSV
        with open(TRAINING_CSV_PATH, "a", newline="", encoding="utf-8") as file:
            fieldnames = [
                "task_id",
                "title",
                "description",
                "tools_used",
                "commands",
                "solution_summary",
                "status",
                "tags",
                "confidence",
                "agent",
                "created_at",
                "completed_at",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header if file is new
            if os.path.getsize(TRAINING_CSV_PATH) == 0:
                writer.writeheader()

            training_entry = {
                "task_id": sanitized_data.get(
                    "task_id", f"task-{datetime.utcnow().timestamp()}"
                ),
                "title": sanitized_data.get("title", ""),
                "description": sanitized_data.get("description", ""),
                "tools_used": "",
                "commands": "",
                "solution_summary": "",
                "status": "Pending",
                "tags": ",".join(sanitized_data.get("tags", [])),
                "confidence": 0.0,
                "agent": "manual",
                "created_at": datetime.now().isoformat(),
                "completed_at": "",
            }

            writer.writerow(training_entry)

        return {
            "status": "queued",
            "task": sanitized_data,
            "message": "Task received and sanitized",
        }

    except Exception as e:
        return {"status": "error", "error": str(e), "message": "Failed to process task"}


@app.post("/learn")
async def learn_from_task(task: LearningTask):
    """
    Receive a task for learning and add it to the training queue.
    """
    try:
        # Add to training queue CSV
        training_entry = {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "tools_used": "",
            "commands": "",
            "solution_summary": "",
            "status": "learning",
            "tags": ",".join(task.tags) if task.tags else "",
            "confidence": task.evaluation.get("confidence", 0.0),
            "agent": task.evaluation.get("agent", "whis_data_input"),
            "created_at": datetime.now().isoformat(),
            "completed_at": "",
        }

        file_exists = os.path.exists(TRAINING_CSV_PATH)

        with open(TRAINING_CSV_PATH, "a", newline="", encoding="utf-8") as file:
            fieldnames = [
                "task_id",
                "title",
                "description",
                "tools_used",
                "commands",
                "solution_summary",
                "status",
                "tags",
                "confidence",
                "agent",
                "created_at",
                "completed_at",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(training_entry)

        return {
            "status": "learning_task_received",
            "task_id": task.task_id,
            "message": "Task added to learning queue",
        }

    except Exception as e:
        return {"status": "error", "task_id": task.task_id, "error": str(e)}


@app.get("/health")
def health():
    """Basic health check"""
    return {"status": "healthy", "service": "whis_data_input"}
