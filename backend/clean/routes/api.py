"""
Main API routes for LinkOps Core
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime
import re

from config.database import get_db
# from config.kafka import get_kafka_manager  # DISABLED - Kafka removed for simplicity
from config.settings import settings
from core.models.schemas import LinkCreate, LinkResponse, LinkUpdate, WhisMemoryInput, WhisMemoryResponse
from core.models.entities import Link
from core.db.models import Orb, Rune

router = APIRouter()


@router.get("/links", response_model=List[LinkResponse])
async def get_links(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all links with pagination"""
    links = db.query(Link).offset(skip).limit(limit).all()
    return links


@router.get("/links/{link_id}", response_model=LinkResponse)
async def get_link(link_id: str, db: Session = Depends(get_db)):
    """Get a specific link by ID"""
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.post("/links", response_model=LinkResponse)
async def create_link(
    link: LinkCreate,
    db: Session = Depends(get_db)
):
    """Create a new link"""
    # Create link in database
    db_link = Link(
        id=str(uuid.uuid4()),
        url=link.url,
        title=link.title,
        description=link.description,
        created_at=datetime.utcnow()
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Send message to Kafka
    # kafka_manager = get_kafka_manager()
    # kafka_manager.send_message(
    #     topic=f"{settings.KAFKA_TOPIC_PREFIX}.links.created",
    #     message={
    #         "link_id": db_link.id,
    #         "url": db_link.url,
    #         "timestamp": datetime.utcnow().isoformat()
    #     }
    # )
    
    return db_link


@router.put("/links/{link_id}", response_model=LinkResponse)
async def update_link(
    link_id: str,
    link_update: LinkUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing link"""
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Update fields
    for field, value in link_update.dict(exclude_unset=True).items():
        setattr(db_link, field, value)
    
    db_link.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_link)
    
    # Send message to Kafka
    # kafka_manager = get_kafka_manager()
    # kafka_manager.send_message(
    #     topic=f"{settings.KAFKA_TOPIC_PREFIX}.links.updated",
    #     message={
    #         "link_id": db_link.id,
    #         "timestamp": datetime.utcnow().isoformat()
    #     }
    # )
    
    return db_link


@router.delete("/links/{link_id}")
async def delete_link(link_id: str, db: Session = Depends(get_db)):
    """Delete a link"""
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(db_link)
    db.commit()
    
    # Send message to Kafka
    # kafka_manager = get_kafka_manager()
    # kafka_manager.send_message(
    #     topic=f"{settings.KAFKA_TOPIC_PREFIX}.links.deleted",
    #     message={
    #         "link_id": link_id,
    #         "timestamp": datetime.utcnow().isoformat()
    #     }
    # )
    
    return {"message": "Link deleted successfully"}


@router.post("/links/{link_id}/screenshot")
async def upload_screenshot(
    link_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a screenshot for a link"""
    # Verify link exists
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Save screenshot
    file_extension = file.filename.split('.')[-1] if file.filename else 'png'
    screenshot_filename = f"{link_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
    screenshot_path = f"{settings.SCREENSHOTS_DIR}/{screenshot_filename}"
    
    with open(screenshot_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Update link with screenshot path
    db_link.screenshot_path = screenshot_path
    db_link.updated_at = datetime.utcnow()
    db.commit()
    
    return {
        "message": "Screenshot uploaded successfully",
        "filename": screenshot_filename,
        "path": screenshot_path
    }


def infer_task_id(task: str) -> str:
    """Extract a task ID from the task description"""
    # Simple heuristic: take first few words and clean them
    words = task.split()[:3]  # Take first 3 words
    task_id = "_".join(words).lower()
    # Remove special characters except underscores and hyphens
    task_id = re.sub(r'[^a-z0-9_-]', '', task_id)
    return task_id[:50]  # Limit length


def generate_orb_tips(task: str, tips: Optional[str] = None) -> str:
    """Generate orb description with tips"""
    description = task
    if tips:
        description += f"\n\nTips:\n{tips}"
    return description


def extract_rune_template(solution: str) -> str:
    """Extract rune template from solution"""
    # For now, just return the solution as-is
    # This could be enhanced with AI processing later
    return solution


@router.post("/api/whis/tasks", response_model=WhisMemoryResponse)
async def create_whis_memory(request: WhisMemoryInput, db: Session = Depends(get_db)):
    """Create Whis memory (Orb + Rune) from task and solution"""
    try:
        # Step 1: Sanitize
        task_id = infer_task_id(request.task)
        orb_description = generate_orb_tips(request.task, request.tips)
        rune_content = extract_rune_template(request.solution)

        # Step 2: Save to Orbs and Runes
        db_orb = Orb(
            name=f"Whis Task: {task_id}",
            description=orb_description,
            category=request.category
        )
        db.add(db_orb)
        db.commit()
        db.refresh(db_orb)

        # Create the Rune
        db_rune = Rune(
            orb_id=db_orb.id,
            script_path=f"/memory/whis/{task_id}.rune",
            script_content=rune_content,
            language="python",
            version=1
        )
        db.add(db_rune)
        db.commit()
        db.refresh(db_rune)

        return WhisMemoryResponse(
            status="stored",
            orb_id=str(db_orb.id),
            rune_id=str(db_rune.id),
            task_id=task_id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create Whis memory: {str(e)}")
