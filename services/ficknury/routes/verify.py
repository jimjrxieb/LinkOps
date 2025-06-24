from fastapi import APIRouter
from logic.verifier import verify_task_completion

router = APIRouter(prefix="/api/ficknury", tags=["Verification"])

@router.get("/verify-task")
def verify(task_id: str):
    result = verify_task_completion(task_id)
    return result 