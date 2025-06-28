"""
LinkOps Core - Streamlined Whis Training Pipeline
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.digest import router as digest_router
from routes.logs import router as logs_router

app = FastAPI(title="LinkOps API Gateway", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "LinkOps API Gateway"}


# Include routers
app.include_router(digest_router)
app.include_router(logs_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
