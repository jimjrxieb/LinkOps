from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import subprocess
import json
from datetime import datetime

router = APIRouter(prefix="/security", tags=["security"])
logger = logging.getLogger(__name__)


class SecurityScanRequest(BaseModel):
    task_id: str
    scan_type: str  # "trivy", "bandit", "checkov", "snyk", "semgrep"
    target: str
    auto_approve: bool = False


class SecurityScanResult(BaseModel):
    agent: str = "auditguard"
    task_id: str
    action: str
    result: Dict[str, Any]
    solution_path: Optional[str] = None
    error_outcome: Optional[str] = None
    sanitized: bool = True
    approved: bool = False
    auto_approved: bool = False
    compliance_tags: List[str] = []


@router.get("/health")
def health() -> Dict[str, Any]:
    """Health check endpoint for security scanning."""
    return {
        "status": "healthy",
        "service": "auditguard-security",
        "capabilities": [
            "Trivy vulnerability scanning",
            "Bandit security linting",
            "Checkov infrastructure scanning",
            "Snyk dependency scanning",
            "Semgrep code analysis",
        ],
    }


@router.get("/")
async def get_security_alerts() -> Dict[str, Any]:
    """Get security alerts."""
    return {
        "alerts": [
            {
                "id": 1,
                "title": "Suspicious Login Attempt",
                "message": "Multiple failed login attempts detected from IP 192.168.1.100",
                "level": "warning",
                "timestamp": "2 minutes ago",
                "source": "Authentication System"
            },
            {
                "id": 2,
                "title": "Dependency Vulnerability",
                "message": "High severity vulnerability found in package lodash@4.17.15",
                "level": "critical",
                "timestamp": "15 minutes ago",
                "source": "Dependency Scanner"
            },
            {
                "id": 3,
                "title": "Configuration Drift",
                "message": "Infrastructure configuration has drifted from Git state",
                "level": "warning",
                "timestamp": "1 hour ago",
                "source": "Infrastructure Monitor"
            }
        ]
    }


@router.post("/scan")
async def execute_security_scan(
    request: SecurityScanRequest, background_tasks: BackgroundTasks
) -> SecurityScanResult:
    """Execute security scan based on scan type."""
    try:
        logger.info(
            "AuditGuard processing %s scan for %s", request.scan_type, request.target
        )

        scan_map = {
            "trivy": _run_trivy_scan,
            "bandit": _run_bandit_scan,
            "checkov": _run_checkov_scan,
            "snyk": _run_snyk_scan,
            "semgrep": _run_semgrep_scan,
        }

        if request.scan_type not in scan_map:
            raise HTTPException(status_code=400, detail="Unsupported scan type")

        result = await scan_map[request.scan_type](request.target)

        sanitized_result = _sanitize_scan_result(result)
        solution_path = _generate_solution_path(result, request.scan_type)

        scan_result = SecurityScanResult(
            task_id=request.task_id,
            action=f"{request.scan_type} scan complete",
            result=sanitized_result,
            solution_path=solution_path,
            sanitized=True,
            approved=request.auto_approve,
            auto_approved=request.auto_approve,
            compliance_tags=["ISO27001", "NIST"],
        )

        return scan_result

    except Exception as exc:
        logger.error("Security scan failed: %r", exc)
        raise HTTPException(status_code=500, detail=f"Security scan failed: {str(exc)}")


async def _run_trivy_scan(target: str) -> Dict[str, Any]:
    """Run Trivy vulnerability scan."""
    try:
        cmd = ["trivy", "fs", "--format", "json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            scan_data = json.loads(result.stdout)
            high, medium, low = 0, 0, 0

            for r in scan_data.get("Results", []):
                for vuln in r.get("Vulnerabilities", []):
                    sev = vuln.get("Severity", "").upper()
                    if sev in ["CRITICAL", "HIGH"]:
                        high += 1
                    elif sev == "MEDIUM":
                        medium += 1
                    else:
                        low += 1

            return {
                "scan_type": "trivy",
                "target": target,
                "high_risk": high,
                "medium_risk": medium,
                "low_risk": low,
                "total_vulnerabilities": high + medium + low,
                "scan_successful": True,
                "raw_data": scan_data,
            }

        return {
            "scan_type": "trivy",
            "target": target,
            "error": result.stderr,
            "scan_successful": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "scan_type": "trivy",
            "target": target,
            "error": "Scan timed out after 5 minutes",
            "scan_successful": False,
        }
    except Exception as exc:
        return {
            "scan_type": "trivy",
            "target": target,
            "error": str(exc),
            "scan_successful": False,
        }


async def _run_bandit_scan(target: str) -> Dict[str, Any]:
    """Run Bandit static analysis."""
    try:
        cmd = ["bandit", "-r", "-f", "json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode in [0, 1]:
            data = json.loads(result.stdout)
            high = sum(
                1 for i in data.get("results", []) if i.get("issue_severity") == "HIGH"
            )
            medium = sum(
                1
                for i in data.get("results", [])
                if i.get("issue_severity") == "MEDIUM"
            )
            low = sum(
                1 for i in data.get("results", []) if i.get("issue_severity") == "LOW"
            )

            return {
                "scan_type": "bandit",
                "target": target,
                "high_issues": high,
                "medium_issues": medium,
                "low_issues": low,
                "total_issues": high + medium + low,
                "scan_successful": True,
                "raw_data": data,
            }

        return {
            "scan_type": "bandit",
            "target": target,
            "error": result.stderr,
            "scan_successful": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "scan_type": "bandit",
            "target": target,
            "error": "Scan timed out",
            "scan_successful": False,
        }
    except Exception as exc:
        return {
            "scan_type": "bandit",
            "target": target,
            "error": str(exc),
            "scan_successful": False,
        }


async def _run_checkov_scan(target: str) -> Dict[str, Any]:
    """Run Checkov IaC scan."""
    try:
        cmd = ["checkov", "-d", target, "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

        if result.returncode in [0, 1]:
            data = json.loads(result.stdout)
            failed = len(data.get("results", {}).get("failed_checks", []))
            passed = len(data.get("results", {}).get("passed_checks", []))

            return {
                "scan_type": "checkov",
                "target": target,
                "failed_checks": failed,
                "passed_checks": passed,
                "total_checks": failed + passed,
                "scan_successful": True,
                "raw_data": data,
            }

        return {
            "scan_type": "checkov",
            "target": target,
            "error": result.stderr,
            "scan_successful": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "scan_type": "checkov",
            "target": target,
            "error": "Timeout after 3 minutes",
            "scan_successful": False,
        }
    except Exception as exc:
        return {
            "scan_type": "checkov",
            "target": target,
            "error": str(exc),
            "scan_successful": False,
        }


async def _run_snyk_scan(target: str) -> Dict[str, Any]:
    """Run Snyk dependency scan."""
    try:
        cmd = ["snyk", "test", "--json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode in [0, 1]:
            data = json.loads(result.stdout)
            vuln_count = len(data.get("vulnerabilities", []))

            return {
                "scan_type": "snyk",
                "target": target,
                "vulnerabilities": vuln_count,
                "scan_successful": True,
                "raw_data": data,
            }

        return {
            "scan_type": "snyk",
            "target": target,
            "error": result.stderr,
            "scan_successful": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "scan_type": "snyk",
            "target": target,
            "error": "Scan timed out",
            "scan_successful": False,
        }
    except Exception as exc:
        return {
            "scan_type": "snyk",
            "target": target,
            "error": str(exc),
            "scan_successful": False,
        }


async def _run_semgrep_scan(target: str) -> Dict[str, Any]:
    """Run Semgrep code analysis."""
    try:
        cmd = ["semgrep", "--json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode in [0, 1]:
            data = json.loads(result.stdout)
            findings = len(data.get("results", []))

            return {
                "scan_type": "semgrep",
                "target": target,
                "findings": findings,
                "scan_successful": True,
                "raw_data": data,
            }

        return {
            "scan_type": "semgrep",
            "target": target,
            "error": result.stderr,
            "scan_successful": False,
        }

    except subprocess.TimeoutExpired:
        return {
            "scan_type": "semgrep",
            "target": target,
            "error": "Scan timed out",
            "scan_successful": False,
        }
    except Exception as exc:
        return {
            "scan_type": "semgrep",
            "target": target,
            "error": str(exc),
            "scan_successful": False,
        }


def _sanitize_scan_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Strip raw data and add compliance metadata."""
    sanitized = result.copy()
    sanitized.pop("raw_data", None)
    sanitized["compliance_metadata"] = {
        "scan_timestamp": datetime.utcnow().isoformat(),
        "sanitized": True,
        "compliance_ready": True,
    }
    return sanitized


def _generate_solution_path(result: Dict[str, Any], scan_type: str) -> str:
    """Map issues to recommended remediation."""
    if not result.get("scan_successful"):
        return f"Fix {scan_type} configuration or permissions"

    if scan_type == "trivy" and result.get("high_risk", 0) > 0:
        return "Update vulnerable packages and rebuild containers"
    if scan_type == "bandit" and result.get("high_issues", 0) > 0:
        return "Address high-severity code issues"
    if scan_type == "checkov" and result.get("failed_checks", 0) > 0:
        return "Resolve IaC policy violations"
    if scan_type == "snyk" and result.get("vulnerabilities", 0) > 0:
        return "Upgrade vulnerable dependencies"
    if scan_type == "semgrep" and result.get("findings", 0) > 0:
        return "Refactor risky patterns flagged by Semgrep"

    return f"{scan_type} scan passed - no immediate action required"
