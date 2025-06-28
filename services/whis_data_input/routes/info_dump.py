from fastapi import APIRouter
from models.collector import InfoDumpInput
from utils.kafka_producer import send_to_kafka

router = APIRouter(prefix="/api/collect", tags=["InfoDump"])


@router.post("/info")
def collect_info(info: InfoDumpInput):
    send_to_kafka("raw-info", info.dict())
    return {"status": "queued", "source": "info"}
