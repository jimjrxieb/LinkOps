from fastapi import APIRouter
import json
import os

router = APIRouter(prefix="/api/scraper", tags=["Agents"])

@router.get("/agents")
def get_agent_profiles():
    agent_file = "storage/agents/capabilities.json"
    if not os.path.exists(agent_file):
        # Create default capabilities if file doesn't exist
        default_capabilities = {
            "katie": ["create storageclass", "deploy pod", "scale deployment"],
            "igris": ["create terraform", "provision infrastructure"],
            "whis": ["train model", "fine-tune", "generate runes"],
            "audit": ["security scan", "compliance check"],
            "ficknury": ["evaluate tasks", "deploy agents", "verify completion"]
        }
        os.makedirs("storage/agents", exist_ok=True)
        with open(agent_file, "w") as f:
            json.dump(default_capabilities, f, indent=2)
    
    with open(agent_file) as f:
        return json.load(f) 