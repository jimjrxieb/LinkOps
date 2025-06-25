"""
AuditGuard Service - PwC-aligned Security & Compliance Microservice
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

app = FastAPI(title="AuditGuard Service - Security & Compliance Specialist")

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
        "service": "auditguard",
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

async def _run_repository_audit(target: str) -> Dict[str, Any]:
    """Run comprehensive repository security audit"""
    try:
        # Check for secrets
        secrets = _check_for_secrets(target)
        
        # Check for credentials
        credentials = _check_for_credentials(target)
        
        # Check for sensitive files
        sensitive_files = _check_for_sensitive_files(target)
        
        return {
            "scan_type": "repo_audit",
            "target": target,
            "secrets_found": len(secrets),
            "credentials_found": len(credentials),
            "sensitive_files_found": len(sensitive_files),
            "secrets": secrets,
            "credentials": credentials,
            "sensitive_files": sensitive_files,
            "scan_successful": True
        }
        
    except Exception as e:
        return {
            "scan_type": "repo_audit",
            "target": target,
            "error": str(e),
            "scan_successful": False
        }

def _check_for_secrets(target: str) -> List[Dict[str, Any]]:
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
        r'aws_secret_access_key["\']?\s*[:=]\s*["\'][^"\']+["\']'
    ]
    
    try:
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith(('.py', '.js', '.json', '.yaml', '.yml', '.env')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for pattern in secret_patterns:
                                matches = re.finditer(pattern, content, re.IGNORECASE)
                                for match in matches:
                                    secrets.append({
                                        "file": file_path,
                                        "line": content[:match.start()].count('\n') + 1,
                                        "pattern": pattern,
                                        "severity": "high"
                                    })
                    except Exception:
                        continue
    except Exception as e:
        logger.error(f"Error scanning for secrets: {str(e)}")
    
    return secrets

def _check_for_credentials(target: str) -> List[Dict[str, Any]]:
    """Check for hardcoded credentials"""
    credentials = []
    
    # Credential patterns
    credential_patterns = [
        r'username["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'user["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'login["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'email["\']?\s*[:=]\s*["\'][^"\']+["\']',
        r'admin["\']?\s*[:=]\s*["\'][^"\']+["\']'
    ]
    
    try:
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith(('.py', '.js', '.json', '.yaml', '.yml', '.env', '.conf')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for pattern in credential_patterns:
                                matches = re.finditer(pattern, content, re.IGNORECASE)
                                for match in matches:
                                    credentials.append({
                                        "file": file_path,
                                        "line": content[:match.start()].count('\n') + 1,
                                        "pattern": pattern,
                                        "severity": "medium"
                                    })
                    except Exception:
                        continue
    except Exception as e:
        logger.error(f"Error scanning for credentials: {str(e)}")
    
    return credentials

def _check_for_sensitive_files(target: str) -> List[Dict[str, Any]]:
    """Check for sensitive files"""
    sensitive_files = []
    
    # Sensitive file patterns
    sensitive_patterns = [
        r'\.env$',
        r'\.pem$',
        r'\.key$',
        r'\.crt$',
        r'\.p12$',
        r'\.pfx$',
        r'id_rsa$',
        r'id_dsa$',
        r'\.keystore$',
        r'\.jks$'
    ]
    
    try:
        for root, dirs, files in os.walk(target):
            for file in files:
                for pattern in sensitive_patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        file_path = os.path.join(root, file)
                        sensitive_files.append({
                            "file": file_path,
                            "pattern": pattern,
                            "severity": "high",
                            "recommendation": "Move to secure storage or add to .gitignore"
                        })
                        break
    except Exception as e:
        logger.error(f"Error scanning for sensitive files: {str(e)}")
    
    return sensitive_files

def _sanitize_audit_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize audit results for compliance"""
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
    elif scan_type == "repo_audit":
        total_issues = (result.get("secrets_found", 0) + 
                       result.get("credentials_found", 0) + 
                       result.get("sensitive_files_found", 0))
        if total_issues > 0:
            return "Remove secrets, credentials, and sensitive files from repository"
    else:
        return f"Security scan {scan_type} passed - no immediate action required"

def _determine_compliance_tags(result: Dict[str, Any], scope: List[str]) -> List[str]:
    """Determine compliance tags based on scan results"""
    tags = []
    
    # Add default compliance tags
    tags.extend(scope)
    
    # Add specific tags based on findings
    if result.get("high_risk", 0) > 0 or result.get("high_issues", 0) > 0:
        tags.append("HIGH_RISK")
    
    if result.get("secrets_found", 0) > 0:
        tags.append("SECRETS_DETECTED")
    
    return tags

async def _log_audit_result(audit_result: AuditResult):
    """Log audit result to external system"""
    try:
        # Log to external system (e.g., database, logging service)
        logger.info(f"Audit result logged: {audit_result.task_id}")
        
        # In a real implementation, this would send to:
        # - Database for audit trail
        # - Logging service for monitoring
        # - Compliance reporting system
        
    except Exception as e:
        logger.error(f"Failed to log audit result: {str(e)}") 