from fastapi import APIRouter
from models.collector import QnAInput
from utils.kafka_producer import send_to_kafka

router = APIRouter(prefix="/api/collect", tags=["QnA"])

@router.post("/qna")
def collect_qna(qna: QnAInput):
    send_to_kafka("raw-qna", qna.dict())
    return {"status": "queued", "source": "qna"} 