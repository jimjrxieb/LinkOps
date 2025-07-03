"""
CKA Operations Module - Certified Kubernetes Administrator
Elite Kubernetes operations with Helm, ArgoCD, and Terraform AKS patterns
"""

from typing import Dict, List, Any, Optional
import yaml
import json
import re


class CKAOperations:
    """Certified Kubernetes Administrator operations"""

    def __init__(self):
        self.cka_domains = {
            "cluster_architecture": {
                "installation": "Kubernetes cluster installation and configuration",
                "upgrades": "Cluster upgrades and version management",
                "backup_restore": "ETCD backup and restore procedures",
                "high_availability": "Multi-master cluster setup",
            },
            "workloads": {
                "pods": "Pod lifecycle and management",
                "deployments": "Deployment strategies and rollouts",
                "statefulsets": "Stateful application management",
                "daemonsets": "System daemon management",
                "jobs": "Batch job processing",
            },
            "networking": {
                "services": "Service discovery and load balancing",
                "ingress": "Ingress controllers and routing",
                "network_policies": "Network security policies",
                "dns": "CoreDNS configuration",
            },
            "storage": {
                "persistent_volumes": "PV and PVC management",
                "storage_classes": "Dynamic provisioning",
                "configmaps": "Configuration management",
                "secrets": "Secret management",
            },
            "security": {
                "rbac": "Role-based access control",
                "service_accounts": "Service account management",
                "pod_security": "Pod security policies",
                "network_policies": "Network security",
            },
            "troubleshooting": {
                "logs": "Log analysis and debugging",
                "events": "Event monitoring",
                "metrics": "Resource monitoring",
                "debugging": "Pod and cluster debugging",
            },
        }

    def analyze_cluster_health(self, cluster_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall cluster health and identify issues"""
        health_analysis = {
            "overall_status": "healthy",
            "issues": [],
            "recommendations": [],
            "metrics": {},
            "components": {},
        }

        # Check node status
        if "nodes" in cluster_info:
            node_issues = self._analyze_node_health(cluster_info["nodes"])
            health_analysis["components"]["nodes"] = node_issues

            if node_issues["issues"]:
                health_analysis["overall_status"] = "degraded"
                health_analysis["issues"].extend(node_issues["issues"])

        # Check pod status
        if "pods" in cluster_info:
            pod_issues = self._analyze_pod_health(cluster_info["pods"])
            health_analysis["components"]["pods"] = pod_issues

            if pod_issues["issues"]:
                health_analysis["overall_status"] = "degraded"
                health_analysis["issues"].extend(pod_issues["issues"])

        # Check service status
        if "services" in cluster_info:
            service_issues = self._analyze_service_health(cluster_info["services"])
            health_analysis["components"]["services"] = service_issues

        # Generate recommendations
        health_analysis["recommendations"] = self._generate_health_recommendations(
            health_analysis
        )

        return health_analysis

    def troubleshoot_pod_failures(self, pod_info: Dict[str, Any]) -> Dict[str, Any]:
        """Troubleshoot pod failures with detailed analysis"""
        troubleshooting = {
            "pod_name": pod_info.get("metadata", {}).get("name", "unknown"),
            "namespace": pod_info.get("metadata", {}).get("namespace", "default"),
            "status": pod_info.get("status", {}).get("phase", "unknown"),
            "issues": [],
            "solutions": [],
            "events": [],
            "logs_analysis": {},
        }

        # Analyze pod status
        pod_status = pod_info.get("status", {})
        pod_phase = pod_status.get("phase", "Unknown")

        if pod_phase == "Pending":
            troubleshooting["issues"].append("Pod is stuck in Pending state")
            troubleshooting["solutions"].extend(
                [
                    "Check if there are enough resources (CPU/Memory)",
                    "Verify node selectors and affinity rules",
                    "Check for taints and tolerations",
                    "Verify PVC binding if using persistent storage",
                ]
            )

        elif pod_phase == "Failed":
            troubleshooting["issues"].append("Pod has failed")
            troubleshooting["solutions"].extend(
                [
                    "Check container exit codes",
                    "Review application logs",
                    "Verify image exists and is accessible",
                    "Check resource limits and requests",
                ]
            )

        # Analyze container statuses
        container_statuses = pod_status.get("containerStatuses", [])
        for container in container_statuses:
            if not container.get("ready", False):
                troubleshooting["issues"].append(
                    f"Container {container.get('name')} is not ready"
                )

                # Check restart count
                restart_count = container.get("restartCount", 0)
                if restart_count > 0:
                    troubleshooting["issues"].append(
                        f"Container {container.get('name')} has restarted {restart_count} times"
                    )

        # Analyze events
        if "events" in pod_info:
            troubleshooting["events"] = self._analyze_pod_events(pod_info["events"])

        return troubleshooting

    def analyze_resource_misconfigurations(
        self, resources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze resources for common misconfigurations"""
        misconfigurations = {
            "critical": [],
            "warning": [],
            "recommendations": [],
            "best_practices": [],
        }

        for resource in resources:
            resource_type = resource.get("kind", "Unknown")
            resource_name = resource.get("metadata", {}).get("name", "unknown")

            if resource_type == "Pod":
                pod_issues = self._analyze_pod_misconfigurations(resource)
                misconfigurations["critical"].extend(pod_issues["critical"])
                misconfigurations["warning"].extend(pod_issues["warning"])

            elif resource_type == "Deployment":
                deployment_issues = self._analyze_deployment_misconfigurations(resource)
                misconfigurations["critical"].extend(deployment_issues["critical"])
                misconfigurations["warning"].extend(deployment_issues["warning"])

            elif resource_type == "Service":
                service_issues = self._analyze_service_misconfigurations(resource)
                misconfigurations["critical"].extend(service_issues["critical"])
                misconfigurations["warning"].extend(service_issues["warning"])

        # Generate recommendations
        misconfigurations["recommendations"] = (
            self._generate_misconfiguration_recommendations(misconfigurations)
        )

        return misconfigurations

    def recommend_best_practices(
        self, resource_type: str, resource_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recommend best practices for Kubernetes resources"""
        recommendations = {
            "probes": [],
            "limits": [],
            "labels": [],
            "security": [],
            "monitoring": [],
        }

        if resource_type == "Pod":
            recommendations.update(self._recommend_pod_best_practices(resource_config))
        elif resource_type == "Deployment":
            recommendations.update(
                self._recommend_deployment_best_practices(resource_config)
            )
        elif resource_type == "Service":
            recommendations.update(
                self._recommend_service_best_practices(resource_config)
            )

        return recommendations

    def enforce_security_policies(
        self, namespace: str, policies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enforce security policies using NetworkPolicy and PodSecurityPolicy"""
        enforcement = {
            "network_policies": [],
            "pod_security_policies": [],
            "rbac_policies": [],
            "compliance_status": "compliant",
            "violations": [],
        }

        # Generate NetworkPolicy
        if "network_policies" in policies:
            enforcement["network_policies"] = self._generate_network_policies(
                namespace, policies["network_policies"]
            )

        # Generate PodSecurityPolicy
        if "pod_security" in policies:
            enforcement["pod_security_policies"] = self._generate_pod_security_policies(
                namespace, policies["pod_security"]
            )

        # Generate RBAC policies
        if "rbac" in policies:
            enforcement["rbac_policies"] = self._generate_rbac_policies(
                namespace, policies["rbac"]
            )

        return enforcement

    def analyze_helm_chart(self, chart_path: str) -> Dict[str, Any]:
        """Analyze Helm chart for best practices and issues"""
        chart_analysis = {
            "chart_name": "",
            "version": "",
            "issues": [],
            "recommendations": [],
            "security_concerns": [],
            "best_practices": [],
        }

        # This would analyze the actual Helm chart
        # For now, provide template analysis
        chart_analysis["recommendations"] = [
            "Use semantic versioning for chart versions",
            "Include resource limits and requests",
            "Add security contexts",
            "Implement health checks",
            "Use labels consistently",
            "Document all parameters in values.yaml",
        ]

        return chart_analysis

    def analyze_argocd_application(
        self, app_manifest: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze ArgoCD application for best practices"""
        app_analysis = {
            "application_name": app_manifest.get("metadata", {}).get("name", "unknown"),
            "sync_policy": app_manifest.get("spec", {}).get("syncPolicy", {}),
            "health_status": "healthy",
            "sync_status": "synced",
            "issues": [],
            "recommendations": [],
        }

        # Analyze sync policy
        sync_policy = app_manifest.get("spec", {}).get("syncPolicy", {})
        if not sync_policy.get("automated"):
            app_analysis["recommendations"].append(
                "Consider enabling automated sync for faster deployments"
            )

        # Check for proper RBAC
        if not app_manifest.get("spec", {}).get("project"):
            app_analysis["recommendations"].append(
                "Specify a project for better access control"
            )

        return app_analysis

    def generate_terraform_aks_config(
        self, cluster_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Terraform configuration for AKS cluster"""
        terraform_config = {
            "main.tf": self._generate_aks_main_config(cluster_config),
            "variables.tf": self._generate_aks_variables(cluster_config),
            "outputs.tf": self._generate_aks_outputs(cluster_config),
            "providers.tf": self._generate_aks_providers(cluster_config),
        }

        return terraform_config

    def explain_yaml_manifest(self, manifest_yaml: str) -> Dict[str, Any]:
        """Explain or suggest changes to YAML manifests"""
        explanation = {
            "manifest_type": "",
            "resources": [],
            "suggestions": [],
            "best_practices": [],
            "security_concerns": [],
        }

        try:
            # Parse YAML
            manifests = list(yaml.safe_load_all(manifest_yaml))

            for manifest in manifests:
                if manifest:
                    resource_info = self._analyze_manifest_resource(manifest)
                    explanation["resources"].append(resource_info)

                    # Generate suggestions
                    suggestions = self._generate_manifest_suggestions(manifest)
                    explanation["suggestions"].extend(suggestions)

        except yaml.YAMLError as e:
            explanation["error"] = f"Invalid YAML: {str(e)}"

        return explanation

    def _analyze_node_health(self, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze node health status"""
        node_analysis = {
            "total_nodes": len(nodes),
            "ready_nodes": 0,
            "issues": [],
            "recommendations": [],
        }

        for node in nodes:
            conditions = node.get("status", {}).get("conditions", [])
            for condition in conditions:
                if condition.get("type") == "Ready":
                    if condition.get("status") == "True":
                        node_analysis["ready_nodes"] += 1
                    else:
                        node_analysis["issues"].append(
                            f"Node {node.get('metadata', {}).get('name')} is not ready"
                        )

        return node_analysis

    def _analyze_pod_health(self, pods: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze pod health status"""
        pod_analysis = {
            "total_pods": len(pods),
            "running_pods": 0,
            "failed_pods": 0,
            "pending_pods": 0,
            "issues": [],
        }

        for pod in pods:
            phase = pod.get("status", {}).get("phase", "Unknown")
            if phase == "Running":
                pod_analysis["running_pods"] += 1
            elif phase == "Failed":
                pod_analysis["failed_pods"] += 1
                pod_analysis["issues"].append(
                    f"Pod {pod.get('metadata', {}).get('name')} has failed"
                )
            elif phase == "Pending":
                pod_analysis["pending_pods"] += 1
                pod_analysis["issues"].append(
                    f"Pod {pod.get('metadata', {}).get('name')} is pending"
                )

        return pod_analysis

    def _analyze_service_health(self, services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze service health status"""
        service_analysis = {"total_services": len(services), "issues": []}

        for service in services:
            endpoints = service.get("subsets", [])
            if not endpoints:
                service_analysis["issues"].append(
                    f"Service {service.get('metadata', {}).get('name')} has no endpoints"
                )

        return service_analysis

    def _analyze_pod_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze pod events for troubleshooting"""
        analyzed_events = []

        for event in events:
            analyzed_events.append(
                {
                    "type": event.get("type"),
                    "reason": event.get("reason"),
                    "message": event.get("message"),
                    "count": event.get("count", 1),
                    "last_timestamp": event.get("lastTimestamp"),
                }
            )

        return analyzed_events

    def _analyze_pod_misconfigurations(
        self, pod: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Analyze pod for misconfigurations"""
        issues = {"critical": [], "warning": []}

        spec = pod.get("spec", {})

        # Check for resource limits
        containers = spec.get("containers", [])
        for container in containers:
            if not container.get("resources", {}).get("limits"):
                issues["warning"].append(
                    f"Container {container.get('name')} missing resource limits"
                )

            if not container.get("resources", {}).get("requests"):
                issues["warning"].append(
                    f"Container {container.get('name')} missing resource requests"
                )

        # Check for security context
        if not spec.get("securityContext"):
            issues["warning"].append("Pod missing security context")

        # Check for liveness/readiness probes
        for container in containers:
            if not container.get("livenessProbe"):
                issues["warning"].append(
                    f"Container {container.get('name')} missing liveness probe"
                )

            if not container.get("readinessProbe"):
                issues["warning"].append(
                    f"Container {container.get('name')} missing readiness probe"
                )

        return issues

    def _analyze_deployment_misconfigurations(
        self, deployment: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Analyze deployment for misconfigurations"""
        issues = {"critical": [], "warning": []}

        spec = deployment.get("spec", {})

        # Check replica count
        replicas = spec.get("replicas", 1)
        if replicas < 2:
            issues["warning"].append(
                "Deployment has less than 2 replicas - consider for high availability"
            )

        # Check update strategy
        strategy = spec.get("strategy", {})
        if not strategy.get("rollingUpdate"):
            issues["warning"].append("Deployment missing rolling update strategy")

        return issues

    def _analyze_service_misconfigurations(
        self, service: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Analyze service for misconfigurations"""
        issues = {"critical": [], "warning": []}

        spec = service.get("spec", {})

        # Check service type
        service_type = spec.get("type", "ClusterIP")
        if service_type == "LoadBalancer":
            issues["warning"].append(
                "LoadBalancer service type may incur additional costs"
            )

        return issues

    def _generate_misconfiguration_recommendations(
        self, misconfigurations: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for misconfigurations"""
        recommendations = []

        if misconfigurations["critical"]:
            recommendations.append("Address critical issues immediately")

        if misconfigurations["warning"]:
            recommendations.append("Review and fix warnings to improve cluster health")

        recommendations.extend(
            [
                "Implement resource limits and requests for all containers",
                "Add security contexts to pods",
                "Configure health checks (liveness and readiness probes)",
                "Use rolling update strategies for deployments",
                "Implement network policies for security",
            ]
        )

        return recommendations

    def _recommend_pod_best_practices(
        self, pod_config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Recommend best practices for pods"""
        recommendations = {
            "probes": [
                "Implement liveness probe to detect deadlocks",
                "Implement readiness probe to ensure traffic routing",
                "Use startup probe for slow-starting containers",
            ],
            "limits": [
                "Set CPU and memory limits",
                "Set resource requests equal to limits for predictable scheduling",
                "Monitor resource usage and adjust limits accordingly",
            ],
            "labels": [
                "Use consistent labeling strategy",
                "Include app, version, and environment labels",
                "Use selectors for service discovery",
            ],
            "security": [
                "Run containers as non-root user",
                "Use read-only root filesystem",
                "Drop unnecessary capabilities",
                "Implement network policies",
            ],
        }

        return recommendations

    def _recommend_deployment_best_practices(
        self, deployment_config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Recommend best practices for deployments"""
        recommendations = {
            "probes": [
                "Configure rolling update strategy",
                "Set appropriate maxSurge and maxUnavailable",
                "Use health checks for deployment validation",
            ],
            "limits": [
                "Set replica count based on expected load",
                "Configure horizontal pod autoscaler",
                "Monitor deployment metrics",
            ],
            "labels": [
                "Use consistent label selectors",
                "Include version labels for rollback",
                "Use annotations for metadata",
            ],
        }

        return recommendations

    def _recommend_service_best_practices(
        self, service_config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Recommend best practices for services"""
        recommendations = {
            "probes": [
                "Use appropriate service type",
                "Configure session affinity if needed",
                "Set up proper port mappings",
            ],
            "limits": [
                "Monitor service endpoints",
                "Configure load balancing appropriately",
            ],
            "labels": [
                "Use consistent label selectors",
                "Include service type in labels",
            ],
        }

        return recommendations

    def _generate_network_policies(
        self, namespace: str, policies: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate NetworkPolicy resources"""
        network_policies = []

        # Default deny all policy
        network_policies.append(
            {
                "apiVersion": "networking.k8s.io/v1",
                "kind": "NetworkPolicy",
                "metadata": {"name": "default-deny-all", "namespace": namespace},
                "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
            }
        )

        return network_policies

    def _generate_pod_security_policies(
        self, namespace: str, security_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate PodSecurityPolicy resources"""
        psp_list = []

        # Restrictive PSP
        psp_list.append(
            {
                "apiVersion": "policy/v1beta1",
                "kind": "PodSecurityPolicy",
                "metadata": {"name": "restrictive-psp"},
                "spec": {
                    "privileged": False,
                    "allowPrivilegeEscalation": False,
                    "runAsUser": {"rule": "MustRunAsNonRoot"},
                    "fsGroup": {"rule": "MustRunAs"},
                    "supplementalGroups": {"rule": "MustRunAs"},
                },
            }
        )

        return psp_list

    def _generate_rbac_policies(
        self, namespace: str, rbac_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate RBAC policies"""
        rbac_resources = []

        # Service account
        rbac_resources.append(
            {
                "apiVersion": "v1",
                "kind": "ServiceAccount",
                "metadata": {"name": "restricted-sa", "namespace": namespace},
            }
        )

        return rbac_resources

    def _generate_aks_main_config(self, cluster_config: Dict[str, Any]) -> str:
        """Generate main.tf for AKS cluster"""
        return f"""
resource "azurerm_resource_group" "rg" {{
  name     = "{cluster_config.get('resource_group', 'k8s-rg')}"
  location = "{cluster_config.get('location', 'East US')}"
}}

resource "azurerm_kubernetes_cluster" "aks" {{
  name                = "{cluster_config.get('cluster_name', 'k8s-cluster')}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "{cluster_config.get('dns_prefix', 'k8s')}"

  default_node_pool {{
    name       = "default"
    node_count = {cluster_config.get('node_count', 1)}
    vm_size    = "{cluster_config.get('vm_size', 'Standard_DS2_v2')}"
  }}

  identity {{
    type = "SystemAssigned"
  }}

  tags = {{
    Environment = "{cluster_config.get('environment', 'production')}"
  }}
}}
"""

    def _generate_aks_variables(self, cluster_config: Dict[str, Any]) -> str:
        """Generate variables.tf for AKS cluster"""
        return """
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "k8s-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "k8s-cluster"
}
"""

    def _generate_aks_outputs(self, cluster_config: Dict[str, Any]) -> str:
        """Generate outputs.tf for AKS cluster"""
        return """
output "cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "cluster_id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}
"""

    def _generate_aks_providers(self, cluster_config: Dict[str, Any]) -> str:
        """Generate providers.tf for AKS cluster"""
        return """
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
"""

    def _analyze_manifest_resource(self, manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual manifest resource"""
        return {
            "kind": manifest.get("kind", "Unknown"),
            "name": manifest.get("metadata", {}).get("name", "unknown"),
            "namespace": manifest.get("metadata", {}).get("namespace", "default"),
            "api_version": manifest.get("apiVersion", "unknown"),
        }

    def _generate_manifest_suggestions(self, manifest: Dict[str, Any]) -> List[str]:
        """Generate suggestions for manifest improvements"""
        suggestions = []

        kind = manifest.get("kind", "")

        if kind == "Pod":
            suggestions.extend(
                [
                    "Consider using Deployment instead of Pod for better management",
                    "Add resource limits and requests",
                    "Include security context",
                ]
            )
        elif kind == "Deployment":
            suggestions.extend(
                [
                    "Set appropriate replica count",
                    "Configure rolling update strategy",
                    "Add resource limits",
                ]
            )
        elif kind == "Service":
            suggestions.extend(
                [
                    "Choose appropriate service type",
                    "Configure session affinity if needed",
                ]
            )

        return suggestions

    def _generate_health_recommendations(
        self, health_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []

        if health_analysis["overall_status"] == "degraded":
            recommendations.append("Address critical issues to restore cluster health")

        recommendations.extend(
            [
                "Implement monitoring and alerting",
                "Set up log aggregation",
                "Configure backup and disaster recovery",
                "Regular security audits and updates",
            ]
        )

        return recommendations


# Global instance
cka_operations = CKAOperations()
