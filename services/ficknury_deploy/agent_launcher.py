"""
Agent Launcher - Packages Logic Sources into Deployed AI Agents
Handles the deployment of logic sources as full AI agents with fallback capabilities
"""

import os
import shutil
import yaml
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import subprocess
import docker
from datetime import datetime

from agent_registry import AgentRegistry

logger = logging.getLogger(__name__)

class AgentLauncher:
    """Launches logic sources as deployed AI agents"""
    
    def __init__(self, base_path: str = "/app", registry: Optional[AgentRegistry] = None):
        self.base_path = Path(base_path)
        self.registry = registry or AgentRegistry()
        self.docker_client = docker.from_env()
        
    def launch_shadow_agent(self, logic_source: str, deployment_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Launch a shadow agent from logic source
        
        Args:
            logic_source: Name of the logic source (e.g., 'igris_logic')
            deployment_config: Optional deployment configuration
            
        Returns:
            Deployment result with status and metadata
        """
        try:
            logger.info(f"Launching shadow agent from {logic_source}")
            
            # Get agent configuration
            agent_config = self.registry.get_agent_config(logic_source)
            if not agent_config:
                raise ValueError(f"No agent configuration found for {logic_source}")
                
            # Prepare deployment config
            if not deployment_config:
                deployment_config = self._get_default_deployment_config(agent_config)
                
            # Package logic source into agent
            package_result = self._package_logic_source(logic_source, agent_config)
            if not package_result['success']:
                return package_result
                
            # Inject OpenAI fallback
            fallback_result = self._inject_openai_fallback(logic_source, agent_config)
            if not fallback_result['success']:
                return fallback_result
                
            # Build agent container
            build_result = self._build_agent_container(logic_source, agent_config)
            if not build_result['success']:
                return build_result
                
            # Deploy agent
            deploy_result = self._deploy_agent(logic_source, agent_config, deployment_config)
            
            # Register deployment
            self.registry.deploy_agent(logic_source, deployment_config)
            
            logger.info(f"Successfully launched {agent_config['agent_name']} from {logic_source}")
            return {
                'success': True,
                'logic_source': logic_source,
                'agent_name': agent_config['agent_name'],
                'deployment_config': deployment_config,
                'deploy_result': deploy_result,
                'launched_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to launch shadow agent {logic_source}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'logic_source': logic_source
            }

    def _package_logic_source(self, logic_source: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Package logic source into deployable agent"""
        try:
            logic_path = self.base_path / "services" / logic_source
            if not logic_path.exists():
                raise ValueError(f"Logic source path not found: {logic_path}")
                
            # Create agent package directory
            agent_name = agent_config['agent_name']
            package_path = self.base_path / "agents" / agent_name
            package_path.mkdir(parents=True, exist_ok=True)
            
            # Copy logic source files
            self._copy_logic_files(logic_path, package_path, agent_config)
            
            # Create agent-specific main.py
            self._create_agent_main(package_path, logic_source, agent_config)
            
            # Create agent Dockerfile
            self._create_agent_dockerfile(package_path, agent_config)
            
            # Create agent requirements
            self._create_agent_requirements(package_path, logic_source)
            
            logger.info(f"Packaged {logic_source} into {agent_name}")
            return {'success': True, 'package_path': str(package_path)}
            
        except Exception as e:
            logger.error(f"Failed to package logic source {logic_source}: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _copy_logic_files(self, source_path: Path, dest_path: Path, agent_config: Dict[str, Any]):
        """Copy logic files to agent package"""
        # Copy main logic modules
        for module in agent_config.get('logic_modules', []):
            module_path = source_path / module
            if module_path.exists():
                if module_path.is_file():
                    # Copy file
                    dest_file = dest_path / module_path.name
                    shutil.copy2(module_path, dest_file)
                else:
                    # Copy directory
                    dest_dir = dest_path / module_path.name
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)
                    shutil.copytree(module_path, dest_dir)
                    
        # Copy requirements.txt if exists
        req_file = source_path / "requirements.txt"
        if req_file.exists():
            shutil.copy2(req_file, dest_path / "requirements.txt")
            
        # Copy any additional files
        additional_files = ['__init__.py', 'config.py', 'utils.py']
        for file_name in additional_files:
            file_path = source_path / file_name
            if file_path.exists():
                shutil.copy2(file_path, dest_path / file_name)

    def _create_agent_main(self, package_path: Path, logic_source: str, agent_config: Dict[str, Any]):
        """Create agent-specific main.py with OpenAI fallback"""
        agent_name = agent_config['agent_name']
        display_name = agent_config['display_name']
        description = agent_config['description']
        port = agent_config['port']
        
        main_content = f'''"""
{display_name} - {description}
Deployed AI Agent from {logic_source}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import openai
import os
import importlib.util
import sys

# Import logic modules
{self._generate_imports(agent_config)}

app = FastAPI(
    title="{display_name} - {description}",
    description="Deployed AI Agent with OpenAI fallback",
    version="2.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI fallback configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
FALLBACK_ENABLED = bool(OPENAI_API_KEY)

class AgentRequest(BaseModel):
    task: str
    parameters: Optional[Dict[str, Any]] = None
    use_fallback: bool = False

class AgentResponse(BaseModel):
    agent: str = "{agent_name}"
    task: str
    response: str
    source: str  # "logic" or "fallback"
    confidence: float

@app.get("/health")
def health():
    return {{
        "status": "healthy",
        "agent": "{agent_name}",
        "display_name": "{display_name}",
        "logic_source": "{logic_source}",
        "fallback_enabled": FALLBACK_ENABLED,
        "capabilities": {agent_config.get('capabilities', [])}
    }}

@app.post("/execute")
def execute(request: AgentRequest):
    """Execute task using logic or OpenAI fallback"""
    try:
        logger.info(f"{{agent_name}} executing task: {{request.task}}")
        
        # Try logic first (unless fallback explicitly requested)
        if not request.use_fallback:
            try:
                result = _execute_logic(request.task, request.parameters)
                return AgentResponse(
                    task=request.task,
                    response=result,
                    source="logic",
                    confidence=0.9
                )
            except Exception as e:
                logger.warning(f"Logic execution failed: {{str(e)}}")
                if not FALLBACK_ENABLED:
                    raise e
                    
        # Use OpenAI fallback
        if FALLBACK_ENABLED:
            result = _execute_fallback(request.task, request.parameters)
            return AgentResponse(
                task=request.task,
                response=result,
                source="fallback",
                confidence=0.7
            )
        else:
            raise HTTPException(status_code=500, detail="Logic failed and fallback disabled")
            
    except Exception as e:
        logger.error(f"{{agent_name}} execution failed: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {{str(e)}}")

@app.post("/enhance")
def enhance(enhancement_data: Dict[str, Any]):
    """Enhance agent capabilities"""
    try:
        logger.info(f"{{agent_name}} enhancement requested")
        
        # Logic for agent enhancement
        enhancement_result = {{
            "agent": "{agent_name}",
            "enhancement": "capabilities_updated",
            "timestamp": "{{datetime.now().isoformat()}}"
        }}
        
        return enhancement_result
        
    except Exception as e:
        logger.error(f"{{agent_name}} enhancement failed: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {{str(e)}}")

def _execute_logic(task: str, parameters: Optional[Dict[str, Any]]) -> str:
    """Execute task using imported logic modules"""
    # This would be customized based on the specific logic source
    # For now, return a generic response
    return f"{{agent_name}} logic executed: {{task}}"

def _execute_fallback(task: str, parameters: Optional[Dict[str, Any]]) -> str:
    """Execute task using OpenAI fallback"""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Create system prompt based on agent capabilities
        system_prompt = f"""You are {{display_name}}, {description}.
Your capabilities include: {{', '.join(agent_config.get('capabilities', []))}}

Provide a helpful response for the user's request."""
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {{"role": "system", "content": system_prompt}},
                {{"role": "user", "content": f"Task: {{task}}\\nParameters: {{parameters or {{}}}"}}
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"OpenAI fallback failed: {{str(e)}}")
        return f"Fallback execution failed: {{str(e)}}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port={port})
'''
        
        with open(package_path / "main.py", 'w') as f:
            f.write(main_content)

    def _generate_imports(self, agent_config: Dict[str, Any]) -> str:
        """Generate import statements for logic modules"""
        imports = []
        for module in agent_config.get('logic_modules', []):
            if module.endswith('.py'):
                module_name = module.replace('.py', '').replace('/', '.')
                imports.append(f"# import {module_name}")
            else:
                imports.append(f"# import {module}")
        return '\n'.join(imports)

    def _create_agent_dockerfile(self, package_path: Path, agent_config: Dict[str, Any]):
        """Create Dockerfile for agent"""
        dockerfile_content = f'''FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \\
    apt-get install -y --no-install-recommends \\
    gcc \\
    && apt-get clean \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \\
    chown -R app:app /app
USER app

EXPOSE {agent_config['port']}

CMD ["python", "main.py"]
'''
        
        with open(package_path / "Dockerfile", 'w') as f:
            f.write(dockerfile_content)

    def _create_agent_requirements(self, package_path: Path, logic_source: str):
        """Create requirements.txt for agent"""
        # Start with base requirements
        requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "openai==1.3.0",
            "requests==2.31.0"
        ]
        
        # Add logic-specific requirements if they exist
        logic_req_file = self.base_path / "services" / logic_source / "requirements.txt"
        if logic_req_file.exists():
            with open(logic_req_file, 'r') as f:
                logic_reqs = f.read().strip().split('\n')
                requirements.extend(logic_reqs)
        
        # Remove duplicates and write
        unique_reqs = list(dict.fromkeys(requirements))
        with open(package_path / "requirements.txt", 'w') as f:
            f.write('\n'.join(unique_reqs))

    def _inject_openai_fallback(self, logic_source: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Inject OpenAI fallback capabilities into agent"""
        try:
            # This is handled in the main.py generation
            logger.info(f"Injected OpenAI fallback for {agent_config['agent_name']}")
            return {'success': True}
        except Exception as e:
            logger.error(f"Failed to inject OpenAI fallback: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _build_agent_container(self, logic_source: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build Docker container for agent"""
        try:
            agent_name = agent_config['agent_name']
            package_path = self.base_path / "agents" / agent_name
            
            # Build Docker image
            image, logs = self.docker_client.images.build(
                path=str(package_path),
                tag=f"linkops-{agent_name}:latest",
                rm=True
            )
            
            logger.info(f"Built Docker image: {image.tags[0]}")
            return {'success': True, 'image_id': image.id, 'tags': image.tags}
            
        except Exception as e:
            logger.error(f"Failed to build agent container: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _deploy_agent(self, logic_source: str, agent_config: Dict[str, Any], deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy agent using deployment configuration"""
        try:
            agent_name = agent_config['agent_name']
            
            # For now, return deployment manifest
            # In production, this would apply to Kubernetes
            deployment_manifest = self.registry._create_deployment_manifest(
                logic_source, agent_config, deployment_config
            )
            
            logger.info(f"Deployed agent: {agent_name}")
            return {
                'success': True,
                'agent_name': agent_name,
                'deployment_manifest': deployment_manifest
            }
            
        except Exception as e:
            logger.error(f"Failed to deploy agent: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _get_default_deployment_config(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get default deployment configuration"""
        return {
            'replicas': 1,
            'resources': {
                'requests': {'cpu': '200m', 'memory': '256Mi'},
                'limits': {'cpu': '500m', 'memory': '512Mi'}
            },
            'environment': {
                'LOGIC_SOURCE': agent_config.get('logic_source', ''),
                'AGENT_NAME': agent_config['agent_name'],
                'FALLBACK_PROVIDER': agent_config.get('fallback_provider', 'openai')
            }
        }

    def list_launched_agents(self) -> List[Dict[str, Any]]:
        """List all launched agents"""
        return self.registry.list_deployed_agents()

    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        try:
            # Check if agent container is running
            containers = self.docker_client.containers.list(
                filters={'label': f'app={agent_name}'}
            )
            
            if containers:
                container = containers[0]
                return {
                    'agent_name': agent_name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else container.image.id,
                    'ports': container.ports,
                    'created': container.attrs['Created']
                }
            else:
                return {
                    'agent_name': agent_name,
                    'status': 'not_running',
                    'message': 'Agent container not found'
                }
                
        except Exception as e:
            return {
                'agent_name': agent_name,
                'status': 'error',
                'error': str(e)
            } 