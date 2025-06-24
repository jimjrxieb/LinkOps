"""
LinkOps Core - Streamlined Whis Training Pipeline
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

# Database
from db.database import get_db, engine
from db.models import Log, WhisQueue, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinkOps Core", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class LogRequest(BaseModel):
    source: str
    task_id: str
    action: str
    result: Dict[str, Any]
    sanitized: bool = True
    approved: bool = False
    auto_approved: bool = False
    compliance_tags: Optional[str] = "[]"

class ApproveRequest(BaseModel):
    task_id: str

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "LinkOps Core"}

# Logs endpoint
@app.post("/api/logs")
async def create_log(request: LogRequest, db: Session = Depends(get_db)):
    """Create a new log entry for Whis training"""
    try:
        log = Log(
            agent=request.source,
            task_id=request.task_id,
            action=request.action,
            result=str(request.result),
            sanitized=request.sanitized,
            approved=request.approved,
            auto_approved=request.auto_approved,
            compliance_tags=request.compliance_tags
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        
        return {
            "status": "success",
            "log_id": str(log.id),
            "task_id": log.task_id,
            "message": "Log created successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Whis approvals endpoint
@app.get("/api/whis/approvals")
async def get_approvals(db: Session = Depends(get_db)):
    """Get pending approvals for Whis training"""
    try:
        logs = db.query(Log).filter(
            Log.sanitized == True,
            Log.approved == False
        ).all()
        
        return [
            {
                "id": str(log.id),
                "task_id": log.task_id,
                "agent": log.agent,
                "action": log.action,
                "result": log.result,
                "created_at": log.created_at.isoformat() if log.created_at else None
            }
            for log in logs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Approve rune endpoint
@app.post("/api/whis/approve-rune")
async def approve_rune(request: ApproveRequest, db: Session = Depends(get_db)):
    """Approve a log entry for Whis training"""
    try:
        log = db.query(Log).filter(Log.task_id == request.task_id).first()
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        
        log.approved = True
        db.commit()
        
        return {
            "status": "success",
            "task_id": request.task_id,
            "message": "Log approved for Whis training"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Whis digest endpoint
@app.get("/api/whis/digest")
async def get_digest(db: Session = Depends(get_db)):
    """Get Whis training digest"""
    try:
        # Get today's approved logs
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        approved_logs = db.query(Log).filter(
            Log.approved == True,
            Log.created_at >= today
        ).all()
        
        # Get queue stats
        pending = db.query(Log).filter(
            Log.sanitized == True,
            Log.approved == False
        ).count()
        
        return {
            "date": today.isoformat(),
            "approved_today": len(approved_logs),
            "pending_approvals": pending,
            "recent_approved": [
                {
                    "task_id": log.task_id,
                    "agent": log.agent,
                    "action": log.action,
                    "result": log.result[:100] + "..." if len(log.result) > 100 else log.result
                }
                for log in approved_logs[-5:]  # Last 5 approved
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Train nightly endpoint
@app.post("/api/whis/train-nightly")
async def train_nightly(db: Session = Depends(get_db)):
    """Process approved logs for Whis training"""
    try:
        # Get all approved logs
        approved_logs = db.query(Log).filter(
            Log.sanitized == True,
            Log.approved == True
        ).all()
        
        # Add to WhisQueue for processing
        for log in approved_logs:
            queue_entry = WhisQueue(
                task_id=log.task_id,
                raw_text=log.result,
                source=log.agent,
                status="pending",
                agent=log.agent
            )
            db.add(queue_entry)
        
        db.commit()
        
        return {
            "status": "success",
            "processed": len(approved_logs),
            "message": f"Added {len(approved_logs)} approved logs to Whis training queue"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
