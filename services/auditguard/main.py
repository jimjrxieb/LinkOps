"""
AuditGuard Service - PwC-aligned Security & Compliance Microservice
Handles security scans, repository audits, and compliance tagging
"""

from fastapi import FastAPI
import logging

# Import routes
from routes import all_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AuditGuard Service",
    description="Security & Compliance Specialist Microservice",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include all routes
for route in all_routes:
    app.include_router(route)


# Root endpoint
@app.get("/")
def root():
    """Root endpoint with service information."""
    return {
        "service": "AuditGuard",
        "version": "1.0.0",
        "description": "Security & Compliance Specialist Microservice",
        "endpoints": {
            "health": "/health",
            "audit": "/audit",
            "compliance": "/compliance",
            "security": "/security",
            "docs": "/docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
