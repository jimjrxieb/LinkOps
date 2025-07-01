"""
Katie - Kubernetes Patch Operations
Handles resource patching with intelligent validation and rollback
"""

import subprocess
import json
import logging
import yaml
from typing import Dict, Any, List, Optional
from kubernetes import client, config
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)


class KubernetesPatcher:
    """
    Katie's Kubernetes patching operations with intelligent validation
    """

    def __init__(self):
        try:
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.networking_v1 = client.NetworkingV1Api()
            self.rbac_v1 = client.RbacAuthorizationV1Api()
            logger.info("Katie patcher initialized with Kubernetes client")
        except Exception as e:
            logger.warning(f"Kubernetes client initialization failed: {e}")
            self.v1 = None
            self.apps_v1 = None
            self.networking_v1 = None
            self.rbac_v1 = None

    def patch_deployment(
        self,
        namespace: str,
        deployment_name: str,
        patch_data: Dict[str, Any],
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Patch a deployment with intelligent validation
        """
        try:
            logger.info(f"Katie patching deployment: {deployment_name}")

            if dry_run:
                return self._dry_run_patch_deployment(
                    namespace, deployment_name, patch_data
                )

            # Validate patch data
            validation_result = self._validate_deployment_patch(patch_data)
            if not validation_result["valid"]:
                return {
                    "agent": "katie",
                    "operation": "patch_deployment",
                    "error": f"Patch validation failed: {validation_result['reason']}",
                    "status": "validation_error",
                }

            # Get current deployment
            current_deployment = self.apps_v1.read_namespaced_deployment(
                deployment_name, namespace
            )

            # Apply patch
            patched_deployment = self.apps_v1.patch_namespaced_deployment(
                deployment_name, namespace, patch_data
            )

            # Analyze patch impact
            impact_analysis = self._analyze_deployment_patch_impact(
                current_deployment, patched_deployment, patch_data
            )

            return {
                "agent": "katie",
                "operation": "patch_deployment",
                "deployment_name": deployment_name,
                "namespace": namespace,
                "patch_applied": True,
                "impact_analysis": impact_analysis,
                "rollback_available": True,
                "katie_insight": self._generate_patch_insight(
                    deployment_name, patch_data, impact_analysis
                ),
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "patch_deployment",
                "error": f"Patch failed: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Deployment patching failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "patch_deployment",
                "error": f"Patching failed: {str(e)}",
                "status": "error",
            }

    def patch_configmap(
        self,
        namespace: str,
        configmap_name: str,
        patch_data: Dict[str, Any],
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Patch a ConfigMap with validation
        """
        try:
            logger.info(f"Katie patching ConfigMap: {configmap_name}")

            if dry_run:
                return self._dry_run_patch_configmap(
                    namespace, configmap_name, patch_data
                )

            # Validate patch data
            validation_result = self._validate_configmap_patch(patch_data)
            if not validation_result["valid"]:
                return {
                    "agent": "katie",
                    "operation": "patch_configmap",
                    "error": f"Patch validation failed: {validation_result['reason']}",
                    "status": "validation_error",
                }

            # Apply patch
            self.v1.patch_namespaced_config_map(
                configmap_name, namespace, patch_data
            )

            return {
                "agent": "katie",
                "operation": "patch_configmap",
                "configmap_name": configmap_name,
                "namespace": namespace,
                "patch_applied": True,
                "katie_insight": f"ConfigMap {configmap_name} updated successfully.",
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "patch_configmap",
                "error": f"Patch failed: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"ConfigMap patching failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "patch_configmap",
                "error": f"Patching failed: {str(e)}",
                "status": "error",
            }

    def patch_service(
        self,
        namespace: str,
        service_name: str,
        patch_data: Dict[str, Any],
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Patch a Service with validation
        """
        try:
            logger.info(f"Katie patching Service: {service_name}")

            if dry_run:
                return self._dry_run_patch_service(namespace, service_name, patch_data)

            # Validate patch data
            validation_result = self._validate_service_patch(patch_data)
            if not validation_result["valid"]:
                return {
                    "agent": "katie",
                    "operation": "patch_service",
                    "error": f"Patch validation failed: {validation_result['reason']}",
                    "status": "validation_error",
                }

            # Apply patch
            self.v1.patch_namespaced_service(
                service_name, namespace, patch_data
            )

            return {
                "agent": "katie",
                "operation": "patch_service",
                "service_name": service_name,
                "namespace": namespace,
                "patch_applied": True,
                "katie_insight": f"Service {service_name} updated successfully.",
            }

        except ApiException as e:
            logger.error(f"Kubernetes API error: {e}")
            return {
                "agent": "katie",
                "operation": "patch_service",
                "error": f"Patch failed: {e.reason}",
                "status": "error",
            }
        except Exception as e:
            logger.error(f"Service patching failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "patch_service",
                "error": f"Patching failed: {str(e)}",
                "status": "error",
            }

    def apply_manifest(
        self, manifest_yaml: str, namespace: str = "default", dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Apply a Kubernetes manifest with validation
        """
        try:
            logger.info(f"Katie applying manifest to namespace: {namespace}")

            if dry_run:
                return self._dry_run_apply_manifest(manifest_yaml, namespace)

            # Validate manifest
            validation_result = self._validate_manifest(manifest_yaml)
            if not validation_result["valid"]:
                return {
                    "agent": "katie",
                    "operation": "apply_manifest",
                    "error": f"Manifest validation failed: {validation_result['reason']}",
                    "status": "validation_error",
                }

            # Apply manifest using kubectl
            result = subprocess.run(
                ["kubectl", "apply", "-f", "-", "-n", namespace],
                input=manifest_yaml,
                text=True,
                capture_output=True,
                timeout=60,
            )

            if result.returncode == 0:
                return {
                    "agent": "katie",
                    "operation": "apply_manifest",
                    "namespace": namespace,
                    "manifest_applied": True,
                    "output": result.stdout,
                    "katie_insight": "Manifest applied successfully.",
                }
            else:
                return {
                    "agent": "katie",
                    "operation": "apply_manifest",
                    "error": f"Manifest application failed: {result.stderr}",
                    "status": "error",
                }

        except Exception as e:
            logger.error(f"Manifest application failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "apply_manifest",
                "error": f"Manifest application failed: {str(e)}",
                "status": "error",
            }

    def rollback_deployment(
        self, namespace: str, deployment_name: str, revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Rollback a deployment to a previous revision
        """
        try:
            logger.info(f"Katie rolling back deployment: {deployment_name}")

            # Get rollout history
            history = self._get_rollout_history(deployment_name, namespace)

            if not revision:
                # Use previous revision
                if len(history) >= 2:
                    revision = history[1]["revision"]
                else:
                    return {
                        "agent": "katie",
                        "operation": "rollback_deployment",
                        "error": "No previous revision available for rollback",
                        "status": "error",
                    }

            # Perform rollback
            result = subprocess.run(
                [
                    "kubectl",
                    "rollout",
                    "undo",
                    f"deployment/{deployment_name}",
                    "-n",
                    namespace,
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                return {
                    "agent": "katie",
                    "operation": "rollback_deployment",
                    "deployment_name": deployment_name,
                    "namespace": namespace,
                    "rollback_revision": revision,
                    "rollback_successful": True,
                    "katie_insight": f"Deployment {deployment_name} rolled back to revision {revision}.",
                }
            else:
                return {
                    "agent": "katie",
                    "operation": "rollback_deployment",
                    "error": f"Rollback failed: {result.stderr}",
                    "status": "error",
                }

        except Exception as e:
            logger.error(f"Deployment rollback failed: {str(e)}")
            return {
                "agent": "katie",
                "operation": "rollback_deployment",
                "error": f"Rollback failed: {str(e)}",
                "status": "error",
            }

    def _validate_deployment_patch(self, patch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate deployment patch data"""
        validation = {"valid": True, "reason": ""}

        # Check for required fields
        if "spec" not in patch_data:
            validation["valid"] = False
            validation["reason"] = "Missing 'spec' field in patch data"
            return validation

        # Check for dangerous changes
        spec = patch_data["spec"]
        if "replicas" in spec and spec["replicas"] == 0:
            validation["valid"] = False
            validation["reason"] = "Setting replicas to 0 will stop the deployment"
            return validation

        # Check container image changes
        if "template" in spec and "spec" in spec["template"]:
            containers = spec["template"]["spec"].get("containers", [])
            for container in containers:
                if "image" in container:
                    # Validate image format
                    if not self._validate_image_format(container["image"]):
                        validation["valid"] = False
                        validation["reason"] = (
                            f"Invalid image format: {container['image']}"
                        )
                        return validation

        return validation

    def _validate_configmap_patch(self, patch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate ConfigMap patch data"""
        validation = {"valid": True, "reason": ""}

        # Check for data field
        if "data" not in patch_data:
            validation["valid"] = False
            validation["reason"] = "Missing 'data' field in ConfigMap patch"
            return validation

        return validation

    def _validate_service_patch(self, patch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Service patch data"""
        validation = {"valid": True, "reason": ""}

        # Check for spec field
        if "spec" not in patch_data:
            validation["valid"] = False
            validation["reason"] = "Missing 'spec' field in Service patch"
            return validation

        return validation

    def _validate_manifest(self, manifest_yaml: str) -> Dict[str, Any]:
        """Validate Kubernetes manifest"""
        validation = {"valid": True, "reason": ""}

        try:
            # Parse YAML
            manifest_data = yaml.safe_load(manifest_yaml)

            # Check for required fields
            if not manifest_data:
                validation["valid"] = False
                validation["reason"] = "Empty or invalid YAML"
                return validation

            # Check for API version and kind
            if "apiVersion" not in manifest_data or "kind" not in manifest_data:
                validation["valid"] = False
                validation["reason"] = "Missing apiVersion or kind"
                return validation

            # Validate specific resource types
            kind = manifest_data["kind"]
            if kind == "Deployment":
                if "spec" not in manifest_data:
                    validation["valid"] = False
                    validation["reason"] = "Deployment missing spec"
                    return validation

        except yaml.YAMLError as e:
            validation["valid"] = False
            validation["reason"] = f"Invalid YAML: {str(e)}"

        return validation

    def _validate_image_format(self, image: str) -> bool:
        """Validate Docker image format"""
        # Basic image format validation
        if not image or ":" not in image:
            return False

        parts = image.split(":")
        if len(parts) != 2:
            return False

        return True

    def _analyze_deployment_patch_impact(
        self, current_deployment, patched_deployment, patch_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze the impact of deployment patch"""
        impact = {
            "changes": [],
            "restart_required": False,
            "scaling_impact": False,
            "risk_level": "low",
        }

        # Check for image changes
        if "spec" in patch_data and "template" in patch_data["spec"]:
            template_spec = patch_data["spec"]["template"]["spec"]
            if "containers" in template_spec:
                impact["restart_required"] = True
                impact["changes"].append("Container image updated")

        # Check for replica changes
        if "spec" in patch_data and "replicas" in patch_data["spec"]:
            impact["scaling_impact"] = True
            impact["changes"].append("Replica count changed")

        # Check for resource changes
        if "spec" in patch_data and "template" in patch_data["spec"]:
            template_spec = patch_data["spec"]["template"]["spec"]
            if "containers" in template_spec:
                for container in template_spec["containers"]:
                    if "resources" in container:
                        impact["changes"].append("Resource limits/requests updated")

        # Determine risk level
        if impact["restart_required"] and impact["scaling_impact"]:
            impact["risk_level"] = "high"
        elif impact["restart_required"] or impact["scaling_impact"]:
            impact["risk_level"] = "medium"

        return impact

    def _get_rollout_history(
        self, deployment_name: str, namespace: str
    ) -> List[Dict[str, Any]]:
        """Get deployment rollout history"""
        try:
            result = subprocess.run(
                [
                    "kubectl",
                    "rollout",
                    "history",
                    f"deployment/{deployment_name}",
                    "-n",
                    namespace,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                history = []
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            history.append(
                                {
                                    "revision": parts[0],
                                    "change_cause": (
                                        " ".join(parts[1:])
                                        if len(parts) > 1
                                        else "No change cause"
                                    ),
                                }
                            )
                return history
            else:
                return []
        except Exception as e:
            logger.warning(f"Failed to get rollout history: {e}")
            return []

    def _dry_run_patch_deployment(
        self, namespace: str, deployment_name: str, patch_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate deployment patch without applying"""
        validation_result = self._validate_deployment_patch(patch_data)
        if not validation_result["valid"]:
            return {
                "agent": "katie",
                "operation": "patch_deployment",
                "error": f"Patch validation failed: {validation_result['reason']}",
                "status": "validation_error",
            }

        impact_analysis = self._analyze_deployment_patch_impact(None, None, patch_data)

        return {
            "agent": "katie",
            "operation": "patch_deployment",
            "deployment_name": deployment_name,
            "namespace": namespace,
            "patch_applied": False,
            "status": "dry_run",
            "impact_analysis": impact_analysis,
            "katie_insight": f"DRY RUN: Would patch {deployment_name} with {len(impact_analysis['changes'])} changes",
        }

    def _dry_run_patch_configmap(
        self, namespace: str, configmap_name: str, patch_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate ConfigMap patch without applying"""
        validation_result = self._validate_configmap_patch(patch_data)
        if not validation_result["valid"]:
            return {
                "agent": "katie",
                "operation": "patch_configmap",
                "error": f"Patch validation failed: {validation_result['reason']}",
                "status": "validation_error",
            }

        return {
            "agent": "katie",
            "operation": "patch_configmap",
            "configmap_name": configmap_name,
            "namespace": namespace,
            "patch_applied": False,
            "status": "dry_run",
            "katie_insight": f"DRY RUN: Would update ConfigMap {configmap_name}",
        }

    def _dry_run_patch_service(
        self, namespace: str, service_name: str, patch_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate Service patch without applying"""
        validation_result = self._validate_service_patch(patch_data)
        if not validation_result["valid"]:
            return {
                "agent": "katie",
                "operation": "patch_service",
                "error": f"Patch validation failed: {validation_result['reason']}",
                "status": "validation_error",
            }

        return {
            "agent": "katie",
            "operation": "patch_service",
            "service_name": service_name,
            "namespace": namespace,
            "patch_applied": False,
            "status": "dry_run",
            "katie_insight": f"DRY RUN: Would update Service {service_name}",
        }

    def _dry_run_apply_manifest(
        self, manifest_yaml: str, namespace: str
    ) -> Dict[str, Any]:
        """Simulate manifest application without applying"""
        validation_result = self._validate_manifest(manifest_yaml)
        if not validation_result["valid"]:
            return {
                "agent": "katie",
                "operation": "apply_manifest",
                "error": f"Manifest validation failed: {validation_result['reason']}",
                "status": "validation_error",
            }

        return {
            "agent": "katie",
            "operation": "apply_manifest",
            "namespace": namespace,
            "manifest_applied": False,
            "status": "dry_run",
            "katie_insight": "DRY RUN: Manifest validation passed, ready for application",
        }

    def _generate_patch_insight(
        self,
        resource_name: str,
        patch_data: Dict[str, Any],
        impact_analysis: Dict[str, Any],
    ) -> str:
        """Generate Katie's insight about patch operation"""
        changes = impact_analysis.get("changes", [])
        risk_level = impact_analysis.get("risk_level", "low")

        if risk_level == "high":
            return f"High-risk patch applied to {resource_name}. Changes: {', '.join(changes)}. Monitor closely."
        elif risk_level == "medium":
            return f"Medium-risk patch applied to {resource_name}. Changes: {', '.join(changes)}."
        else:
            return f"Low-risk patch applied to {resource_name}. Changes: {', '.join(changes)}."


# Global instance
k8s_patcher = KubernetesPatcher()
