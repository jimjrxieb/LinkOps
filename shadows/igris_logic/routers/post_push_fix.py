from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import requests
from pathlib import Path
import logging

router = APIRouter(prefix="/post-push", tags=["Post-Push Error Detection & Fix"])


class PostPushFixRequest(BaseModel):
    service_path: str
    error_type: Optional[str] = None
    ci_logs: Optional[str] = None


class PostPushFixResponse(BaseModel):
    status: str
    error_detected: str
    patch_applied: bool
    patch_result: Dict[str, Any]
    next_steps: List[str]
    validation_score: int


@router.post("/fix", response_model=PostPushFixResponse)
async def post_push_fix(request: PostPushFixRequest = Body(...)):
    """Detect post-push errors and trigger Cursor patches via audit_migrate"""
    try:
        service_path = Path(request.service_path)

        # Step 1: Validate service path exists
        if not service_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Service path not found: {service_path}"
            )

        # Step 2: Diagnose errors
        error_summary = diagnose_error(
            service_path, request.error_type, request.ci_logs
        )

        if not error_summary:
            return PostPushFixResponse(
                status="✅ No errors detected",
                error_detected="None",
                patch_applied=False,
                patch_result={},
                next_steps=["Service is healthy, no action needed"],
                validation_score=100,
            )

        # Step 3: Trigger Cursor patch via audit_migrate
        patch_result = await fix_with_cursor(error_summary, str(service_path))

        # Step 4: Re-validate after patch
        validation_score = revalidate_service(service_path)

        # Step 5: Determine next steps
        next_steps = determine_next_steps(patch_result, validation_score)

        return PostPushFixResponse(
            status=(
                "🔧 Patch applied successfully"
                if patch_result.get("success")
                else "⚠️ Patch failed"
            ),
            error_detected=error_summary,
            patch_applied=patch_result.get("success", False),
            patch_result=patch_result,
            next_steps=next_steps,
            validation_score=validation_score,
        )

    except Exception as e:
        logging.error(f"Post-push fix failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Post-push fix failed: {str(e)}")


def diagnose_error(
    path: Path, error_type: Optional[str] = None, ci_logs: Optional[str] = None
) -> str:
    """Diagnose errors in the service"""
    errors = []

    # Check for missing critical files
    if not (path / "main.py").exists():
        errors.append("Missing main.py")

    if not (path / "Dockerfile").exists():
        errors.append("Missing Dockerfile")

    if not (path / "requirements.txt").exists():
        errors.append("Missing requirements.txt")

    # Check for missing directories
    if not (path / "routers").exists():
        errors.append("Missing routers/ folder")

    if not (path / "helm").exists():
        errors.append("Missing helm/ folder")

    # Check main.py content for common issues
    if (path / "main.py").exists():
        main_content = (path / "main.py").read_text()
        if "from fastapi import FastAPI" not in main_content:
            errors.append("Missing FastAPI import in main.py")
        if "app = FastAPI" not in main_content:
            errors.append("Missing FastAPI app initialization")
        if "@app.get" not in main_content and "@app.post" not in main_content:
            errors.append("Missing route handlers in main.py")

    # Check Dockerfile content
    if (path / "Dockerfile").exists():
        docker_content = (path / "Dockerfile").read_text()
        if "FROM python" not in docker_content:
            errors.append("Invalid Dockerfile base image")
        if "CMD" not in docker_content and "ENTRYPOINT" not in docker_content:
            errors.append("Missing CMD or ENTRYPOINT in Dockerfile")

    # Check CI workflow
    gha_dir = path / ".github" / "workflows"
    if not gha_dir.exists() or not any(gha_dir.glob("*.yml")):
        errors.append("Missing GitHub Actions workflow")

    # Check for specific error types
    if error_type:
        if error_type == "fastapi_crash":
            errors.append("FastAPI application crash detected")
        elif error_type == "docker_build_fail":
            errors.append("Docker build failure")
        elif error_type == "helm_deploy_fail":
            errors.append("Helm deployment failure")

    # Parse CI logs for specific errors
    if ci_logs:
        if "ModuleNotFoundError" in ci_logs:
            errors.append("Missing Python dependencies")
        if "ImportError" in ci_logs:
            errors.append("Import error in code")
        if "SyntaxError" in ci_logs:
            errors.append("Python syntax error")
        if "docker build failed" in ci_logs.lower():
            errors.append("Docker build failure")

    return "; ".join(errors) if errors else ""


async def fix_with_cursor(error_summary: str, service_path: str) -> Dict[str, Any]:
    """Trigger Cursor patch via audit_migrate"""
    try:
        # Create a detailed prompt for Cursor
        prompt = f"""
Fix the following FastAPI scaffold errors in {service_path}:

Errors detected: {error_summary}

Please provide fixes for:
1. Missing or incorrect files
2. FastAPI application structure issues
3. Docker configuration problems
4. CI/CD workflow issues

Return the corrected code/files that need to be updated.
"""

        # Call audit_migrate patch endpoint
        response = requests.post(
            "http://audit_migrate:8007/patch",
            json={
                "prompt": prompt,
                "service_path": service_path,
                "error_summary": error_summary,
            },
            timeout=30,
        )

        if response.status_code == 200:
            return {
                "success": True,
                "patch_applied": True,
                "response": response.json(),
                "message": "Patch applied successfully",
            }
        else:
            return {
                "success": False,
                "patch_applied": False,
                "error": f"Patch request failed: {response.status_code}",
                "response": response.text,
            }

    except Exception as e:
        return {
            "success": False,
            "patch_applied": False,
            "error": f"Failed to apply patch: {str(e)}",
        }


def revalidate_service(path: Path) -> int:
    """Re-validate service after patch application"""
    score = 0

    # Check critical files
    if (path / "main.py").exists():
        score += 20
    if (path / "Dockerfile").exists():
        score += 20
    if (path / "requirements.txt").exists():
        score += 20

    # Check directories
    if (path / "routers").exists():
        score += 15
    if (path / "helm").exists():
        score += 15

    # Check CI workflow
    gha_dir = path / ".github" / "workflows"
    if gha_dir.exists() and any(gha_dir.glob("*.yml")):
        score += 10

    return score


def determine_next_steps(
    patch_result: Dict[str, Any], validation_score: int
) -> List[str]:
    """Determine next steps based on patch result and validation score"""
    steps = []

    if patch_result.get("success"):
        steps.append("✅ Patch applied successfully")

        if validation_score >= 80:
            steps.append("✅ Service validation passed")
            steps.append("🚀 Ready for deployment")
        else:
            steps.append("⚠️ Service needs additional fixes")
            steps.append("🔄 Triggering additional patches")
    else:
        steps.append("❌ Patch application failed")
        steps.append("🔍 Manual intervention required")
        steps.append("📋 Review error logs for details")

    if validation_score < 50:
        steps.append("🚨 Critical issues detected - immediate attention needed")

    return steps


@router.get("/health")
async def health_check():
    """Health check for post-push fix service"""
    return {
        "status": "healthy",
        "service": "igris_post_push_fix",
        "capabilities": [
            "Error detection in scaffolded services",
            "Cursor patch triggering",
            "Service re-validation",
            "Automated fix application",
        ],
    }
