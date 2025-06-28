from fastapi import APIRouter
from pydantic import BaseModel
from models.collector import TaskInput
from utils.kafka_producer import send_to_kafka
import requests
import os
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/collect", tags=["Collector"])

SANITIZER_URL = os.getenv(
    "SANITIZER_URL", "http://whis_sanitize:8002/api/sanitize"
)


class CollectedInput(BaseModel):
    input_type: str
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


@router.post("/collect")
async def collect_data(data: CollectedInput):
    """Unified endpoint to collect and forward data to sanitizer"""
    if data.input_type in ["fix_logs", "screenshots", "qa", "info_dump"]:
        return _forward_to_sanitizer(data)
    else:
        return _forward_to_sanitizer(data)


def _forward_to_sanitizer(data: CollectedInput):
    """Helper function to forward data to sanitizer"""
    try:
        response = requests.post(
            SANITIZER_URL,
            json={
                "input_type": data.input_type,
                "content": data.content,
                "metadata": data.metadata,
            },
        )

        return {
            "status": "success",
            "collected_data": data.dict(),
            "sent_to_sanitizer": True,
            "sanitizer_response": (
                response.json() if response.status_code == 200 else None
            ),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "sent_to_sanitizer": False,
        }


@router.post("/task")
def collect_task(task: TaskInput):
    """Legacy endpoint - still sends to Kafka for backward compatibility"""
    send_to_kafka("raw-tasks", task.dict())
    return {"status": "queued", "source": "task"}
