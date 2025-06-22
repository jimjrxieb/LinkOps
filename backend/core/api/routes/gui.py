"""
GUI routes for LinkOps James workflow
Handles frontend-related endpoints and UI data.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, Any, List
import json
from datetime import datetime

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """Get dashboard data for the main dashboard view"""
    return {
        "james": {
            "orbs": {"current": 8, "desired": 10},
            "runes": {"current": 6, "desired": 9},
            "autonomy": 62,
            "suggestions": [
                "Add orb for 'systemctl troubleshooting'",
                "Refactor James router to support multi-agent fallback"
            ]
        },
        "whis": {
            "last_sync": "2025-06-22 04:13 UTC",
            "updated_orbs": 3,
            "created_runes": 2,
            "unmapped": [
                "openapi-to-kubectl conversion",
                "multi-agent runtime feedback"
            ]
        },
        "agents": [
            {"name": "Katie", "capabilities": ["K8s troubleshooting", "CKA tasks"]},
            {"name": "Igris", "capabilities": ["DevSecOps scripts", "Platform bootstrapping"]},
            {"name": "James", "capabilities": ["Manager Q&A", "Solution path retrieval"]},
            {"name": "Whis", "capabilities": ["AI learning", "Orbs & Runes training"]}
        ]
    }

@router.get("/whis")
async def get_whis_data():
    """Get Whis training pipeline data"""
    return {
        "queue": [
            {
                "id": "queue-1",
                "summary": "Task processing: Kubernetes deployment configuration",
                "type": "task",
                "priority": "medium",
                "created_at": "2024-01-01T10:00:00"
            },
            {
                "id": "queue-2",
                "summary": "Image extraction: k8s-architecture.png",
                "type": "image",
                "priority": "low",
                "created_at": "2024-01-01T09:30:00"
            },
            {
                "id": "queue-3",
                "summary": "Info dump: Kubernetes best practices article",
                "type": "content",
                "priority": "high",
                "created_at": "2024-01-01T09:00:00"
            }
        ],
        "approvals": [
            {
                "id": "approval-1",
                "description": "Approve new orb: 'kubernetes-deployment'",
                "type": "orb",
                "content": "Kubernetes deployment configuration patterns",
                "created_at": "2024-01-01T08:00:00"
            },
            {
                "id": "approval-2",
                "description": "Approve new rune: 'deploy-pod.yaml'",
                "type": "rune",
                "content": "Standard pod deployment template",
                "created_at": "2024-01-01T07:30:00"
            }
        ],
        "orbs": [
            {
                "id": "orb-1",
                "name": "kubernetes-ops",
                "description": "Kubernetes operations and management",
                "created_at": "2024-01-01T06:00:00"
            },
            {
                "id": "orb-2",
                "name": "ml-training",
                "description": "Machine learning model training",
                "created_at": "2024-01-01T05:30:00"
            },
            {
                "id": "orb-3",
                "name": "devsecops",
                "description": "DevSecOps practices and security",
                "created_at": "2024-01-01T05:00:00"
            },
            {
                "id": "orb-4",
                "name": "platform-engineering",
                "description": "Platform engineering and infrastructure",
                "created_at": "2024-01-01T04:30:00"
            }
        ],
        "runes": [
            {
                "id": "rune-1",
                "title": "deploy-pod.yaml",
                "description": "Kubernetes pod deployment template",
                "category": "kubernetes",
                "created_at": "2024-01-01T04:00:00"
            },
            {
                "id": "rune-2",
                "title": "ml-pipeline.py",
                "description": "Machine learning pipeline script",
                "category": "ml",
                "created_at": "2024-01-01T03:30:00"
            },
            {
                "id": "rune-3",
                "title": "security-scan.sh",
                "description": "Security scanning script",
                "category": "security",
                "created_at": "2024-01-01T03:00:00"
            },
            {
                "id": "rune-4",
                "title": "terraform-main.tf",
                "description": "Infrastructure as Code template",
                "category": "infrastructure",
                "created_at": "2024-01-01T02:30:00"
            },
            {
                "id": "rune-5",
                "title": "docker-compose.yml",
                "description": "Multi-container application setup",
                "category": "containerization",
                "created_at": "2024-01-01T02:00:00"
            },
            {
                "id": "rune-6",
                "title": "monitoring-dashboard.json",
                "description": "Monitoring dashboard configuration",
                "category": "monitoring",
                "created_at": "2024-01-01T01:30:00"
            }
        ],
        "capabilities": [
            {
                "name": "James",
                "abilities": ["task-routing", "coordination", "solution-building", "agent-management"]
            },
            {
                "name": "Whis",
                "abilities": ["ml-training", "orb-generation", "rune-creation", "content-processing"]
            },
            {
                "name": "Katie",
                "abilities": ["kubernetes-ops", "cka-certification", "cks-security", "cluster-management"]
            },
            {
                "name": "Igris",
                "abilities": ["devsecops", "platform-engineering", "security-scanning", "infrastructure-automation"]
            }
        ]
    }

@router.get("/james")
async def get_james_gui_info():
    """James UI endpoint - provides information about the James workflow interface"""
    return {
        "section": "James UI",
        "description": "Complete James workflow system with task management and agent routing",
        "features": {
            "🥇 Task Section": {
                "description": "Submit, analyze, and route tasks to agents",
                "endpoints": {
                    "create_task": "/api/tasks",
                    "get_tasks": "/api/tasks",
                    "james_solve": "/api/tasks/{task_id}/james/solve",
                    "agent_dispatch": "/api/tasks/{task_id}/agent-dispatch"
                }
            },
            "🧠 Q&A Training": {
                "description": "Manual reinforcement learning for Whis",
                "endpoints": {
                    "create_qa": "/api/qa"
                }
            },
            "🧑‍💻 AI Assistant": {
                "description": "Chat with James about LinkOps",
                "endpoints": {
                    "chat": "/api/chat",
                    "chat_history": "/api/chat/history"
                }
            },
            "🗃️ Info Dump": {
                "description": "Process documents for Whis training",
                "endpoints": {
                    "info_dump": "/api/info-dump"
                }
            },
            "🖼️ Image Extraction": {
                "description": "OCR and process images for training",
                "endpoints": {
                    "image_extraction": "/api/image-extraction"
                }
            }
        },
        "status": "active",
        "version": "1.0.0"
    }

@router.get("/james/status")
async def get_james_status():
    """Get James system status and health"""
    return {
        "status": "healthy",
        "service": "James Workflow System",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@router.get("/james/dashboard")
async def get_james_dashboard():
    """Get dashboard data for James UI"""
    # This would typically fetch real data from the stores
    # For now, return sample dashboard data
    return {
        "dashboard": {
            "recent_tasks": [
                {
                    "id": "sample-task-1",
                    "input": "How do I deploy a Kubernetes pod?",
                    "status": "received",
                    "priority": "medium",
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "sample-task-2",
                    "input": "Train a machine learning model for image classification",
                    "status": "received",
                    "priority": "high",
                    "created_at": "2024-01-01T00:00:00"
                }
            ],
            "agent_stats": {
                "katie": {"tasks": 5, "status": "active"},
                "igris": {"tasks": 3, "status": "active"},
                "whis": {"tasks": 2, "status": "active"},
                "james": {"tasks": 8, "status": "active"}
            },
            "whis_queue": {
                "pending": 12,
                "processed": 45,
                "total": 57
            }
        }
    }

@router.get("/james/tasks")
async def get_james_tasks():
    """Get tasks for James UI display"""
    # This would fetch from the task store
    return {
        "tasks": [
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
        ],
        "count": 2
    }

@router.get("/james/chat")
async def get_james_chat_history():
    """Get chat history for James UI"""
    # This would fetch from the chat store
    return {
        "history": [
            {
                "message": "Hello James, can you help me with Kubernetes?",
                "response": "Of course! I can help you with Kubernetes deployments, troubleshooting, and best practices. What specific issue are you facing?",
                "context": "general",
                "timestamp": "2024-01-01T00:00:00"
            }
        ]
    }

@router.get("/james/qa")
async def get_james_qa_pairs():
    """Get Q&A pairs for James UI"""
    # This would fetch from the QA store
    return {
        "qa_pairs": [
            {
                "id": "qa-1",
                "task_id": "training-001",
                "question": "How do you scale a Kubernetes deployment?",
                "answer": "Use kubectl scale deployment <name> --replicas=<number>",
                "category": "kubernetes",
                "created_at": "2024-01-01T00:00:00"
            }
        ]
    }

@router.get("/james/info-dumps")
async def get_james_info_dumps():
    """Get info dumps for James UI"""
    # This would fetch from the info dump store
    return {
        "info_dumps": [
            {
                "id": "info-1",
                "content": "Kubernetes best practices: Always set resource limits...",
                "source": "blog",
                "category": "kubernetes",
                "created_at": "2024-01-01T00:00:00"
            }
        ]
    }

@router.get("/james/image-extractions")
async def get_james_image_extractions():
    """Get image extractions for James UI"""
    # This would fetch from the image extraction store
    return {
        "image_extractions": [
            {
                "id": "img-1",
                "filename": "k8s-diagram.png",
                "extracted_text": "Kubernetes architecture diagram showing...",
                "description": "Kubernetes architecture overview",
                "created_at": "2024-01-01T00:00:00"
            }
        ]
    }

# HTML endpoints for direct UI access
@router.get("/james/html", response_class=HTMLResponse)
async def get_james_html():
    """Get James UI as HTML page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LinkOps James Workflow</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 3px; }
            .status { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🚀 LinkOps James Workflow System</h1>
        <p class="status">✅ System Status: Active</p>
        
        <div class="section">
            <h2>🥇 Task Section</h2>
            <p>Submit, analyze, and route tasks to agents</p>
            <div class="endpoint">POST /api/tasks - Create new task</div>
            <div class="endpoint">GET /api/tasks - Get all tasks</div>
            <div class="endpoint">POST /api/tasks/{id}/james/solve - Complete with James</div>
            <div class="endpoint">POST /api/tasks/{id}/agent-dispatch - Send to Agent</div>
        </div>
        
        <div class="section">
            <h2>🧠 Q&A Training</h2>
            <p>Manual reinforcement learning for Whis</p>
            <div class="endpoint">POST /api/qa - Create Q&A pair</div>
        </div>
        
        <div class="section">
            <h2>🧑‍💻 AI Assistant</h2>
            <p>Chat with James about LinkOps</p>
            <div class="endpoint">POST /api/chat - Chat with James</div>
            <div class="endpoint">GET /api/chat/history - Get chat history</div>
        </div>
        
        <div class="section">
            <h2>🗃️ Info Dump</h2>
            <p>Process documents for Whis training</p>
            <div class="endpoint">POST /api/info-dump - Process documents</div>
        </div>
        
        <div class="section">
            <h2>🖼️ Image Extraction</h2>
            <p>OCR and process images for training</p>
            <div class="endpoint">POST /api/image-extraction - Extract text from images</div>
        </div>
        
        <div class="section">
            <h2>📚 API Documentation</h2>
            <p><a href="/docs">Swagger UI</a> | <a href="/redoc">ReDoc</a></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/")
async def get_gui_root():
    """Root GUI endpoint"""
    return {
        "message": "LinkOps GUI Endpoints",
        "endpoints": {
            "james": "/gui/james",
            "james_status": "/gui/james/status",
            "james_dashboard": "/gui/james/dashboard",
            "james_html": "/gui/james/html"
        }
    } 