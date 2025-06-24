# 🛡️ AuditGuard Agent

## Overview

AuditGuard is a PwC-aligned security and compliance agent that performs automated security scans, repository audits, and compliance checks. It integrates with industry-standard security tools to provide comprehensive audit capabilities.

## Capabilities

### Security Scanning
- **Trivy**: Container and filesystem vulnerability scanning
- **Bandit**: Python security linting
- **Checkov**: Infrastructure as Code security scanning
- **Snyk**: Dependency vulnerability scanning
- **Semgrep**: Static code analysis

### Repository Auditing
- **Secrets Detection**: Identifies exposed API keys, passwords, and tokens
- **Credentials Scanning**: Detects AWS keys, database URLs, and connection strings
- **Sensitive Files**: Identifies configuration files and private keys

### Compliance Framework
- **SOC2**: Service Organization Control 2 compliance
- **GDPR**: General Data Protection Regulation
- **ISO27001**: Information security management
- **NIST**: National Institute of Standards and Technology
- **SOX**: Sarbanes-Oxley Act
- **PCI-DSS**: Payment Card Industry Data Security Standard

## API Endpoints

### Health Check
```bash
GET /health
```

### Execute Audit
```bash
POST /execute
{
  "task_id": "audit-001",
  "scan_type": "trivy",
  "target": "/app",
  "compliance_scope": ["SOC2", "GDPR"],
  "auto_approve": false
}
```

## Scan Types

| Scan Type | Purpose | Tools Used |
|-----------|---------|------------|
| `trivy` | Vulnerability scanning | Trivy |
| `bandit` | Python security | Bandit |
| `checkov` | Infrastructure security | Checkov |
| `snyk` | Dependency scanning | Snyk |
| `semgrep` | Code analysis | Semgrep |
| `repo_audit` | Repository security | Custom patterns |

## PwC-Aligned Logging

AuditGuard produces logs in the PwC-aligned format:

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
  "approved": false
}
```

## Deployment

```bash
# Build the container
docker build -t auditguard .

# Run the agent
docker run -p 8000:8000 auditguard
```

## Integration

AuditGuard integrates with the LinkOps platform through:
- Standardized logging format
- Compliance tag propagation
- Solution path recommendations
- Automated approval workflows 