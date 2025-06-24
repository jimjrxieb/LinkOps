from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from typing import Union, Dict
from utils.sanitizer import sanitize_task, sanitize_qna, sanitize_dump, sanitize_image
from core.logger import log_to_whis
from PIL import Image
import pytesseract
import io
from config.database import get_db
from sqlalchemy.orm import Session
from db.models import WhisQueue, Log
import uuid
from datetime import datetime

router = APIRouter()

class DataCollectRequest(BaseModel):
    type: str  # task | qna | dump | image
    content: Union[str, Dict]

@router.post("/api/data-collect/test")
async def test_sanitize_input(request: DataCollectRequest):
    """Test endpoint without database dependency"""
    sanitized = None

    if request.type == "task":
        sanitized = sanitize_task(request.content)
    elif request.type == "qna":
        sanitized = sanitize_qna(request.content)
    elif request.type == "dump":
        sanitized = sanitize_dump(request.content)
    elif request.type == "image":
        sanitized = sanitize_image(request.content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported input type.")

    print(f"[TEST] Sanitized {request.type}: {sanitized}")
    
    return {"status": "ok", "sanitized": sanitized, "message": "Test endpoint working"}

@router.post("/api/data-collect/sanitize")
async def sanitize_input(request: DataCollectRequest, db: Session = Depends(get_db)):
    sanitized = None

    if request.type == "task":
        sanitized = sanitize_task(request.content)
    elif request.type == "qna":
        sanitized = sanitize_qna(request.content)
    elif request.type == "dump":
        sanitized = sanitize_dump(request.content)
    elif request.type == "image":
        sanitized = sanitize_image(request.content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported input type.")

    # Create task_id for this submission
    task_id = f"data-collect-{uuid.uuid4().hex[:8]}"
    
    # Add to WhisQueue for training
    try:
        # Determine agent based on content
        agent = "james"  # Default agent
        if request.type == "qna":
            # For Q&A, check if it's Kubernetes related
            content_str = str(request.content).lower()
            if any(k in content_str for k in ["kubectl", "pod", "deployment", "kubernetes", "k8s"]):
                agent = "katie"
            elif any(k in content_str for k in ["terraform", "infrastructure", "cloud"]):
                agent = "igris"
            elif any(k in content_str for k in ["ml", "model", "training", "ai"]):
                agent = "whis"
        
        # Create WhisQueue entry
        whis_entry = WhisQueue(
            task_id=task_id,
            raw_text=str(sanitized),
            source="data-collection",
            status="pending",
            agent=agent
        )
        db.add(whis_entry)
        
        # Create log entry
        log_entry = Log(
            agent="data-collection",
            task_id=task_id,
            action=f"Data collection: {request.type}",
            result=f"Sanitized and queued for Whis training",
            sanitized=True,
            approved=False,
            auto_approved=False,
            compliance_tags='["GDPR"]'
        )
        db.add(log_entry)
        
        db.commit()
        
        print(f"[DATA-COLLECT] Added to Whis queue: {task_id} (agent: {agent})")
        
    except Exception as e:
        print(f"Database logging failed, using fallback: {e}")
        # Fallback logging without database
        log_to_whis({
            "source": "data-collection",
            "input_type": request.type,
            "sanitized": sanitized
        }, None)

    return {
        "status": "ok", 
        "sanitized": sanitized,
        "task_id": task_id,
        "queued_for_whis": True,
        "agent": agent
    }

@router.post("/api/data-collect/image-text")
async def extract_text_from_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)
        
        # Create task_id for this extraction
        task_id = f"image-extract-{uuid.uuid4().hex[:8]}"
        
        # Add to WhisQueue for training
        try:
            whis_entry = WhisQueue(
                task_id=task_id,
                raw_text=extracted_text.strip(),
                source="image-extraction",
                status="pending",
                agent="james"  # Default for image extraction
            )
            db.add(whis_entry)
            
            # Create log entry
            log_entry = Log(
                agent="data-collection",
                task_id=task_id,
                action="Image text extraction",
                result=f"Extracted text from {file.filename}",
                sanitized=True,
                approved=False,
                auto_approved=False,
                compliance_tags='["GDPR"]'
            )
            db.add(log_entry)
            
            db.commit()
            
            print(f"[DATA-COLLECT] Added image extraction to Whis queue: {task_id}")
            
        except Exception as e:
            print(f"Database logging failed for image: {e}")
            # Fallback logging without database
            log_to_whis({
                "source": "image-extraction",
                "filename": file.filename,
                "content_type": file.content_type,
                "extracted_text": extracted_text.strip()
            }, None)
        
        return {
            "text": extracted_text.strip(),
            "task_id": task_id,
            "queued_for_whis": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 