from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
import subprocess

router = APIRouter(prefix="/patch", tags=["Cursor Patch Handler"])


class CursorPatchRequest(BaseModel):
    prompt: str
    service_path: str
    error_summary: str
    target_files: Optional[List[str]] = None
    patch_type: Optional[str] = "general"  # "general", "lint_fix", "scaffold_fix"


class CursorPatchResponse(BaseModel):
    status: str
    patch_applied: bool
    files_modified: List[str]
    git_commit_hash: Optional[str] = None
    git_push_status: str
    error_message: Optional[str] = None


@router.post("/", response_model=CursorPatchResponse)
async def apply_cursor_patch(request: CursorPatchRequest = Body(...)):
    """Apply Cursor-generated patches and auto-commit/push"""
    try:
        service_path = Path(request.service_path)

        # Step 1: Validate service path
        if not service_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Service path not found: {service_path}"
            )

        # Step 2: Generate patch using Cursor (or fallback)
        if request.patch_type == "lint_fix":
            patch_result = await generate_lint_patch(
                request.prompt, request.error_summary
            )
        else:
            patch_result = await generate_cursor_patch(
                request.prompt, request.error_summary
            )

        if not patch_result.get("success"):
            return CursorPatchResponse(
                status="❌ Patch generation failed",
                patch_applied=False,
                files_modified=[],
                git_commit_hash=None,
                git_push_status="skipped",
                error_message=patch_result.get("error", "Unknown error"),
            )

        # Step 3: Apply patches to files
        files_modified = apply_patches_to_files(service_path, patch_result["patches"])

        # Step 4: Git commit and push
        git_result = git_commit_and_push(
            service_path, f"fix: auto-patch from Cursor - {request.error_summary}"
        )

        return CursorPatchResponse(
            status="✅ Patch applied and pushed successfully",
            patch_applied=True,
            files_modified=files_modified,
            git_commit_hash=git_result.get("commit_hash"),
            git_push_status=git_result.get("push_status", "unknown"),
            error_message=None,
        )

    except Exception as e:
        logging.error(f"Cursor patch application failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Patch application failed: {str(e)}"
        )


async def generate_lint_patch(prompt: str, error_summary: str) -> Dict[str, Any]:
    """Generate lint-specific patches using Cursor or fallback"""
    try:
        # Try to use Cursor local service first
        cursor_result = await call_cursor_local(prompt)

        if cursor_result.get("success"):
            return {
                "success": True,
                "patches": cursor_result["patches"],
                "source": "cursor_local",
            }

        # Fallback to OpenAI or other AI service
        fallback_result = await call_openai_fallback(prompt)

        if fallback_result.get("success"):
            return {
                "success": True,
                "patches": fallback_result["patches"],
                "source": "openai_fallback",
            }

        # Generate lint-specific patches based on common flake8 errors
        lint_patches = generate_lint_specific_patches(error_summary)

        return {"success": True, "patches": lint_patches, "source": "lint_fallback"}

    except Exception as e:
        return {"success": False, "error": f"Failed to generate lint patch: {str(e)}"}


async def generate_cursor_patch(prompt: str, error_summary: str) -> Dict[str, Any]:
    """Generate patch using Cursor or fallback to OpenAI"""
    try:
        # Try to use Cursor local service first
        cursor_result = await call_cursor_local(prompt)

        if cursor_result.get("success"):
            return {
                "success": True,
                "patches": cursor_result["patches"],
                "source": "cursor_local",
            }

        # Fallback to OpenAI or other AI service
        fallback_result = await call_openai_fallback(prompt)

        if fallback_result.get("success"):
            return {
                "success": True,
                "patches": fallback_result["patches"],
                "source": "openai_fallback",
            }

        # Generate basic patches based on common errors
        basic_patches = generate_basic_patches(error_summary)

        return {"success": True, "patches": basic_patches, "source": "basic_fallback"}

    except Exception as e:
        return {"success": False, "error": f"Failed to generate patch: {str(e)}"}


async def call_cursor_local(prompt: str) -> Dict[str, Any]:
    """Call Cursor local service (placeholder)"""
    try:
        # This would be the actual Cursor API call
        # For now, return a placeholder response
        return {"success": False, "error": "Cursor local service not configured"}
    except Exception as e:
        return {"success": False, "error": f"Cursor local call failed: {str(e)}"}


async def call_openai_fallback(prompt: str) -> Dict[str, Any]:
    """Fallback to OpenAI for patch generation (placeholder)"""
    try:
        # This would be the actual OpenAI API call
        # For now, return a placeholder response
        return {"success": False, "error": "OpenAI fallback not configured"}
    except Exception as e:
        return {"success": False, "error": f"OpenAI fallback failed: {str(e)}"}


def generate_lint_specific_patches(error_summary: str) -> List[Dict[str, Any]]:
    """Generate lint-specific patches for common flake8 errors"""
    patches = []

    # Parse the error summary to extract specific lint errors
    if "F841" in error_summary and "unused variable" in error_summary:
        # Remove unused variables
        patches.append(
            {
                "file": "main.py",  # This would be dynamically determined
                "content": "# Remove unused variable 'repo' or other unused variables",
                "action": "comment_out",
                "lint_error": "F841",
            }
        )

    if "E401" in error_summary and "multiple imports" in error_summary:
        # Fix multiple imports on one line
        patches.append(
            {
                "file": "main.py",
                "content": """# Fix multiple imports - separate them:
from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Any""",
                "action": "replace",
                "lint_error": "E401",
            }
        )

    if "E501" in error_summary and "line too long" in error_summary:
        # Fix long lines
        patches.append(
            {
                "file": "main.py",
                "content": "# Break long lines into multiple lines",
                "action": "format",
                "lint_error": "E501",
            }
        )

    if "E302" in error_summary and "expected 2 blank lines" in error_summary:
        # Add blank lines before functions/classes
        patches.append(
            {
                "file": "main.py",
                "content": "\n\n# Add 2 blank lines before function/class definitions",
                "action": "insert",
                "lint_error": "E302",
            }
        )

    if "W291" in error_summary and "trailing whitespace" in error_summary:
        # Remove trailing whitespace
        patches.append(
            {
                "file": "main.py",
                "content": "# Remove trailing whitespace from all lines",
                "action": "clean",
                "lint_error": "W291",
            }
        )

    return patches


def generate_basic_patches(error_summary: str) -> List[Dict[str, Any]]:
    """Generate basic patches based on common error patterns"""
    patches = []

    if "Missing main.py" in error_summary:
        patches.append(
            {
                "file": "main.py",
                "content": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generated Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from generated service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
""",
                "action": "create",
            }
        )

    if "Missing Dockerfile" in error_summary:
        patches.append(
            {
                "file": "Dockerfile",
                "content": """FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
""",
                "action": "create",
            }
        )

    if "Missing requirements.txt" in error_summary:
        patches.append(
            {
                "file": "requirements.txt",
                "content": """fastapi
uvicorn[standard]
pydantic
""",
                "action": "create",
            }
        )

    if "Missing routers/ folder" in error_summary:
        patches.append(
            {
                "file": "routers/__init__.py",
                "content": "# Routers package\n",
                "action": "create",
            }
        )

        patches.append(
            {
                "file": "routers/main_router.py",
                "content": """from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["API"])

@router.get("/")
async def api_root():
    return {"message": "API is working"}
""",
                "action": "create",
            }
        )

    if "Missing helm/ folder" in error_summary:
        patches.append(
            {
                "file": "helm/Chart.yaml",
                "content": """apiVersion: v2
name: generated-service
description: Generated service chart
type: application
version: 0.1.0
appVersion: "1.0.0"
""",
                "action": "create",
            }
        )

        patches.append(
            {
                "file": "helm/values.yaml",
                "content": """replicaCount: 1

image:
  repository: generated-service
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
""",
                "action": "create",
            }
        )

    return patches


def apply_patches_to_files(
    service_path: Path, patches: List[Dict[str, Any]]
) -> List[str]:
    """Apply patches to files in the service directory"""
    files_modified = []

    for patch in patches:
        try:
            file_path = service_path / patch["file"]

            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if patch["action"] == "create":
                with open(file_path, "w") as f:
                    f.write(patch["content"])
                files_modified.append(patch["file"])

            elif patch["action"] == "update":
                with open(file_path, "w") as f:
                    f.write(patch["content"])
                files_modified.append(patch["file"])

            elif patch["action"] == "append":
                with open(file_path, "a") as f:
                    f.write(patch["content"])
                files_modified.append(patch["file"])

        except Exception as e:
            logging.error(f"Failed to apply patch to {patch['file']}: {str(e)}")

    return files_modified


def git_commit_and_push(path: Path, message: str) -> Dict[str, Any]:
    """Commit changes and push to remote repository"""
    try:
        # Check if git repository exists
        git_dir = path / ".git"
        if not git_dir.exists():
            # Initialize git repository
            subprocess.run(["git", "init"], cwd=path, check=True)

        # Add all changes
        subprocess.run(["git", "add", "."], cwd=path, check=True)

        # Commit changes
        commit_result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=path,
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract commit hash
        commit_hash = None
        if "commit" in commit_result.stdout:
            commit_hash = commit_result.stdout.split()[1]

        # Push to remote (if remote exists)
        try:
            _ = subprocess.run(
                ["git", "push"], cwd=path, capture_output=True, text=True, check=True
            )
            push_status = "success"
        except subprocess.CalledProcessError:
            push_status = "no_remote_or_auth_failed"

        return {
            "commit_hash": commit_hash,
            "push_status": push_status,
            "message": message,
        }

    except Exception as e:
        return {"commit_hash": None, "push_status": "failed", "error": str(e)}


@router.get("/health")
async def health_check():
    """Health check for cursor patch service"""
    return {
        "status": "healthy",
        "service": "audit_migrate_cursor_patch",
        "capabilities": [
            "Cursor patch generation",
            "File patch application",
            "Git auto-commit and push",
            "Error recovery",
        ],
    }
