from fastapi import APIRouter
from models.collector import TaskInput
from utils.kafka_producer import send_to_kafka

router = APIRouter(prefix="/api/collect", tags=["Collector"])

@router.post("/task")
def collect_task(task: TaskInput):
    send_to_kafka("raw-tasks", task.dict())
    return {"status": "queued", "source": "task"} 