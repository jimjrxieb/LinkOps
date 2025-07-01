"""
Agent Registry - Manages logic source to agent mappings and deployment configurations
"""

import yaml
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Registry for managing logic source to agent mappings and deployment configurations
    """

    def __init__(self, registry_file: str = "agent_registry.yaml"):
        self.registry_file = registry_file
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """Load agent registry from file"""
        try:
            with open(self.registry_file, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            # Initialize with default agent configurations
            default_registry = {
                "agents": {
                    "igris_logic": {
                        "agent_name": "igris",
                        "description": "Platform Engineering Agent",
                        "capabilities": [
                            "Infrastructure Analysis",
                            "Security Assessment",
                            "OpenDevin Integration",
                            "Platform Engineering",
                        ],
                        "deployment_config": {
                            "image": "ghcr.io/shadow-link-industries/igris_logic:latest",
                            "port": 8000,
                            "env": {"LOG_LEVEL": "INFO", "OPENAI_MODEL": "gpt-4"},
                            "resources": {
                                "limits": {"cpu": "500m", "memory": "512Mi"},
                                "requests": {"cpu": "200m", "memory": "256Mi"},
                            },
                        },
                        "helm_chart": "igris_logic",
                        "deployment_status": "not_deployed",
                        "last_deployed": None,
                    },
                    "katie_logic": {
                        "agent_name": "katie",
                        "description": "Kubernetes AI Agent & Cluster Guardian",
                        "capabilities": [
                            "Cluster Management",
                            "Resource Scaling",
                            "Log Analysis",
                            "K8GPT Integration",
                            "SRE Operations",
                        ],
                        "deployment_config": {
                            "image": "ghcr.io/shadow-link-industries/katie_logic:latest",
                            "port": 8000,
                            "env": {
                                "LOG_LEVEL": "INFO",
                                "OPENAI_MODEL": "gpt-4",
                                "K8GPT_ENABLED": "true",
                            },
                            "resources": {
                                "limits": {"cpu": "500m", "memory": "512Mi"},
                                "requests": {"cpu": "200m", "memory": "256Mi"},
                            },
                            "volumes": {
                                "kubeconfig": {
                                    "enabled": True,
                                    "mountPath": "/root/.kube",
                                    "secretName": "katie-kubeconfig",
                                }
                            },
                        },
                        "helm_chart": "katie_logic",
                        "deployment_status": "not_deployed",
                        "last_deployed": None,
                    },
                    "whis_logic": {
                        "agent_name": "whis",
                        "description": "Intelligence Processing & Analysis Agent",
                        "capabilities": [
                            "Data Processing",
                            "Intelligence Analysis",
                            "Pattern Recognition",
                            "ML Model Integration",
                        ],
                        "deployment_config": {
                            "image": "ghcr.io/shadow-link-industries/whis_logic:latest",
                            "port": 8000,
                            "env": {
                                "LOG_LEVEL": "INFO",
                                "OPENAI_MODEL": "gpt-4",
                                "PROCESSING_MODE": "intelligence",
                            },
                            "resources": {
                                "limits": {"cpu": "1000m", "memory": "1Gi"},
                                "requests": {"cpu": "500m", "memory": "512Mi"},
                            },
                            "persistence": {"enabled": True, "size": "10Gi"},
                        },
                        "helm_chart": "whis_logic",
                        "deployment_status": "not_deployed",
                        "last_deployed": None,
                    },
                    "james_logic": {
                        "agent_name": "james",
                        "description": "Personal AI Assistant & Executive Agent",
                        "capabilities": [
                            "Voice Interaction",
                            "Image Processing",
                            "Executive Assistance",
                            "Personal AI",
                        ],
                        "deployment_config": {
                            "image": "ghcr.io/shadow-link-industries/james_logic:latest",
                            "port": 8000,
                            "env": {
                                "LOG_LEVEL": "INFO",
                                "OPENAI_MODEL": "gpt-4",
                                "VOICE_ENABLED": "true",
                                "IMAGE_PROCESSING_ENABLED": "true",
                            },
                            "resources": {
                                "limits": {"cpu": "500m", "memory": "512Mi"},
                                "requests": {"cpu": "200m", "memory": "256Mi"},
                            },
                        },
                        "helm_chart": "james_logic",
                        "deployment_status": "not_deployed",
                        "last_deployed": None,
                    },
                },
                "deployment_history": {},
                "last_updated": datetime.now().isoformat(),
            }
            self._save_registry(default_registry)
            return default_registry

    def _save_registry(self, registry: Dict[str, Any]):
        """Save agent registry to file"""
        try:
            with open(self.registry_file, "w") as f:
                yaml.dump(registry, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to save registry: {str(e)}")

    def get_agent_config(self, logic_source: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration for a logic source"""
        return self.registry.get("agents", {}).get(logic_source)

    def get_all_agents(self) -> Dict[str, Any]:
        """Get all registered agents"""
        return self.registry.get("agents", {})

    def register_agent(self, logic_source: str, agent_config: Dict[str, Any]):
        """Register a new agent"""
        if "agents" not in self.registry:
            self.registry["agents"] = {}

        self.registry["agents"][logic_source] = agent_config
        self.registry["last_updated"] = datetime.now().isoformat()
        self._save_registry(self.registry)

    def update_agent_config(self, logic_source: str, updates: Dict[str, Any]):
        """Update agent configuration"""
        if logic_source in self.registry.get("agents", {}):
            self.registry["agents"][logic_source].update(updates)
            self.registry["last_updated"] = datetime.now().isoformat()
            self._save_registry(self.registry)

    def get_logic_source_by_agent(self, agent_name: str) -> Optional[str]:
        """Get logic source by agent name"""
        for logic_source, config in self.registry.get("agents", {}).items():
            if config.get("agent_name") == agent_name:
                return logic_source
        return None

    def get_deployment_history(self, logic_source: str) -> Optional[Dict[str, Any]]:
        """Get deployment history for a logic source"""
        return self.registry.get("deployment_history", {}).get(logic_source)

    def record_deployment(self, logic_source: str, deployment_info: Dict[str, Any]):
        """Record deployment information"""
        if "deployment_history" not in self.registry:
            self.registry["deployment_history"] = {}

        if logic_source not in self.registry["deployment_history"]:
            self.registry["deployment_history"][logic_source] = []

        deployment_info["timestamp"] = datetime.now().isoformat()
        self.registry["deployment_history"][logic_source].append(deployment_info)
        self.registry["last_updated"] = datetime.now().isoformat()
        self._save_registry(self.registry)

    def export_registry(self, format: str = "yaml") -> str:
        """Export registry in specified format"""
        if format.lower() == "json":
            return json.dumps(self.registry, indent=2)
        else:
            return yaml.dump(self.registry, default_flow_style=False)
