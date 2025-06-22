# LinkOps James Workflow System

A complete task management and agent routing system that implements the James workflow with all four sections: Task Management, Q&A Training, AI Assistant Chat, Info Dump, and Image Extraction.

## 🏗️ Architecture Overview

The system is built around the **James Workflow** with four main sections:

### 🥇 1st Section: Task Section
- **Task Entry**: Submit job requests, tickets, or questions
- **Ranking**: AI agents (James, Katie, Igris) analyze using Orbs & Runes
- **Path A**: "Complete with James" → Suggested solution path (like ChatGPT)
- **Path B**: "Send to Agent" → Task done 100% autonomously
- **After Completion**: Results sanitized → stored in Whis Queue for nightly training

### 🧠 2nd Section: Q&A Input (Training Mode)
- **Input**: task_id, question, correct answer (exam-style)
- **What Happens**: Saved → Sanitized → Sent to Whis queue
- **Use Case**: Manual reinforcement learning for Whis

### 🧑‍💻 3rd Section: AI Assistant Chatbox
- **Role**: James, your LinkOps general AI
- **Features**:
  - Answers anything about LinkOps, your agents, and architecture
  - Handles follow-up on tasks
  - Feels like ChatGPT but knows your system deeply
  - Hosts "Complete with James" conversations

### 🗃️ 4th Section: Info Dump
- **Input**: Blog posts, cheat sheets, raw copy-paste
- **Action**: Auto-sanitized → Stored for Whis queue
- **Purpose**: Turns your reading into ML gold automatically

### 🖼️ 5th Section: Image Extraction
- **Input**: Upload or paste screenshots/diagrams
- **Action**: OCR (text extraction) → Sanitize → Add to Whis queue
- **Use Case**: Studying from diagrams, lab screenshots, or whiteboard notes

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

The server will start on `http://localhost:8000`

### 3. Access the API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### Task Management
- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Get all tasks (with filtering)
- `GET /api/tasks/{task_id}` - Get specific task
- `GET /api/tasks/{task_id}/analysis` - Get task analysis

### James Solutions
- `POST /api/tasks/{task_id}/james/solve` - Complete with James (Path A)
- `POST /api/tasks/{task_id}/agent-dispatch` - Send to Agent (Path B)

### Q&A Training
- `POST /api/qa` - Create Q&A pair for Whis training

### AI Assistant Chat
- `POST /api/chat` - Chat with James
- `GET /api/chat/history` - Get chat history

### Info Dump
- `POST /api/info-dump` - Process documents for Whis training

### Image Extraction
- `POST /api/image-extraction` - Extract text from images

### System
- `GET /` - Root endpoint with system info
- `GET /health` - Health check

## 💡 Usage Examples

### 1. Create a Task
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_input": "How do I restart a pod in Kubernetes?",
    "origin": "manager",
    "priority": "medium",
    "tags": ["kubernetes", "troubleshooting"]
  }'
```

### 2. Complete with James
```bash
curl -X POST "http://localhost:8000/api/tasks/{task_id}/james/solve"
```

### 3. Send to Agent
```bash
curl -X POST "http://localhost:8000/api/tasks/{task_id}/agent-dispatch" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "{task_id}",
    "agent_id": "katie"
  }'
```

### 4. Chat with James
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the best way to deploy a microservice?",
    "context": "deployment"
  }'
```

### 5. Create Q&A for Training
```bash
curl -X POST "http://localhost:8000/api/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "training-001",
    "question": "How do you scale a Kubernetes deployment?",
    "answer": "Use kubectl scale deployment <name> --replicas=<number>",
    "category": "kubernetes"
  }'
```

### 6. Process Info Dump
```bash
curl -X POST "http://localhost:8000/api/info-dump" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Kubernetes best practices: Always set resource limits...",
    "source": "blog",
    "category": "kubernetes"
  }'
```

## 🔄 Whis Training Loop

Everything in the system loops into Whis for nightly training:

1. **Task completions** (interactive + autonomous)
2. **Q&A entries**
3. **Info dumps**
4. **Extracted text from images**

This improves:
- Solution accuracy
- Task automation intelligence
- Agent adaptability (new orbs + runes)
- Agent recommendations in future tasks

## 🏗️ Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── core/
    ├── api/
    │   └── routes/
    │       └── tasks.py   # All API routes
    ├── logic/
    │   └── task_processor.py  # Task analysis logic
    └── db/
        └── memory.py      # In-memory data stores
```

## 🔧 Configuration

The system uses in-memory storage by default. For production:

1. Replace `core/db/memory.py` with database implementations
2. Add environment variables for configuration
3. Implement proper authentication and authorization
4. Add logging and monitoring

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=core

# Run specific test file
pytest tests/test_tasks.py
```

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t linkops-james .

# Run container
docker run -p 8000:8000 linkops-james
```

### Production Considerations
- Use a proper database (PostgreSQL, Redis)
- Add authentication and rate limiting
- Implement proper logging and monitoring
- Use environment variables for configuration
- Add health checks and graceful shutdown

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the LinkOps system. 