"""
Main FastAPI application for LinkOps James workflow
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import os

# Import routes
from core.api.routes.tasks import router as tasks_router
from core.api.routes.gui import router as gui_router
from routes.data_collect import router as data_collect_router
from routes.whis import router as whis_router

# Import stores for initialization
from core.db.memory import TASK_STORE, QA_STORE, INFO_DUMP_STORE, IMAGE_EXTRACTION_STORE, CHAT_HISTORY

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting LinkOps James workflow system...")
    print("📊 Initializing in-memory stores...")
    
    # Initialize stores with some sample data
    _initialize_sample_data()
    
    print("✅ LinkOps James workflow system ready!")
    yield
    
    # Shutdown
    print("🛑 Shutting down LinkOps James workflow system...")

def _initialize_sample_data():
    """Initialize stores with sample data for testing"""
    # Sample tasks
    sample_tasks = [
        {
            "id": "sample-task-1",
            "input": "How do I deploy a Kubernetes pod?",
            "origin": "manual",
            "priority": "medium",
            "tags": ["kubernetes", "deployment"],
            "status": "received",
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id": "sample-task-2", 
            "input": "Train a machine learning model for image classification",
            "origin": "manager",
            "priority": "high",
            "tags": ["ml", "ai", "training"],
            "status": "received",
            "created_at": "2024-01-01T00:00:00"
        }
    ]
    
    for task in sample_tasks:
        TASK_STORE[task["id"]] = task
    
    # Sample chat history
    sample_chat = [
        {
            "message": "Hello James, can you help me with Kubernetes?",
            "response": "Of course! I can help you with Kubernetes deployments, troubleshooting, and best practices. What specific issue are you facing?",
            "context": "general",
            "timestamp": "2024-01-01T00:00:00"
        }
    ]
    
    CHAT_HISTORY.extend(sample_chat)

# Create FastAPI app
app = FastAPI(
    title="LinkOps James Workflow",
    description="Complete James workflow system with task management, agent routing, and Whis training integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(gui_router, prefix="/api/gui", tags=["gui"])
app.include_router(data_collect_router, tags=["data-collection"])
app.include_router(whis_router, tags=["whis"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LinkOps James Workflow",
        "version": "1.0.0",
        "stores": {
            "tasks": len(TASK_STORE),
            "qa": len(QA_STORE),
            "info_dumps": len(INFO_DUMP_STORE),
            "image_extractions": len(IMAGE_EXTRACTION_STORE),
            "chat_history": len(CHAT_HISTORY)
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Welcome to LinkOps James Workflow System",
        "description": "Complete task management and agent routing system",
        "sections": {
            "🥇 Task Section": "Submit, analyze, and route tasks to agents",
            "🧠 Q&A Training": "Manual reinforcement learning for Whis",
            "🧑‍💻 AI Assistant": "Chat with James about LinkOps",
            "🗃️ Info Dump": "Process documents for Whis training",
            "🖼️ Image Extraction": "OCR and process images for training"
        },
        "endpoints": {
            "tasks": "/api/tasks",
            "qa": "/api/qa", 
            "chat": "/api/chat",
            "info-dump": "/api/info-dump",
            "image-extraction": "/api/image-extraction",
            "health": "/health"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "message": "The requested endpoint does not exist"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌐 Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production/Docker
        log_level="info"
    )
