from fastapi import APIRouter
from logic.scorer import score_task

router = APIRouter(prefix="/api/ficknury", tags=["Task Evaluation"])

@router.post("/evaluate-task")
def evaluate_task(payload: dict):
    result = score_task(payload)
    return {"score": result["score"], "automatable": result["automatable"], "agent": result["agent"]} 