from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

app = FastAPI(
    title="Whis Enhance Service",
    description="Handles agent enhancement, training, and approval logic for Whis AI",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnhancementRequest(BaseModel):
    """Request for agent enhancement"""

    agent_id: str
    agent_type: str
    current_capabilities: List[str]
    target_improvements: List[str]
    context: Dict[str, Any]


class EnhancementResult(BaseModel):
    """Result of agent enhancement"""

    agent_id: str
    enhanced_capabilities: List[str]
    new_skills: List[str]
    confidence_boost: float
    enhancement_data: Dict[str, Any]


@app.get("/")
async def root():
    return {"message": "Whis Enhance Service - Agent Enhancement Handler"}


@app.get("/health")
def health():
    """Basic health check"""
    return {"status": "healthy", "service": "whis_enhance"}


@app.post("/enhance-agent")
async def enhance_agent(request: EnhancementRequest):
    """
    Enhance an agent using ORBs and RUNEs from the smithing service.
    """
    try:
        # Load ORBs and RUNEs from smithing service
        orbs = await load_orbs_from_smithing()
        runes = await load_runes_from_smithing()

        # Find relevant ORBs and RUNEs for this agent
        relevant_orbs = find_relevant_orbs(
            orbs, request.agent_type, request.target_improvements
        )
        relevant_runes = find_relevant_runes(
            runes, request.agent_type, request.target_improvements
        )

        # Generate enhancement plan
        enhancement_plan = create_enhancement_plan(
            request, relevant_orbs, relevant_runes
        )

        # Apply enhancements
        enhanced_capabilities = apply_enhancements(request, enhancement_plan)

        # Calculate confidence boost
        confidence_boost = calculate_confidence_boost(enhancement_plan)

        result = EnhancementResult(
            agent_id=request.agent_id,
            enhanced_capabilities=enhanced_capabilities,
            new_skills=enhancement_plan.get("new_skills", []),
            confidence_boost=confidence_boost,
            enhancement_data=enhancement_plan,
        )

        # Save enhancement record
        save_enhancement_record(result)

        return {
            "status": "success",
            "enhancement": result.dict(),
            "message": f"Agent {request.agent_id} enhanced successfully",
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/enhancement-history/{agent_id}")
async def get_enhancement_history(agent_id: str):
    """Get enhancement history for a specific agent"""
    try:
        history = load_enhancement_history(agent_id)
        return {"enhancement_history": history}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/bulk-enhance")
async def bulk_enhance_agents(agents: List[EnhancementRequest]):
    """
    Enhance multiple agents in batch.
    """
    try:
        results = []

        for agent_request in agents:
            result = await enhance_agent(agent_request)
            results.append(result)

        return {
            "status": "success",
            "enhanced_agents": len(results),
            "results": results,
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/capability-matrix")
async def get_capability_matrix():
    """
    Get a matrix of all agent capabilities and their enhancement levels.
    """
    try:
        # Load all enhancement records
        all_records = load_all_enhancement_records()

        # Create capability matrix
        matrix = create_capability_matrix(all_records)

        return {"capability_matrix": matrix}

    except Exception as e:
        return {"status": "error", "error": str(e)}


async def load_orbs_from_smithing() -> List[Dict[str, Any]]:
    """Load ORBs from the smithing service"""
    try:
        response = requests.get("http://whis_smithing:8000/orbs", timeout=10)
        if response.status_code == 200:
            return response.json().get("orbs", [])
        return []
    except Exception:
        return []


async def load_runes_from_smithing() -> List[Dict[str, Any]]:
    """Load RUNEs from the smithing service"""
    try:
        response = requests.get("http://whis_smithing:8000/runes", timeout=10)
        if response.status_code == 200:
            return response.json().get("runes", [])
        return []
    except Exception:
        return []


def find_relevant_orbs(
    orbs: List[Dict[str, Any]], agent_type: str, improvements: List[str]
) -> List[Dict[str, Any]]:
    """Find ORBs relevant to the agent type and target improvements"""
    relevant_orbs = []

    for orb in orbs:
        # Check if ORB category matches agent type
        if agent_type.lower() in orb.get("category", "").lower():
            relevant_orbs.append(orb)
            continue

        # Check if ORB tags match target improvements
        orb_tags = orb.get("tags", [])
        for improvement in improvements:
            if any(improvement.lower() in tag.lower() for tag in orb_tags):
                relevant_orbs.append(orb)
                break

    return relevant_orbs


def find_relevant_runes(
    runes: List[Dict[str, Any]], agent_type: str, improvements: List[str]
) -> List[Dict[str, Any]]:
    """Find RUNEs relevant to the agent type and target improvements"""
    relevant_runes = []

    for rune in runes:
        # Check if RUNE action type matches agent capabilities
        action_type = rune.get("action_type", "")
        if agent_type.lower() in action_type.lower():
            relevant_runes.append(rune)
            continue

        # Check if RUNE parameters match target improvements
        parameters = rune.get("parameters", {})
        for improvement in improvements:
            if any(
                improvement.lower() in str(value).lower()
                for value in parameters.values()
            ):
                relevant_runes.append(rune)
                break

    return relevant_runes


def create_enhancement_plan(
    request: EnhancementRequest, orbs: List[Dict[str, Any]], runes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create an enhancement plan for the agent"""

    new_skills = []
    enhanced_capabilities = []

    # Extract skills from ORBs
    for orb in orbs:
        knowledge_base = orb.get("knowledge_base", {})
        tools_used = knowledge_base.get("tools_used", [])
        new_skills.extend(tools_used)

        # Add category-specific capabilities
        category = orb.get("category", "")
        if category:
            enhanced_capabilities.append(f"{category}_operations")

    # Extract executable actions from RUNEs
    for rune in runes:
        action_type = rune.get("action_type", "")
        if action_type:
            enhanced_capabilities.append(f"{action_type}_execution")

        commands = rune.get("commands", [])
        if commands:
            enhanced_capabilities.append("automated_command_execution")

    # Remove duplicates
    new_skills = list(set(new_skills))
    enhanced_capabilities = list(set(enhanced_capabilities))

    return {
        "agent_id": request.agent_id,
        "agent_type": request.agent_type,
        "new_skills": new_skills,
        "enhanced_capabilities": enhanced_capabilities,
        "orbs_used": len(orbs),
        "runes_used": len(runes),
        "enhancement_timestamp": datetime.now().isoformat(),
    }


def apply_enhancements(request: EnhancementRequest, plan: Dict[str, Any]) -> List[str]:
    """Apply enhancements to the agent's capabilities"""

    # Combine current capabilities with new ones
    enhanced_capabilities = request.current_capabilities.copy()
    enhanced_capabilities.extend(plan.get("enhanced_capabilities", []))

    # Remove duplicates and sort
    enhanced_capabilities = sorted(list(set(enhanced_capabilities)))

    return enhanced_capabilities


def calculate_confidence_boost(plan: Dict[str, Any]) -> float:
    """Calculate the confidence boost from enhancements"""

    # Base confidence boost from number of ORBs and RUNEs used
    base_boost = (plan.get("orbs_used", 0) * 0.1) + (plan.get("runes_used", 0) * 0.05)

    # Additional boost from new skills
    skill_boost = len(plan.get("new_skills", [])) * 0.02

    # Cap the total boost at 0.5 (50%)
    total_boost = min(0.5, base_boost + skill_boost)

    return round(total_boost, 3)


def save_enhancement_record(result: EnhancementResult):
    """Save enhancement record to file"""
    enhancement_file = "/app/enhancement_records.json"

    # Load existing records
    records = []
    if os.path.exists(enhancement_file):
        with open(enhancement_file, "r") as f:
            records = json.load(f)

    # Add new record
    records.append(result.dict())

    # Save back to file
    with open(enhancement_file, "w") as f:
        json.dump(records, f, indent=2)


def load_enhancement_history(agent_id: str) -> List[Dict[str, Any]]:
    """Load enhancement history for a specific agent"""
    enhancement_file = "/app/enhancement_records.json"

    if not os.path.exists(enhancement_file):
        return []

    with open(enhancement_file, "r") as f:
        all_records = json.load(f)

    # Filter records for the specific agent
    agent_records = [
        record for record in all_records if record.get("agent_id") == agent_id
    ]

    return agent_records


def load_all_enhancement_records() -> List[Dict[str, Any]]:
    """Load all enhancement records"""
    enhancement_file = "/app/enhancement_records.json"

    if not os.path.exists(enhancement_file):
        return []

    with open(enhancement_file, "r") as f:
        return json.load(f)


def create_capability_matrix(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a capability matrix from enhancement records"""

    matrix = {}

    for record in records:
        agent_id = record.get("agent_id")
        if agent_id not in matrix:
            matrix[agent_id] = {
                "capabilities": [],
                "skills": [],
                "confidence_boost": 0.0,
                "enhancement_count": 0,
            }

        # Add capabilities
        capabilities = record.get("enhanced_capabilities", [])
        matrix[agent_id]["capabilities"].extend(capabilities)

        # Add skills
        skills = record.get("new_skills", [])
        matrix[agent_id]["skills"].extend(skills)

        # Update confidence boost
        matrix[agent_id]["confidence_boost"] += record.get("confidence_boost", 0.0)

        # Increment enhancement count
        matrix[agent_id]["enhancement_count"] += 1

    # Remove duplicates and finalize
    for agent_id in matrix:
        matrix[agent_id]["capabilities"] = sorted(
            list(set(matrix[agent_id]["capabilities"]))
        )
        matrix[agent_id]["skills"] = sorted(list(set(matrix[agent_id]["skills"])))
        matrix[agent_id]["confidence_boost"] = round(
            matrix[agent_id]["confidence_boost"], 3
        )

    return matrix


# Import routes (commented until routes are properly set up)
# from routes import enhance_routes
# app.include_router(enhance_routes.router, prefix="/api/v1/enhance", tags=["enhance"])
