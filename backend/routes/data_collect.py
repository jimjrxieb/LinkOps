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

router = APIRouter()

class DataCollectRequest(BaseModel):
    type: str  # task | qna | dump | image
    content: Union[str, Dict]

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

    # Log the sanitized data for Whis
    log_to_whis({
        "source": "data-collection",
        "input_type": request.type,
        "sanitized": sanitized
    }, db)

    return {"status": "ok", "sanitized": sanitized}

@router.post("/api/data-collect/image-text")
async def extract_text_from_image(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)
        
        # Log the extraction for Whis
        log_to_whis({
            "source": "image-extraction",
            "filename": file.filename,
            "content_type": file.content_type,
            "extracted_text": extracted_text.strip()
        })
        
        return {"text": extracted_text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 