from fastapi import APIRouter
from models.collector import ImageTextInput
from utils.kafka_producer import send_to_kafka

router = APIRouter(prefix="/api/collect", tags=["ImageText"])


@router.post("/image")
def collect_image(image: ImageTextInput):
    send_to_kafka("raw-image", image.dict())
    return {"status": "queued", "source": "image"}
