from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import os
import tempfile
import shutil
from logic.analyzer import RepoAnalyzer

router = APIRouter(prefix="/scan", tags=["Repository Assessment"])


class RepoScanRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"


class ProjectSummary(BaseModel):
    repo_name: str
    languages: List[str]
    structure: Dict[str, Any]
    ci_configs: List[Dict[str, Any]]
    helm_charts: List[Dict[str, Any]]
    dockerfiles: List[Dict[str, Any]]
    gitops_tools: List[Dict[str, Any]]
    architecture_patterns: List[Dict[str, Any]]
    security_issues: List[Dict[str, Any]]
    recommendations: List[str]


class MicroserviceSuggestion(BaseModel):
    name: str
    description: str
    reasoning: str
    complexity: str  # "low", "medium", "high"
    dependencies: List[str]


class GitOpsImprovement(BaseModel):
    category: str
    title: str
    description: str
    priority: str  # "low", "medium", "high"
    implementation_steps: List[str]


class ScaffoldPlan(BaseModel):
    services_to_generate: List[Dict[str, Any]]
    execution_steps: List[str]
    estimated_duration: str
    required_tools: List[str]
    next_actions: List[str]


@router.post("/repo/", response_model=ProjectSummary)
async def scan_repository(request: RepoScanRequest = Body(...)):
    """Clone and analyze a GitHub repository"""
    try:
        analyzer = RepoAnalyzer()
        summary = await analyzer.analyze_repository(request.repo_url, request.branch)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze repository: {str(e)}"
        )


@router.get("/suggestions/")
async def get_suggestions():
    """Get microservice decomposition and GitOps improvement suggestions"""
    return {
        "microservice_suggestions": [
            {
                "name": "auth-service",
                "description": "Authentication and authorization microservice",
                "reasoning": "Separate authentication logic to improve security and scalability",
                "complexity": "medium",
                "dependencies": ["user-service", "permission-service"],
            },
            {
                "name": "notification-service",
                "description": "Centralized notification handling",
                "reasoning": "Consolidate all notification logic for better maintainability",
                "complexity": "low",
                "dependencies": ["user-service"],
            },
            {
                "name": "api-gateway",
                "description": "API Gateway for external access",
                "reasoning": "Provide unified entry point and handle cross-cutting concerns",
                "complexity": "medium",
                "dependencies": ["auth-service", "rate-limiting"],
            },
            {
                "name": "monitoring-service",
                "description": "Centralized monitoring and observability",
                "reasoning": "Implement comprehensive monitoring for all services",
                "complexity": "high",
                "dependencies": ["logging-service", "metrics-service"],
            },
        ],
        "gitops_improvements": [
            {
                "category": "Deployment",
                "title": "Implement ArgoCD for GitOps",
                "description": "Replace manual deployments with ArgoCD for automated GitOps workflows",
                "priority": "high",
                "implementation_steps": [
                    "Install ArgoCD in the cluster",
                    "Create Application manifests for each service",
                    "Configure Git repository as source of truth",
                    "Set up automated sync policies",
                ],
            },
            {
                "category": "Configuration",
                "title": "Centralize Configuration Management",
                "description": "Use ConfigMaps and Secrets with external secret management",
                "priority": "medium",
                "implementation_steps": [
                    "Implement HashiCorp Vault or AWS Secrets Manager",
                    "Create ConfigMap templates for each environment",
                    "Set up external-secrets operator",
                    "Migrate hardcoded configurations",
                ],
            },
            {
                "category": "CI/CD",
                "title": "Enhance CI/CD Pipeline",
                "description": "Add security scanning, testing, and automated quality gates",
                "priority": "high",
                "implementation_steps": [
                    "Add security vulnerability scanning",
                    "Implement automated testing in pipeline",
                    "Add code quality checks (SonarQube)",
                    "Set up automated dependency updates",
                ],
            },
            {
                "category": "Monitoring",
                "title": "Implement Service Mesh",
                "description": "Add Istio or Linkerd for service-to-service communication",
                "priority": "medium",
                "implementation_steps": [
                    "Install and configure Istio",
                    "Add sidecar proxies to services",
                    "Configure traffic management rules",
                    "Set up observability dashboards",
                ],
            },
        ],
    }


@router.get("/scaffold-plan/")
async def get_scaffold_plan():
    """Generate scaffold blueprint for execution"""
    return {
        "services_to_generate": [
            {
                "name": "auth-service",
                "type": "microservice",
                "docker": {
                    "base_image": "python:3.10-slim",
                    "ports": [8000],
                    "environment": ["DATABASE_URL", "JWT_SECRET"],
                },
                "helm": {
                    "chart_name": "auth-service",
                    "namespace": "auth",
                    "resources": {"cpu": "500m", "memory": "512Mi"},
                },
                "dependencies": ["postgres", "redis"],
            },
            {
                "name": "notification-service",
                "type": "microservice",
                "docker": {
                    "base_image": "python:3.10-slim",
                    "ports": [8001],
                    "environment": ["SMTP_HOST", "SMTP_PORT"],
                },
                "helm": {
                    "chart_name": "notification-service",
                    "namespace": "notifications",
                    "resources": {"cpu": "250m", "memory": "256Mi"},
                },
                "dependencies": ["redis"],
            },
            {
                "name": "api-gateway",
                "type": "gateway",
                "docker": {
                    "base_image": "nginx:alpine",
                    "ports": [80, 443],
                    "environment": ["UPSTREAM_SERVICES"],
                },
                "helm": {
                    "chart_name": "api-gateway",
                    "namespace": "gateway",
                    "resources": {"cpu": "200m", "memory": "128Mi"},
                },
                "dependencies": ["auth-service", "rate-limiting"],
            },
            {
                "name": "monitoring-stack",
                "type": "observability",
                "docker": {
                    "base_image": "prom/prometheus",
                    "ports": [9090],
                    "environment": ["PROMETHEUS_CONFIG"],
                },
                "helm": {
                    "chart_name": "monitoring",
                    "namespace": "monitoring",
                    "resources": {"cpu": "500m", "memory": "1Gi"},
                },
                "dependencies": ["grafana", "alertmanager"],
            },
        ],
        "execution_steps": [
            "1. Set up base infrastructure (Kubernetes cluster, ArgoCD)",
            "2. Create namespace structure and RBAC policies",
            "3. Deploy monitoring stack (Prometheus, Grafana, AlertManager)",
            "4. Generate and deploy auth-service with database",
            "5. Generate and deploy notification-service",
            "6. Generate and deploy API gateway with routing rules",
            "7. Configure service mesh (Istio) for inter-service communication",
            "8. Set up CI/CD pipelines for each service",
            "9. Configure external secrets management",
            "10. Implement comprehensive monitoring and alerting",
        ],
        "estimated_duration": "2-3 weeks",
        "required_tools": [
            "Kubernetes cluster",
            "ArgoCD",
            "Helm",
            "Docker",
            "Istio (optional)",
            "HashiCorp Vault or AWS Secrets Manager",
            "GitHub Actions or GitLab CI",
        ],
        "next_actions": [
            "Review and approve the scaffold plan",
            "Execute plan using auditmigrate_logic service",
            "Set up monitoring and alerting",
            "Configure CI/CD pipelines",
            "Perform security audit and penetration testing",
        ],
    }
