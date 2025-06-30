from fastapi import APIRouter
import os
import json

router = APIRouter(prefix="/api/scraper", tags=["Orbs/Runes"])


@router.get("/orbs/{agent}")
def list_orbs(agent: str):
    orb_dir = f"storage/orbs/{agent}"
    if not os.path.exists(orb_dir):
        os.makedirs(orb_dir, exist_ok=True)
        return {"orbs": [], "agent": agent}

    files = [f for f in os.listdir(orb_dir) if f.endswith(".json")]
    return {"orbs": files, "agent": agent}


@router.get("/runes/{agent}")
def list_runes(agent: str):
    rune_dir = f"storage/runes/{agent}"
    if not os.path.exists(rune_dir):
        os.makedirs(rune_dir, exist_ok=True)
        return {"runes": [], "agent": agent}

    files = [f for f in os.listdir(rune_dir) if f.endswith(".json")]
    return {"runes": files, "agent": agent}


@router.get("/orbs/{agent}/{filename}")
def read_orb(agent: str, filename: str):
    orb_path = f"storage/orbs/{agent}/{filename}"
    if not os.path.exists(orb_path):
        return {"error": "Orb file not found"}

    with open(orb_path) as f:
        return json.load(f)


@router.get("/runes/{agent}/{filename}")
def read_rune(agent: str, filename: str):
    rune_path = f"storage/runes/{agent}/{filename}"
    if not os.path.exists(rune_path):
        return {"error": "Rune file not found"}

    with open(rune_path) as f:
        return json.load(f)
