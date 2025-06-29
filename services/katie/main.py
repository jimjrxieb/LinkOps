"""
Katie - Kubernetes AI Agent and Cluster Guardian
Handles all Kubernetes operations with intelligent analysis and K8GPT fallback
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import requests

# Import Katie's Kubernetes operations
from kubeops.describe import k8s_describer
from kubeops.scale import k8s_scaler
from kubeops.logs import k8s_log_analyzer
from kubeops.patch import k8s_patcher

app = FastAPI(
    title="Katie - Kubernetes AI Agent",
    description="Cluster Guardian with intelligent K8s operations and K8GPT integration",
    version="2.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# K8GPT configuration
K8GPT_API_URL = "https://api.k8gpt.ai/v1/analyze"  # Example K8GPT endpoint
K8GPT_ENABLED = True


class KubernetesTask(BaseModel):
    task_id: str
    task_type: str  # describe, scale, logs, patch, apply
    resource_type: str  # pod, deployment, service, namespace
    resource_name: str
    namespace: str = "default"
    parameters: Optional[Dict[str, Any]] = None


class KatieResponse(BaseModel):
    agent: str = "katie"
    task: str
    response: str
    operation_result: Dict[str, Any]
    k8gpt_insight: Optional[str] = None
    confidence_score: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "katie",
        "role": "Kubernetes AI Agent & Cluster Guardian",
        "capabilities": [
            "Pod/Deployment/Service Description",
            "Intelligent Scaling Operations",
            "Log Analysis & Search",
            "Resource Patching & Updates",
            "Manifest Application",
            "Rollback Operations",
            "K8GPT Integration",
            "Error Pattern Analysis"
        ],
        "certifications": [
            "Kubernetes CKA",
            "Kubernetes CKS",
            "SRE Best Practices"
        ]
    }


@app.post("/execute")
def execute(data: KubernetesTask):
    """
    Katie executes Kubernetes tasks with intelligent analysis
    """
    try:
        logger.info(f"Katie executing {data.task_type} on {data.resource_type}: {data.resource_name}")

        # Execute the task based on type
        if data.task_type == "describe":
            result = _execute_describe_operation(data)
        elif data.task_type == "scale":
            result = _execute_scale_operation(data)
        elif data.task_type == "logs":
            result = _execute_logs_operation(data)
        elif data.task_type == "patch":
            result = _execute_patch_operation(data)
        elif data.task_type == "apply":
            result = _execute_apply_operation(data)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown task type: {data.task_type}")

        # Get K8GPT insight if enabled and needed
        k8gpt_insight = None
        if K8GPT_ENABLED and result.get("status") == "error":
            k8gpt_insight = _get_k8gpt_insight(data, result)

        # Create response
        response = KatieResponse(
            task=f"{data.task_type} {data.resource_type} {data.resource_name}",
            response=_generate_katie_response(data, result),
            operation_result=result,
            k8gpt_insight=k8gpt_insight,
            confidence_score=_calculate_confidence(result)
        )

        logger.info(f"Katie completed {data.task_type} operation")
        return response

    except Exception as e:
        logger.error(f"Katie execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Katie execution failed: {str(e)}")


@app.get("/describe/pod/{namespace}/{pod_name}")
def describe_pod(namespace: str, pod_name: str):
    """Describe a specific pod"""
    return k8s_describer.describe_pod(namespace, pod_name)


@app.get("/describe/deployment/{namespace}/{deployment_name}")
def describe_deployment(namespace: str, deployment_name: str):
    """Describe a deployment"""
    return k8s_describer.describe_deployment(namespace, deployment_name)


@app.get("/describe/service/{namespace}/{service_name}")
def describe_service(namespace: str, service_name: str):
    """Describe a service"""
    return k8s_describer.describe_service(namespace, service_name)


@app.get("/describe/namespace/{namespace}")
def describe_namespace(namespace: str):
    """Describe a namespace"""
    return k8s_describer.describe_namespace(namespace)


@app.get("/describe/pods/{namespace}")
def describe_all_pods(namespace: str = "default"):
    """Describe all pods in a namespace"""
    return k8s_describer.describe_all_pods(namespace)


@app.post("/scale/deployment/{namespace}/{deployment_name}")
def scale_deployment(namespace: str, deployment_name: str, replicas: int, dry_run: bool = False):
    """Scale a deployment"""
    return k8s_scaler.scale_deployment(namespace, deployment_name, replicas, dry_run)


@app.post("/scale/statefulset/{namespace}/{statefulset_name}")
def scale_statefulset(namespace: str, statefulset_name: str, replicas: int, dry_run: bool = False):
    """Scale a statefulset"""
    return k8s_scaler.scale_statefulset(namespace, statefulset_name, replicas, dry_run)


@app.post("/scale/autoscale/{namespace}/{deployment_name}")
def setup_autoscaling(namespace: str, deployment_name: str, min_replicas: int = 1, max_replicas: int = 10, target_cpu: int = 80):
    """Setup auto-scaling for a deployment"""
    return k8s_scaler.auto_scale_deployment(namespace, deployment_name, min_replicas, max_replicas, target_cpu)


@app.get("/logs/pod/{namespace}/{pod_name}")
def get_pod_logs(namespace: str, pod_name: str, container: Optional[str] = None, tail_lines: int = 100):
    """Get logs from a pod"""
    return k8s_log_analyzer.get_pod_logs(namespace, pod_name, container, tail_lines)


@app.get("/logs/deployment/{namespace}/{deployment_name}")
def get_deployment_logs(namespace: str, deployment_name: str, tail_lines: int = 50):
    """Get logs from all pods in a deployment"""
    return k8s_log_analyzer.get_deployment_logs(namespace, deployment_name, tail_lines)


@app.post("/logs/search/{namespace}")
def search_logs(namespace: str, search_pattern: str, pod_selector: Optional[str] = None, max_results: int = 100):
    """Search logs across pods"""
    return k8s_log_analyzer.search_logs(namespace, search_pattern, pod_selector, max_results=max_results)


@app.get("/logs/errors/{namespace}")
def analyze_errors(namespace: str, pod_name: Optional[str] = None, hours_back: int = 24):
    """Analyze error patterns in logs"""
    return k8s_log_analyzer.analyze_error_patterns(namespace, pod_name, hours_back)


@app.get("/logs/summary/{namespace}")
def get_log_summary(namespace: str, deployment_name: Optional[str] = None, hours_back: int = 1):
    """Get log activity summary"""
    return k8s_log_analyzer.get_log_summary(namespace, deployment_name, hours_back)


@app.post("/patch/deployment/{namespace}/{deployment_name}")
def patch_deployment(namespace: str, deployment_name: str, patch_data: Dict[str, Any], dry_run: bool = False):
    """Patch a deployment"""
    return k8s_patcher.patch_deployment(namespace, deployment_name, patch_data, dry_run)


@app.post("/patch/configmap/{namespace}/{configmap_name}")
def patch_configmap(namespace: str, configmap_name: str, patch_data: Dict[str, Any], dry_run: bool = False):
    """Patch a ConfigMap"""
    return k8s_patcher.patch_configmap(namespace, configmap_name, patch_data, dry_run)


@app.post("/patch/service/{namespace}/{service_name}")
def patch_service(namespace: str, service_name: str, patch_data: Dict[str, Any], dry_run: bool = False):
    """Patch a Service"""
    return k8s_patcher.patch_service(namespace, service_name, patch_data, dry_run)


@app.post("/apply/manifest")
def apply_manifest(manifest_yaml: str, namespace: str = "default", dry_run: bool = False):
    """Apply a Kubernetes manifest"""
    return k8s_patcher.apply_manifest(manifest_yaml, namespace, dry_run)


@app.post("/rollback/deployment/{namespace}/{deployment_name}")
def rollback_deployment(namespace: str, deployment_name: str, revision: Optional[int] = None):
    """Rollback a deployment"""
    return k8s_patcher.rollback_deployment(namespace, deployment_name, revision)


@app.get("/recommendations/{namespace}/{deployment_name}")
def get_scaling_recommendations(namespace: str, deployment_name: str):
    """Get intelligent scaling recommendations"""
    return k8s_scaler.get_scaling_recommendations(namespace, deployment_name)


@app.get("/capabilities")
def get_capabilities():
    """Get Katie's current capabilities"""
    return {
        "agent": "katie",
        "role": "Kubernetes AI Agent & Cluster Guardian",
        "specialization": "Kubernetes Operations & SRE",
        "current_capabilities": [
            "Pod/Deployment/Service Description",
            "Intelligent Scaling Operations",
            "Log Analysis & Search",
            "Resource Patching & Updates",
            "Manifest Application",
            "Rollback Operations",
            "Error Pattern Analysis",
            "Scaling Recommendations",
            "K8GPT Integration"
        ],
        "certifications": [
            "Kubernetes CKA",
            "Kubernetes CKS",
            "SRE Best Practices"
        ],
        "focus_areas": [
            "Cluster Operations",
            "Resource Management",
            "Troubleshooting",
            "Performance Optimization",
            "Security Hardening",
            "Automation"
        ]
    }


def _execute_describe_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute describe operations"""
    if data.resource_type == "pod":
        return k8s_describer.describe_pod(data.namespace, data.resource_name)
    elif data.resource_type == "deployment":
        return k8s_describer.describe_deployment(data.namespace, data.resource_name)
    elif data.resource_type == "service":
        return k8s_describer.describe_service(data.namespace, data.resource_name)
    elif data.resource_type == "namespace":
        return k8s_describer.describe_namespace(data.resource_name)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported resource type: {data.resource_type}")


def _execute_scale_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute scale operations"""
    parameters = data.parameters or {}
    replicas = parameters.get("replicas", 1)
    dry_run = parameters.get("dry_run", False)
    
    if data.resource_type == "deployment":
        return k8s_scaler.scale_deployment(data.namespace, data.resource_name, replicas, dry_run)
    elif data.resource_type == "statefulset":
        return k8s_scaler.scale_statefulset(data.namespace, data.resource_name, replicas, dry_run)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported scaling resource: {data.resource_type}")


def _execute_logs_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute logs operations"""
    parameters = data.parameters or {}
    tail_lines = parameters.get("tail_lines", 100)
    
    if data.resource_type == "pod":
        container = parameters.get("container")
        return k8s_log_analyzer.get_pod_logs(data.namespace, data.resource_name, container, tail_lines)
    elif data.resource_type == "deployment":
        return k8s_log_analyzer.get_deployment_logs(data.namespace, data.resource_name, tail_lines)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported logs resource: {data.resource_type}")


def _execute_patch_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute patch operations"""
    parameters = data.parameters or {}
    patch_data = parameters.get("patch_data", {})
    dry_run = parameters.get("dry_run", False)
    
    if data.resource_type == "deployment":
        return k8s_patcher.patch_deployment(data.namespace, data.resource_name, patch_data, dry_run)
    elif data.resource_type == "configmap":
        return k8s_patcher.patch_configmap(data.namespace, data.resource_name, patch_data, dry_run)
    elif data.resource_type == "service":
        return k8s_patcher.patch_service(data.namespace, data.resource_name, patch_data, dry_run)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported patch resource: {data.resource_type}")


def _execute_apply_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute apply operations"""
    parameters = data.parameters or {}
    manifest_yaml = parameters.get("manifest_yaml", "")
    dry_run = parameters.get("dry_run", False)
    
    return k8s_patcher.apply_manifest(manifest_yaml, data.namespace, dry_run)


def _get_k8gpt_insight(data: KubernetesTask, result: Dict[str, Any]) -> Optional[str]:
    """Get K8GPT insight for error analysis"""
    try:
        if not K8GPT_ENABLED:
            return None
        
        # Prepare context for K8GPT
        context = {
            "task_type": data.task_type,
            "resource_type": data.resource_type,
            "resource_name": data.resource_name,
            "namespace": data.namespace,
            "error": result.get("error", ""),
            "operation_result": result
        }
        
        # Call K8GPT API (example implementation)
        response = requests.post(
            K8GPT_API_URL,
            json=context,
            timeout=30
        )
        
        if response.status_code == 200:
            k8gpt_data = response.json()
            return k8gpt_data.get("insight", "K8GPT analysis unavailable")
        else:
            return "K8GPT analysis failed"
            
    except Exception as e:
        logger.warning(f"K8GPT integration failed: {e}")
        return "K8GPT analysis unavailable"


def _generate_katie_response(data: KubernetesTask, result: Dict[str, Any]) -> str:
    """Generate Katie's response message"""
    if result.get("status") == "error":
        return f"Katie encountered an issue with {data.task_type} on {data.resource_type} {data.resource_name}: {result.get('error', 'Unknown error')}"
    
    # Use Katie's insight if available
    if "katie_insight" in result:
        return result["katie_insight"]
    
    # Generate default response
    return f"Katie successfully completed {data.task_type} operation on {data.resource_type} {data.resource_name}"


def _calculate_confidence(result: Dict[str, Any]) -> float:
    """Calculate confidence score based on operation result"""
    if result.get("status") == "error":
        return 0.0
    
    # Base confidence
    confidence = 0.8
    
    # Adjust based on operation type and success indicators
    if "katie_insight" in result:
        confidence += 0.1
    
    if result.get("operation_result", {}).get("status") == "success":
        confidence += 0.1
    
    return min(confidence, 1.0)
