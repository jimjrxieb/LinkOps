from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
from executor import deploy_agent
from verifier import verify_task_completion
from fallback import handle_automation_failure

app = FastAPI(title="FickNury Deploy")


class DeploymentRequest(BaseModel):
    task_id: str
    agent: str
    rune_script: str
    task_description: str


@app.post("/api/launch")
async def launch_agent_task(req: DeploymentRequest):
    task = req.dict()
    result = deploy_agent(task)

    if result["status"] == "failed":
        fallback = handle_automation_failure(
            req.task_id, result["error"], req.task_description
        )
        return {"status": "fallback_triggered", "fallback": fallback}

    return {"status": "success", "result": result}


@app.get("/api/status/{task_id}")
def get_task_status(task_id: str):
    return verify_task_completion(task_id)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "healthy", "service": "ficknury-deploy"} 