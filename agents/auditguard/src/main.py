"""
AuditGuard Agent - PwC-aligned Security & Compliance Agent
Handles security scans, repository audits, and compliance tagging
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import logging
import subprocess
import os
import re
from datetime import datetime
import uuid

app = FastAPI(title="AuditGuard Agent - Security & Compliance Specialist")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditTask(BaseModel):
    task_id: str
    scan_type: str  # "trivy", "bandit", "checkov", "snyk", "semgrep", "repo_audit"
    target: str  # file path, directory, or repository URL
    compliance_scope: Optional[List[str]] = ["SOC2", "GDPR"]  # Default compliance tags
    auto_approve: bool = False

class AuditResult(BaseModel):
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

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent": "auditguard",
        "specialization": "Security & Compliance Auditing",
        "capabilities": [
            "Trivy vulnerability scanning",
            "Bandit security linting",
            "Checkov infrastructure scanning",
            "Snyk dependency scanning",
            "Semgrep code analysis",
            "Repository security audits",
            "PwC-aligned compliance tagging"
        ]
    }

@app.post("/execute")
async def execute_audit(task: AuditTask, background_tasks: BackgroundTasks):
    """
    Execute security audit based on scan type
    """
    try:
        logger.info(f"AuditGuard processing {task.scan_type} scan for {task.target}")
        
        # Execute the appropriate scan
        if task.scan_type == "trivy":
            result = await _run_trivy_scan(task.target)
        elif task.scan_type == "bandit":
            result = await _run_bandit_scan(task.target)
        elif task.scan_type == "checkov":
            result = await _run_checkov_scan(task.target)
        elif task.scan_type == "snyk":
            result = await _run_snyk_scan(task.target)
        elif task.scan_type == "semgrep":
            result = await _run_semgrep_scan(task.target)
        elif task.scan_type == "repo_audit":
            result = await _run_repository_audit(task.target)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported scan type: {task.scan_type}")
        
        # Sanitize results for compliance
        sanitized_result = _sanitize_audit_result(result)
        
        # Generate solution path
        solution_path = _generate_solution_path(result, task.scan_type)
        
        # Determine compliance tags
        compliance_tags = _determine_compliance_tags(result, task.compliance_scope)
        
        # Create audit result
        audit_result = AuditResult(
            task_id=task.task_id,
            action=f"{task.scan_type} scan complete",
            result=sanitized_result,
            solution_path=solution_path,
            sanitized=True,
            approved=task.auto_approve,
            auto_approved=task.auto_approve,
            compliance_tags=compliance_tags
        )
        
        # Log the audit result
        background_tasks.add_task(_log_audit_result, audit_result)
        
        logger.info(f"AuditGuard completed {task.scan_type} scan with {len(compliance_tags)} compliance tags")
        return audit_result
        
    except Exception as e:
        logger.error(f"AuditGuard execution failed: {str(e)}")
        error_result = AuditResult(
            task_id=task.task_id,
            action=f"{task.scan_type} scan failed",
            result={"error": "Scan execution failed"},
            error_outcome=str(e),
            sanitized=True,
            approved=False,
            compliance_tags=task.compliance_scope
        )
        background_tasks.add_task(_log_audit_result, error_result)
        raise HTTPException(status_code=500, detail=f"Audit execution failed: {str(e)}")

async def _run_trivy_scan(target: str) -> Dict[str, Any]:
    """Run Trivy vulnerability scan"""
    try:
        # Run Trivy scan
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
            
            high_issues = len([check for check in scan_data.get("results", {}).get("failed_checks", []) 
                             if check.get("severity") == "HIGH"])
            medium_issues = len([check for check in scan_data.get("results", {}).get("failed_checks", []) 
                               if check.get("severity") == "MEDIUM"])
            low_issues = len([check for check in scan_data.get("results", {}).get("failed_checks", []) 
                            if check.get("severity") == "LOW"])
            
            return {
                "scan_type": "checkov",
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
                "scan_type": "checkov",
                "target": target,
                "error": result.stderr,
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
        cmd = ["snyk", "test", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode in [0, 1]:  # Snyk returns 1 if vulnerabilities found
            scan_data = json.loads(result.stdout)
            
            high_vulns = len([vuln for vuln in scan_data.get("vulnerabilities", []) 
                            if vuln.get("severity") == "high"])
            medium_vulns = len([vuln for vuln in scan_data.get("vulnerabilities", []) 
                              if vuln.get("severity") == "medium"])
            low_vulns = len([vuln for vuln in scan_data.get("vulnerabilities", []) 
                           if vuln.get("severity") == "low"])
            
            return {
                "scan_type": "snyk",
                "target": target,
                "high_vulnerabilities": high_vulns,
                "medium_vulnerabilities": medium_vulns,
                "low_vulnerabilities": low_vulns,
                "total_vulnerabilities": high_vulns + medium_vulns + low_vulns,
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode in [0, 1]:  # Semgrep returns 1 if issues found
            scan_data = json.loads(result.stdout)
            
            high_issues = len([finding for finding in scan_data.get("results", []) 
                             if finding.get("extra", {}).get("severity") == "ERROR"])
            medium_issues = len([finding for finding in scan_data.get("results", []) 
                               if finding.get("extra", {}).get("severity") == "WARNING"])
            low_issues = len([finding for finding in scan_data.get("results", []) 
                            if finding.get("extra", {}).get("severity") == "INFO"])
            
            return {
                "scan_type": "semgrep",
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
                "scan_type": "semgrep",
                "target": target,
                "error": result.stderr,
                "scan_successful": False
            }
            
    except Exception as e:
        return {
            "scan_type": "semgrep",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

async def _run_repository_audit(target: str) -> Dict[str, Any]:
    """Run comprehensive repository security audit"""
    try:
        audit_results = {
            "scan_type": "repo_audit",
            "target": target,
            "scan_successful": True,
            "audit_findings": []
        }
        
        # Check for secrets in repository
        secrets_found = _check_for_secrets(target)
        audit_results["audit_findings"].append({
            "type": "secrets_detection",
            "findings": secrets_found
        })
        
        # Check for exposed credentials
        credentials_found = _check_for_credentials(target)
        audit_results["audit_findings"].append({
            "type": "credentials_detection",
            "findings": credentials_found
        })
        
        # Check for sensitive files
        sensitive_files = _check_for_sensitive_files(target)
        audit_results["audit_findings"].append({
            "type": "sensitive_files",
            "findings": sensitive_files
        })
        
        return audit_results
        
    except Exception as e:
        return {
            "scan_type": "repo_audit",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

def _check_for_secrets(target: str) -> List[Dict[str, Any]]:
    """Check for secrets in repository"""
    secrets_patterns = [
        r"api_key\s*[:=]\s*['\"][^'\"]+['\"]",
        r"password\s*[:=]\s*['\"][^'\"]+['\"]",
        r"secret\s*[:=]\s*['\"][^'\"]+['\"]",
        r"token\s*[:=]\s*['\"][^'\"]+['\"]",
        r"private_key\s*[:=]\s*['\"][^'\"]+['\"]"
    ]
    
    findings = []
    
    for root, dirs, files in os.walk(target):
        for file in files:
            if file.endswith(('.py', '.js', '.json', '.yaml', '.yml', '.env')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern in secrets_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                findings.append({
                                    "file": file_path,
                                    "pattern": pattern,
                                    "matches": len(matches),
                                    "severity": "HIGH"
                                })
                except Exception:
                    continue
    
    return findings

def _check_for_credentials(target: str) -> List[Dict[str, Any]]:
    """Check for exposed credentials"""
    credential_patterns = [
        r"aws_access_key_id\s*[:=]\s*['\"][^'\"]+['\"]",
        r"aws_secret_access_key\s*[:=]\s*['\"][^'\"]+['\"]",
        r"database_url\s*[:=]\s*['\"][^'\"]+['\"]",
        r"connection_string\s*[:=]\s*['\"][^'\"]+['\"]"
    ]
    
    findings = []
    
    for root, dirs, files in os.walk(target):
        for file in files:
            if file.endswith(('.py', '.js', '.json', '.yaml', '.yml', '.env')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern in credential_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                findings.append({
                                    "file": file_path,
                                    "pattern": pattern,
                                    "matches": len(matches),
                                    "severity": "CRITICAL"
                                })
                except Exception:
                    continue
    
    return findings

def _check_for_sensitive_files(target: str) -> List[Dict[str, Any]]:
    """Check for sensitive files"""
    sensitive_files = [
        ".env", ".env.local", ".env.production",
        "id_rsa", "id_rsa.pub", "private.key",
        "config.json", "secrets.json", "credentials.json"
    ]
    
    findings = []
    
    for root, dirs, files in os.walk(target):
        for file in files:
            if file in sensitive_files:
                file_path = os.path.join(root, file)
                findings.append({
                    "file": file_path,
                    "type": "sensitive_file",
                    "severity": "HIGH"
                })
    
    return findings

def _sanitize_audit_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize audit results for compliance"""
    sanitized = result.copy()
    
    # Remove sensitive information from raw data
    if "raw_data" in sanitized:
        sanitized["raw_data"] = "[SANITIZED_RAW_DATA]"
    
    # Replace file paths with placeholders
    if "target" in sanitized:
        sanitized["target"] = "[SANITIZED_TARGET_PATH]"
    
    # Sanitize any findings that might contain sensitive data
    if "audit_findings" in sanitized:
        for finding in sanitized["audit_findings"]:
            if "file" in finding:
                finding["file"] = "[SANITIZED_FILE_PATH]"
    
    return sanitized

def _generate_solution_path(result: Dict[str, Any], scan_type: str) -> str:
    """Generate recommended solution path based on scan results"""
    if not result.get("scan_successful", False):
        return "Investigate scan failure and retry"
    
    if scan_type == "trivy":
        high_risk = result.get("high_risk", 0)
        if high_risk > 0:
            return f"Update {high_risk} high-risk dependencies immediately"
        elif result.get("total_vulnerabilities", 0) > 0:
            return "Update vulnerable dependencies in next release cycle"
        else:
            return "No immediate action required - dependencies are secure"
    
    elif scan_type == "bandit":
        high_issues = result.get("high_issues", 0)
        if high_issues > 0:
            return f"Fix {high_issues} high-severity security issues in code"
        elif result.get("total_issues", 0) > 0:
            return "Review and fix security issues in code review"
        else:
            return "No security issues detected in code"
    
    elif scan_type == "checkov":
        high_issues = result.get("high_issues", 0)
        if high_issues > 0:
            return f"Fix {high_issues} high-severity infrastructure issues"
        elif result.get("total_issues", 0) > 0:
            return "Review and fix infrastructure security issues"
        else:
            return "Infrastructure configuration is secure"
    
    elif scan_type == "repo_audit":
        critical_findings = sum(1 for finding in result.get("audit_findings", [])
                              for item in finding.get("findings", [])
                              if item.get("severity") == "CRITICAL")
        if critical_findings > 0:
            return f"Immediate action required: {critical_findings} critical security findings"
        else:
            return "Repository security audit passed"
    
    return "Review scan results and take appropriate action"

def _determine_compliance_tags(result: Dict[str, Any], scope: List[str]) -> List[str]:
    """Determine applicable compliance tags based on scan results"""
    tags = scope.copy()
    
    # Add specific compliance tags based on findings
    if result.get("scan_successful", False):
        if result.get("high_risk", 0) > 0 or result.get("high_issues", 0) > 0:
            tags.extend(["ISO27001", "NIST"])
        
        if "repo_audit" in result.get("scan_type", ""):
            tags.extend(["SOX", "PCI-DSS"])
    
    return list(set(tags))  # Remove duplicates

async def _log_audit_result(audit_result: AuditResult):
    """Log audit result to backend"""
    try:
        # This would typically send to the backend logging system
        # For now, we'll log locally
        log_entry = {
            "id": str(uuid.uuid4()),
            "agent": audit_result.agent,
            "task_id": audit_result.task_id,
            "action": audit_result.action,
            "result": json.dumps(audit_result.result),
            "solution_path": audit_result.solution_path,
            "error_outcome": audit_result.error_outcome,
            "sanitized": audit_result.sanitized,
            "approved": audit_result.approved,
            "auto_approved": audit_result.auto_approved,
            "compliance_tags": json.dumps(audit_result.compliance_tags),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Log to file for now
        with open("/app/logs/auditguard.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"Audit result logged: {audit_result.task_id}")
        
    except Exception as e:
        logger.error(f"Failed to log audit result: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 