"""
Igris Service - Platform Engineer Microservice
Handles infrastructure automation, DevSecOps, and multi-cloud management
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import logging
import subprocess
import os
import yaml

app = FastAPI(title="Igris Service - Platform Engineer")

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
    """
    try:
        logger.info(f"Igris processing platform task: {data.task_text}")

        # Analyze task for platform components
        platform_components = _analyze_platform_components(
            data.task_text, data.platform
        )

        # Generate infrastructure solution
        infrastructure_solution = _generate_infrastructure_solution(
            data.task_text, platform_components, data.platform
        )

        # Generate configurations
        generated_configs = _generate_configurations(
            data.task_text, platform_components, data.platform
        )

        # Security recommendations
        security_recommendations = _generate_security_recommendations(
            data.task_text, platform_components, data.platform
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
        )

        logger.info(
            f"Igris completed task with {len(generated_configs)} configurations"
        )
        return response

    except Exception as e:
        logger.error(f"Igris execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Igris execution failed: {str(e)}")


@app.post("/opendevin/automate")
def opendevin_automate(task: Dict[str, Any]):
    """
    Integrate with OpenDevin for intelligent automation
    """
    try:
        logger.info("Igris using OpenDevin for automation")

        # Simulate OpenDevin automation
        automation = _simulate_opendevin_automation(task)

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
        ],
        "certifications": [
            "Terraform Certified",
            "AWS Solutions Architect",
            "Azure DevOps Engineer",
            "Google Cloud Professional",
            "OpenDevin Integration Specialist",
        ],
        "focus_areas": [
            "Infrastructure Automation",
            "Security & Compliance",
            "Multi-Cloud Strategy",
            "DevOps Transformation",
            "Platform Engineering",
            "Cost Optimization",
        ],
    }


def _analyze_platform_components(task_text: str, platform: str) -> Dict[str, Any]:
    """Analyze task for platform components"""
    platform_keywords = {
        "kubernetes": ["k8s", "kubernetes", "pod", "deployment", "service", "ingress"],
        "aws": ["aws", "ec2", "s3", "lambda", "rds", "vpc", "iam"],
        "azure": ["azure", "vm", "storage", "function", "sql", "vnet", "rbac"],
        "gcp": ["gcp", "gce", "storage", "function", "sql", "vpc", "iam"],
        "terraform": ["terraform", "infrastructure", "iac", "provisioning"],
        "security": ["security", "compliance", "audit", "scan", "vulnerability"],
        "automation": [
            "automation",
            "ci/cd",
            "pipeline",
            "deployment",
            "orchestration",
        ],
    }

    components = {}
    task_lower = task_text.lower()

    for category, keywords in platform_keywords.items():
        components[category] = any(keyword in task_lower for keyword in keywords)

    # Add platform-specific components
    components[platform] = True

    return components


def _generate_infrastructure_solution(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> Dict[str, Any]:
    """Generate infrastructure solution"""
    solution = {
        "approach": "platform-native",
        "platform": platform,
        "components": [],
        "security_level": "high",
        "automation_level": "full",
    }

    if platform_components.get("terraform"):
        solution["components"].append("Infrastructure as Code with Terraform")

    if platform_components.get("kubernetes"):
        solution["components"].append("Kubernetes Cluster Management")

    if platform_components.get("aws"):
        solution["components"].append("AWS Cloud Infrastructure")

    if platform_components.get("azure"):
        solution["components"].append("Azure Cloud Infrastructure")

    if platform_components.get("gcp"):
        solution["components"].append("Google Cloud Infrastructure")

    if platform_components.get("security"):
        solution["components"].append("Security & Compliance Framework")

    if platform_components.get("automation"):
        solution["components"].append("CI/CD Pipeline Automation")

    return solution


def _generate_configurations(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> List[str]:
    """Generate platform configurations"""
    configs = []

    if platform_components.get("terraform"):
        configs.append(
            """
# Terraform configuration for infrastructure
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "main-vpc"
    Environment = "production"
  }
}
"""
        )

    if platform_components.get("kubernetes"):
        configs.append(
            """
# Kubernetes cluster configuration
apiVersion: v1
kind: Namespace
metadata:
  name: platform-engineering
  labels:
    name: platform-engineering

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: platform-app
  namespace: platform-engineering
spec:
  replicas: 3
  selector:
    matchLabels:
      app: platform-app
  template:
    metadata:
      labels:
        app: platform-app
    spec:
      containers:
      - name: app
        image: platform-app:latest
        ports:
        - containerPort: 8080
"""
        )

    if platform_components.get("security"):
        configs.append(
            """
# Security configuration
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: platform-engineering
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
"""
        )

    return configs


def _generate_security_recommendations(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> List[str]:
    """Generate security recommendations"""
    recommendations = []

    if platform_components.get("terraform"):
        recommendations.extend(
            [
                "Use Terraform Cloud for state management",
                "Implement remote state with encryption",
                "Use Terraform modules for reusability",
                "Enable Terraform plan validation",
            ]
        )

    if platform_components.get("kubernetes"):
        recommendations.extend(
            [
                "Enable pod security policies",
                "Implement network policies",
                "Use RBAC for access control",
                "Enable audit logging",
            ]
        )

    if platform_components.get("aws"):
        recommendations.extend(
            [
                "Use IAM roles with least privilege",
                "Enable CloudTrail logging",
                "Implement VPC security groups",
                "Use AWS Config for compliance",
            ]
        )

    if platform_components.get("azure"):
        recommendations.extend(
            [
                "Use Azure RBAC for access control",
                "Enable Azure Security Center",
                "Implement network security groups",
                "Use Azure Policy for compliance",
            ]
        )

    if not recommendations:
        recommendations.append("Follow platform security best practices")

    return recommendations


def _generate_platform_response(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> str:
    """Generate platform response"""
    if platform_components.get("terraform"):
        return (
            f"Infrastructure as Code solution generated for {platform} using Terraform"
        )
    elif platform_components.get("kubernetes"):
        return "Kubernetes platform configuration created with security best practices"
    elif platform_components.get("security"):
        return "Security and compliance framework implemented"
    else:
        return f"Platform engineering solution prepared for {platform}"


def _calculate_confidence(platform_components: Dict[str, Any]) -> float:
    """Calculate confidence score based on components"""
    if not platform_components:
        return 0.5

    # Higher confidence for more specific components
    confidence = 0.6
    if platform_components.get("terraform"):
        confidence += 0.2
    if platform_components.get("security"):
        confidence += 0.15
    if platform_components.get("kubernetes"):
        confidence += 0.1

    return min(confidence, 1.0)


def _simulate_opendevin_automation(task: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate OpenDevin automation"""
    return {
        "insights": [
            "Infrastructure can be automated with Terraform",
            "Security policies need to be implemented",
            "CI/CD pipeline requires optimization",
        ],
        "actions": [
            "Generated Terraform configuration",
            "Created security policy templates",
            "Updated CI/CD pipeline configuration",
        ],
        "code_generated": [
            "Terraform main.tf",
            "Security policy YAML",
            "GitHub Actions workflow",
        ],
        "infrastructure_changes": [
            "Added VPC with security groups",
            "Configured Kubernetes cluster",
            "Implemented monitoring stack",
        ],
    }
