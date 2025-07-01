"""
Security module for Igris service.
Handles security recommendations, compliance, and DevSecOps practices.
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def generate_security_recommendations(
    task_text: str, platform_components: Dict[str, Any], platform: str
) -> List[str]:
    recommendations = []

    if platform_components.get("terraform"):
        recommendations += [
            "Use Terraform Cloud for state management",
            "Implement remote state with encryption",
            "Use Terraform modules for reusability",
            "Enable Terraform plan validation",
        ]

    if platform_components.get("kubernetes"):
        recommendations += [
            "Enable pod security policies",
            "Implement network policies",
            "Use RBAC for access control",
            "Enable audit logging",
        ]

    if platform_components.get("aws"):
        recommendations += [
            "Use IAM roles with least privilege",
            "Enable CloudTrail logging",
            "Implement VPC security groups",
            "Use AWS Config for compliance",
        ]

    if platform_components.get("azure"):
        recommendations += [
            "Use Azure RBAC for access control",
            "Enable Azure Security Center",
            "Implement network security groups",
            "Use Azure Policy for compliance",
        ]

    if not recommendations:
        recommendations.append("Follow platform security best practices")

    return recommendations


def generate_compliance_framework_recommendations(
    platform: str,
) -> Dict[str, List[str]]:
    """Generate compliance framework recommendations by platform."""
    frameworks = {
        "aws": [
            "SOC 2 Type II compliance",
            "PCI DSS for payment processing",
            "HIPAA for healthcare data",
            "FedRAMP for government workloads",
            "ISO 27001 for information security",
        ],
        "azure": [
            "SOC 1, 2, and 3 compliance",
            "PCI DSS for payment processing",
            "HIPAA for healthcare data",
            "FedRAMP for government workloads",
            "ISO 27001 for information security",
        ],
        "gcp": [
            "SOC 1, 2, and 3 compliance",
            "PCI DSS for payment processing",
            "HIPAA for healthcare data",
            "FedRAMP for government workloads",
            "ISO 27001 for information security",
        ],
        "kubernetes": [
            "CIS Kubernetes Benchmark",
            "NIST Cybersecurity Framework",
            "ISO 27001 for container security",
            "SOC 2 for containerized applications",
        ],
    }

    return frameworks.get(platform, [])


def generate_security_baseline_config(platform: str) -> Dict[str, Any]:
    """Generate security baseline configuration for platform."""
    baselines = {
        "kubernetes": {
            "pod_security_standards": "restricted",
            "network_policies": True,
            "rbac_enabled": True,
            "audit_logging": True,
            "image_scanning": True,
        },
        "aws": {
            "cloudtrail_enabled": True,
            "config_enabled": True,
            "guardduty_enabled": True,
            "security_hub_enabled": True,
            "backup_enabled": True,
        },
        "azure": {
            "security_center_enabled": True,
            "key_vault_enabled": True,
            "monitor_enabled": True,
            "backup_enabled": True,
            "sentinel_enabled": True,
        },
        "gcp": {
            "security_command_center_enabled": True,
            "secret_manager_enabled": True,
            "monitoring_enabled": True,
            "logging_enabled": True,
            "armor_enabled": True,
        },
    }

    return baselines.get(platform, {})
