"""
FickNury Meta-Agent - Agent Orchestration & Deployment Controller
Receives intelligence from Whis and makes decisions about agent creation, upgrades, and deployment
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import logging
import subprocess
import os
import yaml
from datetime import datetime
import uuid
import requests

app = FastAPI(title="FickNury Meta-Agent - Orchestration & Deployment")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentProposal(BaseModel):
    task_id: str
    agent_name: str
    agent_type: str  # "new", "upgrade", "deploy"
    intelligence_source: str  # "whis", "manual", "external"
    reasoning: str
    capabilities: List[str]
    deployment_target: str  # "docker", "kubernetes", "local"
    priority: str = "medium"  # "high", "medium", "low"

class DeploymentRequest(BaseModel):
    task_id: str
    agent_name: str
    version: str
    deployment_target: str
    configuration: Dict[str, Any]
    auto_approve: bool = False

class OrchestrationResult(BaseModel):
    agent: str = "ficknury"
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
        "agent": "ficknury",
        "specialization": "Agent Orchestration & Deployment",
        "capabilities": [
            "Agent creation and deployment",
            "Agent version management",
            "Kubernetes cluster orchestration",
            "Docker container management",
            "Intelligence-driven decisions",
            "Multi-cluster deployment",
            "Agent lifecycle management"
        ]
    }

@app.post("/propose-agent")
async def propose_agent(proposal: AgentProposal, background_tasks: BackgroundTasks):
    """
    Propose creation, upgrade, or deployment of an agent based on intelligence
    """
    try:
        logger.info(f"FickNury processing agent proposal: {proposal.agent_name} ({proposal.agent_type})")
        
        # Analyze the proposal
        analysis = _analyze_agent_proposal(proposal)
        
        # Make deployment decision
        decision = _make_deployment_decision(proposal, analysis)
        
        # Execute deployment if approved
        if decision["approved"]:
            deployment_result = await _execute_deployment(proposal, decision)
        else:
            deployment_result = {"status": "proposal_rejected", "reason": decision["reason"]}
        
        # Create orchestration result
        result = OrchestrationResult(
            task_id=proposal.task_id,
            action=f"Agent {proposal.agent_type} proposal processed",
            result={
                "proposal": proposal.dict(),
                "analysis": analysis,
                "decision": decision,
                "deployment_result": deployment_result
            },
            solution_path=decision.get("solution_path"),
            sanitized=True,
            approved=decision["approved"],
            auto_approved=decision.get("auto_approved", False),
            compliance_tags=["ISO27001", "NIST"]
        )
        
        # Log the orchestration result
        background_tasks.add_task(_log_orchestration_result, result)
        
        logger.info(f"FickNury completed agent proposal with decision: {decision['approved']}")
        return result
        
    except Exception as e:
        logger.error(f"FickNury proposal processing failed: {str(e)}")
        error_result = OrchestrationResult(
            task_id=proposal.task_id,
            action=f"Agent {proposal.agent_type} proposal failed",
            result={"error": "Proposal processing failed"},
            error_outcome=str(e),
            sanitized=True,
            approved=False,
            compliance_tags=["ISO27001", "NIST"]
        )
        background_tasks.add_task(_log_orchestration_result, error_result)
        raise HTTPException(status_code=500, detail=f"Proposal processing failed: {str(e)}")

@app.post("/deploy-agent")
async def deploy_agent(request: DeploymentRequest, background_tasks: BackgroundTasks):
    """
    Deploy an agent to the specified target environment
    """
    try:
        logger.info(f"FickNury deploying agent: {request.agent_name} to {request.deployment_target}")
        
        # Validate deployment request
        validation = _validate_deployment_request(request)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["reason"])
        
        # Execute deployment
        deployment_result = await _execute_deployment_by_type(request)
        
        # Create orchestration result
        result = OrchestrationResult(
            task_id=request.task_id,
            action=f"Agent deployment to {request.deployment_target}",
            result=deployment_result,
            solution_path=deployment_result.get("solution_path"),
            sanitized=True,
            approved=request.auto_approve,
            auto_approved=request.auto_approve,
            compliance_tags=["ISO27001", "NIST"]
        )
        
        # Log the orchestration result
        background_tasks.add_task(_log_orchestration_result, result)
        
        logger.info(f"FickNury completed agent deployment: {deployment_result['status']}")
        return result
        
    except Exception as e:
        logger.error(f"FickNury deployment failed: {str(e)}")
        error_result = OrchestrationResult(
            task_id=request.task_id,
            action=f"Agent deployment failed",
            result={"error": "Deployment failed"},
            error_outcome=str(e),
            sanitized=True,
            approved=False,
            compliance_tags=["ISO27001", "NIST"]
        )
        background_tasks.add_task(_log_orchestration_result, error_result)
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@app.get("/agent-status")
async def get_agent_status():
    """
    Get status of all deployed agents
    """
    try:
        # Check Docker containers
        docker_agents = _get_docker_agent_status()
        
        # Check Kubernetes deployments
        k8s_agents = _get_kubernetes_agent_status()
        
        # Check local processes
        local_agents = _get_local_agent_status()
        
        return {
            "docker_agents": docker_agents,
            "kubernetes_agents": k8s_agents,
            "local_agents": local_agents,
            "total_agents": len(docker_agents) + len(k8s_agents) + len(local_agents)
        }
        
    except Exception as e:
        logger.error(f"Failed to get agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

def _analyze_agent_proposal(proposal: AgentProposal) -> Dict[str, Any]:
    """Analyze agent proposal for feasibility and impact"""
    analysis = {
        "feasibility_score": 0.0,
        "impact_score": 0.0,
        "resource_requirements": {},
        "risks": [],
        "recommendations": []
    }
    
    # Calculate feasibility score
    if proposal.agent_type == "new":
        analysis["feasibility_score"] = 0.7  # New agents require more work
    elif proposal.agent_type == "upgrade":
        analysis["feasibility_score"] = 0.9  # Upgrades are usually feasible
    elif proposal.agent_type == "deploy":
        analysis["feasibility_score"] = 0.95  # Deployments are highly feasible
    
    # Calculate impact score based on capabilities
    capability_impact = {
        "security": 0.9,
        "compliance": 0.8,
        "automation": 0.7,
        "monitoring": 0.6,
        "analysis": 0.7
    }
    
    impact_score = 0.0
    for capability in proposal.capabilities:
        for key, value in capability_impact.items():
            if key in capability.lower():
                impact_score += value
    
    analysis["impact_score"] = min(impact_score / len(proposal.capabilities), 1.0)
    
    # Assess resource requirements
    analysis["resource_requirements"] = {
        "cpu": "100m-500m",
        "memory": "128Mi-512Mi",
        "storage": "1Gi-5Gi"
    }
    
    # Identify risks
    if proposal.deployment_target == "kubernetes":
        analysis["risks"].append("Kubernetes cluster availability")
    elif proposal.deployment_target == "docker":
        analysis["risks"].append("Docker daemon availability")
    
    # Generate recommendations
    if analysis["feasibility_score"] < 0.5:
        analysis["recommendations"].append("Consider alternative approach")
    if analysis["impact_score"] < 0.5:
        analysis["recommendations"].append("Low impact - consider deferring")
    
    return analysis

def _make_deployment_decision(proposal: AgentProposal, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Make deployment decision based on analysis"""
    decision = {
        "approved": False,
        "reason": "",
        "auto_approved": False,
        "solution_path": ""
    }
    
    # Auto-approve high-impact, feasible proposals
    if analysis["feasibility_score"] > 0.8 and analysis["impact_score"] > 0.7:
        decision["approved"] = True
        decision["auto_approved"] = True
        decision["reason"] = "High feasibility and impact"
        decision["solution_path"] = f"Deploy {proposal.agent_name} to {proposal.deployment_target}"
    
    # Approve medium-impact proposals with manual review
    elif analysis["feasibility_score"] > 0.6 and analysis["impact_score"] > 0.5:
        decision["approved"] = True
        decision["auto_approved"] = False
        decision["reason"] = "Medium feasibility and impact - requires review"
        decision["solution_path"] = f"Review and deploy {proposal.agent_name}"
    
    # Reject low-feasibility or low-impact proposals
    else:
        decision["approved"] = False
        decision["reason"] = "Low feasibility or impact"
        decision["solution_path"] = "Reconsider proposal or defer deployment"
    
    return decision

async def _execute_deployment(proposal: AgentProposal, decision: Dict[str, Any]) -> Dict[str, Any]:
    """Execute agent deployment"""
    try:
        if proposal.deployment_target == "docker":
            return await _deploy_to_docker(proposal)
        elif proposal.deployment_target == "kubernetes":
            return await _deploy_to_kubernetes(proposal)
        elif proposal.deployment_target == "local":
            return await _deploy_locally(proposal)
        else:
            return {"status": "error", "reason": f"Unsupported deployment target: {proposal.deployment_target}"}
    except Exception as e:
        return {"status": "error", "reason": str(e)}

async def _deploy_to_docker(proposal: AgentProposal) -> Dict[str, Any]:
    """Deploy agent to Docker"""
    try:
        # Build Docker image
        build_cmd = [
            "docker", "build", "-t", f"linkops-{proposal.agent_name}:latest",
            f"../{proposal.agent_name}/"
        ]
        build_result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if build_result.returncode != 0:
            return {
                "status": "error",
                "reason": f"Docker build failed: {build_result.stderr}",
                "solution_path": "Fix Dockerfile and retry build"
            }
        
        # Run Docker container
        run_cmd = [
            "docker", "run", "-d", "--name", f"linkops-{proposal.agent_name}",
            "-p", "8000:8000", f"linkops-{proposal.agent_name}:latest"
        ]
        run_result = subprocess.run(run_cmd, capture_output=True, text=True)
        
        if run_result.returncode != 0:
            return {
                "status": "error",
                "reason": f"Docker run failed: {run_result.stderr}",
                "solution_path": "Check container logs and fix configuration"
            }
        
        return {
            "status": "success",
            "deployment_target": "docker",
            "container_id": run_result.stdout.strip(),
            "solution_path": f"Agent {proposal.agent_name} deployed to Docker successfully"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "solution_path": "Check Docker daemon and retry deployment"
        }

async def _deploy_to_kubernetes(proposal: AgentProposal) -> Dict[str, Any]:
    """Deploy agent to Kubernetes"""
    try:
        # Generate Kubernetes manifests
        manifests = _generate_kubernetes_manifests(proposal)
        
        # Apply manifests
        for manifest in manifests:
            apply_cmd = ["kubectl", "apply", "-f", "-"]
            apply_result = subprocess.run(
                apply_cmd, 
                input=yaml.dump(manifest), 
                capture_output=True, 
                text=True
            )
            
            if apply_result.returncode != 0:
                return {
                    "status": "error",
                    "reason": f"Kubernetes apply failed: {apply_result.stderr}",
                    "solution_path": "Check Kubernetes cluster and retry deployment"
                }
        
        return {
            "status": "success",
            "deployment_target": "kubernetes",
            "manifests_applied": len(manifests),
            "solution_path": f"Agent {proposal.agent_name} deployed to Kubernetes successfully"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "solution_path": "Check Kubernetes configuration and retry deployment"
        }

async def _deploy_locally(proposal: AgentProposal) -> Dict[str, Any]:
    """Deploy agent locally"""
    try:
        # Start local process
        agent_path = f"../{proposal.agent_name}/src/main.py"
        if not os.path.exists(agent_path):
            return {
                "status": "error",
                "reason": f"Agent source not found: {agent_path}",
                "solution_path": "Check agent source code and retry deployment"
            }
        
        # Start process in background
        process = subprocess.Popen(
            ["python", agent_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return {
            "status": "success",
            "deployment_target": "local",
            "process_id": process.pid,
            "solution_path": f"Agent {proposal.agent_name} started locally"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "solution_path": "Check Python environment and retry deployment"
        }

def _generate_kubernetes_manifests(proposal: AgentProposal) -> List[Dict[str, Any]]:
    """Generate Kubernetes manifests for agent deployment"""
    manifests = []
    
    # Deployment manifest
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"linkops-{proposal.agent_name}",
            "labels": {
                "app": f"linkops-{proposal.agent_name}",
                "agent": proposal.agent_name
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": f"linkops-{proposal.agent_name}"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": f"linkops-{proposal.agent_name}"
                    }
                },
                "spec": {
                    "containers": [{
                        "name": proposal.agent_name,
                        "image": f"linkops-{proposal.agent_name}:latest",
                        "ports": [{
                            "containerPort": 8000
                        }],
                        "resources": {
                            "requests": {
                                "memory": "128Mi",
                                "cpu": "100m"
                            },
                            "limits": {
                                "memory": "512Mi",
                                "cpu": "500m"
                            }
                        }
                    }]
                }
            }
        }
    }
    manifests.append(deployment)
    
    # Service manifest
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"linkops-{proposal.agent_name}-service"
        },
        "spec": {
            "selector": {
                "app": f"linkops-{proposal.agent_name}"
            },
            "ports": [{
                "protocol": "TCP",
                "port": 80,
                "targetPort": 8000
            }],
            "type": "ClusterIP"
        }
    }
    manifests.append(service)
    
    return manifests

def _validate_deployment_request(request: DeploymentRequest) -> Dict[str, Any]:
    """Validate deployment request"""
    validation = {
        "valid": True,
        "reason": ""
    }
    
    # Check required fields
    if not request.agent_name:
        validation["valid"] = False
        validation["reason"] = "Agent name is required"
        return validation
    
    if not request.deployment_target:
        validation["valid"] = False
        validation["reason"] = "Deployment target is required"
        return validation
    
    # Check deployment target availability
    if request.deployment_target == "docker":
        try:
            subprocess.run(["docker", "version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            validation["valid"] = False
            validation["reason"] = "Docker is not available"
            return validation
    
    elif request.deployment_target == "kubernetes":
        try:
            subprocess.run(["kubectl", "version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            validation["valid"] = False
            validation["reason"] = "Kubernetes is not available"
            return validation
    
    return validation

async def _execute_deployment_by_type(request: DeploymentRequest) -> Dict[str, Any]:
    """Execute deployment based on request type"""
    if request.deployment_target == "docker":
        return await _deploy_to_docker_by_request(request)
    elif request.deployment_target == "kubernetes":
        return await _deploy_to_kubernetes_by_request(request)
    elif request.deployment_target == "local":
        return await _deploy_locally_by_request(request)
    else:
        return {"status": "error", "reason": f"Unsupported deployment target: {request.deployment_target}"}

async def _deploy_to_docker_by_request(request: DeploymentRequest) -> Dict[str, Any]:
    """Deploy to Docker based on deployment request"""
    # Similar to _deploy_to_docker but with request-specific configuration
    return await _deploy_to_docker(AgentProposal(
        task_id=request.task_id,
        agent_name=request.agent_name,
        agent_type="deploy",
        intelligence_source="manual",
        reasoning="Direct deployment request",
        capabilities=[],
        deployment_target=request.deployment_target
    ))

async def _deploy_to_kubernetes_by_request(request: DeploymentRequest) -> Dict[str, Any]:
    """Deploy to Kubernetes based on deployment request"""
    # Similar to _deploy_to_kubernetes but with request-specific configuration
    return await _deploy_to_kubernetes(AgentProposal(
        task_id=request.task_id,
        agent_name=request.agent_name,
        agent_type="deploy",
        intelligence_source="manual",
        reasoning="Direct deployment request",
        capabilities=[],
        deployment_target=request.deployment_target
    ))

async def _deploy_locally_by_request(request: DeploymentRequest) -> Dict[str, Any]:
    """Deploy locally based on deployment request"""
    # Similar to _deploy_locally but with request-specific configuration
    return await _deploy_locally(AgentProposal(
        task_id=request.task_id,
        agent_name=request.agent_name,
        agent_type="deploy",
        intelligence_source="manual",
        reasoning="Direct deployment request",
        capabilities=[],
        deployment_target=request.deployment_target
    ))

def _get_docker_agent_status() -> List[Dict[str, Any]]:
    """Get status of Docker agents"""
    try:
        cmd = ["docker", "ps", "--format", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    container = json.loads(line)
                    if "linkops-" in container.get("Names", ""):
                        containers.append({
                            "name": container.get("Names", ""),
                            "status": container.get("Status", ""),
                            "ports": container.get("Ports", ""),
                            "deployment_target": "docker"
                        })
            return containers
        else:
            return []
    except Exception:
        return []

def _get_kubernetes_agent_status() -> List[Dict[str, Any]]:
    """Get status of Kubernetes agents"""
    try:
        cmd = ["kubectl", "get", "deployments", "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            deployments = json.loads(result.stdout)
            agents = []
            for deployment in deployments.get("items", []):
                name = deployment.get("metadata", {}).get("name", "")
                if "linkops-" in name:
                    agents.append({
                        "name": name,
                        "status": deployment.get("status", {}).get("conditions", [{}])[0].get("type", ""),
                        "replicas": deployment.get("status", {}).get("readyReplicas", 0),
                        "deployment_target": "kubernetes"
                    })
            return agents
        else:
            return []
    except Exception:
        return []

def _get_local_agent_status() -> List[Dict[str, Any]]:
    """Get status of local agents"""
    try:
        cmd = ["ps", "aux"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            processes = []
            for line in result.stdout.strip().split('\n'):
                if "python" in line and "main.py" in line and "agents" in line:
                    parts = line.split()
                    if len(parts) > 1:
                        processes.append({
                            "name": f"local-agent-{parts[1]}",
                            "status": "running",
                            "pid": parts[1],
                            "deployment_target": "local"
                        })
            return processes
        else:
            return []
    except Exception:
        return []

async def _log_orchestration_result(result: OrchestrationResult):
    """Log orchestration result to backend"""
    try:
        # This would typically send to the backend logging system
        # For now, we'll log locally
        log_entry = {
            "id": str(uuid.uuid4()),
            "agent": result.agent,
            "task_id": result.task_id,
            "action": result.action,
            "result": json.dumps(result.result),
            "solution_path": result.solution_path,
            "error_outcome": result.error_outcome,
            "sanitized": result.sanitized,
            "approved": result.approved,
            "auto_approved": result.auto_approved,
            "compliance_tags": json.dumps(result.compliance_tags),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Log to file for now
        with open("/app/logs/ficknury.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"Orchestration result logged: {result.task_id}")
        
    except Exception as e:
        logger.error(f"Failed to log orchestration result: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 