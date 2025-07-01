import httpx
from typing import Any, Dict


class ServiceConnector:
    def __init__(self):
        self.assess_base = "http://audit_assess:8005/scan"
        # In production, use service discovery or config

    async def call_audit_assess_scan(
        self, repo_url: str, branch: str = "main"
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.assess_base}/repo/",
                json={"repo_url": repo_url, "branch": branch},
            )
            resp.raise_for_status()
            return resp.json()

    async def call_audit_assess_suggestions(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.assess_base}/suggestions/")
            resp.raise_for_status()
            return resp.json()

    async def call_audit_assess_scaffold_plan(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.assess_base}/scaffold-plan/")
            resp.raise_for_status()
            return resp.json()
