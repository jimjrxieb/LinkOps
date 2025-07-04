## === TEMPLATE SHADOW AGENT ===

# File: shadows/template_shadow_agent/main.py
from fastapi import FastAPI
from routers import main_router

app = FastAPI(title="Template Shadow Agent")

app.include_router(main_router.router)


# File: shadows/template_shadow_agent/routers/main_router.py
from fastapi import APIRouter

router = APIRouter(prefix="/template", tags=["TemplateAgent"])

@router.get("/ping")
def ping():
    return {"status": "🟢 Template agent is alive"}

@router.post("/execute")
def execute_task():
    # Replace with real logic
    return {"result": "Task executed successfully by template agent"}


# File: shadows/template_shadow_agent/logic/core.py
def core_logic(input_data):
    # Replace this with your agent's main logic
    return {"message": "Core logic executed", "input": input_data}


# File: shadows/template_shadow_agent/utils/helpers.py
def helper_function():
    return "This is a helper function for your shadow agent."


# File: shadows/template_shadow_agent/requirements.txt
fastapi
uvicorn
pydantic


# File: shadows/template_shadow_agent/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "800X"]
