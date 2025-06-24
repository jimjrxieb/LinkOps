from fastapi import APIRouter
import os
import json

router = APIRouter(prefix="/api/scraper", tags=["Logs"])

@router.get("/logs")
def list_logs():
    log_dir = "storage/logs/"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    logs = [f for f in os.listdir(log_dir) if f.endswith(".json")]
    return {"logs": logs}

@router.get("/logs/{filename}")
def read_log(filename: str):
    log_path = f"storage/logs/{filename}"
    if not os.path.exists(log_path):
        return {"error": "Log file not found"}
    
    with open(log_path) as f:
        return json.load(f) 