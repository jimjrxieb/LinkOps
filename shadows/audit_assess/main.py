from fastapi import FastAPI
from routers import scan_router

app = FastAPI(
    title="Audit Assess Service",
    description="GitHub repository scanning, analysis, and GitOps assessment tool",
    version="1.0.0",
)

app.include_router(scan_router.router)
