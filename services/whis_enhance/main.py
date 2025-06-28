from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Whis Enhance Service",
    description="Handles agent enhancement, training, and approval logic for Whis AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Whis Enhance Service - Agent Enhancement Handler"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "whis_enhance"}

# Import routes (commented until routes are properly set up)
# from routes import enhance_routes
# app.include_router(enhance_routes.router, prefix="/api/v1/enhance", tags=["enhance"]) 