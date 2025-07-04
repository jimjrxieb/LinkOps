from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from scorer import score_task
from selector import select_agent_for_task
from task_router import evaluate_task, Task, TaskEvaluation

app = FastAPI(title="FickNury Evaluator")


class TaskItem(BaseModel):
    task_id: str
    task_description: str


class EvaluationResponse(BaseModel):
    automatable: List[str]
    non_automatable: List[str]
    score_map: Dict[str, float]
    suggestions: Dict[str, str]


@app.post("/api/evaluate", response_model=EvaluationResponse)
async def evaluate_tasks(request: Request):
    data = await request.json()
    tasks = data.get("tasks", [])

    auto_ids = []
    non_auto_ids = []
    score_map = {}
    suggestions = {}

    for task in tasks:
        task_id = task.get("task_id")
        description = task.get("task_description")
        score_data = score_task(task)
        agent = select_agent_for_task(description, {})

        score_map[task_id] = score_data["score"]
        suggestions[task_id] = agent

        if score_data["automatable"]:
            auto_ids.append(task_id)
        else:
            non_auto_ids.append(task_id)

    return EvaluationResponse(
        automatable=auto_ids,
        non_automatable=non_auto_ids,
        score_map=score_map,
        suggestions=suggestions,
    )


@app.post("/evaluate")
async def evaluate_single_task(task: Task) -> TaskEvaluation:
    """
    Evaluate a single task using the new task router.
    """
    return await evaluate_task(task)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "healthy", "service": "ficknury-evaluator"}
