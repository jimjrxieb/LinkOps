"""
FickNury Deploy - Agent Deployment Service
Deploys logic sources as AI agents using the agent registry and launcher
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Import agent deployment components
from agent_registry import AgentRegistry
from agent_launcher import AgentLauncher

app = FastAPI(
    title="FickNury Deploy - Agent Deployment Service",
    description="Deploys logic sources as AI agents with OpenAI fallback",
    version="2.0.0",
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
agent_registry = AgentRegistry()
agent_launcher = AgentLauncher(registry=agent_registry)


class DeployRequest(BaseModel):
    logic_source: str
    deployment_config: Optional[Dict[str, Any]] = None
    force_redeploy: bool = False


class DeployResponse(BaseModel):
    deployment_id: str
    logic_source: str
    agent_name: str
    status: str
    deployment_config: Dict[str, Any]
    deployed_at: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ficknury_deploy",
        "role": "Agent Deployment Service",
        "capabilities": [
            "Logic Source to Agent Deployment",
            "Agent Registry Management",
            "OpenAI Fallback Injection",
            "Container Building & Deployment",
            "Agent Status Monitoring",
        ],
        "version": "2.0.0",
    }


@app.post("/deploy/agent", response_model=DeployResponse)
async def deploy_agent(request: DeployRequest, background_tasks: BackgroundTasks):
    """
    Deploy a logic source as an AI agent
    """
    try:
        logger.info(f"Deploying agent from logic source: {request.logic_source}")

        # Check if agent config exists
        agent_config = agent_registry.get_agent_config(request.logic_source)
        if not agent_config:
            raise HTTPException(
                status_code=404,
                detail=f"No agent configuration found for logic source: "
                f"{request.logic_source}",
            )

        # Check if already deployed (unless force redeploy)
        if not request.force_redeploy:
            deployment_history = agent_registry.get_deployment_history(
                request.logic_source
            )
            if deployment_history and deployment_history.get("status") == "deployed":
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Agent {agent_config['agent_name']} is already deployed. "
                        "Use force_redeploy=true to override."
                    ),
                )

        # Launch shadow agent
        launch_result = agent_launcher.launch_shadow_agent(
            request.logic_source, request.deployment_config
        )

        if not launch_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Agent deployment failed: "
                f"{launch_result.get('error', 'Unknown error')}",
            )

        # Create response
        response = DeployResponse(
            deployment_id=f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            logic_source=request.logic_source,
            agent_name=agent_config["agent_name"],
            status="deployed",
            deployment_config=launch_result.get("deployment_config", {}),
            deployed_at=launch_result.get("launched_at", datetime.now().isoformat()),
        )

        logger.info(
            f"Successfully deployed {agent_config['agent_name']} "
            f"from {request.logic_source}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent deployment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")


@app.get("/deploy/agents")
async def list_deployed_agents():
    """
    List all deployed agents
    """
    try:
        deployed_agents = agent_launcher.list_launched_agents()

        # Add current status for each agent
        for agent in deployed_agents:
            agent_name = agent.get("agent_name")
            if agent_name:
                status = agent_launcher.get_agent_status(agent_name)
                agent["current_status"] = status

        return {
            "deployed_agents": deployed_agents,
            "total_count": len(deployed_agents),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to list deployed agents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")


@app.get("/deploy/agent/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """
    Get status of a specific deployed agent
    """
    try:
        status = agent_launcher.get_agent_status(agent_name)

        # Add deployment history
        logic_source = agent_registry.get_logic_source_by_agent(agent_name)
        if logic_source:
            deployment_history = agent_registry.get_deployment_history(logic_source)
            status["deployment_history"] = deployment_history

        return status

    except Exception as e:
        logger.error(f"Failed to get agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@app.delete("/deploy/agent/{agent_name}")
async def undeploy_agent(agent_name: str):
    """
    Undeploy an agent
    """
    try:
        logger.info(f"Undeploying agent: {agent_name}")

        # Get logic source
        logic_source = agent_registry.get_logic_source_by_agent(agent_name)
        if not logic_source:
            raise HTTPException(
                status_code=404, detail=f"Agent {agent_name} not found in registry"
            )

        # Stop and remove container
        try:
            containers = agent_launcher.docker_client.containers.list(
                filters={"label": f"app={agent_name}"}
            )

            for container in containers:
                container.stop()
                container.remove()
                logger.info(f"Stopped and removed container: {container.id}")

        except Exception as e:
            logger.warning(f"Failed to stop container: {str(e)}")

        # Update deployment record
        agent_registry.update_agent_config(
            logic_source,
            {
                "deployment_status": "undeployed",
                "undeployed_at": datetime.now().isoformat(),
            },
        )

        return {
            "agent_name": agent_name,
            "logic_source": logic_source,
            "status": "undeployed",
            "undeployed_at": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to undeploy agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Undeploy failed: {str(e)}")


@app.get("/registry/agents")
async def list_registered_agents():
    """
    List all registered agents in the registry
    """
    try:
        agents = agent_registry.get_all_agents()

        return {
            "registered_agents": [
                {"logic_source": logic_source, "agent_config": config}
                for logic_source, config in agents.items()
            ],
            "total_count": len(agents),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to list registered agents: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to list registry: {str(e)}"
        )


@app.get("/registry/agent/{logic_source}")
async def get_registered_agent(logic_source: str):
    """
    Get configuration for a specific registered agent
    """
    try:
        config = agent_registry.get_agent_config(logic_source)
        if not config:
            raise HTTPException(
                status_code=404,
                detail=f"No agent configuration found for: {logic_source}",
            )

        # Add deployment history
        deployment_history = agent_registry.get_deployment_history(logic_source)

        return {
            "logic_source": logic_source,
            "agent_config": config,
            "deployment_history": deployment_history,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")


@app.post("/registry/agent/{logic_source}")
async def register_agent(logic_source: str, agent_config: Dict[str, Any]):
    """
    Register a new agent configuration
    """
    try:
        success = agent_registry.register_agent(logic_source, agent_config)

        if success:
            return {
                "status": "success",
                "logic_source": logic_source,
                "message": f"Agent {logic_source} registered successfully",
            }
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to register agent {logic_source}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to register agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.put("/registry/agent/{logic_source}")
async def update_agent_config(logic_source: str, updates: Dict[str, Any]):
    """
    Update agent configuration
    """
    try:
        success = agent_registry.update_agent_config(logic_source, updates)

        if success:
            return {
                "status": "success",
                "logic_source": logic_source,
                "message": f"Agent {logic_source} configuration updated",
            }
        else:
            raise HTTPException(
                status_code=404, detail=f"Agent {logic_source} not found in registry"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update agent config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@app.get("/registry/export")
async def export_registry(format: str = "yaml"):
    """
    Export agent registry
    """
    try:
        if format.lower() not in ["yaml", "json"]:
            raise HTTPException(
                status_code=400, detail="Format must be 'yaml' or 'json'"
            )

        exported = agent_registry.export_registry(format)

        return {
            "format": format,
            "registry_data": exported,
            "exported_at": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export registry: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/capabilities")
def get_capabilities():
    """
    Get FickNury Deploy capabilities
    """
    return {
        "service": "ficknury_deploy",
        "version": "2.0.0",
        "capabilities": {
            "agent_deployment": {
                "logic_to_agent": "Deploy logic sources as AI agents",
                "openai_fallback": "Inject OpenAI fallback capabilities",
                "container_building": "Build Docker containers for agents",
                "kubernetes_deployment": "Deploy to Kubernetes clusters",
            },
            "registry_management": {
                "agent_registration": "Register new agent configurations",
                "config_updates": "Update existing agent configurations",
                "deployment_tracking": "Track deployment history and status",
            },
            "monitoring": {
                "agent_status": "Monitor deployed agent status",
                "health_checks": "Perform health checks on agents",
                "deployment_analytics": "Analyze deployment patterns",
            },
        },
        "supported_logic_sources": list(agent_registry.logic_to_agent.keys()),
        "deployment_methods": ["docker", "kubernetes", "docker_compose"],
    }
