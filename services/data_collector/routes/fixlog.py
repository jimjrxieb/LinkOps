from fastapi import APIRouter
from models.collector import FixLogInput
from utils.kafka_producer import send_to_kafka

router = APIRouter(prefix="/api/collect", tags=["FixLogs"])

@router.post("/fixlog")
def collect_fixlog(entry: FixLogInput):
    send_to_kafka("raw-fixlog", entry.dict())
    return {"status": "queued", "source": "fixlog"} 