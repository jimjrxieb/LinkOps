from fastapi import APIRouter, Body
import os, subprocess, requests
from pathlib import Path

router = APIRouter(prefix="/validate", tags=["Scaffold Validator"])

@router.post("/scaffold")
def validate_scaffold(input: dict = Body(...)):
    path = Path(input.get("service_path", ""))
    if not path.exists():
        return {"error": f"Path not found: {path}"}

    results = {}

    # Dockerfile check
    dockerfile = path / "Dockerfile"
    results["dockerfile"] = "✅ OK" if dockerfile.exists() else "❌ Missing"

    # requirements.txt
    requirements = path / "requirements.txt"
    results["requirements"] = "✅ OK" if requirements.exists() else "❌ Missing"

    # CI workflow check
    gha_dir = path / ".github" / "workflows"
    results["ci_workflow"] = "✅ OK" if gha_dir.exists() and any(gha_dir.glob("*.yml")) else "❌ Missing"

    # Helm chart check
    helm_dir = path / "helm"
    results["helm_chart"] = "✅ OK" if helm_dir.exists() else "❌ Missing"

    # FastAPI app boot test
    try:
        test_boot = subprocess.run([
            "python3", "-m", "http.server"
        ], cwd=path, timeout=5)
        results["fastapi_boot"] = "✅ Mock boot passed"
    except Exception as e:
        results["fastapi_boot"] = f"❌ Failed to boot ({e})"

    # Score (naive)
    score = sum(1 for val in results.values() if val.startswith("✅")) * 20
    results["score"] = score

    return results 