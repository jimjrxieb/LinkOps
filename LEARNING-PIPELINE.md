# LinkOps Learning Pipeline

## 🧠 Overview

The LinkOps Learning Pipeline is an intelligent task routing and learning system that automatically evaluates, routes, and learns from tasks to improve automation capabilities over time.

## 🏗️ Architecture

```
Task Input → FickNury Evaluator → Task Router → Agent Assignment
                                    ↓
                              Confidence Score
                                    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   High Conf.    │  Medium Conf.   │   Low Conf.     │
│   (≥0.95)       │   (≥0.7)        │   (<0.7)        │
│                 │                 │                 │
│ Direct Agent    │ Whis Learning   │ Manual Review   │
│ Assignment      │                 │                 │
│                 │                 │                 │
│ • Katie Logic   │ • Whis Logic    │ • James Logic   │
│ • Igris Logic   │ • Training      │ • Manual Export │
│ • Audit Logic   │   Queue         │ • CSV Tracking  │
└─────────────────┴─────────────────┴─────────────────┘
```

## 🔧 Components

### 1. FickNury Evaluator (`ficknury_evaluator`)
- **Purpose**: Task evaluation and routing
- **Port**: 8008
- **Key Files**: `task_router.py`, `main.py`
- **Endpoints**:
  - `POST /evaluate` - Evaluate and route tasks
  - `GET /health` - Health check

### 2. James Logic (`james_logic`)
- **Purpose**: Manual task review and export
- **Port**: 8002
- **Key Files**: `manual_task_export.py`
- **Endpoints**:
  - `POST /manual/manual-review` - Save manual tasks
  - `POST /manual/complete-task` - Mark tasks complete
  - `GET /manual/pending-tasks` - List pending tasks

### 3. Whis Data Input (`whis_data_input`)
- **Purpose**: Learning queue management
- **Port**: 8004
- **Key Files**: `training_queue.csv`
- **Endpoints**:
  - `POST /learn` - Add tasks to learning queue

## 📊 Training Queue Structure

The `training_queue.csv` file tracks all tasks for learning:

```csv
task_id,title,description,tools_used,commands,solution_summary,status,tags,confidence,agent,created_at,completed_at
TASK-001,Deploy Helm Chart,Create Helm chart for microservice,helm kubectl,"helm create mychart; helm install ...",Successfully deployed,completed,"k8s,helm,deployment",0.95,katie_logic,2024-01-15T10:30:00,2024-01-15T11:15:00
```

## 🚀 Usage

### 1. Submit a Task

```python
import requests

task = {
    "task_id": "TASK-001",
    "title": "Deploy Helm Chart",
    "description": "Create and deploy a Helm chart for our new microservice",
    "priority": "high",
    "category": "deployment",
    "tags": ["helm", "kubernetes", "deployment"]
}

response = requests.post("http://localhost:8008/evaluate", json=task)
evaluation = response.json()

print(f"Confidence: {evaluation['confidence']}")
print(f"Agent: {evaluation['agent']}")
print(f"Status: {evaluation['status']}")
```

### 2. Check Task Status

```python
# Get pending tasks
response = requests.get("http://localhost:8002/manual/pending-tasks")
pending_tasks = response.json()

# Get training statistics
response = requests.get("http://localhost:8002/manual/training-stats")
stats = response.json()
```

### 3. Complete Manual Tasks

```python
solution = {
    "task_id": "TASK-001",
    "tools_used": ["helm", "kubectl"],
    "commands": ["helm create mychart", "helm install mychart ./mychart"],
    "solution_summary": "Successfully deployed using Helm chart",
    "status": "completed",
    "tags": ["k8s", "helm", "deployment"]
}

response = requests.post("http://localhost:8002/manual/complete-task", json=solution)
```

## 🎯 Confidence Scoring

The system calculates confidence based on:

### High Confidence Keywords (0.3 each)
- Infrastructure: `helm`, `terraform`, `kubernetes`, `k8s`, `docker`
- Security: `security`, `audit`, `compliance`, `migration`
- Cloud: `aws`, `azure`, `gcp`, `cloud`, `ci/cd`

### Medium Confidence Keywords (0.1 each)
- Development: `test`, `testing`, `monitor`, `logging`, `debug`
- Operations: `fix`, `update`, `upgrade`, `install`, `configure`

### Adjustments
- **Category Bonus**: Infrastructure/Security (+0.1), Development (+0.05)
- **Priority Penalty**: High priority tasks (-0.1) for extra caution

## 🔄 Learning Flow

1. **Task Submission** → FickNury evaluates confidence
2. **High Confidence (≥0.95)** → Direct agent assignment
3. **Medium Confidence (≥0.7)** → Whis learning queue
4. **Low Confidence (<0.7)** → Manual review via James
5. **Manual Completion** → Solution saved to training queue
6. **Export to Whis** → Completed tasks used for training

## 📈 Monitoring

### Key Metrics
- Total tasks processed
- Tasks by agent
- Average confidence scores
- Success rates
- Learning queue size

### Health Checks
```bash
# Check all services
curl http://localhost:8008/health  # FickNury
curl http://localhost:8002/health  # James
curl http://localhost:8004/health  # Whis Data Input
```

## 🧪 Testing

Run the test suite:

```bash
python test_learning_pipeline.py
```

This will:
- Test task evaluation and routing
- Test manual task export
- Test learning queue functionality
- Check service health

## 🔮 Future Enhancements

1. **Machine Learning Integration**
   - Train models on completed tasks
   - Predict confidence scores
   - Suggest optimal agents

2. **Advanced Routing**
   - Load balancing across agents
   - Priority-based queuing
   - SLA monitoring

3. **Analytics Dashboard**
   - Real-time metrics
   - Performance trends
   - Learning progress

4. **Automated Deployment**
   - Confidence threshold triggers
   - Automatic agent scaling
   - Self-healing capabilities

## 🛠️ Development

### Adding New Agents

1. Create agent service in `shadows/`
2. Add Helm chart in `helm/`
3. Update `helmfile.yaml`
4. Add routing logic in `task_router.py`

### Customizing Confidence Scoring

Modify the `calculate_confidence()` function in `task_router.py`:

```python
def calculate_confidence(task: Task) -> float:
    # Add your custom logic here
    # Return confidence score between 0.0 and 1.0
    pass
```

### Extending Training Data

The `training_queue.csv` can be extended with additional columns:

```csv
task_id,title,description,tools_used,commands,solution_summary,status,tags,confidence,agent,created_at,completed_at,complexity,estimated_time,actual_time,success_rate
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Helm Charts](https://helm.sh/docs/)
- [Kubernetes](https://kubernetes.io/docs/)
- [MLOps Best Practices](https://mlops.community/)

---

**Built with ❤️ by Shadow Link Industries** 