from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
import os
import re
from datetime import datetime

router = APIRouter(prefix="/audit", tags=["audit"])

logger = logging.getLogger(__name__)


class RepositoryAuditRequest(BaseModel):
    task_id: str
    repository_path: str
    audit_scope: List[str] = ["secrets", "credentials", "sensitive_files"]


class RepositoryAuditResult(BaseModel):
    task_id: str
    repository_path: str
    findings: Dict[str, Any]
    risk_score: float
    recommendations: List[str]


@router.get("/health")
def health() -> Dict[str, Any]:
    """Health check endpoint for the audit module."""
    return {
        "status": "healthy",
        "service": "auditguard-audit",
        "capabilities": [
            "Repository security audit",
            "Secret detection",
            "Credential scanning",
            "Sensitive file identification",
        ],
    }


@router.post("/repository")
async def audit_repository(request: RepositoryAuditRequest) -> RepositoryAuditResult:
    """Audit repository for security issues."""
    try:
        logger.info("AuditGuard repository audit for %s", request.repository_path)

        findings: Dict[str, Any] = {}

        for scope in request.audit_scope:
            if scope == "secrets":
                findings["secrets"] = await _check_for_secrets(request.repository_path)
            elif scope == "credentials":
                findings["credentials"] = await _check_for_credentials(
                    request.repository_path
                )
            elif scope == "sensitive_files":
                findings["sensitive_files"] = await _check_for_sensitive_files(
                    request.repository_path
                )

        risk_score = _calculate_risk_score(findings)
        recommendations = _generate_recommendations(findings)

        result = RepositoryAuditResult(
            task_id=request.task_id,
            repository_path=request.repository_path,
            findings=findings,
            risk_score=risk_score,
            recommendations=recommendations,
        )

        logger.info("Repository audit completed with risk score: %s", risk_score)
        return result

    except Exception as exc:
        logger.error("Repository audit failed: %r", exc)
        raise HTTPException(
            status_code=500, detail=f"Repository audit failed: {str(exc)}"
        )


async def _check_for_secrets(repo_path: str) -> List[Dict[str, Any]]:
    """Check for secrets in repository."""
    secrets: List[Dict[str, Any]] = []

    patterns = [
        r'api_key["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'password["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'secret["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'token["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'private_key["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'aws_access_key_id["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'aws_secret_access_key["\']?\s*[:=]\s*["\'][^"\']+["\']',
    ]

    try:
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith((".py", ".js", ".json", ".yaml", ".yml", ".env")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()
                            for pattern in patterns:
                                for match in re.finditer(
                                    pattern, content, re.IGNORECASE
                                ):
                                    secrets.append(
                                        {
                                            "file": file_path,
                                            "line": content[: match.start()].count("\n")
                                            + 1,
                                            "pattern": pattern,
                                            "severity": "high",
                                        }
                                    )
                    except Exception:
                        continue
    except Exception as exc:
        logger.error("Error scanning for secrets: %r", exc)

    return secrets


async def _check_for_credentials(repo_path: str) -> List[Dict[str, Any]]:
    """Check for hardcoded credentials."""
    credentials: List[Dict[str, Any]] = []

    patterns = [
        r'username["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'user["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'login["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'email["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'admin["\']?\s*[:=]\s*["\'][^"\']+["\']',
    ]

    try:
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(
                    (".py", ".js", ".json", ".yaml", ".yml", ".env", ".conf")
                ):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()
                            for pattern in patterns:
                                for match in re.finditer(
                                    pattern, content, re.IGNORECASE
                                ):
                                    credentials.append(
                                        {
                                            "file": file_path,
                                            "line": content[: match.start()].count("\n")
                                            + 1,
                                            "pattern": pattern,
                                            "severity": "medium",
                                        }
                                    )
                    except Exception:
                        continue
    except Exception as exc:
        logger.error("Error scanning for credentials: %r", exc)

    return credentials


async def _check_for_sensitive_files(repo_path: str) -> List[Dict[str, Any]]:
    """Check for sensitive file names."""
    sensitive_files: List[Dict[str, Any]] = []

    patterns = [
        r"\.env$",
        r"\.pem$",
        r"\.key$",
        r"\.crt$",
        r"\.p12$",
        r"\.pfx$",
        r"id_rsa$",
        r"id_dsa$",
        r"\.keystore$",
        r"\.jks$",
    ]

    try:
        for root, _, files in os.walk(repo_path):
            for file in files:
                for pattern in patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        file_path = os.path.join(root, file)
                        sensitive_files.append(
                            {
                                "file": file_path,
                                "pattern": pattern,
                                "severity": "high",
                                "recommendation": "Move to secure storage or add to .gitignore",
                            }
                        )
                        break
    except Exception as exc:
        logger.error("Error scanning for sensitive files: %r", exc)

    return sensitive_files


def _calculate_risk_score(findings: Dict[str, Any]) -> float:
    """Calculate normalized risk score based on findings."""
    score = 0.0
    if findings.get("secrets"):
        score += len(findings["secrets"]) * 0.3
    if findings.get("credentials"):
        score += len(findings["credentials"]) * 0.2
    if findings.get("sensitive_files"):
        score += len(findings["sensitive_files"]) * 0.25
    return min(score, 1.0)


def _generate_recommendations(findings: Dict[str, Any]) -> List[str]:
    """Generate best-practice remediation tips."""
    recs: List[str] = []

    if findings.get("secrets"):
        recs.append("Remove hardcoded secrets and use environment variables.")
        recs.append("Implement secret management (e.g., HashiCorp Vault).")

    if findings.get("credentials"):
        recs.append("Use secure authentication flows.")
        recs.append("Enable credential rotation policies.")

    if findings.get("sensitive_files"):
        recs.append("Move sensitive files to secure storage.")
        recs.append("Add sensitive files to .gitignore.")

    if not recs:
        recs.append("No immediate security risks found.")

    return recs
