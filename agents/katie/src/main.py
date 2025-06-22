from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI(title="Katie Agent")

class AgentTaskInput(BaseModel):
    task_text: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/execute")
def execute(data: AgentTaskInput):
    return {"agent": "katie", "received": data.task_text, "status": "executed (simulated)"} 