from fastapi import APIRouter
from logic.executor import deploy_agent

router = APIRouter(prefix="/api/ficknury", tags=["Agent Deployment"])

@router.post("/deploy-agent")
def deploy(payload: dict):
    result = deploy_agent(payload)
    return result 