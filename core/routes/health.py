"""
Health check routes for monitoring and status
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import psutil
import os

from config.database import get_db
from config.kafka import get_kafka_manager
from config.settings import get_settings

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "LinkOps Core"
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with database and system metrics"""
    settings = get_settings()
    
    # Check database connection
    db_status = "healthy"
    try:
        db.execute("SELECT 1")
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check Kafka connection
    kafka_status = "healthy"
    try:
        kafka_manager = get_kafka_manager()
        producer = kafka_manager.get_producer()
        # Simple test - this would need proper error handling in production
    except Exception as e:
        kafka_status = f"unhealthy: {str(e)}"
    
    # System metrics
    system_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    
    # Check if directories exist
    directories = {
        "screenshots": os.path.exists(settings.SCREENSHOTS_DIR),
        "logs": os.path.exists(settings.LOGS_DIR)
    }
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "LinkOps Core",
        "database": db_status,
        "kafka": kafka_status,
        "system": system_info,
        "directories": directories
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes"""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/live")
async def liveness_check():
    """Liveness check for Kubernetes"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
