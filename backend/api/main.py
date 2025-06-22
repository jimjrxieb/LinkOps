from fastapi import FastAPI
from api.routes import router as api_router
from gui.routes import router as gui_router
from api.whis import router as whis_router

app = FastAPI(
    title="LinkOps Core",
    version="0.1.0",
    description="Manage Orbs, Runes, Logs and ML input via GUI"
)

app.include_router(api_router)
app.include_router(gui_router)
app.include_router(whis_router)

@app.on_event("startup")
async def startup():
    """Initialize the application on startup"""
    from bootstrap import ensure_static_orbs
    ensure_static_orbs()

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 