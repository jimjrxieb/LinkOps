from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from logic.flake8_lint_parser import Flake8LintParser
import requests
import logging

router = APIRouter(prefix="/lint", tags=["Lint Detection & Fix"])


class LintRequest(BaseModel):
    service_path: str
    max_line_length: Optional[int] = 88
    auto_fix: Optional[bool] = True


class LintResponse(BaseModel):
    status: str
    total_errors: int
    files_affected: int
    error_types: Dict[str, int]
    errors: List[Dict[str, Any]]
    fix_applied: bool = False
    fix_result: Optional[Dict[str, Any]] = None


@router.post("/flake8", response_model=LintResponse)
async def run_flake8_lint(request: LintRequest = Body(...)):
    """Run flake8 linting and optionally auto-fix errors"""
    try:
        parser = Flake8LintParser()

        # Run flake8 linting
        errors = parser.run_flake8(request.service_path, request.max_line_length)

        # Get error summary
        summary = parser.get_error_summary(errors)

        # If no errors, return clean status
        if not errors:
            return LintResponse(
                status="✅ No lint errors found",
                total_errors=0,
                files_affected=0,
                error_types={},
                errors=[],
                fix_applied=False,
            )

        # If auto-fix is enabled and there are errors, trigger fix
        fix_result = None
        if request.auto_fix and errors:
            fix_result = await trigger_lint_fix(request.service_path, errors, parser)

        return LintResponse(
            status=f"⚠️ Found {len(errors)} lint errors" if errors else "✅ Clean",
            total_errors=summary["total_errors"],
            files_affected=summary["files_affected"],
            error_types=summary["error_types"],
            errors=errors,
            fix_applied=fix_result.get("success", False) if fix_result else False,
            fix_result=fix_result,
        )

    except Exception as e:
        logging.error(f"Flake8 linting failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lint check failed: {str(e)}")


async def trigger_lint_fix(
    service_path: str, errors: List[Dict[str, Any]], parser: Flake8LintParser
) -> Dict[str, Any]:
    """Trigger lint fix via audit_migrate"""
    try:
        # Create detailed prompt for Cursor
        prompt = parser.create_cursor_prompt(errors)

        # Call audit_migrate patch endpoint
        response = requests.post(
            "http://audit_migrate:8007/patch",
            json={
                "prompt": prompt,
                "service_path": service_path,
                "error_summary": f"Found {len(errors)} flake8 lint errors",
                "patch_type": "lint_fix",
            },
            timeout=30,
        )

        if response.status_code == 200:
            return {
                "success": True,
                "patch_applied": True,
                "response": response.json(),
                "message": f"Applied fixes for {len(errors)} lint errors",
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
            "error": f"Failed to apply lint fixes: {str(e)}",
        }


@router.get("/health")
async def health_check():
    """Health check for lint service"""
    return {
        "status": "healthy",
        "service": "igris_lint",
        "capabilities": [
            "Flake8 lint error detection",
            "Lint error parsing and categorization",
            "Auto-fix triggering via audit_migrate",
            "Cursor integration for lint fixes",
        ],
    }
