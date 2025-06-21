"""
Whis API routes for AI/ML training and learning
Updated Architecture: No manual training, approval queue system
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.models import Orb, Rune, Log
from db.database import get_db
from datetime import datetime, timedelta
from bootstrap import get_agent_orb
from whis_nightly import train_whis_nightly, get_training_stats
import uuid

router = APIRouter()

class ApproveRuneRequest(BaseModel):
    rune_id: str

@router.get("/api/whis/queue")
async def get_training_queue_status(db: Session = Depends(get_db)):
    """Get training queue status - shows task_ids awaiting processing"""
    logs = db.query(Log).filter(Log.agent == "whis").all()
    counts = {"pending": 0, "trained": 0, "fallbacks": 0, "matches": 0}
    
    for log in logs:
        result = log.result.lower()
        if "match" in result:
            counts["matches"] += 1
        elif "fallback" in result:
            counts["fallbacks"] += 1
        elif "trained" in result or "rune" in result:
            counts["trained"] += 1
        else:
            counts["pending"] += 1
    
    return counts

@router.get("/api/whis/approvals")
async def get_approval_queue(db: Session = Depends(get_db)):
    """Get approval queue - lists new Runes awaiting human validation"""
    runes = db.query(Rune).filter(Rune.is_flagged == True).order_by(Rune.created_at.desc()).all()
    approval_list = []
    
    for rune in runes:
        orb = db.query(Orb).filter(Orb.id == rune.orb_id).first()
        approval_list.append({
            "rune_id": str(rune.id),
            "orb": orb.name if orb else "Unknown",
            "script_path": rune.script_path,
            "script_content": rune.script_content,
            "language": rune.language,
            "version": rune.version,
            "task_id": rune.task_id,
            "created_at": rune.created_at.isoformat(),
            "orb_id": str(rune.orb_id)
        })
    
    return approval_list

@router.post("/api/whis/approve-rune")
async def approve_rune(payload: ApproveRuneRequest, db: Session = Depends(get_db)):
    """Approve a rune - removes flagged status"""
    try:
        rune = db.query(Rune).filter(Rune.id == uuid.UUID(payload.rune_id)).first()
        if not rune:
            raise HTTPException(status_code=404, detail="Rune not found")
        
        rune.is_flagged = False
        db.commit()
        
        return {"status": "approved", "rune_id": payload.rune_id}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rune ID format")

@router.post("/api/whis/train-nightly")
async def trigger_night_training():
    """Trigger nightly training to process all today's logs"""
    summary = train_whis_nightly()
    return summary

@router.get("/api/whis/training-stats")
async def get_whis_training_stats():
    """Get comprehensive training statistics"""
    stats = get_training_stats()
    return stats

@router.get("/api/whis/digest")
async def get_whis_daily_digest(db: Session = Depends(get_db)):
    """Get daily summary of Whis's learning activity"""
    since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    orbs_updated = db.query(Orb).filter(Orb.updated_at >= since).count()
    runes_created = db.query(Rune).filter(Rune.created_at >= since).count()
    logs_processed = db.query(Log).filter(Log.created_at >= since).count()

    return {
        "timestamp": since.isoformat(),
        "orbs_created": orbs_updated,
        "runes_created": runes_created,
        "logs_processed": logs_processed
    }

@router.get("/api/whis/stats")
async def get_whis_stats(db: Session = Depends(get_db)):
    """Get comprehensive Whis statistics"""
    orb = db.query(Orb).filter(Orb.name == "AI/ML Engineering Best Practices").first()
    if not orb:
        return {"error": "Whis orb not found"}
    
    total_runes = db.query(Rune).filter(Rune.orb_id == orb.id).count()
    total_logs = db.query(Log).filter(Log.agent == "whis").count()
    
    # Recent activity (last 7 days)
    since = datetime.utcnow() - timedelta(days=7)
    recent_runes = db.query(Rune).filter(
        Rune.orb_id == orb.id, 
        Rune.created_at >= since
    ).count()
    
    recent_logs = db.query(Log).filter(
        Log.agent == "whis", 
        Log.created_at >= since
    ).count()
    
    # Approval queue stats
    pending_approvals = db.query(Rune).filter(Rune.is_flagged == True).count()
    
    return {
        "orb_name": orb.name,
        "orb_id": str(orb.id),
        "total_runes": total_runes,
        "total_logs": total_logs,
        "recent_runes": recent_runes,
        "recent_logs": recent_logs,
        "pending_approvals": pending_approvals,
        "last_updated": orb.updated_at.isoformat() if orb.updated_at else None
    } 