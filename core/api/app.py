"""
FastAPI application factory and configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from config.settings import get_settings
from core.routes import health, api


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description="LinkOps Core - A FastAPI microservice following MLOps best practices",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )
    
    # Include routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(api.router, prefix="/api/v1", tags=["api"])
    
    # Add startup and shutdown events
    @app.on_event("startup")
    async def startup_event():
        """Application startup event"""
        # Initialize database
        from config.database import init_db
        init_db()
        
        # Create necessary directories
        import os
        os.makedirs(settings.SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(settings.LOGS_DIR, exist_ok=True)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Application shutdown event"""
        # Close Kafka connections
        from config.kafka import get_kafka_manager
        kafka_manager = get_kafka_manager()
        kafka_manager.close()
    
    return app
