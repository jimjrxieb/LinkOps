# 🧭 LinkOps PwC-Aligned Upgrade Guide

## Overview

This guide documents the transformation of LinkOps from a general AI agent platform to a PwC-aligned AI audit platform with comprehensive security, compliance, and orchestration capabilities.

## 🎯 What Changed

### New Agent Framework

| Agent | Role | New Capabilities |
|-------|------|------------------|
| **James** | General intake, task router, evaluator | Enhanced with PwC-aligned logging |
| **Whis** | Training engine, Rune builder | Filters by `sanitized: true && (approved: true \|\| auto_approved)` |
| **Katie** | Kubernetes operations, CKA/CKS-level tasks | Enhanced with compliance tagging |
| **Igris** | Platform engineer (infra, cloud, cost optimization) | Enhanced with security scanning |
| **AuditGuard** | 🆕 PwC-aligned audit agent | Security scans, repo audits, compliance tagging |
| **FickNury** | 🆕 Meta-agent orchestrator | Creates, upgrades, and deploys other agents |

### PwC-Aligned Logging Model

The logging system now includes:

```json
{
  "agent": "auditguard",
  "task_id": "audit-001",
  "action": "Trivy scan complete",
  "result": {
    "high_risk": 2,
    "notes": "[SECRET_DETECTED] Placeholder inserted",
    "compliance_tags": ["SOC2", "GDPR"]
  },
  "solution_path": "Rotate GitHub secrets + enable image scanning",
  "error_outcome": null,
  "sanitized": true,
  "approved": false,
  "auto_approved": false,
  "compliance_tags": ["SOC2", "GDPR"]
}
```

### Enhanced Whis Training

- **Filtering**: Only uses logs with `sanitized: true && (approved: true || auto_approved)`
- **Compliance Tags**: Runes carry compliance tags for filtering and reporting
- **Solution Paths**: Each rune includes recommended solution paths
- **Error Handling**: Failed operations create fallback logic

## 🚀 Quick Start

### 1. Run the Upgrade Script

```bash
./upgrade-to-pwc.sh
```

This script will:
- Run database migrations
- Build new agents (AuditGuard, FickNury)
- Update docker-compose.yml
- Create PwC-aligned orbs
- Start all services

### 2. Access the Platform

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **AuditGuard**: http://localhost:8001
- **FickNury**: http://localhost:8002

### 3. Run Your First Audit

```bash
# Run a security scan
curl -X POST http://localhost:8000/api/auditguard/scan \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "trivy",
    "target": "/app",
    "compliance_scope": ["SOC2", "GDPR"],
    "auto_approve": false
  }'
```

## 🛡️ AuditGuard Agent

### Capabilities

- **Trivy**: Container and filesystem vulnerability scanning
- **Bandit**: Python security linting
- **Checkov**: Infrastructure as Code security scanning
- **Snyk**: Dependency vulnerability scanning
- **Semgrep**: Static code analysis
- **Repository Auditing**: Secrets detection, credentials scanning

### Usage

```bash
# Security scan
POST /api/auditguard/scan
{
  "scan_type": "trivy",
  "target": "/app",
  "compliance_scope": ["SOC2", "GDPR"],
  "auto_approve": false
}

# Repository audit
POST /api/auditguard/scan
{
  "scan_type": "repo_audit",
  "target": "/path/to/repo",
  "compliance_scope": ["ISO27001", "NIST"],
  "auto_approve": true
}
```

### Compliance Frameworks

- **SOC2**: Service Organization Control 2
- **GDPR**: General Data Protection Regulation
- **ISO27001**: Information security management
- **NIST**: National Institute of Standards and Technology
- **SOX**: Sarbanes-Oxley Act
- **PCI-DSS**: Payment Card Industry Data Security Standard

## 🎭 FickNury Meta-Agent

### Capabilities

- **Agent Creation**: Creates new agents based on Whis intelligence
- **Agent Upgrades**: Upgrades existing agents with new capabilities
- **Agent Deployment**: Deploys agents to Docker, Kubernetes, or local environments
- **Version Management**: Tracks agent versions and deployment history

### Usage

```bash
# Propose new agent
POST /api/ficknury/propose-agent
{
  "agent_name": "new-security-agent",
  "agent_type": "new",
  "intelligence_source": "whis",
  "reasoning": "Repeated security scan patterns detected",
  "capabilities": ["security", "compliance", "automation"],
  "deployment_target": "kubernetes",
  "priority": "high"
}

# Deploy agent
POST /api/ficknury/deploy-agent
{
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

### Decision Logic

- **High Feasibility** (>0.8) + **High Impact** (>0.7) = Auto-approved
- **Medium Feasibility** (>0.6) + **Medium Impact** (>0.5) = Manual review required
- **Low Feasibility** or **Low Impact** = Rejected

## 📊 PwC Dashboard

### Features

- **Compliance Overview**: Real-time compliance statistics
- **Audit Logs**: Filterable audit log viewer
- **Agent Activity**: Agent performance and activity metrics
- **Quick Actions**: One-click security scans and agent proposals

### Access

Navigate to the PwC Dashboard in the frontend to see:
- Total audit logs and approval rates
- Compliance framework coverage
- Security findings and agent activity
- Recent audit logs with filtering options

## 🔄 End-to-End Workflow

### 1. Task Intake
- Tasks enter via James input bar
- James evaluates and routes to appropriate agent

### 2. Agent Execution + Logging
- Agents execute tasks with PwC-aligned logging
- All actions include compliance tags and solution paths
- Sensitive data is automatically sanitized

### 3. Whis Learning Pipeline
- Nightly job processes approved logs only
- Creates runes tagged with compliance information
- Builds intelligence for FickNury decisions

### 4. FickNury Orchestration
- Receives intelligence from Whis
- Makes deployment decisions based on patterns
- Creates, upgrades, or deploys agents as needed

### 5. Agent Deployment
- Final deployment handled by FickNury
- All deployments tracked and versioned
- Multi-environment support (Docker, Kubernetes, Local)

## 🛡️ Security & Compliance

### Data Sanitization

- Sensitive fields replaced with placeholders
- API keys, passwords, and tokens automatically detected
- Client names and PII redacted for compliance

### Audit Trail

- All agent actions logged with full context
- Compliance tags for regulatory reporting
- Solution paths for remediation tracking
- Approval workflows for quality control

### Access Control

- RBAC for Kubernetes deployments
- Network policies for agent communication
- Secrets management for credentials
- Audit logging for all deployment decisions

## 📈 Monitoring & Observability

### Metrics

- Deployment success rates
- Agent creation frequency
- Intelligence processing time
- Resource optimization impact
- Compliance framework coverage

### Health Checks

- Agent availability monitoring
- Deployment status tracking
- Resource utilization metrics
- Error rate monitoring

## 🔧 Configuration

### Environment Variables

```bash
# AuditGuard
LOG_LEVEL=INFO
TRIVY_CACHE_DIR=/app/cache

# FickNury
KUBECONFIG=/root/.kube/config
DOCKER_HOST=unix:///var/run/docker.sock
LOG_LEVEL=INFO
```

### Database Schema

The new PwC-aligned logging fields:
- `solution_path`: Recommended solution path
- `error_outcome`: Error details if failed
- `sanitized`: Whether data is sanitized
- `approved`: Whether action is approved
- `auto_approved`: Whether auto-approved
- `compliance_tags`: JSON array of compliance tags

## 🚨 Troubleshooting

### Common Issues

1. **Database Migration Failures**
   ```bash
   cd backend
   alembic upgrade head
   ```

2. **Agent Build Failures**
   ```bash
   # Rebuild specific agent
   docker build -t linkops-auditguard:latest agents/auditguard/
   ```

3. **Service Startup Issues**
   ```bash
   # Check logs
   docker-compose logs auditguard
   docker-compose logs ficknury
   ```

4. **API Endpoint Issues**
   ```bash
   # Test endpoints
   curl http://localhost:8001/health  # AuditGuard
   curl http://localhost:8002/health  # FickNury
   ```

### Log Locations

- **AuditGuard**: `agents/auditguard/logs/auditguard.log`
- **FickNury**: `agents/ficknury/logs/ficknury.log`
- **Backend**: `backend/logs/`
- **Docker**: `docker-compose logs [service-name]`

## 📚 API Reference

### New Endpoints

#### AuditGuard
- `POST /api/auditguard/scan` - Execute security scan

#### FickNury
- `POST /api/ficknury/propose-agent` - Propose agent creation/upgrade
- `POST /api/ficknury/deploy-agent` - Deploy agent
- `GET /api/agents/status` - Get agent status

#### PwC-Aligned Logging
- `POST /api/logs` - Log with PwC-aligned fields
- `GET /api/audit-logs` - Get filtered audit logs
- `GET /api/compliance/stats` - Get compliance statistics

### Updated Endpoints

- `POST /api/whis/train-nightly` - Now filters by sanitized and approved
- `GET /api/whis/digest` - Now includes compliance statistics

## 🎯 Next Steps

1. **Run Initial Audits**: Execute security scans across your infrastructure
2. **Review Compliance**: Check compliance statistics and identify gaps
3. **Propose Agents**: Use FickNury to create specialized agents for your needs
4. **Customize Workflows**: Adapt the PwC-aligned workflows to your specific requirements
5. **Scale Deployment**: Deploy agents across multiple environments using FickNury

## 📞 Support

For issues or questions about the PwC-aligned upgrade:

1. Check the troubleshooting section above
2. Review agent-specific README files in `agents/` directories
3. Check logs for detailed error information
4. Verify database migrations completed successfully

---

**LinkOps is now a comprehensive PwC-aligned AI audit platform ready for enterprise deployment!** 🎉 