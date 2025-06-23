from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.log import LogEntry
from backend.models.rune import RuneCandidate
from backend.config.database import get_db

router = APIRouter()

@router.post("/api/whis/train-nightly")
def train_whis_nightly(db: Session = Depends(get_db)):
    # Get today's date range
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    logs_today = db.query(LogEntry).filter(LogEntry.created_at >= start_of_day).all()

    # Group and flag entries (fake logic for now)
    queue = []
    for log in logs_today:
        rune_candidate = RuneCandidate(
            agent=detect_agent(log),
            origin=log.input_type,
            content=log.sanitized,
            approved=False
        )
        db.add(rune_candidate)
        queue.append(rune_candidate)

    db.commit()
    print(f"[WHIS] Queued {len(queue)} rune candidates for review.")

    return {
        "status": "training_complete",
        "count": len(queue),
        "preview": [{"agent": r.agent, "origin": r.origin, "content": r.content} for r in queue[:3]]
    }

@router.get("/api/whis/approvals")
def get_pending_runes(db: Session = Depends(get_db)):
    runes = db.query(RuneCandidate).filter(RuneCandidate.approved == False).all()
    return runes

@router.post("/api/whis/approve-rune/{rune_id}")
def approve_rune(rune_id: int, db: Session = Depends(get_db)):
    rune = db.query(RuneCandidate).filter(RuneCandidate.id == rune_id).first()
    if not rune:
        raise HTTPException(status_code=404, detail="Rune not found")
    rune.approved = True
    db.commit()
    return {"status": "approved", "rune_id": rune_id}

@router.get("/api/whis/digest")
def whis_daily_digest(db: Session = Depends(get_db)):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    logs = db.query(LogEntry).filter(LogEntry.created_at >= today).all()
    runes = db.query(RuneCandidate).filter(RuneCandidate.created_at >= today).all()
    approved = [r for r in runes if r.approved]
    pending = [r for r in runes if not r.approved]

    agent_summary = {}
    for r in runes:
        agent_summary[r.agent] = agent_summary.get(r.agent, 0) + 1

    return {
        "log_count": len(logs),
        "runes_total": len(runes),
        "runes_approved": len(approved),
        "runes_pending": len(pending),
        "agents_affected": agent_summary,
        "preview": [r.content for r in runes[:3]]
    }

def detect_agent(log: LogEntry):
    if "kube" in str(log.sanitized).lower():
        return "katie"
    elif "model" in str(log.sanitized).lower():
        return "whis"
    elif "terraform" in str(log.sanitized).lower():
        return "igris"
    else:
        return "james" 