from fastapi import FastAPI
from routers import audit_router

app = FastAPI(
    title="Audit Logic Service",
    description=(
        "Best practices, GitOps rules, audit scoring criteria, and logic checklists"
    ),
    version="1.0.0",
)

app.include_router(audit_router.router)
