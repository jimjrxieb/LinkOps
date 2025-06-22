# LinkOps James Workflow Backend - Deployment Guide

## 🚀 Quick Deployment

### 1. Build and Start the Backend
```bash
# From the project root directory
docker-compose up -d backend
```

### 2. Verify Deployment
```bash
# Check if the container is running
docker ps | grep linkops-backend

# Check logs
docker logs linkops-backend

# Test the API
curl http://localhost:8000/health
curl http://localhost:8000/
```

### 3. Access the API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables
The backend uses these environment variables (set in docker-compose.yml):

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for enhanced features
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

### Health Checks
The container includes health checks that verify:
- Server is responding on port 8000
- `/health` endpoint returns 200 OK

## 📋 API Endpoints

### Core Endpoints
- `GET /` - System information and available endpoints
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Task Management
- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/{task_id}` - Get specific task
- `GET /api/tasks/{task_id}/analysis` - Get task analysis

### James Workflow
- `POST /api/tasks/{task_id}/james/solve` - Complete with James (Path A)
- `POST /api/tasks/{task_id}/agent-dispatch` - Send to Agent (Path B)

### Training & Chat
- `POST /api/qa` - Create Q&A pair for Whis training
- `POST /api/chat` - Chat with James
- `GET /api/chat/history` - Get chat history

### Data Processing
- `POST /api/info-dump` - Process documents for Whis training
- `POST /api/image-extraction` - Extract text from images

## 🧪 Testing

### Run Tests
```bash
# Test the deployed backend
python3 test_docker.py

# Or use curl
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_input": "How do I restart a Kubernetes pod?",
    "origin": "manager",
    "priority": "medium",
    "tags": ["kubernetes", "troubleshooting"]
  }'
```

## 🔍 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check logs
   docker logs linkops-backend
   
   # Check if port 8000 is available
   netstat -tulpn | grep 8000
   ```

2. **Health check failing**
   ```bash
   # Check if the app is running inside the container
   docker exec linkops-backend curl http://localhost:8000/health
   ```

3. **Import errors**
   ```bash
   # Rebuild the container
   docker-compose build backend
   docker-compose up -d backend
   ```

### Logs
```bash
# View real-time logs
docker logs -f linkops-backend

# View last 100 lines
docker logs --tail 100 linkops-backend
```

## 🔄 Updates

### Update the Backend
```bash
# Stop the current container
docker-compose stop backend

# Rebuild and start
docker-compose build backend
docker-compose up -d backend
```

### Full System Update
```bash
# Update all services
docker-compose down
docker-compose build
docker-compose up -d
```

## 📊 Monitoring

### Container Status
```bash
# Check container status
docker ps -a | grep linkops

# Check resource usage
docker stats linkops-backend
```

### API Monitoring
```bash
# Monitor health endpoint
watch -n 5 'curl -s http://localhost:8000/health | jq'
```

## 🎯 What's New in This Version

### ✅ New James Workflow System
- Complete task management with agent routing
- Path A: "Complete with James" with chat-style solutions
- Path B: "Send to Agent" for autonomous execution
- Q&A training system for Whis
- AI assistant chat with James
- Info dump and image extraction processing

### ✅ Sanitization for Whis
- Automatic removal of sensitive data (IPs, emails, tokens)
- Standardized formatting for ML training
- Structured output for Whis queue

### ✅ Docker Optimization
- Multi-stage build for smaller images
- Health checks for reliability
- Proper logging and error handling
- Environment-based configuration

## 🚀 Next Steps

1. **Test the API endpoints** using the Swagger UI
2. **Create some sample tasks** to see the workflow in action
3. **Try the chat feature** to interact with James
4. **Add Q&A pairs** for Whis training
5. **Process some documents** through the info dump feature

The new James workflow system is now ready for production use! 