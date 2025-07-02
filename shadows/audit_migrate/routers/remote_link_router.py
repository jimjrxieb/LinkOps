from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/link", tags=["Service Linking"])


class RepoScanRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"


class AssessPlanRequest(BaseModel):
    scaffold_plan: Dict[str, Any]


class LinkResult(BaseModel):
    status: str
    source: str
    services_generated: List[str]
    output_directory: str
    generated_files: Dict[str, List[str]]
    errors: List[str] = []
    execution_chain: List[str] = []


class RemoteLinkRequest(BaseModel):
    name: str
    url: str
    type: str


@router.post("/from-assess", response_model=LinkResult)
async def link_from_assess(request: AssessPlanRequest = Body(...)):
    """Receive scaffold plan from audit_assess and forward to migrate"""
    try:
        from routers.migrate_router import execute_migration, ScaffoldPlan

        # Convert to ScaffoldPlan format
        plan = ScaffoldPlan(**request.scaffold_plan)

        # Forward to migrate endpoint
        result = await execute_migration(plan)

        return LinkResult(
            status=result["status"],
            source="audit_assess",
            services_generated=result["services_generated"],
            output_directory=result["output_directory"],
            generated_files=result["generated_files"],
            errors=result["errors"],
            execution_chain=["audit_assess → audit_migrate"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Link from assess failed: {str(e)}"
        )


@router.post("/from-repo", response_model=LinkResult)
async def link_from_repo(request: RepoScanRequest = Body(...)):
    """Trigger full chain: audit_assess → audit_migrate"""
    try:
        # from .service_connector import ServiceConnector
        # Uncomment if you have this module

        class ServiceConnector:
            async def call_audit_assess_scan(self, repo_url, branch):
                pass

            async def call_audit_assess_suggestions(self):
                pass

            async def call_audit_assess_scaffold_plan(self):
                pass

        connector = ServiceConnector()
        execution_chain = []

        # Step 1: Call audit_assess to scan repository
        execution_chain.append("audit_assess.scan_repo")
        _ = await connector.call_audit_assess_scan(request.repo_url, request.branch)

        # Step 2: Get suggestions from audit_assess
        execution_chain.append("audit_assess.suggestions")
        _ = await connector.call_audit_assess_suggestions()

        # Step 3: Get scaffold plan from audit_assess
        execution_chain.append("audit_assess.scaffold_plan")
        scaffold_plan = await connector.call_audit_assess_scaffold_plan()

        # Step 4: Execute migration
        execution_chain.append("audit_migrate.migrate")
        from routers.migrate_router import execute_migration, ScaffoldPlan

        plan = ScaffoldPlan(**scaffold_plan)
        result = await execute_migration(plan)

        # Step 5: Optionally forward to Whis and Igris (future)
        # execution_chain.append("whis_logic.learn")
        # execution_chain.append("igris_logic.validate")

        return LinkResult(
            status=result["status"],
            source="repo_scan_chain",
            services_generated=result["services_generated"],
            output_directory=result["output_directory"],
            generated_files=result["generated_files"],
            errors=result["errors"],
            execution_chain=execution_chain,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Link from repo failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for the linking service"""
    return {
        "status": "healthy",
        "service": "audit_migrate_link",
        "connected_services": [
            "audit_assess",
            "audit_logic",
            "whis_logic",
            "igris_logic",
        ],
    }


@router.post("/remote-link/")
async def create_remote_link(request: RemoteLinkRequest = Body(...)) -> Dict[str, Any]:
    """Create a remote link to external system"""
    try:
        # Validate request
        if not request.name or not request.url:
            raise HTTPException(status_code=400, detail="Name and URL are required")

        # Create remote link
        remote_link = {
            "id": str(uuid.uuid4()),
            "name": request.name,
            "url": request.url,
            "type": request.type,
            "created_at": datetime.now().isoformat(),
            "status": "active",
        }

        return {
            "agent": "audit_migrate",
            "operation": "create_remote_link",
            "remote_link": remote_link,
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create remote link: {str(e)}"
        )


@router.get("/remote-links/")
async def get_remote_links() -> Dict[str, Any]:
    """Get all remote links"""
    try:
        # Mock remote links data
        remote_links = [
            {
                "id": "link-1",
                "name": "GitHub Repository",
                "url": "https://github.com/org/repo",
                "type": "repository",
                "created_at": "2024-01-01T00:00:00Z",
                "status": "active",
            },
            {
                "id": "link-2",
                "name": "JIRA Project",
                "url": "https://jira.company.com/project",
                "type": "issue_tracker",
                "created_at": "2024-01-02T00:00:00Z",
                "status": "active",
            },
        ]

        return {
            "agent": "audit_migrate",
            "operation": "get_remote_links",
            "remote_links": remote_links,
            "count": len(remote_links),
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get remote links: {str(e)}"
        )
