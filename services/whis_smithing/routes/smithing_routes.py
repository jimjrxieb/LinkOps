from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator import generate_rune
from merger import merge_runes
from recurrence import check_recurrence

router = APIRouter()

class RuneRequest(BaseModel):
    input_data: Dict[str, Any]
    rune_type: str = "standard"

class MergeRequest(BaseModel):
    runes: List[Dict[str, Any]]
    merge_strategy: str = "standard"

class RecurrenceRequest(BaseModel):
    rune_data: Dict[str, Any]
    threshold: float = 0.8

@router.post("/generate-rune")
async def generate_rune_endpoint(request: RuneRequest):
    """Generate a new rune based on input data"""
    try:
        result = generate_rune(request.input_data, request.rune_type)
        return {
            "status": "success",
            "rune": result,
            "message": "Rune generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rune generation failed: {str(e)}")

@router.post("/merge-runes")
async def merge_runes_endpoint(request: MergeRequest):
    """Merge multiple runes into a single enhanced rune"""
    try:
        result = merge_runes(request.runes, request.merge_strategy)
        return {
            "status": "success",
            "merged_rune": result,
            "message": "Runes merged successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rune merging failed: {str(e)}")

@router.post("/check-recurrence")
async def check_recurrence_endpoint(request: RecurrenceRequest):
    """Check for recurrence patterns in rune data"""
    try:
        result = check_recurrence(request.rune_data, request.threshold)
        return {
            "status": "success",
            "recurrence_detected": result,
            "message": "Recurrence check completed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recurrence check failed: {str(e)}")

@router.get("/smithing-status")
async def smithing_status():
    """Get the current status of the smithing service"""
    return {
        "status": "operational",
        "service": "whis_smithing",
        "capabilities": ["rune_generation", "rune_merging", "recurrence_detection"]
    } 