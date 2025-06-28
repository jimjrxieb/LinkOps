from fastapi import APIRouter
from sanitizer.schemas import SanitizationRequest
from sanitizer.processor import sanitize_input
import requests
import os

router = APIRouter(prefix="/api/sanitize", tags=["Sanitizer"])

WHIS_URL = os.getenv("WHIS_URL", "http://whis:8003/api/whis/train")

@router.post("/")
def sanitize(request: SanitizationRequest):
    # Sanitize the input
    sanitized = sanitize_input(request.input_type, request.payload)
    
    try:
        # Forward to Whis for training
        response = requests.post(WHIS_URL, json={
            "input_type": request.input_type,
            "payload": sanitized
        }, timeout=10)
        
        return {
            "status": "sanitized",
            "sanitized": sanitized,
            "forwarded_to_whis": True,
            "whis_response": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {
            "status": "sanitized", 
            "sanitized": sanitized,
            "forwarded_to_whis": False,
            "error": str(e)
        } 