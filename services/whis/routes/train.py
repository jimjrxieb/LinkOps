from fastapi import APIRouter
from pydantic import BaseModel
from logic.generator import process_batch
from logic.categorizer import categorize_input
from logic.updater import update_training_data

router = APIRouter(prefix="/api/whis", tags=["Training"])

class TrainingPayload(BaseModel):
    input_type: str
    payload: dict

@router.post("/train")
def receive_training_data(data: TrainingPayload):
    """Receive training data from sanitizer and other services"""
    print(f"[WHIS] Received training data: {data.input_type}")
    
    try:
        # Categorize the input
        category = categorize_input(data.input_type, data.payload)
        
        # Update training data
        update_training_data(data.input_type, data.payload, category)
        
        return {
            "status": "received", 
            "type": data.input_type,
            "category": category,
            "message": "Training data processed successfully"
        }
    except Exception as e:
        print(f"[WHIS] Error processing training data: {str(e)}")
        return {
            "status": "error",
            "type": data.input_type,
            "error": str(e)
        }

@router.post("/train-nightly")
def trigger_training():
    """Trigger nightly batch training process"""
    processed = process_batch()
    return {"status": "done", "processed": len(processed)} 