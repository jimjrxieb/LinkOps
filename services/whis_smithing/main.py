from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.smithing_routes import router as smithing_router

app = FastAPI(
    title="Whis Smithing Service",
    description=(
        "Handles rune/orb generation, merging, and recurrence logic for "
        "Whis AI training"
    ),
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(smithing_router, prefix="/smithing")


@app.get("/")
async def root():
    return {"message": "Whis Smithing Service - Rune/Orb Logic Handler"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "whis_smithing"
    }


# Import routes (commented until routes are properly set up)
# from routes import smithing_routes
# app.include_router(smithing_routes.router, prefix="/api/v1/smithing", tags=["smithing"])
