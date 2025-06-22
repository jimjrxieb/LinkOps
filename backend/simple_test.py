#!/usr/bin/env python3
"""
Simple test server for LinkOps James Workflow
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from uuid import uuid4
import json
from datetime import datetime

app = FastAPI(title="LinkOps James Workflow - Simple Test")

# In-memory storage
TASK_STORE = {}
QA_STORE = {}
CHAT_HISTORY = []

# Pydantic models
class TaskCreateRequest(BaseModel):
    task_input: str
    origin: str = "manual"
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = None

class QACreateRequest(BaseModel):
    task_id: str
    question: str
    answer: str
    category: Optional[str] = "general"

class ChatMessageRequest(BaseModel):
    message: str
    context: Optional[str] = None

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
            "health": "/health"
        }
    }

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
            "chat_history": len(CHAT_HISTORY)
        }
    }

# Task endpoints
@app.post("/api/tasks")
async def create_task(request: TaskCreateRequest):
    """Create a new task"""
    task_id = str(uuid4())
    
    # Create task data
    task_data = {
        "id": task_id,
        "input": request.task_input,
        "origin": request.origin,
        "priority": request.priority,
        "tags": request.tags or [],
        "status": "received",
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Simple analysis
    analysis = {
        "task_id": task_id,
        "task_input": request.task_input,
        "agent_rankings": {
            "katie": 85 if "kubernetes" in request.task_input.lower() else 20,
            "igris": 90 if "ml" in request.task_input.lower() or "ai" in request.task_input.lower() else 15,
            "whis": 75 if "knowledge" in request.task_input.lower() else 25,
            "james": 60
        },
        "recommended_agent": "katie" if "kubernetes" in request.task_input.lower() else "james",
        "confidence_score": 0.85,
        "priority": request.priority,
        "complexity_score": 0.6,
        "insights": ["Task analyzed successfully"],
        "status": "analyzed"
    }
    
    # Save to store
    TASK_STORE[task_id] = {**task_data, **analysis}
    
    return {
        "task_id": task_id,
        "task_input": request.task_input,
        "analysis": analysis,
        "message": "Task created and analyzed successfully. Ready for James to offer solutions."
    }

@app.get("/api/tasks")
async def get_tasks():
    """Get all tasks"""
    tasks = list(TASK_STORE.values())
    return {
        "tasks": tasks,
        "count": len(tasks)
    }

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """Get a specific task by ID"""
    task = TASK_STORE.get(task_id)
    if not task:
        return {"error": "Task not found"}
    return task

@app.post("/api/tasks/{task_id}/james/solve")
async def james_solve_task(task_id: str):
    """Complete with James"""
    task = TASK_STORE.get(task_id)
    if not task:
        return {"error": "Task not found"}
    
    solution = f"""# Solution for: {task['input']}

## Analysis Insights
- This task involves {task.get('recommended_agent', 'general')} expertise
- Priority: {task.get('priority', 'medium')}
- Complexity: {task.get('complexity_score', 0.5):.1f}

## Step-by-Step Solution
1. **Analyze the problem**
   - Understand the requirements
   - Identify key components

2. **Implement solution**
   - Use appropriate tools and techniques
   - Follow best practices

3. **Verify results**
   - Test the solution
   - Document outcomes

## Next Steps
- Review the solution above
- Customize based on your specific environment
- Test in a non-production environment first
"""
    
    return {
        "task_id": task_id,
        "task_input": task["input"],
        "solution": solution,
        "message": "James has provided a complete solution"
    }

# Q&A endpoints
@app.post("/api/qa")
async def create_qa(request: QACreateRequest):
    """Create Q&A pair for training"""
    qa_id = str(uuid4())
    
    qa_data = {
        "id": qa_id,
        "task_id": request.task_id,
        "question": request.question,
        "answer": request.answer,
        "category": request.category,
        "created_at": datetime.utcnow().isoformat()
    }
    
    QA_STORE[qa_id] = qa_data
    
    return {
        "qa_id": qa_id,
        "task_id": request.task_id,
        "message": "Q&A pair saved and queued for Whis training"
    }

# Chat endpoints
@app.post("/api/chat")
async def chat_with_james(request: ChatMessageRequest):
    """Chat with James"""
    response = "I can help you with that! Let me analyze your request and provide a solution."
    
    chat_data = {
        "message": request.message,
        "response": response,
        "context": request.context,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    CHAT_HISTORY.append(chat_data)
    
    return {
        "message": request.message,
        "response": response,
        "context": request.context
    }

@app.get("/api/chat/history")
async def get_chat_history():
    """Get chat history"""
    return {"history": CHAT_HISTORY}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 