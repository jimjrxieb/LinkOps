# 🎭 FickNury Meta-Agent

## Overview

FickNury is the meta-agent controller that orchestrates other agents and makes deployment decisions based on intelligence from Whis. It handles agent creation, upgrades, and deployment across different environments.

## Capabilities

### Agent Orchestration
- **Agent Creation**: Creates new agents based on Whis intelligence
- **Agent Upgrades**: Upgrades existing agents with new capabilities
- **Agent Deployment**: Deploys agents to Docker, Kubernetes, or local environments
- **Version Management**: Tracks agent versions and deployment history

### Intelligence-Driven Decisions
- **Whis Integration**: Receives intelligence from Whis training system
- **Pattern Recognition**: Identifies when new agents are needed
- **Resource Optimization**: Optimizes agent deployment across clusters
- **Risk Assessment**: Evaluates deployment risks and impact

### Multi-Environment Deployment
- **Docker**: Containerized agent deployment
- **Kubernetes**: Cluster-based agent orchestration
- **Local**: Development and testing deployments
- **Hybrid**: Multi-environment agent distribution

## API Endpoints

### Health Check
```bash
GET /health
```

### Propose Agent
```bash
POST /propose-agent
{
  "task_id": "proposal-001",
  "agent_name": "new-security-agent",
  "agent_type": "new",
  "intelligence_source": "whis",
  "reasoning": "Repeated security scan patterns detected",
  "capabilities": ["security", "compliance", "automation"],
  "deployment_target": "kubernetes",
  "priority": "high"
}
```

### Deploy Agent
```bash
POST /deploy-agent
{
  "task_id": "deploy-001",
  "agent_name": "auditguard",
  "version": "1.0.0",
  "deployment_target": "kubernetes",
  "configuration": {
    "replicas": 2,
    "resources": {
      "cpu": "500m",
      "memory": "512Mi"
    }
  },
  "auto_approve": true
}
```

### Agent Status
```bash
GET /agent-status
```

## Decision Logic

### Auto-Approval Criteria
- **High Feasibility** (>0.8) + **High Impact** (>0.7) = Auto-approved
- **Medium Feasibility** (>0.6) + **Medium Impact** (>0.5) = Manual review required
- **Low Feasibility** or **Low Impact** = Rejected

### Intelligence Sources
- **Whis**: Training data and pattern recognition
- **Manual**: Direct user requests
- **External**: Third-party integrations and triggers

## Deployment Targets

| Target | Use Case | Advantages |
|--------|----------|------------|
| **Docker** | Development, testing | Fast deployment, easy debugging |
| **Kubernetes** | Production, scaling | High availability, auto-scaling |
| **Local** | Development, debugging | Direct access, quick iteration |

## Integration with Whis

FickNury receives intelligence from Whis through:
- **Pattern Analysis**: Identifies repeated tasks that could be automated
- **Capability Gaps**: Detects missing functionality that new agents could provide
- **Performance Metrics**: Monitors agent performance and suggests improvements
- **Resource Utilization**: Optimizes agent distribution based on usage patterns

## PwC-Aligned Logging

FickNury produces logs in the PwC-aligned format:

```json
{
  "agent": "ficknury",
  "task_id": "proposal-001",
  "action": "Approved AuditGuard deployment",
  "result": {
    "proposal": {...},
    "analysis": {...},
    "decision": {...},
    "deployment_result": {...}
  },
  "solution_path": "Agent version 1.0 live on Minikube",
  "error_outcome": null,
  "sanitized": true,
  "approved": true
}
```

## Deployment

```bash
# Build the container
docker build -t ficknury .

# Run the agent
docker run -p 8000:8000 -v /var/run/docker.sock:/var/run/docker.sock ficknury
```

## Configuration

### Environment Variables
- `KUBECONFIG`: Path to Kubernetes configuration
- `DOCKER_HOST`: Docker daemon socket
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

### Security Considerations
- **RBAC**: Kubernetes role-based access control
- **Network Policies**: Restrict agent communication
- **Secrets Management**: Secure credential handling
- **Audit Logging**: Track all deployment decisions

## Monitoring

### Health Checks
- Agent availability monitoring
- Deployment status tracking
- Resource utilization metrics
- Error rate monitoring

### Metrics
- Deployment success rate
- Agent creation frequency
- Intelligence processing time
- Resource optimization impact 