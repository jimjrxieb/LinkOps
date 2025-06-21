from fastapi import APIRouter, Depends, HTTPException, Path, Body, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import re
from jinja2 import Template
from difflib import SequenceMatcher
import pandas as pd
from io import StringIO
import tempfile
from PIL import Image
import pytesseract
import os

from db.models import Orb, Rune, Log, WhisQueue
from db.database import get_db
# from config.kafka import get_kafka_manager  # DISABLED - Kafka removed for simplicity
from utils.llm import infer_agent_category, sanitize_input, generate_rune_with_openai, contains_code
from bootstrap import get_agent_orb

router = APIRouter()

# === Pydantic Schemas ===
class OrbCreate(BaseModel):
    name: str
    description: str
    category: Optional[str] = None

class OrbResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    category: str

    class Config:
        from_attributes = True

class RuneResponse(BaseModel):
    id: uuid.UUID
    orb_id: uuid.UUID
    script_path: Optional[str] = None
    script_content: Optional[str] = None
    language: str
    version: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LogCreate(BaseModel):
    agent: str
    task_id: str
    action: str
    result: str

class WhisMemoryInput(BaseModel):
    """Schema for Whis memory input"""
    task: str
    solution: str
    category: Optional[str] = "mlops"
    tips: Optional[str] = None

class WhisMemoryResponse(BaseModel):
    """Schema for Whis memory response"""
    status: str
    orb_id: str
    rune_id: Optional[str] = None
    task_id: str

class WhisQueueResponse(BaseModel):
    """Schema for Whis queue response"""
    id: str
    task_id: str
    raw_text: str
    source: str
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    task_id: str
    task_description: str

# === API Routes ===
@router.post("/api/orbs", response_model=OrbResponse)
async def create_orb(orb: OrbCreate, db: Session = Depends(get_db)):
    # Auto-classify the agent based on orb content
    task_text = f"{orb.description or ''} {orb.name}"
    category = classify_agent(task_text)
    
    # Create orb with auto-assigned category
    db_orb = Orb(
        name=orb.name,
        description=orb.description,
        category=category
    )
    db.add(db_orb)
    db.commit()
    db.refresh(db_orb)
    return db_orb

@router.get("/api/orbs", response_model=List[OrbResponse])
async def get_orbs(task_id: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Orb)
    if task_id:
        query = query.filter(Orb.description.contains(task_id))
    if category:
        query = query.filter(Orb.category.ilike(category))
    return query.all()

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

@router.get("/api/runes/{orb_id}")
def get_runes_for_orb(
    orb_id: str,
    db: Session = Depends(get_db)
):
    try:
        orb_uuid = uuid.UUID(orb_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    runes = db.query(Rune).filter(Rune.orb_id == orb_uuid).all()
    return [rune.to_dict() for rune in runes]

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

def classify_agent(task_text: str) -> str:
    """Classify which agent should handle this task based on content"""
    task_lower = task_text.lower()
    
    # Katie: Kubernetes, infrastructure, platform engineering
    if any(k in task_lower for k in ["pod", "deployment", "k8s", "kubernetes", "service", "configmap", "secret", "ingress", "namespace"]):
        return "katie"
    
    # Whis: MLOps, model training, ML pipelines
    elif any(k in task_lower for k in ["mlflow", "train", "model", "pipeline", "ml", "machine learning", "prediction", "inference", "serving"]):
        return "whis"
    
    # Igris: DevOps, CI/CD, infrastructure as code
    elif any(k in task_lower for k in ["terraform", "cicd", "jenkins", "devsecops", "gitlab", "github actions", "docker", "helm", "ansible"]):
        return "igris"
    
    # James: Search, discovery, documentation, general knowledge
    else:
        return "james"

@router.post("/api/whis/tasks", response_model=WhisMemoryResponse)
async def create_whis_memory(request: WhisMemoryInput, db: Session = Depends(get_db)):
    """Save a new Whis memory (Rune) under the correct master orb"""
    from utils.llm import infer_agent_category
    agent = infer_agent_category(request.task + " " + (request.tips or "") + " " + (request.solution or ""))
    orb = db.query(Orb).filter(Orb.name == agent).first()
    if not orb:
        orb = Orb(name=agent, description=f"{agent.capitalize()} agent orb", category=agent)
        db.add(orb)
        db.commit()
        db.refresh(orb)
    # Add the new Rune to the master orb
    rune = Rune(
        orb_id=orb.id,
        script_path=request.task.strip(),
        script_content=request.solution.strip(),
        language="yaml" if "apiVersion" in request.solution else "text",
        version=1,
        task_id=request.task
    )
    db.add(rune)
    db.commit()
    return WhisMemoryResponse(
        status="created",
        orb_id=str(orb.id),
        rune_id=str(rune.id),
        task_id=request.task
    )

@router.get("/api/whis/tasks", response_model=List[WhisMemoryResponse])
async def get_whis_memories(db: Session = Depends(get_db)):
    # Fetch all Orbs with their first Rune (if any)
    orbs = db.query(Orb).order_by(Orb.created_at.desc()).all()
    memories = []
    for orb in orbs:
        rune = orb.runes[0] if orb.runes else None
        memories.append(WhisMemoryResponse(
            status="stored",
            orb_id=str(orb.id),
            rune_id=str(rune.id) if rune else None,
            task_id=orb.name.replace("Whis Task: ", ""),
        ))
    return memories

@router.post("/api/whis/expand-rune")
async def expand_rune(template_str: str = Body(...), values: dict = Body(...)):
    try:
        rendered = Template(template_str).render(**values)
        return {"rendered": rendered}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/whis/audit-orbs")
async def audit_orbs(db: Session = Depends(get_db)):
    """Audit orbs for patterns and suggest improvements"""
    orbs = db.query(Orb).all()
    result = []
    
    # Pattern-based audit
    patterns = {
        "pod_creation": ["create pod", "deploy pod", "kubernetes pod"],
        "model_serving": ["serve model", "model serving", "fastapi model"],
        "mlflow": ["mlflow", "mlflow tracking", "mlflow model"],
        "docker": ["docker", "container", "dockerfile"],
        "monitoring": ["prometheus", "metrics", "monitoring"]
    }
    
    for orb in orbs:
        orb_lower = orb.description.lower() if orb.description else ""
        
        # Check for specific patterns
        if "create pod" in orb_lower:
            result.append({
                "id": str(orb.id),
                "name": orb.name,
                "note": "Consider merging with other pod-creation orbs",
                "type": "pattern_match"
            })
        
        # Check for MLflow patterns
        if "mlflow" in orb_lower:
            result.append({
                "id": str(orb.id),
                "name": orb.name,
                "note": "Consider grouping with other MLflow orbs",
                "type": "pattern_match"
            })
        
        # Check for similar names
        for other_orb in orbs:
            if orb.id != other_orb.id:
                name_similarity = SequenceMatcher(None, orb.name.lower(), other_orb.name.lower()).ratio()
                if name_similarity > 0.8:
                    result.append({
                        "id": str(orb.id),
                        "name": orb.name,
                        "note": f"Similar name to '{other_orb.name}' (similarity: {name_similarity:.2f})",
                        "type": "similar_name",
                        "similar_orb_id": str(other_orb.id)
                    })
    
    return {
        "audit_results": result,
        "total_orbs": len(orbs),
        "suggestions_count": len(result)
    }

@router.post("/api/whis/train")
async def train_whis(db: Session = Depends(get_db)):
    """Process queue items - classify, sanitize, and generate runes with OpenAI if needed"""
    try:
        from utils.llm import generate_rune_with_openai, contains_code
        
        queue = db.query(WhisQueue).filter(WhisQueue.status == "pending").all()
        trained_count = 0
        
        for item in queue:
            try:
                # Classify and sanitize
                agent = infer_agent_category(item.raw_text)
                sanitized = sanitize_input(item.raw_text)
                
                # Generate rune with OpenAI if text doesn't contain code
                if not contains_code(sanitized):
                    generated_rune = generate_rune_with_openai(sanitized)
                    item.raw_text = f"# Agent: {agent}\n# Original: {sanitized}\n\n# Generated Rune:\n{generated_rune}"
                else:
                    item.raw_text = f"# Agent: {agent}\n# Sanitized: {sanitized}\n\n# Original:\n{item.raw_text}"
                
                # Mark as trained (ready for review)
                item.status = "trained"
                trained_count += 1
                
                # Log the training
                log_entry = Log(
                    agent="whis",
                    task_id=item.task_id,
                    action=f"Trained queue item for {agent}",
                    result=f"Marked item {item.id} as trained and ready for review"
                )
                db.add(log_entry)
                
            except Exception as e:
                # Log error but continue with other items
                print(f"Error training item {item.id}: {str(e)}")
                item.status = "error"
                item.raw_text += f"\n\n# Training Error: {str(e)}"
        
        db.commit()
        
        return {
            "status": "training_completed",
            "trained": trained_count,
            "total_processed": len(queue),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

def infer_category(text: str) -> str:
    """Infer agent/category from raw text input"""
    if "apiVersion" in text and ("pod" in text.lower() or "deployment" in text.lower()):
        return "katie"
    elif "mlflow" in text or "pipeline" in text:
        return "whis"
    elif "terraform" in text or "snyk" in text or "ci/cd" in text.lower():
        return "igris"
    return "james"

@router.post("/api/whis/dump")
async def ingest_text(task_id: str = Body(...), dump: str = Body(...), db: Session = Depends(get_db)):
    category = infer_category(dump)
    
    # Get or create agent orb
    orb = db.query(Orb).filter(Orb.name == category).first()
    if not orb:
        orb = Orb(name=category, description=f"{category.capitalize()} Agent Orb", category=category)
        db.add(orb)
        db.commit()
        db.refresh(orb)

    # Save as a Rune
    rune = Rune(
        orb_id=orb.id,
        script_path=dump.strip(),
        script_content=dump.strip(),
        language="yaml" if "apiVersion" in dump else "text",
        version=1
    )
    db.add(rune)
    db.commit()

    return {"status": "processed", "task_id": task_id, "assigned_to": category}

@router.post("/api/whis/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload CSV file and process it for learning"""
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        # Get or create Whis orb
        orb = db.query(Orb).filter(Orb.name == "whis").first()
        if not orb:
            orb = Orb(name="whis", description="Whis Agent Orb", category="whis")
            db.add(orb)
            db.commit()
            db.refresh(orb)

        # Generate summary statistics
        summary = df.describe(include="all").to_string()
        
        # Create rune with CSV insights
        rune = Rune(
            orb_id=orb.id,
            script_path=f"/data/csv/{file.filename}",
            script_content=f"CSV Analysis:\n{summary}\n\nColumns: {list(df.columns)}\nRows: {len(df)}",
            language="text",
            version=1
        )
        db.add(rune)
        db.commit()
        
        return {
            "status": "csv processed", 
            "rows": len(df), 
            "columns": list(df.columns),
            "orb": orb.name,
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")

@router.post("/api/whis/upload-image")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload image and extract text using OCR"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Extract text using OCR
        image = Image.open(temp_file_path)
        extracted_text = pytesseract.image_to_string(image)
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        # Process the extracted text using the existing ingest_text logic
        category = infer_category(extracted_text)
        
        # Get or create agent orb
        orb = db.query(Orb).filter(Orb.name == category).first()
        if not orb:
            orb = Orb(
                name=category, 
                description=f"{category.capitalize()} Agent Orb", 
                category=category
            )
            db.add(orb)
            db.commit()
            db.refresh(orb)

        # Save as a Rune
        rune = Rune(
            orb_id=orb.id,
            script_path=f"/images/{file.filename}",
            script_content=extracted_text,
            language="text",
            version=1
        )
        db.add(rune)
        db.commit()

        return {
            "status": "image processed", 
            "task_id": f"image-{file.filename}",
            "assigned_to": category,
            "extracted_text_length": len(extracted_text),
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

@router.post("/api/runes/{rune_id}/feedback")
async def feedback_on_rune(
    rune_id: str,
    score: int = Body(..., embed=True),  # +1 or -1
    comment: str = Body("", embed=True),
    db: Session = Depends(get_db)
):
    """Provide feedback on a rune (thumbs up/down with optional comment)"""
    try:
        rune_uuid = uuid.UUID(rune_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rune_id format")
    
    rune = db.query(Rune).filter(Rune.id == rune_uuid).first()
    if not rune:
        raise HTTPException(status_code=404, detail="Rune not found")

    # Validate score
    if score not in [1, -1]:
        raise HTTPException(status_code=400, detail="Score must be 1 (positive) or -1 (negative)")

    # Update feedback
    rune.feedback_score += score
    rune.feedback_count += 1
    rune.last_feedback = comment
    if score < 0:
        rune.is_flagged = True

    db.commit()
    
    return {
        "status": "feedback recorded", 
        "rune_id": str(rune.id),
        "score": rune.feedback_score, 
        "count": rune.feedback_count,
        "flagged": rune.is_flagged,
        "average_score": rune.feedback_score / rune.feedback_count if rune.feedback_count > 0 else 0
    }

@router.post("/api/james/complete")
async def complete_with_james(task_id: str = Body(...), dump: str = Body(...), db: Session = Depends(get_db)):
    sanitized = sanitize_input(dump)
    agent = infer_agent_category(sanitized)

    # 1. Search for matching rune in assigned agent's orb
    runes = db.query(Rune).join(Orb).filter(Orb.name == agent).all()
    match = next((r for r in runes if task_id.lower() in r.script_path.lower()), None)

    if match:
        # ✅ Log match usage
        log = Log(
            agent=agent,
            task_id=task_id,
            action=f"Resolved task with rune {match.id}",
            result=match.script_path
        )
        db.add(log)
        db.commit()

        return {
            "match": True,
            "rune": match.script_path,
            "agent": agent,
            "orb": agent,
            "rune_id": str(match.id)
        }

    # ❌ No match — fallback to OpenAI
    fallback = generate_fallback_with_openai(sanitized)  # Use local or OpenAI call
    item = WhisQueue(task_id=task_id, raw_text=dump, source="openai_fallback", agent=agent)
    db.add(item)
    db.commit()

    return {
        "match": False,
        "fallback": fallback,
        "queued_for": "whis",
        "agent": agent,
        "task_id": task_id
    }

@router.post("/api/james/submit-answer")
async def submit_task_with_answer(
    task_id: str = Body(...),
    question: str = Body(...),
    answer: str = Body(...),
    db: Session = Depends(get_db)
):
    # Combine question and answer block
    full_block = f"Q: {question.strip()}\nA: {answer.strip()}"

    # Sanitize and classify
    sanitized = sanitize_input(full_block)
    agent = infer_agent_category(sanitized)

    # Add to Whis training queue
    item = WhisQueue(
        task_id=task_id,
        raw_text=sanitized,
        source="exam_data",
        agent=agent,
        status="pending"
    )
    db.add(item)
    db.commit()

    return {
        "status": "submitted",
        "agent": agent,
        "queued_for": "whis",
        "task_id": task_id
    }

def generate_fallback_with_openai(task_text: str) -> str:
    return f"# Fallback suggestion for unresolved task:\n{task_text}"

def log_agent_usage(agent: str, task_id: str, orb_id: str = None, rune_id: str = None, action: str = "task_processed", db: Session = None):
    """Log agent usage for analytics and training"""
    try:
        log_entry = Log(
            agent=agent,
            task_id=task_id,
            action=action,
            result=f"Agent {agent} processed task {task_id}" + (f" using orb {orb_id}" if orb_id else "") + (f" and rune {rune_id}" if rune_id else "")
        )
        if db:
            db.add(log_entry)
            db.commit()
        return str(log_entry.id)
    except Exception as e:
        print(f"Failed to log agent usage: {e}")
        return None

@router.post("/api/whis/queue")
async def save_for_whis(task_id: str = Body(...), dump: str = Body(...), source: str = Body("james"), db: Session = Depends(get_db)):
    """Save tasks to Whis queue for future training with enhanced source tracking and correct orb assignment"""
    try:
        # Validate source
        valid_sources = ["james", "openai_fallback", "match_usage", "manual", "katie", "igris"]
        if source not in valid_sources:
            source = "james"  # Default fallback

        # Determine agent category
        agent = infer_agent_category(dump)
        orb = db.query(Orb).filter(Orb.name == agent).first()
        if not orb:
            orb = Orb(name=agent, description=f"{agent.capitalize()} agent orb", category=agent)
            db.add(orb)
            db.commit()
            db.refresh(orb)

        # Optionally, create a Rune immediately (if that's the desired flow)
        # rune = Rune(orb_id=orb.id, script_path=dump.strip(), language="yaml", task_id=task_id)
        # db.add(rune)

        item = WhisQueue(
            task_id=task_id, 
            raw_text=dump, 
            source=source,
            status="pending"
        )
        db.add(item)
        
        # Log the queue action
        log_entry = Log(
            agent=agent,
            task_id=task_id,
            action=f"Queued for training (source: {source})",
            result=f"Task {task_id} saved to Whis queue with source {source} and assigned to orb {agent}"
        )
        db.add(log_entry)
        db.commit()
        
        return {
            "status": "queued", 
            "task_id": task_id,
            "queue_id": str(item.id),
            "source": source,
            "log_id": str(log_entry.id),
            "agent": agent,
            "orb_id": str(orb.id),
            "message": f"Task saved for Whis training (source: {source}) and assigned to orb {agent}"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to queue task: {str(e)}")

@router.get("/api/whis/queue")
async def get_whis_queue(status: str = "pending", db: Session = Depends(get_db)):
    """Fetch pending or trained-but-unapproved queue items"""
    try:
        # Allow filtering by status: pending, trained, approved, rejected
        query = db.query(WhisQueue)
        if status:
            query = query.filter(WhisQueue.status == status)
        
        queue_items = query.order_by(WhisQueue.created_at.desc()).all()
        return [
            {
                "id": str(item.id),
                "task_id": item.task_id,
                "raw_text": item.raw_text,
                "source": item.source,
                "status": item.status,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            for item in queue_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get queue: {str(e)}")

@router.post("/api/whis/queue/{queue_id}/approve")
async def approve_trained_rune(
    queue_id: str, 
    edited_rune: str = Body(...), 
    db: Session = Depends(get_db)
):
    """Approve a trained queue item and create a rune in the appropriate orb"""
    try:
        queue_uuid = uuid.UUID(queue_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid queue_id format")
    
    item = db.query(WhisQueue).filter(WhisQueue.id == queue_uuid).first()
    if not item or item.status != "trained":
        raise HTTPException(status_code=404, detail="Queue item not found or not ready for approval")
    
    # Extract agent from the trained item
    agent = None
    if "# Agent:" in item.raw_text:
        agent_line = [line for line in item.raw_text.split('\n') if line.startswith('# Agent:')]
        if agent_line:
            agent = agent_line[0].replace('# Agent:', '').strip()
    
    if not agent:
        agent = infer_agent_category(item.raw_text)
    
    # Get or create orb
    orb = db.query(Orb).filter(Orb.name == agent).first()
    if not orb:
        orb = Orb(name=agent, description=f"{agent.capitalize()} Orb", category=agent)
        db.add(orb)
        db.commit()
        db.refresh(orb)
    
    # Create the rune
    rune = Rune(
        orb_id=orb.id,
        script_path=edited_rune,
        script_content=edited_rune,
        language="yaml" if "apiVersion" in edited_rune else "text",
        version=1,
        task_id=item.task_id
    )
    db.add(rune)
    
    # Mark as approved
    item.status = "approved"
    
    # Log the approval
    log_entry = Log(
        agent="whis",
        task_id=item.task_id,
        action="Approved trained item",
        result=f"Created rune {rune.id} in orb {orb.name} from queue item {item.id}"
    )
    db.add(log_entry)
    
    db.commit()
    
    return {
        "status": "approved", 
        "agent": agent, 
        "orb": orb.name,
        "rune_id": str(rune.id),
        "orb_id": str(orb.id)
    }

@router.patch("/api/whis/queue/{queue_id}/train")
async def mark_as_trained(
    queue_id: str, 
    suggested_rune: str = Body(""), 
    db: Session = Depends(get_db)
):
    """Mark a queue item as trained with optional suggested rune content"""
    try:
        queue_uuid = uuid.UUID(queue_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid queue_id format")
    
    item = db.query(WhisQueue).filter(WhisQueue.id == queue_uuid).first()
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    if item.status != "pending":
        raise HTTPException(status_code=400, detail="Item is not pending")
    
    # Update status to trained and add suggestion if provided
    item.status = "trained"
    if suggested_rune:
        item.raw_text += f"\n\n# Whis Suggestion:\n{suggested_rune}"
    
    db.commit()
    
    return {
        "status": "trained",
        "queue_id": str(item.id),
        "task_id": item.task_id,
        "suggestion_added": bool(suggested_rune)
    }

@router.delete("/api/whis/queue/{queue_id}")
async def delete_queue_item(queue_id: str, db: Session = Depends(get_db)):
    """Delete a queue item"""
    try:
        queue_uuid = uuid.UUID(queue_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid queue_id format")
    
    item = db.query(WhisQueue).filter(WhisQueue.id == queue_uuid).first()
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    db.delete(item)
    db.commit()
    
    return {"status": "deleted", "queue_id": str(queue_uuid)}

@router.post("/api/whis/nightly-train")
async def run_nightly_training(db: Session = Depends(get_db)):
    """Run nightly training on pending queue items"""
    try:
        # Import the nightly training function
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
        
        from whis_nightly import nightly_train
        
        # Get count of pending items before training
        pending_before = db.query(WhisQueue).filter(WhisQueue.status == "pending").count()
        
        # Run the training
        nightly_train()
        
        # Get count after training
        pending_after = db.query(WhisQueue).filter(WhisQueue.status == "pending").count()
        trained_count = db.query(WhisQueue).filter(WhisQueue.status == "trained").count()
        
        items_trained = pending_before - pending_after
        
        return {
            "status": "training_completed",
            "items_trained": items_trained,
            "pending_before": pending_before,
            "pending_after": pending_after,
            "total_trained": trained_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get("/api/whis/queue-status")
async def get_whis_queue_status(db: Session = Depends(get_db)):
    """Get Whis queue statistics"""
    try:
        pending = db.query(WhisQueue).filter(WhisQueue.status == "pending").count()
        trained = db.query(WhisQueue).filter(WhisQueue.status == "trained").count()
        fallbacks = db.query(WhisQueue).filter(WhisQueue.source == "openai_fallback").count()
        matches = db.query(WhisQueue).filter(WhisQueue.source == "match_usage").count()
        
        return {
            "pending": pending,
            "trained": trained,
            "fallbacks": fallbacks,
            "matches": matches,
            "total": pending + trained
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get queue status: {str(e)}")

@router.get("/api/whis/queue-details")
async def get_whis_queue_details(db: Session = Depends(get_db)):
    """Get detailed Whis queue information"""
    try:
        items = db.query(WhisQueue).order_by(WhisQueue.created_at.desc()).limit(50).all()
        
        return {
            "items": [
                {
                    "id": str(item.id),
                    "task_id": item.task_id,
                    "source": item.source,
                    "status": item.status,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "raw_text": item.raw_text[:200] + "..." if len(item.raw_text) > 200 else item.raw_text
                }
                for item in items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get queue details: {str(e)}")

@router.patch("/api/runes/{rune_id}/approve")
async def approve_draft_rune(
    rune_id: str, 
    edited_content: str = Body(""), 
    db: Session = Depends(get_db)
):
    """Approve a draft rune (version 0) and convert to production (version 1)"""
    try:
        rune_uuid = uuid.UUID(rune_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rune_id format")
    
    rune = db.query(Rune).filter(Rune.id == rune_uuid).first()
    if not rune:
        raise HTTPException(status_code=404, detail="Rune not found")
    
    if rune.version != 0:
        raise HTTPException(status_code=400, detail="Only draft runes (version 0) can be approved")
    
    # Update rune to production version
    rune.version = 1
    if edited_content:
        rune.script_content = edited_content
    
    # Log the approval
    log_entry = Log(
        agent="whis",
        task_id=rune.task_id or "unknown",
        action="Approved draft rune",
        result=f"Converted rune {rune.id} from draft to production version"
    )
    db.add(log_entry)
    db.commit()
    
    return {
        "status": "approved",
        "rune_id": str(rune.id),
        "orb_id": str(rune.orb_id),
        "version": rune.version,
        "log_id": str(log_entry.id)
    }

@router.post("/api/james/upload-image")
async def upload_image_for_ocr(
    task_id: str = Body("k8s/ocr-task"), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """Upload image for OCR processing and queue for Whis training"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        try:
            # Extract text using OCR
            image = Image.open(tmp_path)
            raw_text = pytesseract.image_to_string(image)
            
            # Sanitize and classify
            sanitized = sanitize_input(raw_text)
            agent = infer_agent_category(sanitized)
            
            # Queue for Whis
            item = WhisQueue(
                task_id=task_id,
                raw_text=sanitized,
                source="image-ocr",
                status="pending"
            )
            db.add(item)
            
            # Log the OCR processing
            log_entry = Log(
                agent="james",
                task_id=task_id,
                action="Image OCR processed",
                result=f"Extracted {len(sanitized.splitlines())} lines, classified as {agent}, queued for Whis"
            )
            db.add(log_entry)
            db.commit()
            
            return {
                "status": "image processed",
                "queued_for": "whis",
                "agent": agent,
                "lines_extracted": len(sanitized.splitlines()),
                "queue_id": str(item.id),
                "log_id": str(log_entry.id),
                "preview": sanitized[:200] + "..." if len(sanitized) > 200 else sanitized
            }
            
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

@router.post("/api/james/queue-ocr")
async def queue_ocr_text(
    task_id: str = Body(...),
    raw_text: str = Body(...),
    db: Session = Depends(get_db)
):
    """Queue reviewed OCR text for Whis training"""
    from utils.llm import sanitize_input, infer_agent_category
    sanitized = sanitize_input(raw_text)
    agent = infer_agent_category(sanitized)
    item = WhisQueue(
        task_id=task_id,
        raw_text=sanitized,
        source="image-ocr-reviewed",
        status="pending"
    )
    db.add(item)
    log_entry = Log(
        agent="james",
        task_id=task_id,
        action="OCR text approved and queued",
        result=f"Queued {len(sanitized.splitlines())} lines for Whis as {agent}"
    )
    db.add(log_entry)
    db.commit()
    return {
        "status": "queued",
        "agent": agent,
        "lines": len(sanitized.splitlines()),
        "queue_id": str(item.id),
        "log_id": str(log_entry.id)
    }

@router.post("/api/whis/queue/{queue_id}/reject")
async def reject_trained_item(queue_id: str, db: Session = Depends(get_db)):
    """Reject a trained queue item"""
    try:
        queue_uuid = uuid.UUID(queue_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid queue_id format")
    
    item = db.query(WhisQueue).filter(WhisQueue.id == queue_uuid).first()
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    item.status = "rejected"
    
    # Log the rejection
    log_entry = Log(
        agent="whis",
        task_id=item.task_id,
        action="Rejected trained item",
        result=f"Rejected queue item {item.id}"
    )
    db.add(log_entry)
    
    db.commit()
    
    return {"status": "rejected", "queue_id": str(queue_uuid)}

@router.get("/api/orbs/{name}/runes")
async def get_runes_by_orb_name(name: str, db: Session = Depends(get_db)):
    """Get all runes for a specific orb (agent) by name"""
    try:
        # Get the orb by name
        orb = db.query(Orb).filter(Orb.name == name).first()
        if not orb:
            raise HTTPException(status_code=404, detail=f"Orb '{name}' not found")
        
        # Get all runes for this orb
        runes = db.query(Rune).filter(Rune.orb_id == orb.id).order_by(Rune.created_at.desc()).all()
        
        return {
            "orb": {
                "id": str(orb.id),
                "name": orb.name,
                "description": orb.description,
                "category": orb.category
            },
            "runes": [
                {
                    "id": str(rune.id),
                    "script_path": rune.script_path,
                    "script_content": rune.script_content,
                    "language": rune.language,
                    "version": rune.version,
                    "task_id": rune.task_id,
                    "feedback_score": rune.feedback_score,
                    "feedback_count": rune.feedback_count,
                    "created_at": rune.created_at.isoformat() if rune.created_at else None
                }
                for rune in runes
            ],
            "total_runes": len(runes)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get runes: {str(e)}")

@router.post("/api/james/evaluate")
async def evaluate_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """James evaluates and sanitizes a submitted task with automatic category detection"""
    try:
        # Automatic task category detection
        task_text = f"{payload.task_description} {payload.task_id}"
        detected_category = classify_agent(task_text)
        
        # Search for existing orbs and runes
        matching_orbs = db.query(Orb).filter(
            Orb.name.ilike(f"%{detected_category}%") |
            Orb.description.ilike(f"%{payload.task_description[:50]}%")
        ).limit(3).all()
        
        # Check for autonomous task patterns
        is_autonomous = any(keyword in task_text.lower() for keyword in [
            "create", "deploy", "install", "configure", "setup", "build"
        ])
        
        # Determine evaluation outcome
        if matching_orbs:
            evaluation_result = "match_found"
            action = "Found matching orbs for task"
        elif is_autonomous:
            evaluation_result = "autonomous_task"
            action = "Detected autonomous task pattern"
        else:
            evaluation_result = "needs_processing"
            action = "Task requires AI processing"
        
        # Create evaluation log
        log = Log(
            agent="james",
            task_id=payload.task_id,
            action=action,
            result=evaluation_result
        )
        db.add(log)
        db.commit()

        # Prepare response based on evaluation
        if evaluation_result == "match_found":
            options = ["Complete with James"]
            if detected_category != "james":
                options.append(f"Send to Agent: {detected_category}")
        elif evaluation_result == "autonomous_task":
            options = ["Complete with James", f"Send to Agent: {detected_category}"]
        else:
            options = [
                "Complete with James",
                "Send to Agent: whis",
                "Send to Agent: katie", 
                "Send to Agent: igris"
            ]

        return {
            "status": "evaluated",
            "task_id": payload.task_id,
            "detected_category": detected_category,
            "evaluation_result": evaluation_result,
            "is_autonomous": is_autonomous,
            "matching_orbs": [{"id": str(orb.id), "name": orb.name} for orb in matching_orbs],
            "options": options,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.post("/api/tasks/complete-with-james")
async def complete_with_james(task_id: str, db: Session = Depends(get_db)):
    """Complete a task internally with James"""
    try:
        log = Log(
            agent="james",
            task_id=task_id,
            action="Completed internally",
            result="success"
        )
        db.add(log)
        db.commit()
        
        return {
            "status": "done",
            "task_id": task_id,
            "agent": "james",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Completion failed: {str(e)}")

@router.post("/api/tasks/send-to-agent")
async def send_to_agent(task_id: str, agent: str, db: Session = Depends(get_db)):
    """Send a task to a specific agent for processing"""
    valid_agents = ["whis", "katie", "igris"]
    if agent not in valid_agents:
        raise HTTPException(status_code=400, detail=f"Invalid agent. Must be one of: {valid_agents}")
    
    try:
        log = Log(
            agent=agent,
            task_id=task_id,
            action="Received from James",
            result="queued"
        )
        db.add(log)
        db.commit()
        
        return {
            "status": "forwarded",
            "task_id": task_id,
            "agent": agent,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Forwarding failed: {str(e)}") 