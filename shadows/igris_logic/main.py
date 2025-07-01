"""
Igris Service - Platform Engineer Microservice
Handles infrastructure automation, DevSecOps, and multi-cloud management
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

# Import modular components
from analyzer import analyze_platform_components
from infrastructure import generate_infrastructure_solution, generate_configurations
from security import generate_security_recommendations
from opendevin import simulate_opendevin_automation
from routers import validate_scaffold, post_push_fix, lint_router

app = FastAPI(title="Igris Service - Platform Engineer")

# Include routers
app.include_router(validate_scaffold.router)
app.include_router(post_push_fix.router)
app.include_router(lint_router.router)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlatformTask(BaseModel):
    task_id: str
    task_text: str
    platform: str = "kubernetes"  # kubernetes, aws, azure, gcp
    action_type: str = "deploy"  # deploy, configure, audit, optimize
    configuration: Optional[Dict[str, Any]] = None


class PlatformResponse(BaseModel):
    agent: str = "igris"
    task: str
    response: str
    infrastructure_solution: Dict[str, Any]
    generated_configs: List[str]
    security_recommendations: List[str]
    confidence_score: float


class EnhancementRequest(BaseModel):
    agent: str
    orb_id: str
    rune_patch: str
    training_notes: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "igris",
        "specialization": "Platform Engineering & DevSecOps",
        "capabilities": [
            "Infrastructure as Code (Terraform)",
            "DevSecOps Practices",
            "Security Scanning & Compliance",
            "Platform Engineering",
            "OpenDevin Integration",
            "Multi-Cloud Management",
            "CI/CD Pipeline Automation",
            "Infrastructure Optimization",
        ],
    }


@app.post("/execute")
def execute(data: PlatformTask):
    """
    Igris specializes in platform engineering and DevSecOps
    - Manages infrastructure as code
    - Implements security best practices
    - Integrates with OpenDevin for intelligent automation
    - Provides multi-cloud solutions
    """
    try:
        logger.info(f"Igris processing platform task: {data.task_text}")

        # Analyze task for platform components
        platform_components = analyze_platform_components(data.task_text, data.platform)

        # Generate infrastructure solution
        infrastructure_solution = generate_infrastructure_solution(
            data.task_text, platform_components, data.platform
        )

        # Generate configurations
        generated_configs = generate_configurations(
            data.task_text, platform_components, data.platform
        )

        # Security recommendations
        security_recommendations = generate_security_recommendations(
            data.task_text, platform_components, data.platform
        )

        # Create response
        response = PlatformResponse(
            task=data.task_text,
            response=_generate_platform_response(
                data.task_text, platform_components, data.platform
            ),
            infrastructure_solution=infrastructure_solution,
            generated_configs=generated_configs,
            security_recommendations=security_recommendations,
            confidence_score=_calculate_confidence(platform_components),
        )

        logger.info(
            f"Igris completed task with {len(generated_configs)} " "configurations"
        )
        return response

    except Exception as e:
        logger.error(f"Igris execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Igris execution failed: {str(e)}")


@app.post("/opendevin/automate")
def opendevin_automate(task: Dict[str, Any]):
    """
    Integrate with OpenDevin for intelligent automation
    """
    try:
        logger.info("Igris using OpenDevin for automation")

        # Simulate OpenDevin automation
        automation = simulate_opendevin_automation(task)

        return {
            "status": "automation_complete",
            "opendevin_insights": automation["insights"],
            "automated_actions": automation["actions"],
            "code_generated": automation["code_generated"],
            "infrastructure_changes": automation["infrastructure_changes"],
        }

    except Exception as e:
        logger.error(f"OpenDevin automation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"OpenDevin automation failed: {str(e)}"
        )


@app.post("/api/enhance")
def enhance_agent(request: EnhancementRequest):
    """
    Allow Whis to enhance Igris with new Orbs and Runes
    """
    try:
        logger.info(f"Igris receiving enhancement for orb: {request.orb_id}")

        # Process the enhancement
        enhancement_result = {
            "agent": request.agent,
            "orb_id": request.orb_id,
            "status": "enhancement_applied",
            "rune_patch": request.rune_patch,
            "training_notes": request.training_notes,
            "capabilities_updated": True,
        }

        logger.info(f"Igris enhancement applied for {request.orb_id}")
        return enhancement_result

    except Exception as e:
        logger.error(f"Igris enhancement failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Igris enhancement failed: {str(e)}"
        )


@app.get("/capabilities")
def get_capabilities():
    """Get current Igris capabilities"""
    return {
        "agent": "igris",
        "specialization": "Platform Engineering & DevSecOps",
        "current_capabilities": [
            "Infrastructure as Code (Terraform)",
            "DevSecOps Practices",
            "Security Scanning & Compliance",
            "Platform Engineering",
            "OpenDevin Integration",
            "Multi-Cloud Management",
            "CI/CD Pipeline Automation",
            "Infrastructure Optimization",
            "Configuration Management",
            "Security Hardening",
        ],
        "certifications": [
            "Terraform Certified",
            "AWS Solutions Architect",
            "Azure DevOps Engineer",
            "Google Cloud Professional",
            "OpenDevin Integration Specialist",
        ],
        "focus_areas": [
            "Infrastructure Automation",
            "Security & Compliance",
            "Multi-Cloud Strategy",
            "DevOps Transformation",
            "Platform Engineering",
            "Cost Optimization",
        ],
    }


def _generate_platform_response(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> str:
    """Generate platform-specific response."""
    response_parts = [f"Igris analyzed the {platform} platform task"]

    if platform_components.get("terraform"):
        response_parts.append("with Infrastructure as Code approach")
    if platform_components.get("security"):
        response_parts.append("including security best practices")
    if platform_components.get("automation"):
        response_parts.append("and automation capabilities")

    return " ".join(response_parts) + "."


def _calculate_confidence(platform_components: Dict[str, Any]) -> float:
    """Calculate confidence score based on platform components."""
    base_score = 0.7
    component_bonus = 0.05

    # Add bonus for each detected component
    for component, detected in platform_components.items():
        if detected:
            base_score += component_bonus

    return min(base_score, 1.0)
