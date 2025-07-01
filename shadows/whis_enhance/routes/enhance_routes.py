import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from updater import update_agent
from routes.train import train_agent
from routes.approvals import approve_enhancement

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()


class TrainingRequest(BaseModel):
    training_data: Dict[str, Any]
    model_config: Dict[str, Any] = {}
    epochs: int = 10


class UpdateRequest(BaseModel):
    agent_data: Dict[str, Any]
    enhancement_type: str = "standard"


class ApprovalRequest(BaseModel):
    enhancement_id: str
    approved: bool
    feedback: str = ""


@router.post("/train-agent")
async def train_agent_endpoint(request: TrainingRequest):
    """Train the Whis agent with new data"""
    try:
        result = train_agent(
            request.training_data, request.model_config, request.epochs
        )
        return {
            "status": "success",
            "training_result": result,
            "message": "Agent training completed successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent training failed: {str(e)}")


@router.post("/update-agent")
async def update_agent_endpoint(request: UpdateRequest):
    """Update the Whis agent with enhancements"""
    try:
        result = update_agent(request.agent_data, request.enhancement_type)
        return {
            "status": "success",
            "update_result": result,
            "message": "Agent updated successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent update failed: {str(e)}")


@router.post("/approve-enhancement")
async def approve_enhancement_endpoint(request: ApprovalRequest):
    """Approve or reject an enhancement"""
    try:
        result = approve_enhancement(
            request.enhancement_id, request.approved, request.feedback
        )
        return {
            "status": "success",
            "approval_result": result,
            "message": "Enhancement approval processed",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Enhancement approval failed: {str(e)}"
        )


@router.get("/enhancement-status")
async def enhancement_status():
    """Get the current status of the enhancement service"""
    return {
        "status": "operational",
        "service": "whis_enhance",
        "capabilities": ["agent_training", "agent_updates", "enhancement_approvals"],
    }
