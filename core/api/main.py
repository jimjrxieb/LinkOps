from fastapi import FastAPI
from core.api.routes import router as api_router
from core.gui.routes import router as gui_router

app = FastAPI(
    title="LinkOps Core",
    version="0.1.0",
    description="Manage Orbs, Runes, Logs and ML input via GUI"
)

app.include_router(api_router)
app.include_router(gui_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 