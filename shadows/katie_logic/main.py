"""
Katie - Kubernetes AI Agent and Cluster Guardian
Handles all Kubernetes operations with intelligent analysis and K8GPT fallback
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging

# Import Katie's Kubernetes operations
from kubeops.describe import k8s_describer
from kubeops.scale import k8s_scaler
from kubeops.logs import k8s_log_analyzer
from kubeops.patch import k8s_patcher

# Import new CKA/CKS modules
from cka_operations import cka_operations
from cks_security import cks_security

app = FastAPI(
    title="Katie - Kubernetes AI Agent",
    description=(
        "Cluster Guardian with intelligent K8s operations and K8GPT integration"
    ),
    version="2.0.0",
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


class SecurityAnalysisRequest(BaseModel):
    cluster_config: Dict[str, Any]
    compliance_standard: str = "cis"


class ThreatDetectionRequest(BaseModel):
    cluster_events: List[Dict[str, Any]]
    logs: List[str]


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
            "Error Pattern Analysis",
            "CKA Operations & Troubleshooting",
            "CKS Security Analysis",
            "Helm Chart Analysis",
            "ArgoCD Application Management",
            "Terraform AKS Patterns",
            "Security Policy Enforcement",
            "Vulnerability Scanning",
            "Compliance Auditing",
            "Threat Detection",
            "Container Runtime Security",
            "Secrets Management",
            "Network Security Configuration",
        ],
        "certifications": ["CKA", "Kubernetes CKS", "SRE Best Practices"],
    }


@app.post("/execute")
def execute(data: KubernetesTask):
    """
    Katie executes Kubernetes tasks with intelligent analysis
    """
    try:
        logger.info(
            f"Katie executing {data.task_type} on {data.resource_type}: "
            f"{data.resource_name}"
        )

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
            raise HTTPException(
                status_code=400, detail=f"Unknown task type: {data.task_type}"
            )

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
            confidence_score=_calculate_confidence(result),
        )

        logger.info(f"Katie completed {data.task_type} operation")
        return response

    except Exception as e:
        logger.error(f"Katie execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Katie execution failed: {str(e)}")


@app.get("/describe/pod/{namespace}/{pod_name}")
def describe_pod(namespace: str, pod_name: str):
    """Describe a specific pod"""
    result = k8s_describer.describe_pod(namespace, pod_name)
    return {
        "pod_name": pod_name,
        "namespace": namespace,
        "status": result.get("status", "unknown"),
        "details": result,
    }


@app.get("/describe/deployment/{namespace}/{deployment_name}")
def describe_deployment(namespace: str, deployment_name: str):
    """Describe a deployment"""
    result = k8s_describer.describe_deployment(namespace, deployment_name)
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "status": result.get("status", "unknown"),
        "details": result,
    }


@app.get("/describe/service/{namespace}/{service_name}")
def describe_service(namespace: str, service_name: str):
    """Describe a service"""
    result = k8s_describer.describe_service(namespace, service_name)
    return {
        "service_name": service_name,
        "namespace": namespace,
        "status": result.get("status", "unknown"),
        "details": result,
    }


@app.get("/describe/namespace/{namespace}")
def describe_namespace(namespace: str):
    """Describe a namespace"""
    result = k8s_describer.describe_namespace(namespace)
    return {
        "namespace": namespace,
        "status": result.get("status", "unknown"),
        "details": result,
    }


@app.get("/describe/pods/{namespace}")
def describe_all_pods(namespace: str = "default"):
    """Describe all pods in a namespace"""
    result = k8s_describer.describe_all_pods(namespace)
    return {
        "namespace": namespace,
        "pod_count": len(result.get("pods", [])),
        "pods": result.get("pods", []),
    }


@app.post("/scale/deployment/{namespace}/{deployment_name}")
def scale_deployment(
    namespace: str, deployment_name: str, replicas: int, dry_run: bool = False
):
    """Scale a deployment"""
    result = k8s_scaler.scale_deployment(namespace, deployment_name, replicas, dry_run)
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "new_replicas": replicas,
        "status": "dry_run" if dry_run else "success",
        "details": result,
    }


@app.post("/scale/statefulset/{namespace}/{statefulset_name}")
def scale_statefulset(
    namespace: str, statefulset_name: str, replicas: int, dry_run: bool = False
):
    """Scale a statefulset"""
    result = k8s_scaler.scale_statefulset(
        namespace, statefulset_name, replicas, dry_run
    )
    return {
        "statefulset_name": statefulset_name,
        "namespace": namespace,
        "new_replicas": replicas,
        "status": "dry_run" if dry_run else "success",
        "details": result,
    }


@app.post("/scale/autoscale/{namespace}/{deployment_name}")
def setup_autoscaling(
    namespace: str,
    deployment_name: str,
    min_replicas: int = 1,
    max_replicas: int = 10,
    target_cpu: int = 80,
):
    """Setup auto-scaling for a deployment"""
    result = k8s_scaler.auto_scale_deployment(
        namespace, deployment_name, min_replicas, max_replicas, target_cpu
    )
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "min_replicas": min_replicas,
        "max_replicas": max_replicas,
        "target_cpu": target_cpu,
        "status": "success",
        "details": result,
    }


@app.get("/logs/pod/{namespace}/{pod_name}")
def get_pod_logs(
    namespace: str,
    pod_name: str,
    container: Optional[str] = None,
    tail_lines: int = 100,
):
    """Get logs from a pod"""
    result = k8s_log_analyzer.get_pod_logs(namespace, pod_name, container, tail_lines)
    return {
        "pod_name": pod_name,
        "namespace": namespace,
        "log_count": len(result.get("logs", [])),
        "logs": result.get("logs", []),
        "details": result,
    }


@app.get("/logs/deployment/{namespace}/{deployment_name}")
def get_deployment_logs(namespace: str, deployment_name: str, tail_lines: int = 50):
    """Get logs from all pods in a deployment"""
    result = k8s_log_analyzer.get_deployment_logs(
        namespace, deployment_name, tail_lines
    )
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "log_count": len(result.get("logs", [])),
        "logs": result.get("logs", []),
        "details": result,
    }


@app.post("/logs/search/{namespace}")
def search_logs(
    namespace: str,
    search_pattern: str,
    pod_selector: Optional[str] = None,
    max_results: int = 100,
):
    """Search logs across pods in a namespace"""
    result = k8s_log_analyzer.search_logs(
        namespace, search_pattern, pod_selector, max_results
    )
    return {
        "namespace": namespace,
        "search_pattern": search_pattern,
        "results_count": len(result.get("results", [])),
        "results": result.get("results", []),
        "details": result,
    }


@app.get("/logs/errors/{namespace}")
def analyze_errors(
    namespace: str, pod_name: Optional[str] = None, hours_back: int = 24
):
    """Analyze error patterns in logs"""
    result = k8s_log_analyzer.analyze_error_patterns(namespace, pod_name, hours_back)
    return {
        "namespace": namespace,
        "pod_name": pod_name,
        "hours_back": hours_back,
        "error_analysis": result.get("error_analysis", {}),
        "details": result,
    }


@app.get("/logs/summary/{namespace}")
def get_log_summary(
    namespace: str, deployment_name: Optional[str] = None, hours_back: int = 1
):
    """Get log summary for namespace or deployment"""
    result = k8s_log_analyzer.get_log_summary(namespace, deployment_name, hours_back)
    return {
        "namespace": namespace,
        "deployment_name": deployment_name,
        "hours_back": hours_back,
        "summary": result.get("summary", {}),
        "details": result,
    }


@app.post("/patch/deployment/{namespace}/{deployment_name}")
def patch_deployment(
    namespace: str,
    deployment_name: str,
    patch_data: Dict[str, Any],
    dry_run: bool = False,
):
    """Patch a deployment"""
    result = k8s_patcher.patch_deployment(
        namespace, deployment_name, patch_data, dry_run
    )
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "patch_applied": True,
        "status": "dry_run" if dry_run else "success",
        "details": result,
    }


@app.post("/patch/configmap/{namespace}/{configmap_name}")
def patch_configmap(
    namespace: str,
    configmap_name: str,
    patch_data: Dict[str, Any],
    dry_run: bool = False,
):
    """Patch a configmap"""
    result = k8s_patcher.patch_configmap(namespace, configmap_name, patch_data, dry_run)
    return {
        "configmap_name": configmap_name,
        "namespace": namespace,
        "patch_applied": True,
        "status": "dry_run" if dry_run else "success",
        "details": result,
    }


@app.post("/patch/service/{namespace}/{service_name}")
def patch_service(
    namespace: str, service_name: str, patch_data: Dict[str, Any], dry_run: bool = False
):
    """Patch a service"""
    result = k8s_patcher.patch_service(namespace, service_name, patch_data, dry_run)
    return {
        "service_name": service_name,
        "namespace": namespace,
        "patch_applied": True,
        "status": "dry_run" if dry_run else "success",
        "details": result,
    }


class ManifestRequest(BaseModel):
    manifest_yaml: str


@app.post("/apply/manifest")
def apply_manifest(
    request: ManifestRequest, namespace: str = "default", dry_run: bool = False
):
    """Apply a Kubernetes manifest"""
    result = k8s_patcher.apply_manifest(request.manifest_yaml, namespace, dry_run)
    return {
        "namespace": namespace,
        "manifest_applied": True,
        "status": "dry_run" if dry_run else "success",
        "details": result,
    }


@app.post("/rollback/deployment/{namespace}/{deployment_name}")
def rollback_deployment(
    namespace: str, deployment_name: str, revision: Optional[int] = None
):
    """Rollback a deployment to a previous revision"""
    result = k8s_patcher.rollback_deployment(namespace, deployment_name, revision)
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "rollback_completed": True,
        "revision": revision,
        "details": result,
    }


@app.get("/recommendations/{namespace}/{deployment_name}")
def get_scaling_recommendations(namespace: str, deployment_name: str):
    """Get scaling recommendations for a deployment"""
    result = k8s_scaler.get_scaling_recommendations(namespace, deployment_name)
    return {
        "deployment_name": deployment_name,
        "namespace": namespace,
        "recommendations": result.get("recommendations", []),
        "details": result,
    }


# New CKA/CKS endpoints
@app.post("/cka/cluster-health")
def analyze_cluster_health(cluster_config: Dict[str, Any]):
    """Analyze cluster health using CKA knowledge"""
    try:
        logger.info("Katie analyzing cluster health")
        analysis = cka_operations.analyze_cluster_health(cluster_config)

        return {
            "analysis": analysis,
            "status": "success",
            "overall_status": analysis.get("overall_status", "unknown"),
        }
    except Exception as e:
        logger.error(f"Cluster health analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Cluster health analysis failed: {str(e)}"
        )


@app.post("/cka/troubleshoot-pod")
def troubleshoot_pod_failures(pod_info: Dict[str, Any]):
    """Troubleshoot pod failures using CKA knowledge"""
    try:
        logger.info("Katie troubleshooting pod failures")
        troubleshooting = cka_operations.troubleshoot_pod_failures(pod_info)

        return {
            "troubleshooting": troubleshooting,
            "status": "success",
            "pod_name": troubleshooting.get("pod_name", "unknown"),
        }
    except Exception as e:
        logger.error(f"Pod troubleshooting failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Pod troubleshooting failed: {str(e)}"
        )


@app.post("/cka/resource-misconfigurations")
def analyze_resource_misconfigurations(resources: List[Dict[str, Any]]):
    """Analyze resource misconfigurations using CKA knowledge"""
    try:
        logger.info("Katie analyzing resource misconfigurations")
        misconfigurations = cka_operations.analyze_resource_misconfigurations(resources)

        return {
            "misconfigurations": misconfigurations,
            "status": "success",
            "total_resources": len(resources),
        }
    except Exception as e:
        logger.error(f"Resource misconfiguration analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Resource misconfiguration analysis failed: {str(e)}",
        )


@app.post("/cka/best-practices")
def recommend_best_practices(resource_type: str, resource_config: Dict[str, Any]):
    """Recommend best practices using CKA knowledge"""
    try:
        logger.info(f"Katie recommending best practices for {resource_type}")
        recommendations = cka_operations.recommend_best_practices(
            resource_type, resource_config
        )

        return {
            "recommendations": recommendations,
            "status": "success",
            "resource_type": resource_type,
        }
    except Exception as e:
        logger.error(f"Best practices recommendation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Best practices recommendation failed: {str(e)}"
        )


@app.post("/cks/security-analysis")
def analyze_security(data: SecurityAnalysisRequest):
    """Analyze cluster security using CKS knowledge"""
    try:
        logger.info("Katie analyzing cluster security")
        security_analysis = cks_security.analyze_cluster_security(data.cluster_config)

        return {
            "security_analysis": security_analysis,
            "status": "success",
            "compliance_standard": data.compliance_standard,
        }
    except Exception as e:
        logger.error(f"Security analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Security analysis failed: {str(e)}"
        )


@app.post("/cks/enforce-policies")
def enforce_security_policies(namespace: str, policy_type: str, config: Dict[str, Any]):
    """Enforce security policies using CKS knowledge"""
    try:
        logger.info(f"Katie enforcing {policy_type} policies in {namespace}")
        enforcement = cks_security.enforce_security_policies(
            namespace, policy_type, config
        )

        return {
            "enforcement": enforcement,
            "status": "success",
            "namespace": namespace,
            "policy_type": policy_type,
        }
    except Exception as e:
        logger.error(f"Policy enforcement failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Policy enforcement failed: {str(e)}"
        )


@app.post("/cks/vulnerability-scan")
def scan_vulnerabilities(resources: List[Dict[str, Any]]):
    """Scan for vulnerabilities using CKS knowledge"""
    try:
        logger.info("Katie scanning for vulnerabilities")
        vulnerability_scan = cks_security.scan_for_vulnerabilities(resources)

        return {
            "vulnerability_scan": vulnerability_scan,
            "status": "success",
            "total_resources": len(resources),
        }
    except Exception as e:
        logger.error(f"Vulnerability scan failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Vulnerability scan failed: {str(e)}"
        )


@app.post("/cks/threat-detection")
def detect_threats(data: ThreatDetectionRequest):
    """Detect threats using CKS knowledge"""
    try:
        logger.info("Katie detecting threats")
        threat_detection = cks_security.detect_threats(data.cluster_events, data.logs)

        return {
            "threat_detection": threat_detection,
            "status": "success",
            "threats_detected": threat_detection.get("threats_detected", 0),
        }
    except Exception as e:
        logger.error(f"Threat detection failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Threat detection failed: {str(e)}"
        )


@app.post("/cka/helm-analysis")
def analyze_helm_chart(chart_path: str):
    """Analyze Helm chart using CKA knowledge"""
    try:
        logger.info(f"Katie analyzing Helm chart: {chart_path}")
        chart_analysis = cka_operations.analyze_helm_chart(chart_path)

        return {
            "chart_analysis": chart_analysis,
            "status": "success",
            "chart_path": chart_path,
        }
    except Exception as e:
        logger.error(f"Helm chart analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Helm chart analysis failed: {str(e)}"
        )


@app.post("/cka/argocd-analysis")
def analyze_argocd_application(app_manifest: Dict[str, Any]):
    """Analyze ArgoCD application using CKA knowledge"""
    try:
        logger.info("Katie analyzing ArgoCD application")
        app_analysis = cka_operations.analyze_argocd_application(app_manifest)

        return {
            "app_analysis": app_analysis,
            "status": "success",
            "application_name": app_analysis.get("application_name", "unknown"),
        }
    except Exception as e:
        logger.error(f"ArgoCD application analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"ArgoCD application analysis failed: {str(e)}"
        )


@app.post("/cka/terraform-aks")
def generate_terraform_aks_config(cluster_config: Dict[str, Any]):
    """Generate Terraform AKS configuration using CKA knowledge"""
    try:
        logger.info("Katie generating Terraform AKS configuration")
        terraform_config = cka_operations.generate_terraform_aks_config(cluster_config)

        return {
            "terraform_config": terraform_config,
            "status": "success",
            "cluster_name": cluster_config.get("cluster_name", "unknown"),
        }
    except Exception as e:
        logger.error(f"Terraform AKS configuration generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Terraform AKS configuration generation failed: {str(e)}",
        )


@app.post("/cka/explain-manifest")
def explain_yaml_manifest(manifest_yaml: str):
    """Explain or suggest changes to YAML manifests using CKA knowledge"""
    try:
        logger.info("Katie explaining YAML manifest")
        explanation = cka_operations.explain_yaml_manifest(manifest_yaml)

        return {
            "explanation": explanation,
            "status": "success",
            "manifest_length": len(manifest_yaml),
        }
    except Exception as e:
        logger.error(f"YAML manifest explanation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"YAML manifest explanation failed: {str(e)}"
        )


@app.get("/capabilities")
def get_capabilities():
    """Get current Katie capabilities"""
    return {
        "agent": "katie",
        "role": "Kubernetes AI Agent & Cluster Guardian",
        "specialization": "Certified Kubernetes Administrator (CKA) & Security Specialist (CKS)",
        "current_capabilities": [
            "Pod/Deployment/Service Description",
            "Intelligent Scaling Operations",
            "Log Analysis & Search",
            "Resource Patching & Updates",
            "Manifest Application",
            "Rollback Operations",
            "K8GPT Integration",
            "Error Pattern Analysis",
            "Cluster Health Analysis",
            "Pod Failure Troubleshooting",
            "Resource Misconfiguration Detection",
            "Best Practices Recommendations",
            "Security Policy Enforcement",
            "Vulnerability Scanning",
            "Compliance Auditing",
            "Threat Detection",
            "Container Runtime Security",
            "Secrets Management",
            "Network Security Configuration",
            "Helm Chart Analysis",
            "ArgoCD Application Management",
            "Terraform AKS Patterns",
            "YAML Manifest Explanation",
        ],
        "certifications": [
            "Certified Kubernetes Administrator (CKA)",
            "Certified Kubernetes Security Specialist (CKS)",
            "SRE Best Practices",
            "DevSecOps Professional",
        ],
        "focus_areas": [
            "Kubernetes Cluster Administration",
            "Security Hardening & Compliance",
            "Troubleshooting & Debugging",
            "Best Practices Implementation",
            "Helm & ArgoCD Management",
            "Infrastructure as Code (Terraform)",
            "Threat Detection & Response",
            "Performance Optimization",
        ],
    }


def _execute_describe_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute describe operation"""
    if data.resource_type == "pod":
        return k8s_describer.describe_pod(data.namespace, data.resource_name)
    elif data.resource_type == "deployment":
        return k8s_describer.describe_deployment(data.namespace, data.resource_name)
    elif data.resource_type == "service":
        return k8s_describer.describe_service(data.namespace, data.resource_name)
    elif data.resource_type == "namespace":
        return k8s_describer.describe_namespace(data.resource_name)
    else:
        return {
            "status": "error",
            "message": f"Unknown resource type: {data.resource_type}",
        }


def _execute_scale_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute scale operation"""
    replicas = data.parameters.get("replicas", 1) if data.parameters else 1
    dry_run = data.parameters.get("dry_run", False) if data.parameters else False

    if data.resource_type == "deployment":
        return k8s_scaler.scale_deployment(
            data.namespace, data.resource_name, replicas, dry_run
        )
    elif data.resource_type == "statefulset":
        return k8s_scaler.scale_statefulset(
            data.namespace, data.resource_name, replicas, dry_run
        )
    else:
        return {
            "status": "error",
            "message": f"Cannot scale resource type: {data.resource_type}",
        }


def _execute_logs_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute logs operation"""
    container = data.parameters.get("container") if data.parameters else None
    tail_lines = data.parameters.get("tail_lines", 100) if data.parameters else 100

    if data.resource_type == "pod":
        return k8s_log_analyzer.get_pod_logs(
            data.namespace, data.resource_name, container, tail_lines
        )
    elif data.resource_type == "deployment":
        return k8s_log_analyzer.get_deployment_logs(
            data.namespace, data.resource_name, tail_lines
        )
    else:
        return {
            "status": "error",
            "message": f"Cannot get logs for resource type: {data.resource_type}",
        }


def _execute_patch_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute patch operation"""
    patch_data = data.parameters.get("patch_data", {}) if data.parameters else {}
    dry_run = data.parameters.get("dry_run", False) if data.parameters else False

    if data.resource_type == "deployment":
        return k8s_patcher.patch_deployment(
            data.namespace, data.resource_name, patch_data, dry_run
        )
    elif data.resource_type == "configmap":
        return k8s_patcher.patch_configmap(
            data.namespace, data.resource_name, patch_data, dry_run
        )
    elif data.resource_type == "service":
        return k8s_patcher.patch_service(
            data.namespace, data.resource_name, patch_data, dry_run
        )
    else:
        return {
            "status": "error",
            "message": f"Cannot patch resource type: {data.resource_type}",
        }


def _execute_apply_operation(data: KubernetesTask) -> Dict[str, Any]:
    """Execute apply operation"""
    manifest_yaml = data.parameters.get("manifest_yaml", "") if data.parameters else ""
    dry_run = data.parameters.get("dry_run", False) if data.parameters else False

    return k8s_patcher.apply_manifest(manifest_yaml, data.namespace, dry_run)


def _get_k8gpt_insight(data: KubernetesTask, result: Dict[str, Any]) -> Optional[str]:
    """Get K8GPT insight for failed operations"""
    try:
        if not K8GPT_ENABLED:
            return None

        # Prepare data for K8GPT
        k8gpt_data = {
            "task_type": data.task_type,
            "resource_type": data.resource_type,
            "resource_name": data.resource_name,
            "namespace": data.namespace,
            "error": result.get("message", "Unknown error"),
            "context": result,
        }

        # This would make an actual API call to K8GPT
        # For now, return a simulated insight
        return f"K8GPT suggests checking {data.resource_type} {data.resource_name} in namespace {data.namespace} for common configuration issues."

    except Exception as e:
        logger.error(f"K8GPT insight failed: {str(e)}")
        return None


def _generate_katie_response(data: KubernetesTask, result: Dict[str, Any]) -> str:
    """Generate Katie's response message"""
    if result.get("status") == "error":
        return f"Katie encountered an error while {data.task_type}ing {data.resource_type} {data.resource_name}: {result.get('message', 'Unknown error')}"
    else:
        return f"Katie successfully completed {data.task_type} operation on {data.resource_type} {data.resource_name} in namespace {data.namespace}"


def _calculate_confidence(result: Dict[str, Any]) -> float:
    """Calculate confidence score based on operation result"""
    if result.get("status") == "error":
        return 0.3
    elif result.get("status") == "success":
        return 0.9
    else:
        return 0.7


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
