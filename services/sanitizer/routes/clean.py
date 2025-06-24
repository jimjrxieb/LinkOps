from fastapi import APIRouter
from sanitizer.schemas import SanitizationRequest
from sanitizer.processor import sanitize_input

router = APIRouter(prefix="/api/sanitize", tags=["Sanitizer"])

@router.post("/")
def sanitize(request: SanitizationRequest):
    result = sanitize_input(request.input_type, request.payload)
    return {"status": "sanitized", "sanitized": result} 