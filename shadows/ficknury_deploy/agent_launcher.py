"""
Agent Launcher - Deploys logic sources as AI agents using Helm charts and ArgoCD
"""

import subprocess
import yaml
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class AgentLauncher:
    """
    Launches logic sources as deployable AI agents
    """

    def __init__(self, registry=None):
        self.registry = registry
        self.helm_repo = "https://github.com/shadow-link-industries/LinkOps-Helm.git"
        self.argocd_namespace = "argocd"
        self.linkops_namespace = "linkops"

    def launch_shadow_agent(
        self, logic_source: str, deployment_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Launch a shadow agent from logic source using Helm and ArgoCD
        """
        try:
            logger.info(f"Launching shadow agent for logic source: {logic_source}")

            # Get agent configuration
            agent_config = self.registry.get_agent_config(logic_source)
            if not agent_config:
                return {
                    "success": False,
                    "error": f"No agent configuration found for {logic_source}",
                }

            agent_name = agent_config["agent_name"]
            helm_chart = agent_config["helm_chart"]

            # Merge deployment config
            final_config = agent_config["deployment_config"].copy()
            if deployment_config:
                final_config.update(deployment_config)

            # Create ArgoCD application manifest
            app_manifest = self._create_argocd_app_manifest(
                agent_name, helm_chart, final_config
            )

            # Apply ArgoCD application
            success = self._apply_argocd_application(app_manifest)
            if not success:
                return {"success": False, "error": "Failed to apply ArgoCD application"}

            # Update registry
            self.registry.update_agent_config(
                logic_source,
                {
                    "deployment_status": "deployed",
                    "last_deployed": datetime.now().isoformat(),
                },
            )

            # Record deployment
            self.registry.record_deployment(
                logic_source,
                {
                    "action": "deploy",
                    "agent_name": agent_name,
                    "helm_chart": helm_chart,
                    "deployment_config": final_config,
                    "status": "success",
                },
            )

            return {
                "success": True,
                "agent_name": agent_name,
                "helm_chart": helm_chart,
                "deployment_config": final_config,
                "launched_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to launch shadow agent: {str(e)}")
            return {"success": False, "error": str(e)}

    def _create_argocd_app_manifest(
        self, agent_name: str, helm_chart: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create ArgoCD application manifest"""

        # Convert config to Helm values format
        helm_values = self._config_to_helm_values(config)

        app_manifest = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {
                "name": f"{agent_name}-logic",
                "namespace": self.argocd_namespace,
                "labels": {
                    "app.kubernetes.io/name": f"{agent_name}-logic",
                    "app.kubernetes.io/instance": "linkops",
                    "app.kubernetes.io/part-of": "linkops-mlops",
                },
            },
            "spec": {
                "project": "default",
                "source": {
                    "repoURL": self.helm_repo,
                    "targetRevision": "HEAD",
                    "chart": helm_chart,
                    "helm": {
                        "values": yaml.dump(helm_values, default_flow_style=False)
                    },
                },
                "destination": {
                    "server": "https://kubernetes.default.svc",
                    "namespace": self.linkops_namespace,
                },
                "syncPolicy": {
                    "automated": {"prune": True, "selfHeal": True},
                    "syncOptions": [
                        "CreateNamespace=true",
                        "PrunePropagationPolicy=foreground",
                        "PruneLast=true",
                    ],
                },
                "revisionHistoryLimit": 10,
            },
        }

        return app_manifest

    def _config_to_helm_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert deployment config to Helm values format"""
        helm_values = {
            "replicaCount": 1,
            "image": {
                "repository": config.get(
                    "image", "ghcr.io/shadow-link-industries/placeholder"
                ),
                "tag": "latest",
                "pullPolicy": "Always",
            },
            "service": {"type": "ClusterIP", "port": config.get("port", 8000)},
        }

        # Add environment variables
        if "env" in config:
            helm_values["env"] = config["env"]

        # Add secrets
        if "secrets" in config:
            helm_values["secrets"] = config["secrets"]

        # Add resources
        if "resources" in config:
            helm_values["resources"] = config["resources"]

        # Add volumes
        if "volumes" in config:
            helm_values["volumes"] = config["volumes"]

        # Add persistence
        if "persistence" in config:
            helm_values["persistence"] = config["persistence"]

        return helm_values

    def _apply_argocd_application(self, app_manifest: Dict[str, Any]) -> bool:
        """Apply ArgoCD application using kubectl"""
        try:
            # Write manifest to temporary file
            temp_file = f"/tmp/{app_manifest['metadata']['name']}.yaml"
            with open(temp_file, "w") as f:
                yaml.dump(app_manifest, f, default_flow_style=False)

            # Apply using kubectl
            result = subprocess.run(
                ["kubectl", "apply", "-f", temp_file], capture_output=True, text=True
            )

            # Clean up temp file
            os.remove(temp_file)

            if result.returncode == 0:
                logger.info(
                    f"Successfully applied ArgoCD application: {app_manifest['metadata']['name']}"
                )
                return True
            else:
                logger.error(f"Failed to apply ArgoCD application: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error applying ArgoCD application: {str(e)}")
            return False

    def list_launched_agents(self) -> List[Dict[str, Any]]:
        """List all launched agents"""
        try:
            # Get ArgoCD applications
            result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "applications",
                    "-n",
                    self.argocd_namespace,
                    "-o",
                    "json",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                logger.error(f"Failed to get ArgoCD applications: {result.stderr}")
                return []

            apps_data = json.loads(result.stdout)
            launched_agents = []

            for app in apps_data.get("items", []):
                app_name = app["metadata"]["name"]
                if app_name.endswith("-logic"):
                    agent_name = app_name.replace("-logic", "")

                    # Get agent info from registry
                    logic_source = self.registry.get_logic_source_by_agent(agent_name)
                    agent_config = None
                    if logic_source:
                        agent_config = self.registry.get_agent_config(logic_source)

                    launched_agents.append(
                        {
                            "agent_name": agent_name,
                            "app_name": app_name,
                            "status": app["status"]
                            .get("health", {})
                            .get("status", "Unknown"),
                            "sync_status": app["status"]
                            .get("sync", {})
                            .get("status", "Unknown"),
                            "agent_config": agent_config,
                        }
                    )

            return launched_agents

        except Exception as e:
            logger.error(f"Failed to list launched agents: {str(e)}")
            return []

    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        try:
            app_name = f"{agent_name}-logic"

            # Get ArgoCD application status
            result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "application",
                    app_name,
                    "-n",
                    self.argocd_namespace,
                    "-o",
                    "json",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                return {
                    "status": "not_found",
                    "error": f"Application {app_name} not found",
                }

            app_data = json.loads(result.stdout)

            # Get Kubernetes deployment status
            deployment_name = f"{agent_name}-logic"
            deploy_result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "deployment",
                    deployment_name,
                    "-n",
                    self.linkops_namespace,
                    "-o",
                    "json",
                ],
                capture_output=True,
                text=True,
            )

            deployment_status = {}
            if deploy_result.returncode == 0:
                deploy_data = json.loads(deploy_result.stdout)
                deployment_status = {
                    "replicas": deploy_data["status"].get("replicas", 0),
                    "available_replicas": deploy_data["status"].get(
                        "availableReplicas", 0
                    ),
                    "ready_replicas": deploy_data["status"].get("readyReplicas", 0),
                    "updated_replicas": deploy_data["status"].get("updatedReplicas", 0),
                }

            return {
                "agent_name": agent_name,
                "app_name": app_name,
                "argocd_status": {
                    "health": app_data["status"]
                    .get("health", {})
                    .get("status", "Unknown"),
                    "sync_status": app_data["status"]
                    .get("sync", {})
                    .get("status", "Unknown"),
                    "last_sync": app_data["status"]
                    .get("operationState", {})
                    .get("finishedAt", "Unknown"),
                },
                "deployment_status": deployment_status,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to get agent status: {str(e)}")
            return {"status": "error", "error": str(e)}
