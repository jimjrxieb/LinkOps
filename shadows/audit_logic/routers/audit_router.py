from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import Dict, Any, List
from logic.scorer import AuditScorer

router = APIRouter(prefix="/audit", tags=["Audit Logic"])


class RepoScanSummary(BaseModel):
    repo_name: str
    helm_charts: List[Dict[str, Any]] = []
    ci_cd_files: List[Dict[str, Any]] = []
    security_issues: List[Dict[str, Any]] = []
    architecture_patterns: List[Dict[str, Any]] = []
    gitops_tools: List[Dict[str, Any]] = []
    rbac_configs: List[Dict[str, Any]] = []
    secrets_management: List[Dict[str, Any]] = []


class AuditScore(BaseModel):
    overall_score: float
    risk_level: str
    explanation: str
    breakdown: Dict[str, float]
    recommendations: List[str]


@router.get("/standards/")
def get_audit_standards():
    """Return YAML-style best practices for various audit categories"""
    return {
        "helm_best_practices": {
            "chart_structure": {
                "required_files": ["Chart.yaml", "values.yaml", "templates/"],
                "versioning": "Semantic versioning (x.y.z)",
                "dependencies": "Use requirements.yaml for dependencies",
                "values_management": "Use environment-specific values files",
            },
            "security": {
                "image_pinning": "Use specific image tags, not 'latest'",
                "rbac_enabled": "Always enable RBAC",
                "network_policies": "Define network policies",
                "resource_limits": "Set CPU and memory limits",
            },
        },
        "ci_cd_best_practices": {
            "pipeline_structure": {
                "stages": ["lint", "test", "build", "deploy"],
                "artifacts": "Store build artifacts",
                "environments": "Separate dev/staging/prod pipelines",
            },
            "security": {
                "secrets_management": "Use encrypted secrets",
                "access_control": "Limit pipeline permissions",
                "audit_logging": "Log all pipeline executions",
            },
        },
        "rbac_best_practices": {
            "principle_of_least_privilege": "Grant minimum required permissions",
            "role_separation": "Separate admin, developer, and read-only roles",
            "regular_reviews": "Review permissions quarterly",
            "service_accounts": "Use dedicated service accounts for applications",
        },
        "microservices_best_practices": {
            "service_discovery": "Use service mesh or DNS-based discovery",
            "api_gateway": "Implement API gateway for external access",
            "circuit_breakers": "Implement circuit breakers for resilience",
            "distributed_tracing": "Use tracing for debugging and monitoring",
            "health_checks": "Implement liveness and readiness probes",
        },
        "gitops_best_practices": {
            "declarative_configs": "Store all configs in Git",
            "automated_deployments": "Use ArgoCD or Flux for deployments",
            "drift_detection": "Monitor for configuration drift",
            "rollback_strategy": "Implement automated rollback capabilities",
        },
    }


@router.post("/score-repo/", response_model=AuditScore)
def score_repository(repo_scan: RepoScanSummary = Body(...)):
    """Score a repository based on audit criteria and return risk assessment"""
    scorer = AuditScorer()
    return scorer.score_repository(repo_scan)
