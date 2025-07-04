from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import csv
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="James Logic Manual Task Export", version="1.0.0")


class ManualTask(BaseModel):
    task_id: str
    title: str
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = "general"
    tags: Optional[List[str]] = []
    evaluation: Optional[Dict[str, Any]] = None


class TaskSolution(BaseModel):
    task_id: str
    tools_used: List[str]
    commands: List[str]
    solution_summary: str
    status: str = "completed"
    tags: Optional[List[str]] = None


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "james-logic-manual-export"}


@app.post("/manual-review")
async def save_manual_task(task: ManualTask):
    """
    Save a task that requires manual review to the training queue.
    """
    logger.info(f"Received manual review task: {task.task_id} - {task.title}")

    try:
        # Create training queue entry
        training_entry = {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "tools_used": "",  # Will be filled when solved
            "commands": "",  # Will be filled when solved
            "solution_summary": "",  # Will be filled when solved
            "status": "pending",
            "tags": ",".join(task.tags) if task.tags else "",
            "confidence": (
                task.evaluation.get("confidence", 0.0) if task.evaluation else 0.0
            ),
            "agent": (
                task.evaluation.get("agent", "manual") if task.evaluation else "manual"
            ),
            "created_at": datetime.now().isoformat(),
            "completed_at": "",
        }

        # Append to training queue CSV
        csv_file_path = "/app/training_queue.csv"
        file_exists = os.path.exists(csv_file_path)

        with open(csv_file_path, "a", newline="", encoding="utf-8") as file:
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
            if not file_exists:
                writer.writeheader()

            writer.writerow(training_entry)

        logger.info(f"Task {task.task_id} saved to training queue")

        return {
            "status": "task_queued_for_solution",
            "task_id": task.task_id,
            "message": "Task has been queued for manual solution and training",
        }

    except Exception as e:
        logger.error(f"Failed to save task {task.task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save task: {str(e)}")


@app.post("/complete-task")
async def complete_manual_task(solution: TaskSolution):
    """
    Mark a task as completed and save the solution for training.
    """
    logger.info(f"Completing task: {solution.task_id}")

    try:
        # Read existing training queue
        csv_file_path = "/app/training_queue.csv"
        rows = []

        with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["task_id"] == solution.task_id:
                    # Update the row with solution data
                    row["tools_used"] = ",".join(solution.tools_used)
                    row["commands"] = "; ".join(solution.commands)
                    row["solution_summary"] = solution.solution_summary
                    row["status"] = solution.status
                    row["completed_at"] = datetime.now().isoformat()
                    if solution.tags:
                        row["tags"] = ",".join(solution.tags)
                rows.append(row)

        # Write back the updated data
        with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
            if rows:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        logger.info(f"Task {solution.task_id} marked as completed")

        return {
            "status": "task_completed",
            "task_id": solution.task_id,
            "message": "Task solution has been saved for training",
        }

    except Exception as e:
        logger.error(f"Failed to complete task {solution.task_id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to complete task: {str(e)}"
        )


@app.get("/pending-tasks")
async def get_pending_tasks():
    """
    Get all pending tasks that need manual review.
    """
    try:
        csv_file_path = "/app/training_queue.csv"
        pending_tasks = []

        if os.path.exists(csv_file_path):
            with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["status"] == "pending":
                        pending_tasks.append(row)

        return {"pending_tasks": pending_tasks, "count": len(pending_tasks)}

    except Exception as e:
        logger.error(f"Failed to get pending tasks: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get pending tasks: {str(e)}"
        )


@app.get("/training-stats")
async def get_training_stats():
    """
    Get statistics about the training queue.
    """
    try:
        csv_file_path = "/app/training_queue.csv"
        stats = {
            "total_tasks": 0,
            "pending_tasks": 0,
            "completed_tasks": 0,
            "average_confidence": 0.0,
        }

        if os.path.exists(csv_file_path):
            with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                total_confidence = 0.0
                for row in reader:
                    stats["total_tasks"] += 1
                    if row["status"] == "pending":
                        stats["pending_tasks"] += 1
                    elif row["status"] == "completed":
                        stats["completed_tasks"] += 1

                    try:
                        confidence = float(row.get("confidence", 0))
                        total_confidence += confidence
                    except ValueError:
                        pass

                if stats["total_tasks"] > 0:
                    stats["average_confidence"] = (
                        total_confidence / stats["total_tasks"]
                    )

        return stats

    except Exception as e:
        logger.error(f"Failed to get training stats: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get training stats: {str(e)}"
        )


@app.post("/export-to-whis")
async def export_completed_tasks_to_whis():
    """
    Export completed tasks to Whis for learning.
    """
    try:
        csv_file_path = "/app/training_queue.csv"
        completed_tasks = []

        if os.path.exists(csv_file_path):
            with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["status"] == "completed":
                        completed_tasks.append(row)

        # Send completed tasks to Whis for learning
        if completed_tasks:
            # This would typically send to Whis Logic for processing
            # For now, just log the export
            logger.info(f"Exported {len(completed_tasks)} completed tasks to Whis")

        return {
            "status": "exported",
            "tasks_exported": len(completed_tasks),
            "message": f"Exported {len(completed_tasks)} completed tasks to Whis",
        }

    except Exception as e:
        logger.error(f"Failed to export tasks to Whis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to export tasks: {str(e)}")
