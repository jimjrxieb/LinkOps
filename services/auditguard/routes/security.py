from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import logging
import subprocess
import os
import re
from datetime import datetime
import uuid

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
def health():
    return {
        "status": "healthy",
        "service": "auditguard-security",
        "capabilities": [
            "Trivy vulnerability scanning",
            "Bandit security linting", 
            "Checkov infrastructure scanning",
            "Snyk dependency scanning",
            "Semgrep code analysis"
        ]
    }

@router.post("/scan")
async def execute_security_scan(request: SecurityScanRequest, background_tasks: BackgroundTasks):
    """Execute security scan based on scan type"""
    try:
        logger.info(f"AuditGuard processing {request.scan_type} scan for {request.target}")
        
        # Execute the appropriate scan
        if request.scan_type == "trivy":
            result = await _run_trivy_scan(request.target)
        elif request.scan_type == "bandit":
            result = await _run_bandit_scan(request.target)
        elif request.scan_type == "checkov":
            result = await _run_checkov_scan(request.target)
        elif request.scan_type == "snyk":
            result = await _run_snyk_scan(request.target)
        elif request.scan_type == "semgrep":
            result = await _run_semgrep_scan(request.target)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scan type: {request.scan_type}")
        
        # Sanitize results
        sanitized_result = _sanitize_scan_result(result)
        
        # Generate solution path
        solution_path = _generate_solution_path(result, request.scan_type)
        
        # Create scan result
        scan_result = SecurityScanResult(
            task_id=request.task_id,
            action=f"{request.scan_type} scan complete",
            result=sanitized_result,
            solution_path=solution_path,
            sanitized=True,
            approved=request.auto_approve,
            auto_approved=request.auto_approve,
            compliance_tags=["ISO27001", "NIST"]
        )
        
        logger.info(f"AuditGuard completed {request.scan_type} scan")
        return scan_result
        
    except Exception as e:
        logger.error(f"Security scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Security scan failed: {str(e)}")

async def _run_trivy_scan(target: str) -> Dict[str, Any]:
    """Run Trivy vulnerability scan"""
    try:
        cmd = ["trivy", "fs", "--format", "json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            scan_data = json.loads(result.stdout)
            
            # Extract vulnerability counts
            high_risk = 0
            medium_risk = 0
            low_risk = 0
            
            for result_data in scan_data.get("Results", []):
                for vuln in result_data.get("Vulnerabilities", []):
                    severity = vuln.get("Severity", "UNKNOWN")
                    if severity == "HIGH" or severity == "CRITICAL":
                        high_risk += 1
                    elif severity == "MEDIUM":
                        medium_risk += 1
                    else:
                        low_risk += 1
            
            return {
                "scan_type": "trivy",
                "target": target,
                "high_risk": high_risk,
                "medium_risk": medium_risk,
                "low_risk": low_risk,
                "total_vulnerabilities": high_risk + medium_risk + low_risk,
                "scan_successful": True,
                "raw_data": scan_data
            }
        else:
            return {
                "scan_type": "trivy",
                "target": target,
                "error": result.stderr,
                "scan_successful": False
            }
            
    except subprocess.TimeoutExpired:
        return {
            "scan_type": "trivy",
            "target": target,
            "error": "Scan timed out after 5 minutes",
            "scan_successful": False
        }
    except Exception as e:
        return {
            "scan_type": "trivy",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

async def _run_bandit_scan(target: str) -> Dict[str, Any]:
    """Run Bandit security linting scan"""
    try:
        cmd = ["bandit", "-r", "-f", "json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode in [0, 1]:  # Bandit returns 1 if issues found
            scan_data = json.loads(result.stdout)
            
            high_issues = len([issue for issue in scan_data.get("results", []) 
                             if issue.get("issue_severity") == "HIGH"])
            medium_issues = len([issue for issue in scan_data.get("results", []) 
                               if issue.get("issue_severity") == "MEDIUM"])
            low_issues = len([issue for issue in scan_data.get("results", []) 
                            if issue.get("issue_severity") == "LOW"])
            
            return {
                "scan_type": "bandit",
                "target": target,
                "high_issues": high_issues,
                "medium_issues": medium_issues,
                "low_issues": low_issues,
                "total_issues": high_issues + medium_issues + low_issues,
                "scan_successful": True,
                "raw_data": scan_data
            }
        else:
            return {
                "scan_type": "bandit",
                "target": target,
                "error": result.stderr,
                "scan_successful": False
            }
            
    except subprocess.TimeoutExpired:
        return {
            "scan_type": "bandit",
            "target": target,
            "error": "Scan timed out after 2 minutes",
            "scan_successful": False
        }
    except Exception as e:
        return {
            "scan_type": "bandit",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

async def _run_checkov_scan(target: str) -> Dict[str, Any]:
    """Run Checkov infrastructure scanning"""
    try:
        cmd = ["checkov", "-d", target, "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode in [0, 1]:  # Checkov returns 1 if issues found
            scan_data = json.loads(result.stdout)
            
            failed_checks = len(scan_data.get("results", {}).get("failed_checks", []))
            passed_checks = len(scan_data.get("results", {}).get("passed_checks", []))
            
            return {
                "scan_type": "checkov",
                "target": target,
                "failed_checks": failed_checks,
                "passed_checks": passed_checks,
                "total_checks": failed_checks + passed_checks,
                "scan_successful": True,
                "raw_data": scan_data
            }
        else:
            return {
                "scan_type": "checkov",
                "target": target,
                "error": result.stderr,
                "scan_successful": False
            }
            
    except subprocess.TimeoutExpired:
        return {
            "scan_type": "checkov",
            "target": target,
            "error": "Scan timed out after 3 minutes",
            "scan_successful": False
        }
    except Exception as e:
        return {
            "scan_type": "checkov",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

async def _run_snyk_scan(target: str) -> Dict[str, Any]:
    """Run Snyk dependency scanning"""
    try:
        cmd = ["snyk", "test", "--json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode in [0, 1]:  # Snyk returns 1 if vulnerabilities found
            scan_data = json.loads(result.stdout)
            
            vulnerabilities = len(scan_data.get("vulnerabilities", []))
            
            return {
                "scan_type": "snyk",
                "target": target,
                "vulnerabilities": vulnerabilities,
                "scan_successful": True,
                "raw_data": scan_data
            }
        else:
            return {
                "scan_type": "snyk",
                "target": target,
                "error": result.stderr,
                "scan_successful": False
            }
            
    except subprocess.TimeoutExpired:
        return {
            "scan_type": "snyk",
            "target": target,
            "error": "Scan timed out after 2 minutes",
            "scan_successful": False
        }
    except Exception as e:
        return {
            "scan_type": "snyk",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

async def _run_semgrep_scan(target: str) -> Dict[str, Any]:
    """Run Semgrep code analysis"""
    try:
        cmd = ["semgrep", "--json", target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode in [0, 1]:  # Semgrep returns 1 if issues found
            scan_data = json.loads(result.stdout)
            
            findings = len(scan_data.get("results", []))
            
            return {
                "scan_type": "semgrep",
                "target": target,
                "findings": findings,
                "scan_successful": True,
                "raw_data": scan_data
            }
        else:
            return {
                "scan_type": "semgrep",
                "target": target,
                "error": result.stderr,
                "scan_successful": False
            }
            
    except subprocess.TimeoutExpired:
        return {
            "scan_type": "semgrep",
            "target": target,
            "error": "Scan timed out after 2 minutes",
            "scan_successful": False
        }
    except Exception as e:
        return {
            "scan_type": "semgrep",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

def _sanitize_scan_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize scan results for compliance"""
    sanitized = result.copy()
    
    # Remove sensitive data
    if "raw_data" in sanitized:
        del sanitized["raw_data"]
    
    # Add compliance metadata
    sanitized["compliance_metadata"] = {
        "scan_timestamp": datetime.utcnow().isoformat(),
        "sanitized": True,
        "compliance_ready": True
    }
    
    return sanitized

def _generate_solution_path(result: Dict[str, Any], scan_type: str) -> str:
    """Generate solution path based on scan results"""
    if not result.get("scan_successful", False):
        return f"Fix {scan_type} scan configuration"
    
    if scan_type == "trivy" and result.get("high_risk", 0) > 0:
        return "Update vulnerable dependencies and rebuild containers"
    elif scan_type == "bandit" and result.get("high_issues", 0) > 0:
        return "Fix high-severity security issues in code"
    elif scan_type == "checkov" and result.get("failed_checks", 0) > 0:
        return "Fix infrastructure security misconfigurations"
    elif scan_type == "snyk" and result.get("vulnerabilities", 0) > 0:
        return "Update vulnerable dependencies"
    elif scan_type == "semgrep" and result.get("findings", 0) > 0:
        return "Fix code security issues identified by Semgrep"
    else:
        return f"Security scan {scan_type} passed - no immediate action required" 