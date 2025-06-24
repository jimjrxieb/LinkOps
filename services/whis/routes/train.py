from fastapi import APIRouter
from logic.generator import process_batch

router = APIRouter(prefix="/api/whis", tags=["Training"])

@router.post("/train-nightly")
def trigger_training():
    processed = process_batch()
    return {"status": "done", "processed": len(processed)} 