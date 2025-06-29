from fastapi import APIRouter
from utils.forward_to_collector import forward_payload

router = APIRouter(prefix="/api/scraper", tags=["Reloop"])


@router.post("/reloop")
def reloop(payload: dict):
    result = forward_payload(payload)
    return {"status": "forwarded", "result": result}
