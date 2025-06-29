"""
Agent Registry - Maps Logic Sources to Deployed Agents
Manages the relationship between logic sources and deployed AI agents
"""

import yaml
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class AgentRegistry:
    """Registry for managing logic source to agent mappings"""
    
    def __init__(self, registry_path: str = "/app/registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(exist_ok=True)
        
        # Logic source to agent mappings
        self.logic_to_agent = {
            'igris_logic': {
                'agent_name': 'igris-agent',
                'display_name': 'Igris',
                'description': 'Platform Engineering AI Agent',
                'capabilities': [
                    'Infrastructure Analysis',
                    'Security Assessment', 
                    'Platform Engineering',
                    'OpenDevin Integration'
                ],
                'logic_modules': [
                    'analyzer.py',
                    'infrastructure.py', 
                    'security.py',
                    'opendevin.py'
                ],
                'port': 8009,
                'health_endpoint': '/health',
                'enhancement_endpoint': '/enhance',
                'fallback_provider': 'openai',
                'deployment_priority': 'high'
            },
            'katie_logic': {
                'agent_name': 'katie-agent',
                'display_name': 'Katie',
                'description': 'Kubernetes AI Agent & Cluster Guardian',
                'capabilities': [
                    'Kubernetes Operations',
                    'Cluster Management',
                    'Resource Scaling',
                    'Log Analysis',
                    'K8GPT Integration'
                ],
                'logic_modules': [
                    'kubeops/describe.py',
                    'kubeops/scale.py',
                    'kubeops/logs.py',
                    'kubeops/patch.py'
                ],
                'port': 8008,
                'health_endpoint': '/health',
                'enhancement_endpoint': '/enhance',
                'fallback_provider': 'openai',
                'deployment_priority': 'high'
            },
            'james_logic': {
                'agent_name': 'james-agent',
                'display_name': 'James',
                'description': 'Personal AI Assistant & Executive Aid',
                'capabilities': [
                    'Voice Interaction',
                    'Image Description',
                    'Task Management',
                    'Executive Assistance'
                ],
                'logic_modules': [
                    'voice_response.py',
                    'routes/voice.py',
                    'routes/describe_image.py'
                ],
                'port': 8006,
                'health_endpoint': '/health',
                'enhancement_endpoint': '/enhance',
                'fallback_provider': 'openai',
                'deployment_priority': 'medium'
            },
            'whis_logic': {
                'agent_name': 'whis-agent',
                'display_name': 'Whis',
                'description': 'ML Training & Agent Enhancement AI',
                'capabilities': [
                    'Orb Generation',
                    'Rune Creation',
                    'Agent Enhancement',
                    'Training Management'
                ],
                'logic_modules': [
                    'logic/orbs.py',
                    'logic/runes.py',
                    'logic/enhancement.py'
                ],
                'port': 8003,
                'health_endpoint': '/health',
                'enhancement_endpoint': '/enhance',
                'fallback_provider': 'openai',
                'deployment_priority': 'critical'
            }
        }
        
        # Load existing registry
        self.load_registry()

    def register_agent(self, logic_source: str, agent_config: Dict[str, Any]) -> bool:
        """Register a new agent mapping"""
        try:
            if logic_source not in self.logic_to_agent:
                self.logic_to_agent[logic_source] = agent_config
                
            # Save to registry file
            registry_file = self.registry_path / f"{logic_source}_registry.yaml"
            with open(registry_file, 'w') as f:
                yaml.dump(agent_config, f, default_flow_style=False)
                
            logger.info(f"Registered agent mapping: {logic_source} -> {agent_config.get('agent_name')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent {logic_source}: {str(e)}")
            return False

    def get_agent_config(self, logic_source: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration for a logic source"""
        return self.logic_to_agent.get(logic_source)

    def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered agent configurations"""
        return self.logic_to_agent.copy()

    def get_agent_by_name(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get agent config by agent name"""
        for logic_source, config in self.logic_to_agent.items():
            if config.get('agent_name') == agent_name:
                return config
        return None

    def get_logic_source_by_agent(self, agent_name: str) -> Optional[str]:
        """Get logic source name by agent name"""
        for logic_source, config in self.logic_to_agent.items():
            if config.get('agent_name') == agent_name:
                return logic_source
        return None

    def update_agent_config(self, logic_source: str, updates: Dict[str, Any]) -> bool:
        """Update agent configuration"""
        try:
            if logic_source in self.logic_to_agent:
                self.logic_to_agent[logic_source].update(updates)
                
                # Save updated config
                registry_file = self.registry_path / f"{logic_source}_registry.yaml"
                with open(registry_file, 'w') as f:
                    yaml.dump(self.logic_to_agent[logic_source], f, default_flow_style=False)
                    
                logger.info(f"Updated agent config: {logic_source}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to update agent config {logic_source}: {str(e)}")
            return False

    def deploy_agent(self, logic_source: str, deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy an agent from logic source"""
        try:
            agent_config = self.get_agent_config(logic_source)
            if not agent_config:
                raise ValueError(f"No agent config found for {logic_source}")
                
            # Create deployment manifest
            deployment_manifest = self._create_deployment_manifest(logic_source, agent_config, deployment_config)
            
            # Save deployment record
            deployment_record = {
                'logic_source': logic_source,
                'agent_name': agent_config['agent_name'],
                'deployment_config': deployment_config,
                'deployment_manifest': deployment_manifest,
                'deployed_at': datetime.now().isoformat(),
                'status': 'deployed'
            }
            
            # Save to deployment history
            deployment_file = self.registry_path / f"{logic_source}_deployment.yaml"
            with open(deployment_file, 'w') as f:
                yaml.dump(deployment_record, f, default_flow_style=False)
                
            logger.info(f"Deployed agent: {logic_source} -> {agent_config['agent_name']}")
            return deployment_record
            
        except Exception as e:
            logger.error(f"Failed to deploy agent {logic_source}: {str(e)}")
            return {'error': str(e)}

    def _create_deployment_manifest(self, logic_source: str, agent_config: Dict[str, Any], deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Kubernetes deployment manifest for agent"""
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': agent_config['agent_name'],
                'labels': {
                    'app': agent_config['agent_name'],
                    'logic_source': logic_source,
                    'managed_by': 'ficknury_deploy'
                }
            },
            'spec': {
                'replicas': deployment_config.get('replicas', 1),
                'selector': {
                    'matchLabels': {
                        'app': agent_config['agent_name']
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': agent_config['agent_name'],
                            'logic_source': logic_source
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': agent_config['agent_name'],
                            'image': f"linkops-{logic_source}:latest",
                            'ports': [{
                                'containerPort': agent_config['port']
                            }],
                            'env': [
                                {'name': 'LOGIC_SOURCE', 'value': logic_source},
                                {'name': 'AGENT_NAME', 'value': agent_config['agent_name']},
                                {'name': 'FALLBACK_PROVIDER', 'value': agent_config['fallback_provider']}
                            ],
                            'livenessProbe': {
                                'httpGet': {
                                    'path': agent_config['health_endpoint'],
                                    'port': agent_config['port']
                                },
                                'initialDelaySeconds': 30,
                                'periodSeconds': 10
                            },
                            'readinessProbe': {
                                'httpGet': {
                                    'path': agent_config['health_endpoint'],
                                    'port': agent_config['port']
                                },
                                'initialDelaySeconds': 5,
                                'periodSeconds': 5
                            }
                        }]
                    }
                }
            }
        }

    def get_deployment_history(self, logic_source: str) -> Optional[Dict[str, Any]]:
        """Get deployment history for a logic source"""
        try:
            deployment_file = self.registry_path / f"{logic_source}_deployment.yaml"
            if deployment_file.exists():
                with open(deployment_file, 'r') as f:
                    return yaml.safe_load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load deployment history for {logic_source}: {str(e)}")
            return None

    def list_deployed_agents(self) -> List[Dict[str, Any]]:
        """List all deployed agents"""
        deployed_agents = []
        for logic_source in self.logic_to_agent.keys():
            deployment_record = self.get_deployment_history(logic_source)
            if deployment_record:
                deployed_agents.append(deployment_record)
        return deployed_agents

    def load_registry(self):
        """Load registry from files"""
        try:
            for logic_source in self.logic_to_agent.keys():
                registry_file = self.registry_path / f"{logic_source}_registry.yaml"
                if registry_file.exists():
                    with open(registry_file, 'r') as f:
                        loaded_config = yaml.safe_load(f)
                        if loaded_config:
                            self.logic_to_agent[logic_source].update(loaded_config)
                            
            logger.info(f"Loaded registry with {len(self.logic_to_agent)} agent mappings")
        except Exception as e:
            logger.error(f"Failed to load registry: {str(e)}")

    def export_registry(self, format: str = 'yaml') -> str:
        """Export registry in specified format"""
        try:
            if format.lower() == 'json':
                return json.dumps(self.logic_to_agent, indent=2)
            else:
                return yaml.dump(self.logic_to_agent, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to export registry: {str(e)}")
            return "" 