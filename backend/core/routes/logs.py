from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class LogRequest(BaseModel):
    source: str
    task_id: str
    action: str
    result: Dict[str, Any]
    sanitized: bool = True
    approved: bool = False
    auto_approved: bool = False
    compliance_tags: str = "[]"

@router.post("/api/logs")
async def create_log(request: LogRequest):
    """Stub: Create a new log entry (no DB)"""
    return {
        "status": "success",
        "log_id": "stub-123",
        "task_id": request.task_id,
        "message": "Log created (stub)"
    } 