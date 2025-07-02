from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
from logic.generator import ServiceGenerator

router = APIRouter(prefix="/migrate", tags=["Service Migration"])


class ScaffoldPlan(BaseModel):
    services_to_generate: List[Dict[str, Any]]
    execution_steps: List[str]
    estimated_duration: str
    required_tools: List[str]
    next_actions: List[str]


class MigrationResult(BaseModel):
    status: str
    services_generated: List[str]
    output_directory: str
    generated_files: Dict[str, List[str]]
    errors: List[str] = []
    execution_summary: Dict[str, Any] = {}


@router.post("/", response_model=MigrationResult)
async def execute_migration(plan: ScaffoldPlan = Body(...)):
    """Execute migration based on scaffold plan from audit_assess"""
    try:
        generator = ServiceGenerator()
        result = await generator.generate_services(plan)

        # Add execution summary
        result["execution_summary"] = {
            "total_services": len(plan.services_to_generate),
            "successful_generations": len(result["services_generated"]),
            "failed_generations": len(result["errors"]),
            "estimated_duration": plan.estimated_duration,
            "required_tools": plan.required_tools,
            "next_actions": plan.next_actions,
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")
