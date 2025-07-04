from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.smithing_routes import router as smithing_router
from pydantic import BaseModel
import csv
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

app = FastAPI(
    title="Whis Smithing Service - ORB & RUNE Generation",
    description=(
        "Handles rune/orb generation, merging, and recurrence logic for "
        "Whis AI training"
    ),
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

app.include_router(smithing_router, prefix="/smithing")


class Orb(BaseModel):
    """Orb - Structured knowledge representation"""

    orb_id: str
    name: str
    description: str
    category: str
    tags: List[str]
    knowledge_base: Dict[str, Any]
    confidence: float
    created_at: str
    updated_at: str


class Rune(BaseModel):
    """Rune - Executable action pattern"""

    rune_id: str
    name: str
    description: str
    orb_id: str
    action_type: str
    commands: List[str]
    parameters: Dict[str, Any]
    success_criteria: Dict[str, Any]
    created_at: str


class TrainingData(BaseModel):
    """Training data from CSV"""

    task_id: str
    title: str
    description: str
    tools_used: str
    commands: str
    solution_summary: str
    status: str
    tags: str
    confidence: float
    agent: str


@app.get("/")
async def root():
    return {"message": "Whis Smithing Service - Rune/Orb Logic Handler"}


@app.get("/health")
def health():
    """Basic health check"""
    return {"status": "healthy", "service": "whis_smithing"}


@app.post("/generate-orbs")
async def generate_orbs_from_training():
    """
    Generate ORBs from completed tasks in the training queue.
    """
    try:
        csv_file_path = "/app/training_queue.csv"
        orbs = []

        if not os.path.exists(csv_file_path):
            return {"status": "error", "message": "Training queue not found"}

        with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            completed_tasks = [row for row in reader if row["status"] == "completed"]

        # Group tasks by category/tags to create ORBs
        task_groups = {}
        for task in completed_tasks:
            category = (
                task.get("tags", "").split(",")[0].strip()
                if task.get("tags")
                else "general"
            )
            if category not in task_groups:
                task_groups[category] = []
            task_groups[category].append(task)

        # Generate ORBs for each group
        for category, tasks in task_groups.items():
            orb = create_orb_from_tasks(category, tasks)
            orbs.append(orb)

        # Save ORBs to file
        save_orbs(orbs)

        return {
            "status": "success",
            "orbs_generated": len(orbs),
            "orbs": [orb.dict() for orb in orbs],
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/generate-runes")
async def generate_runes_from_orbs():
    """
    Generate RUNEs from existing ORBs.
    """
    try:
        orbs = load_orbs()
        runes = []

        for orb in orbs:
            rune = create_rune_from_orb(orb)
            runes.append(rune)

        # Save RUNEs to file
        save_runes(runes)

        return {
            "status": "success",
            "runes_generated": len(runes),
            "runes": [rune.dict() for rune in runes],
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/orbs")
async def get_orbs():
    """Get all generated ORBs"""
    try:
        orbs = load_orbs()
        return {"orbs": [orb.dict() for orb in orbs]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/runes")
async def get_runes():
    """Get all generated RUNEs"""
    try:
        runes = load_runes()
        return {"runes": [rune.dict() for rune in runes]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/process-training-queue")
async def process_training_queue():
    """
    Complete pipeline: Generate ORBs and RUNEs from training queue.
    """
    try:
        # Step 1: Generate ORBs
        orbs_result = await generate_orbs_from_training()
        if orbs_result["status"] != "success":
            return orbs_result

        # Step 2: Generate RUNEs
        runes_result = await generate_runes_from_orbs()
        if runes_result["status"] != "success":
            return runes_result

        return {
            "status": "success",
            "orbs_generated": orbs_result["orbs_generated"],
            "runes_generated": runes_result["runes_generated"],
            "message": "Training queue processed successfully",
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


def create_orb_from_tasks(category: str, tasks: List[Dict[str, Any]]) -> Orb:
    """Create an ORB from a group of related tasks"""

    # Extract common patterns
    tools_used = set()
    commands = []
    success_patterns = []

    for task in tasks:
        if task.get("tools_used"):
            tools_used.update(task["tools_used"].split(","))
        if task.get("commands"):
            commands.append(task["commands"])
        if task.get("solution_summary"):
            success_patterns.append(task["solution_summary"])

    # Calculate confidence based on success rate
    success_rate = len([t for t in tasks if t.get("status") == "completed"]) / len(
        tasks
    )

    orb = Orb(
        orb_id=f"orb-{category.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}",
        name=f"{category.title()} Operations",
        description=f"Knowledge base for {category} operations based on {len(tasks)} completed tasks",
        category=category,
        tags=list(tools_used),
        knowledge_base={
            "tools_used": list(tools_used),
            "common_commands": commands,
            "success_patterns": success_patterns,
            "task_count": len(tasks),
            "success_rate": success_rate,
        },
        confidence=success_rate,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    )

    return orb


def create_rune_from_orb(orb: Orb) -> Rune:
    """Create a RUNE from an ORB"""

    # Extract the most common command pattern
    commands = orb.knowledge_base.get("common_commands", [])
    primary_command = commands[0] if commands else "echo 'No commands available'"

    rune = Rune(
        rune_id=f"rune-{orb.orb_id}",
        name=f"Execute {orb.name}",
        description=f"Execute {orb.description}",
        orb_id=orb.orb_id,
        action_type="command_execution",
        commands=[primary_command],
        parameters={
            "category": orb.category,
            "tools_required": orb.knowledge_base.get("tools_used", []),
            "estimated_time": "5m",
            "risk_level": "medium",
        },
        success_criteria={"exit_code": 0, "output_contains": "success", "timeout": 300},
        created_at=datetime.now().isoformat(),
    )

    return rune


def save_orbs(orbs: List[Orb]):
    """Save ORBs to JSON file"""
    orbs_file = "/app/orbs.json"
    with open(orbs_file, "w") as f:
        json.dump([orb.dict() for orb in orbs], f, indent=2)


def load_orbs() -> List[Orb]:
    """Load ORBs from JSON file"""
    orbs_file = "/app/orbs.json"
    if not os.path.exists(orbs_file):
        return []

    with open(orbs_file, "r") as f:
        data = json.load(f)
        return [Orb(**orb_data) for orb_data in data]


def save_runes(runes: List[Rune]):
    """Save RUNEs to JSON file"""
    runes_file = "/app/runes.json"
    with open(runes_file, "w") as f:
        json.dump([rune.dict() for rune in runes], f, indent=2)


def load_runes() -> List[Rune]:
    """Load RUNEs from JSON file"""
    runes_file = "/app/runes.json"
    if not os.path.exists(runes_file):
        return []

    with open(runes_file, "r") as f:
        data = json.load(f)
        return [Rune(**rune_data) for rune_data in data]


# Import routes (commented until routes are properly set up)
# from routes import smithing_routes
# app.include_router(smithing_routes.router, prefix="/api/v1/smithing"
# , tags=["smithing"])
