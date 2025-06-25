from fastapi import APIRouter
from pydantic import BaseModel
from models.collector import TaskInput
from utils.kafka_producer import send_to_kafka
import requests
import os

router = APIRouter(prefix="/api/collect", tags=["Collector"])

SANITIZER_URL = os.getenv("SANITIZER_URL", "http://sanitizer:8002/api/sanitize")

class CollectedInput(BaseModel):
    input_type: str  # task | qa | info_dump | image
    payload: dict

@router.post("/")
def collect_data(data: CollectedInput):
    """Unified endpoint to collect and forward data to sanitizer"""
    try:
        # Forward to sanitizer
        response = requests.post(SANITIZER_URL, json={
            "input_type": data.input_type,
            "payload": data.payload
        }, timeout=10)
        
        return {
            "status": "collected",
            "sent_to_sanitizer": True,
            "sanitizer_response": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {
            "status": "collected",
            "sent_to_sanitizer": False,
            "error": str(e)
        }

@router.post("/task")
def collect_task(task: TaskInput):
    """Legacy endpoint - still sends to Kafka for backward compatibility"""
    send_to_kafka("raw-tasks", task.dict())
    return {"status": "queued", "source": "task"} 