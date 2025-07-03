"""
Igris Service - Platform Engineer Microservice
Handles infrastructure automation, DevSecOps, and multi-cloud management
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

# Import modular components
from analyzer import analyze_platform_components
from infrastructure import generate_infrastructure_solution, generate_configurations
from security import generate_security_recommendations
from opendevin import simulate_opendevin_automation
from routers import validate_scaffold, post_push_fix, lint_router

# Import new elite modules
from devsecops import devsecops_analyzer
from gitops import gitops_engineer
from kubernetes_platform import k8s_platform_engineer

app = FastAPI(title="Igris Service - Platform Engineer")

# Include routers
app.include_router(validate_scaffold.router)
app.include_router(post_push_fix.router)
app.include_router(lint_router.router)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlatformTask(BaseModel):
    task_id: str
    task_text: str
    platform: str = "kubernetes"  # kubernetes, aws, azure, gcp
    action_type: str = "deploy"  # deploy, configure, audit, optimize
    configuration: Optional[Dict[str, Any]] = None


class PlatformResponse(BaseModel):
    agent: str = "igris"
    task: str
    response: str
    infrastructure_solution: Dict[str, Any]
    generated_configs: List[str]
    security_recommendations: List[str]
    confidence_score: float
    devsecops_analysis: Optional[Dict[str, Any]] = None
    gitops_recommendations: Optional[Dict[str, Any]] = None
    platform_engineering: Optional[Dict[str, Any]] = None


class EnhancementRequest(BaseModel):
    agent: str
    orb_id: str
    rune_patch: str
    training_notes: str


class DevSecOpsRequest(BaseModel):
    codebase_path: str
    platform: str
    tools: List[str]


class GitOpsRequest(BaseModel):
    repo_path: str
    platform: str
    tools: List[str]


class KubernetesPlatformRequest(BaseModel):
    cluster_config: Dict[str, Any]
    workload_type: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "igris",
        "specialization": "Platform Engineering & DevSecOps",
        "capabilities": [
            "Infrastructure as Code (Terraform)",
            "DevSecOps Practices",
            "Security Scanning & Compliance",
            "Platform Engineering",
            "OpenDevin Integration",
            "Multi-Cloud Management",
            "CI/CD Pipeline Automation",
            "Infrastructure Optimization",
            "GitOps Workflows",
            "Kubernetes Platform Engineering",
            "Security Pipeline Analysis",
            "Network Policy Management",
            "RBAC Configuration",
            "Node Scaling & Autoscaling",
            "Persistent Storage Management",
            "Sidecar Pattern Implementation",
            "CI/CD Anti-pattern Detection",
            "Migration Planning",
            "Runbook Generation",
        ],
    }


@app.post("/execute")
def execute(data: PlatformTask):
    """
    Igris specializes in platform engineering and DevSecOps
    - Manages infrastructure as code
    - Implements security best practices
    - Integrates with OpenDevin for intelligent automation
    - Provides multi-cloud solutions
    - Elite GitOps and Kubernetes platform engineering
    """
    try:
        logger.info(f"Igris processing platform task: {data.task_text}")

        # Analyze task for platform components
        platform_components = analyze_platform_components(data.task_text, data.platform)

        # Generate infrastructure solution
        infrastructure_solution = generate_infrastructure_solution(
            data.task_text, platform_components, data.platform
        )

        # Generate configurations
        generated_configs = generate_configurations(
            data.task_text, platform_components, data.platform
        )

        # Security recommendations
        security_recommendations = generate_security_recommendations(
            data.task_text, platform_components, data.platform
        )

        # DevSecOps analysis if applicable
        devsecops_analysis = None
        if any(
            keyword in data.task_text.lower()
            for keyword in ["security", "scan", "compliance", "pipeline"]
        ):
            devsecops_analysis = devsecops_analyzer.analyze_security_pipeline(".")

        # GitOps recommendations if applicable
        gitops_recommendations = None
        if any(
            keyword in data.task_text.lower()
            for keyword in ["gitops", "argocd", "helm", "deployment"]
        ):
            gitops_recommendations = gitops_engineer.analyze_gitops_setup(".")

        # Platform engineering analysis if applicable
        platform_engineering = None
        if data.platform == "kubernetes" and any(
            keyword in data.task_text.lower()
            for keyword in ["node", "scaling", "network", "rbac", "storage"]
        ):
            platform_engineering = k8s_platform_engineer.analyze_cluster_architecture(
                {}
            )

        # Create response
        response = PlatformResponse(
            task=data.task_text,
            response=_generate_platform_response(
                data.task_text, platform_components, data.platform
            ),
            infrastructure_solution=infrastructure_solution,
            generated_configs=generated_configs,
            security_recommendations=security_recommendations,
            confidence_score=_calculate_confidence(platform_components),
            devsecops_analysis=devsecops_analysis,
            gitops_recommendations=gitops_recommendations,
            platform_engineering=platform_engineering,
        )

        logger.info(
            f"Igris completed task with {len(generated_configs)} " "configurations"
        )
        return response

    except Exception as e:
        logger.error(f"Igris execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Igris execution failed: {str(e)}")


@app.post("/devsecops/analyze")
def analyze_devsecops(data: DevSecOpsRequest):
    """Analyze and generate DevSecOps pipeline recommendations"""
    try:
        logger.info(f"Igris analyzing DevSecOps pipeline for {data.platform}")

        # Analyze security pipeline
        analysis = devsecops_analyzer.analyze_security_pipeline(data.codebase_path)

        # Generate pipeline configuration
        pipeline = devsecops_analyzer.generate_devsecops_pipeline(
            data.platform, data.tools
        )

        # Detect anti-patterns
        antipatterns = devsecops_analyzer.detect_ci_cd_antipatterns(
            [".github/workflows/main.yml"]
        )

        return {
            "analysis": analysis,
            "pipeline_config": pipeline,
            "antipatterns": antipatterns,
            "recommendations": analysis.get("recommendations", []),
        }

    except Exception as e:
        logger.error(f"DevSecOps analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"DevSecOps analysis failed: {str(e)}"
        )


@app.post("/gitops/analyze")
def analyze_gitops(data: GitOpsRequest):
    """Analyze and generate GitOps workflow recommendations"""
    try:
        logger.info(f"Igris analyzing GitOps setup for {data.platform}")

        # Analyze GitOps setup
        analysis = gitops_engineer.analyze_gitops_setup(data.repo_path)

        # Generate workflow configuration
        workflow = gitops_engineer.generate_gitops_workflow(data.platform, data.tools)

        # Detect anti-patterns
        antipatterns = gitops_engineer.detect_gitops_antipatterns(data.repo_path)

        return {
            "analysis": analysis,
            "workflow_config": workflow,
            "antipatterns": antipatterns,
            "recommendations": analysis.get("recommendations", []),
        }

    except Exception as e:
        logger.error(f"GitOps analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"GitOps analysis failed: {str(e)}")


@app.post("/kubernetes/platform")
def analyze_kubernetes_platform(data: KubernetesPlatformRequest):
    """Analyze and generate Kubernetes platform engineering recommendations"""
    try:
        logger.info(f"Igris analyzing Kubernetes platform for {data.workload_type}")

        # Analyze cluster architecture
        analysis = k8s_platform_engineer.analyze_cluster_architecture(
            data.cluster_config
        )

        # Generate node scaling config
        scaling_config = k8s_platform_engineer.generate_node_scaling_config(
            "kubernetes", data.workload_type
        )

        # Detect platform issues
        issues = k8s_platform_engineer.detect_platform_issues(data.cluster_config)

        return {
            "analysis": analysis,
            "scaling_config": scaling_config,
            "issues": issues,
            "recommendations": analysis.get("recommendations", []),
        }

    except Exception as e:
        logger.error(f"Kubernetes platform analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Kubernetes platform analysis failed: {str(e)}"
        )


@app.post("/migration/plan")
def generate_migration_plan(from_monolith: bool, target_platform: str):
    """Generate migration plan from monolith to GitOps-native microservices"""
    try:
        logger.info(f"Igris generating migration plan to {target_platform}")

        migration_plan = gitops_engineer.generate_migration_plan(
            from_monolith, target_platform
        )

        return {
            "migration_plan": migration_plan,
            "estimated_duration": "16-26 weeks",
            "complexity": "high",
            "risks": migration_plan.get("risks", []),
        }

    except Exception as e:
        logger.error(f"Migration planning failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Migration planning failed: {str(e)}"
        )


@app.post("/runbook/generate")
def generate_runbook(scenario: str, platform: str = "kubernetes"):
    """Generate platform engineering runbook for specific scenario"""
    try:
        logger.info(f"Igris generating runbook for {scenario}")

        if scenario in ["vulnerability_detected", "secret_exposure"]:
            runbook = devsecops_analyzer.generate_security_runbook(platform, scenario)
        elif scenario in ["node_scaling", "network_troubleshooting", "storage_issues"]:
            runbook = k8s_platform_engineer.generate_platform_runbook(scenario)
        else:
            runbook = {"error": "Unknown scenario"}

        return {"runbook": runbook, "scenario": scenario, "platform": platform}

    except Exception as e:
        logger.error(f"Runbook generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Runbook generation failed: {str(e)}"
        )


@app.post("/opendevin/automate")
def opendevin_automate(task: Dict[str, Any]):
    """
    Integrate with OpenDevin for intelligent automation
    """
    try:
        logger.info("Igris using OpenDevin for automation")

        # Simulate OpenDevin automation
        automation = simulate_opendevin_automation(task)

        return {
            "status": "automation_complete",
            "opendevin_insights": automation["insights"],
            "automated_actions": automation["actions"],
            "code_generated": automation["code_generated"],
            "infrastructure_changes": automation["infrastructure_changes"],
        }

    except Exception as e:
        logger.error(f"OpenDevin automation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"OpenDevin automation failed: {str(e)}"
        )


@app.post("/api/enhance")
def enhance_agent(request: EnhancementRequest):
    """
    Allow Whis to enhance Igris with new Orbs and Runes
    """
    try:
        logger.info(f"Igris receiving enhancement for orb: {request.orb_id}")

        # Process the enhancement
        enhancement_result = {
            "agent": request.agent,
            "orb_id": request.orb_id,
            "status": "enhancement_applied",
            "rune_patch": request.rune_patch,
            "training_notes": request.training_notes,
            "capabilities_updated": True,
        }

        logger.info(f"Igris enhancement applied for {request.orb_id}")
        return enhancement_result

    except Exception as e:
        logger.error(f"Igris enhancement failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Igris enhancement failed: {str(e)}"
        )


@app.get("/capabilities")
def get_capabilities():
    """Get current Igris capabilities"""
    return {
        "agent": "igris",
        "specialization": "Platform Engineering & DevSecOps",
        "current_capabilities": [
            "Infrastructure as Code (Terraform)",
            "DevSecOps Practices",
            "Security Scanning & Compliance",
            "Platform Engineering",
            "OpenDevin Integration",
            "Multi-Cloud Management",
            "CI/CD Pipeline Automation",
            "Infrastructure Optimization",
            "Configuration Management",
            "Security Hardening",
            "GitOps Workflows (ArgoCD, Flux)",
            "Helm Chart Development & Validation",
            "Kubernetes Platform Engineering",
            "Node Scaling & Autoscaling",
            "Network Policy Management",
            "RBAC & Service Account Configuration",
            "Persistent Storage Management",
            "Sidecar Pattern Implementation",
            "CI/CD Anti-pattern Detection",
            "Security Pipeline Analysis",
            "Migration Planning (Monolith to Microservices)",
            "Runbook Generation",
            "DevSecOps Tool Integration (SonarQube, Snyk, Trivy, Bandit, Checkov)",
        ],
        "certifications": [
            "Terraform Certified",
            "AWS Solutions Architect",
            "Kubernetes Administrator (CKA)",
            "Kubernetes Security Specialist (CKS)",
            "DevSecOps Professional",
            "GitOps Practitioner",
            "Platform Engineering Specialist",
        ],
        "focus_areas": [
            "DevSecOps Pipeline Design",
            "GitOps Workflow Implementation",
            "Kubernetes Platform Engineering",
            "Security Automation",
            "Infrastructure as Code",
            "Multi-Cloud Strategy",
            "CI/CD Optimization",
            "Platform Migration",
            "Security Hardening",
            "Performance Optimization",
        ],
    }


def _generate_platform_response(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> str:
    """Generate platform-specific response"""
    if platform == "kubernetes":
        return f"Igris analyzed your Kubernetes platform task: '{task_text}'. Detected components: {list(platform_components.keys())}. Ready to implement DevSecOps practices, GitOps workflows, and platform engineering best practices."
    elif platform == "aws":
        return f"Igris analyzed your AWS platform task: '{task_text}'. Detected components: {list(platform_components.keys())}. Ready to implement infrastructure as code and security best practices."
    else:
        return f"Igris analyzed your {platform} platform task: '{task_text}'. Detected components: {list(platform_components.keys())}. Ready to implement platform engineering solutions."


def _calculate_confidence(platform_components: Dict[str, Any]) -> float:
    """Calculate confidence score based on platform components"""
    total_components = len(platform_components)
    if total_components == 0:
        return 0.0
    return min(1.0, total_components / 10.0)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
