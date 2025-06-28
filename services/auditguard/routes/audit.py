from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
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
def health():
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
async def audit_repository(request: RepositoryAuditRequest):
    """Audit repository for security issues"""
    try:
        logger.info(f"AuditGuard repository audit for {request.repository_path}")

        findings = {}

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

        # Calculate risk score
        risk_score = _calculate_risk_score(findings)

        # Generate recommendations
        recommendations = _generate_recommendations(findings)

        result = RepositoryAuditResult(
            task_id=request.task_id,
            repository_path=request.repository_path,
            findings=findings,
            risk_score=risk_score,
            recommendations=recommendations,
        )

        logger.info(f"Repository audit completed with risk score: {risk_score}")
        return result

    except Exception as e:
        logger.error(f"Repository audit failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Repository audit failed: {str(e)}"
        )


async def _check_for_secrets(repo_path: str) -> List[Dict[str, Any]]:
    """Check for secrets in repository"""
    secrets = []

    # Common secret patterns
    secret_patterns = [
        r'api_key["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'password["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'secret["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'token["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'private_key["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'aws_access_key_id["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'aws_secret_access_key["\']?\s*[:=]\s*["\'][^"\']+["\']',
    ]

    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith((".py", ".js", ".json", ".yaml", ".yml", ".env")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            for pattern in secret_patterns:
                                matches = re.finditer(pattern, content, re.IGNORECASE)
                                for match in matches:
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
    except Exception as e:
        logger.error(f"Error scanning for secrets: {str(e)}")

    return secrets


async def _check_for_credentials(repo_path: str) -> List[Dict[str, Any]]:
    """Check for hardcoded credentials"""
    credentials = []

    # Credential patterns
    credential_patterns = [
        r'username["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'user["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'login["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'email["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'admin["\']?\s*[:=]\s*["\'][^"\']+["\']',
    ]

    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(
                    (".py", ".js", ".json", ".yaml", ".yml", ".env", ".conf")
                ):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            for pattern in credential_patterns:
                                matches = re.finditer(pattern, content, re.IGNORECASE)
                                for match in matches:
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
    except Exception as e:
        logger.error(f"Error scanning for credentials: {str(e)}")

    return credentials


async def _check_for_sensitive_files(repo_path: str) -> List[Dict[str, Any]]:
    """Check for sensitive files"""
    sensitive_files = []

    # Sensitive file patterns
    sensitive_patterns = [
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
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                for pattern in sensitive_patterns:
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
    except Exception as e:
        logger.error(f"Error scanning for sensitive files: {str(e)}")

    return sensitive_files


def _calculate_risk_score(findings: Dict[str, Any]) -> float:
    """Calculate risk score based on findings"""
    risk_score = 0.0

    # Weight different types of findings
    if findings.get("secrets"):
        risk_score += len(findings["secrets"]) * 0.3  # High weight for secrets

    if findings.get("credentials"):
        risk_score += (
            len(findings["credentials"]) * 0.2
        )  # Medium weight for credentials

    if findings.get("sensitive_files"):
        risk_score += (
            len(findings["sensitive_files"]) * 0.25
        )  # High weight for sensitive files

    # Normalize to 0-1 scale
    return min(risk_score, 1.0)


def _generate_recommendations(findings: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on findings"""
    recommendations = []

    if findings.get("secrets"):
        recommendations.append("Remove hardcoded secrets and use environment variables")
        recommendations.append(
            "Implement secret management solution (e.g., HashiCorp Vault)"
        )

    if findings.get("credentials"):
        recommendations.append(
            "Remove hardcoded credentials and use secure authentication"
        )
        recommendations.append("Implement proper credential rotation procedures")

    if findings.get("sensitive_files"):
        recommendations.append("Move sensitive files to secure storage")
        recommendations.append("Update .gitignore to exclude sensitive files")

    if not recommendations:
        recommendations.append("No immediate security issues found")

    return recommendations
