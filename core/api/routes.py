from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import uuid

from core.db.models import Orb, Rune, Log
from core.db.database import get_db

router = APIRouter()

# === Pydantic Schemas ===
class OrbCreate(BaseModel):
    name: str
    description: str
    category: str

class OrbResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    category: str

    class Config:
        from_attributes = True

class LogCreate(BaseModel):
    agent: str
    task_id: str
    action: str
    result: str

# === API Routes ===
@router.post("/api/orbs", response_model=OrbResponse)
async def create_orb(orb: OrbCreate, db: Session = Depends(get_db)):
    db_orb = Orb(**orb.dict())
    db.add(db_orb)
    db.commit()
    db.refresh(db_orb)
    return db_orb

@router.get("/api/orbs", response_model=List[OrbResponse])
async def get_orbs(db: Session = Depends(get_db)):
    return db.query(Orb).all()

@router.post("/api/runes")
async def create_rune(orb_id: str, script_path: str, language: str, db: Session = Depends(get_db)):
    try:
        orb_uuid = uuid.UUID(orb_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid orb_id format")
    
    orb = db.query(Orb).filter(Orb.id == orb_uuid).first()
    if not orb:
        raise HTTPException(status_code=404, detail="Orb not found")
    
    rune = Rune(orb_id=orb_uuid, script_path=script_path, language=language)
    db.add(rune)
    db.commit()
    return {"status": "rune created"}

@router.post("/api/logs")
async def log_action(log: LogCreate, db: Session = Depends(get_db)):
    db_log = Log(**log.dict())
    db.add(db_log)
    db.commit()
    return {"status": "log saved"} 