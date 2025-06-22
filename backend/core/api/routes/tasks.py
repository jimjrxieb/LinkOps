"""
Task routes for LinkOps James workflow
Handles task submission, analysis, and routing to agents.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from uuid import uuid4
import json
from datetime import datetime
import re

from core.logic.task_processor import analyze_task
from core.db.memory import get_task_store, get_qa_store, get_info_dump_store, get_image_extraction_store, get_chat_history_store

router = APIRouter()

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

class InfoDumpRequest(BaseModel):
    content: str
    source: Optional[str] = "manual"
    category: Optional[str] = "general"

class ChatMessageRequest(BaseModel):
    message: str
    context: Optional[str] = None

class AgentDispatchRequest(BaseModel):
    task_id: str
    agent_id: str

# 🥇 1st Section: Task Section

@router.post("/tasks")
async def create_task(request: TaskCreateRequest):
    """
    Step 1.1 - Task Entry
    Submit a job request, ticket, or question
    """
    task_id = str(uuid4())
    task_store = get_task_store()
    
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
    
    # Save to store
    task_store.create(task_data, task_id)
    
    # Step 1.2 - Ranking: AI agents analyze using Orbs & Runes
    analysis = analyze_task(request.task_input, task_id)
    
    # Update task with analysis
    task_data.update(analysis)
    task_store.update(task_id, analysis)
    
    return {
        "task_id": task_id,
        "task_input": request.task_input,
        "analysis": analysis,
        "message": "Task created and analyzed successfully. Ready for James to offer solutions."
    }

@router.get("/tasks")
async def get_tasks(
    status: Optional[str] = None,
    origin: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50
):
    """Get all tasks with optional filtering"""
    task_store = get_task_store()
    tasks = task_store.get_all()
    
    # Apply filters
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if origin:
        tasks = [t for t in tasks if t.get("origin") == origin]
    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]
    
    # Limit results
    tasks = tasks[:limit]
    
    return {
        "tasks": tasks,
        "count": len(tasks)
    }

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get a specific task by ID"""
    task_store = get_task_store()
    task = task_store.get(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.get("/tasks/{task_id}/analysis")
async def get_task_analysis(task_id: str):
    """Get analysis for a specific task"""
    task_store = get_task_store()
    task = task_store.get(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Return analysis data
    analysis_keys = [
        "agent_rankings", "recommended_agent", "confidence_score",
        "matching_orbs", "matching_runes", "priority", "complexity_score", "insights"
    ]
    
    analysis = {key: task.get(key) for key in analysis_keys if key in task}
    
    return {
        "task_id": task_id,
        "task_input": task.get("input"),
        "analysis": analysis
    }

# 🧭 Path A: "Complete with James"
@router.post("/tasks/{task_id}/james/solve")
async def james_solve_task(task_id: str):
    """
    Path A: Complete with James
    James provides a suggested solution path (like ChatGPT)
    """
    task_store = get_task_store()
    task = task_store.get(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get fresh analysis
    analysis = analyze_task(task["input"], task_id)
    
    # Build solution using orbs and runes
    solution = _build_james_solution(task["input"], analysis)
    
    # Log conversation for Whis
    _log_for_whis(task_id, task["input"], solution, "james_solve", agent=analysis.get("recommended_agent"), orb=None, rune=None)
    
    return {
        "task_id": task_id,
        "task_input": task["input"],
        "solution": solution,
        "analysis": analysis,
        "message": "James has provided a complete solution using available orbs and runes"
    }

# ⚡ Path B: "Send to Agent"
@router.post("/tasks/{task_id}/agent-dispatch")
async def dispatch_agent_task(task_id: str, request: AgentDispatchRequest):
    """
    Path B: Send to Agent
    Task done 100% autonomously by the specified agent
    """
    task_store = get_task_store()
    task = task_store.get(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Validate agent
    valid_agents = ["katie", "igris", "whis"]
    if request.agent_id.lower() not in valid_agents:
        raise HTTPException(status_code=400, detail=f"Invalid agent. Must be one of: {valid_agents}")
    
    # Update task status
    task_store.update(task_id, {
        "status": "assigned",
        "assigned_agent": request.agent_id.lower(),
        "assigned_at": datetime.utcnow().isoformat()
    })
    
    # Simulate agent execution
    result = await _execute_agent_task(task_id, request.agent_id.lower(), task["input"])
    
    # Log completion for Whis
    _log_for_whis(task_id, task["input"], str(result), f"{request.agent_id}_execution", agent=request.agent_id.lower())
    
    return {
        "task_id": task_id,
        "agent_id": request.agent_id,
        "status": "dispatched",
        "result": result,
        "message": f"Task dispatched to {request.agent_id} for autonomous execution"
    }

# 🧠 Q&A Input Section (Training Mode)
@router.post("/qa")
async def create_qa(request: QACreateRequest):
    """
    Q&A Input Section (Training Mode)
    Input: task_id, question, correct answer (exam-style)
    What Happens: Saved → Sanitized → Sent to Whis queue
    Use Case: Manual reinforcement learning for Whis
    """
    qa_store = get_qa_store()
    
    qa_data = {
        "task_id": request.task_id,
        "question": request.question,
        "answer": request.answer,
        "category": request.category,
        "created_at": datetime.utcnow().isoformat()
    }
    
    qa_id = qa_store.create(qa_data)
    
    # Log for Whis training
    _log_for_whis(request.task_id, request.question, request.answer, "qa_training", agent=request.category)
    
    return {
        "qa_id": qa_id,
        "task_id": request.task_id,
        "message": "Q&A pair saved and queued for Whis training"
    }

# 🧑‍💻 AI Assistant Chatbox
@router.post("/chat")
async def chat_with_james(request: ChatMessageRequest):
    """
    AI Assistant Chatbox
    Role: James, your LinkOps general AI
    Features:
    - Answers anything about LinkOps, your agents, and architecture
    - Handles follow-up on tasks
    - Feels like ChatGPT but knows your system deeply
    - Hosts "Complete with James" conversations
    """
    chat_store = get_chat_history_store()
    
    # Generate James response
    response = _generate_james_response(request.message, request.context)
    
    # Store chat history
    chat_data = {
        "message": request.message,
        "response": response,
        "context": request.context,
        "timestamp": datetime.utcnow().isoformat()
    }
    chat_store.create(chat_data)
    
    return {
        "message": request.message,
        "response": response,
        "context": request.context
    }

@router.get("/chat/history")
async def get_chat_history(limit: int = 20):
    """Get chat history"""
    chat_store = get_chat_history_store()
    history = chat_store.get_all()
    return {"history": history[-limit:]}

# 🗃️ Info Dump Section
@router.post("/info-dump")
async def create_info_dump(request: InfoDumpRequest):
    """
    Info Dump Section
    Input: Blog posts, cheat sheets, raw copy-paste
    Action: Auto-sanitized → Stored for Whis queue
    Purpose: Turns your reading into ML gold automatically
    """
    info_store = get_info_dump_store()
    
    # Sanitize content
    sanitized_content = _sanitize_content(request.content)
    
    info_data = {
        "content": sanitized_content,
        "original_content": request.content,
        "source": request.source,
        "category": request.category,
        "created_at": datetime.utcnow().isoformat()
    }
    
    info_id = info_store.create(info_data)
    
    # Log for Whis training
    _log_for_whis(f"info-dump-{info_id}", "Info dump", sanitized_content, "info_dump", orb=request.category)
    
    return {
        "info_id": info_id,
        "message": "Info dump processed and queued for Whis training"
    }

# 🖼️ Image Extraction Section
@router.post("/image-extraction")
async def extract_from_image(
    file: UploadFile = File(...),
    task_id: str = Body("image-extraction"),
    description: str = Body("")
):
    """
    Image Extraction Section
    Input: Upload or paste screenshots/diagrams
    Action: OCR (text extraction) → Sanitize → Add to Whis queue
    Use Case: Studying from diagrams, lab screenshots, or whiteboard notes
    """
    image_store = get_image_extraction_store()
    
    # Simulate OCR extraction (in real implementation, use OCR library)
    extracted_text = _extract_text_from_image(file)
    
    # Sanitize extracted text
    sanitized_text = _sanitize_content(extracted_text)
    
    image_data = {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "sanitized_text": sanitized_text,
        "description": description,
        "task_id": task_id,
        "created_at": datetime.utcnow().isoformat()
    }
    
    image_id = image_store.create(image_data)
    
    # Log for Whis training
    _log_for_whis(task_id, f"Image: {file.filename}", sanitized_text, "image_extraction", orb=description)
    
    return {
        "image_id": image_id,
        "extracted_text": extracted_text,
        "sanitized_text": sanitized_text,
        "message": "Image processed and queued for Whis training"
    }

# Helper functions
def _build_james_solution(task_input: str, analysis: Dict[str, Any]) -> str:
    """Build a natural language solution using orbs and runes"""
    solution_parts = []
    solution_parts.append(f"# Solution for: {task_input}\n")
    
    # Add analysis insights
    if analysis.get("insights"):
        solution_parts.append("## Analysis Insights")
        for insight in analysis["insights"]:
            solution_parts.append(f"- {insight}")
        solution_parts.append("")
    
    # Add recommended agent
    recommended_agent = analysis.get("recommended_agent", "unknown")
    solution_parts.append(f"## Recommended Agent: {recommended_agent.title()}")
    solution_parts.append(f"Confidence Score: {analysis.get('confidence_score', 0):.2f}")
    solution_parts.append("")
    
    # Add matching orbs
    matching_orbs = analysis.get("matching_orbs", [])
    if matching_orbs:
        solution_parts.append("## Relevant Knowledge Orbs")
        for orb in matching_orbs[:3]:  # Top 3 orbs
            solution_parts.append(f"### {orb['name']}")
            if orb.get('description'):
                solution_parts.append(f"{orb['description']}")
            solution_parts.append(f"Category: {orb.get('category', 'N/A')}")
            solution_parts.append("")
    
    # Add matching runes
    matching_runes = analysis.get("matching_runes", [])
    if matching_runes:
        solution_parts.append("## Available Implementation Runes")
        for rune in matching_runes[:3]:  # Top 3 runes
            solution_parts.append(f"### {rune['language']} Rune")
            if rune.get('script_path'):
                solution_parts.append(f"Path: {rune['script_path']}")
            if rune.get('script_content'):
                # Truncate long content
                content = rune['script_content'][:200] + "..." if len(rune['script_content']) > 200 else rune['script_content']
                solution_parts.append(f"Content: ```\n{content}\n```")
            solution_parts.append("")
    
    # Add step-by-step solution
    solution_parts.append("## Step-by-Step Solution")
    
    # Generate solution based on task type
    task_lower = task_input.lower()
    
    if any(word in task_lower for word in ["kubernetes", "k8s", "pod", "deployment"]):
        solution_parts.extend([
            "1. **Create Kubernetes Manifest**",
            "   - Define pod/deployment YAML",
            "   - Set resource limits and requests",
            "   - Configure health checks",
            "",
            "2. **Apply Configuration**",
            "   ```bash",
            "   kubectl apply -f deployment.yaml",
            "   ```",
            "",
            "3. **Verify Deployment**",
            "   ```bash",
            "   kubectl get pods",
            "   kubectl describe pod <pod-name>",
            "   ```"
        ])
    elif any(word in task_lower for word in ["terraform", "infrastructure", "iac"]):
        solution_parts.extend([
            "1. **Define Infrastructure**",
            "   - Create Terraform configuration files",
            "   - Define providers and resources",
            "   - Set up variables and outputs",
            "",
            "2. **Initialize and Plan**",
            "   ```bash",
            "   terraform init",
            "   terraform plan",
            "   ```",
            "",
            "3. **Apply Changes**",
            "   ```bash",
            "   terraform apply",
            "   ```"
        ])
    elif any(word in task_lower for word in ["train", "ml", "ai", "model"]):
        solution_parts.extend([
            "1. **Data Preparation**",
            "   - Collect and clean training data",
            "   - Split into train/validation sets",
            "   - Feature engineering",
            "",
            "2. **Model Training**",
            "   - Select appropriate algorithm",
            "   - Train model with hyperparameters",
            "   - Validate performance",
            "",
            "3. **Model Deployment**",
            "   - Save trained model",
            "   - Deploy to production environment",
            "   - Monitor performance"
        ])
    else:
        solution_parts.extend([
            "1. **Analyze Requirements**",
            "   - Break down the task into components",
            "   - Identify dependencies and constraints",
            "",
            "2. **Design Solution**",
            "   - Create implementation plan",
            "   - Select appropriate tools and technologies",
            "",
            "3. **Implement and Test**",
            "   - Execute the solution",
            "   - Validate results",
            "   - Document outcomes"
        ])
    
    solution_parts.append("")
    solution_parts.append("## Next Steps")
    solution_parts.append("- Review the solution above")
    solution_parts.append("- Customize based on your specific environment")
    solution_parts.append("- Test in a non-production environment first")
    solution_parts.append("- Consider security and compliance requirements")
    
    return "\n".join(solution_parts)

async def _execute_agent_task(task_id: str, agent_id: str, task_input: str) -> Dict[str, Any]:
    """Execute agent task asynchronously"""
    # Simulate agent execution
    if agent_id == "katie":
        return {
            "agent": "katie",
            "task_id": task_id,
            "status": "completed",
            "result": f"Katie executed infrastructure task: {task_input}",
            "output": {
                "kubernetes_manifests": ["deployment.yaml", "service.yaml"],
                "terraform_files": ["main.tf", "variables.tf"],
                "execution_time": "2.5s"
            }
        }
    elif agent_id == "igris":
        return {
            "agent": "igris",
            "task_id": task_id,
            "status": "completed",
            "result": f"Igris executed AI/ML task: {task_input}",
            "output": {
                "model_trained": True,
                "accuracy": 0.94,
                "training_time": "15m",
                "model_path": "/models/task_model.pkl"
            }
        }
    elif agent_id == "whis":
        return {
            "agent": "whis",
            "task_id": task_id,
            "status": "completed",
            "result": f"Whis executed knowledge task: {task_input}",
            "output": {
                "orbs_created": 2,
                "runes_generated": 3,
                "knowledge_indexed": True,
                "training_data_updated": True
            }
        }
    else:
        return {"status": "unknown_agent", "result": "Agent not implemented"}

def _generate_james_response(message: str, context: Optional[str] = None) -> str:
    """Generate James response for chat"""
    # Simple response generation (in real implementation, use LLM)
    responses = [
        "I can help you with that! Let me analyze your request and provide a solution.",
        "Based on your question, I'd recommend checking our knowledge base for similar cases.",
        "That's an interesting challenge. Let me break down the solution for you.",
        "I can see this involves multiple components. Let me guide you through the process.",
        "Great question! This is exactly the kind of task our agents are designed to handle."
    ]
    
    import random
    return random.choice(responses)

def _sanitize_content(content: str) -> str:
    """Sanitize content for Whis training"""
    # Remove sensitive information, normalize formatting, etc.
    # This is a simple implementation
    sanitized = content.strip()
    # Remove common sensitive patterns
    sanitized = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_ADDRESS]', sanitized)
    sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', sanitized)
    return sanitized

def _extract_text_from_image(file: UploadFile) -> str:
    """Extract text from image using OCR"""
    # Simulate OCR extraction
    # In real implementation, use libraries like pytesseract or cloud OCR services
    return f"Extracted text from {file.filename}:\nThis is simulated OCR text extraction.\nIn a real implementation, this would contain the actual text from the image."

def sanitize_for_whis(
    task_id: str,
    question: str,
    answer: str,
    source: str,
    agent: Optional[str] = None,
    orb: Optional[str] = None,
    rune: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sanitize and structure a task completion for Whis training.
    """
    def _sanitize(text: str) -> str:
        text = re.sub(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', '<ip>', text)  # IPs
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '<email>', text)  # emails
        text = re.sub(r'AKIA[0-9A-Z]{16}', '<aws_key>', text)  # AWS keys
        text = re.sub(r'(password|passwd|pwd)\s*[:=]\s*\S+', '<password>', text, flags=re.I)
        text = re.sub(r'(?i)token\s*[:=]\s*\S+', '<token>', text)
        text = re.sub(r'(?i)user(name)?\s*[:=]\s*\S+', '<user>', text)
        return text
    question = _sanitize(question).strip()
    answer = _sanitize(answer).strip()
    answer = re.sub(r'\r?\n', '\n', answer)
    answer = re.sub(r'\s+$', '', answer, flags=re.MULTILINE)
    answer = re.sub(r'\n{3,}', '\n\n', answer)
    if len(question) < 10 or '?' not in question:
        raise ValueError('Question is too short or unclear.')
    if len(answer) < 5:
        raise ValueError('Answer is too short.')
    whis_entry = {
        'task_id': task_id,
        'question': question,
        'answer': answer,
        'source': source,
        'agent': agent or '',
        'orb': orb or '',
        'rune': rune or ''
    }
    whis_entry = {k: v for k, v in whis_entry.items() if v}
    return whis_entry

def _log_for_whis(task_id: str, question: str, answer: str, source: str, agent: Optional[str] = None, orb: Optional[str] = None, rune: Optional[str] = None):
    """Log conversation for Whis training (sanitized)"""
    try:
        sanitized = sanitize_for_whis(task_id, question, answer, source, agent, orb, rune)
        print("[Whis Log] Sanitized for Whis:")
        print(sanitized)
        # Here you would push to Whis queue or DB
    except Exception as e:
        print(f"[Whis Log] Sanitize error: {e}") 