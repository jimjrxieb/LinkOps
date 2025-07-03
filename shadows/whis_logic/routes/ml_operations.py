"""
ML Operations Routes - AI/ML Workflow Endpoints
Handles data science workflows, model training, and deployment operations
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging

# Import the AI/ML workflows and systems
from mlops_engine import mlops_engine
from orbs_runes_system import orbs_runes_system
from ai_ml_workflows import ai_ml_workflows

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ml", tags=["ML Operations"])


class DataWorkflowRequest(BaseModel):
    data_sources: List[Dict[str, Any]]
    requirements: Dict[str, Any]
    quality_config: Optional[Dict[str, Any]] = None


class ModelWorkflowRequest(BaseModel):
    task_type: str
    data_config: Dict[str, Any]
    model_config: Dict[str, Any]
    evaluation_config: Optional[Dict[str, Any]] = None


class DeploymentWorkflowRequest(BaseModel):
    model_id: str
    deployment_config: Dict[str, Any]
    monitoring_config: Optional[Dict[str, Any]] = None


class ExperimentTrackingRequest(BaseModel):
    experiment_config: Dict[str, Any]
    metrics: Optional[Dict[str, Any]] = None


class FeatureStoreRequest(BaseModel):
    data_sources: List[Dict[str, Any]]
    requirements: Dict[str, Any]
    feature_definitions: Optional[List[Dict[str, Any]]] = None


class DataQualityRequest(BaseModel):
    data: Dict[str, Any]
    quality_config: Dict[str, Any]


class RuneExecutionRequest(BaseModel):
    task_description: str
    context: Dict[str, Any]
    use_openai_fallback: bool = True


class WorkflowExecutionRequest(BaseModel):
    workflow: Dict[str, Any]
    context: Dict[str, Any]
    execute_async: bool = False


@router.post("/data-workflow/design")
async def design_data_workflow(request: DataWorkflowRequest):
    """Design comprehensive data pipeline for ML workflows"""
    try:
        pipeline_design = mlops_engine.design_data_pipeline(
            data_sources=request.data_sources, requirements=request.requirements
        )

        return {
            "status": "success",
            "pipeline_design": pipeline_design,
            "estimated_cost": pipeline_design.get("estimated_cost", 0.0),
            "recommendations": [
                "Implement data validation at each stage",
                "Set up monitoring for data quality metrics",
                "Consider feature store for reusable features",
            ],
        }
    except Exception as e:
        logger.error(f"Error designing data workflow: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to design data workflow: {str(e)}"
        )


@router.post("/model-workflow/create")
async def create_model_workflow(request: ModelWorkflowRequest):
    """Create end-to-end ML pipeline"""
    try:
        pipeline = mlops_engine.create_ml_pipeline(
            task_type=request.task_type,
            data_config=request.data_config,
            model_config=request.model_config,
        )

        return {
            "status": "success",
            "pipeline": pipeline,
            "pipeline_id": pipeline["pipeline_id"],
            "stages_count": len(pipeline["stages"]),
            "estimated_duration": "2-4 hours",
        }
    except Exception as e:
        logger.error(f"Error creating model workflow: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create model workflow: {str(e)}"
        )


@router.post("/model/train")
async def train_model(request: ModelWorkflowRequest):
    """Execute model training with comprehensive tracking"""
    try:
        # Create pipeline first
        pipeline = mlops_engine.create_ml_pipeline(
            task_type=request.task_type,
            data_config=request.data_config,
            model_config=request.model_config,
        )

        # Execute training
        training_data = {
            "train_data": request.data_config.get("train_data", {}),
            "validation_data": request.data_config.get("validation_data", {}),
            "test_data": request.data_config.get("test_data", {}),
        }

        training_result = mlops_engine.train_model(pipeline, training_data)

        return {
            "status": "success",
            "training_result": training_result,
            "model_id": training_result["model_id"],
            "metrics": training_result["metrics"],
            "recommendations": training_result["recommendations"],
        }
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to train model: {str(e)}")


@router.post("/model/evaluate")
async def evaluate_model(request: ModelWorkflowRequest):
    """Comprehensive model evaluation with bias detection"""
    try:
        model_id = request.model_config.get("model_id")
        if not model_id:
            raise ValueError("model_id is required for evaluation")

        test_data = request.data_config.get("test_data", {})
        evaluation_config = request.evaluation_config or {}

        evaluation_result = mlops_engine.evaluate_model(
            model_id=model_id, test_data=test_data, evaluation_config=evaluation_config
        )

        return {
            "status": "success",
            "evaluation_result": evaluation_result,
            "model_id": model_id,
            "metrics": evaluation_result["evaluation_metrics"],
            "bias_analysis": evaluation_result["bias_analysis"],
            "recommendations": evaluation_result["recommendations"],
        }
    except Exception as e:
        logger.error(f"Error evaluating model: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to evaluate model: {str(e)}"
        )


@router.post("/model/deploy")
async def deploy_model(request: DeploymentWorkflowRequest):
    """Deploy model to production with monitoring"""
    try:
        deployment_result = mlops_engine.deploy_model(
            model_id=request.model_id, deployment_config=request.deployment_config
        )

        return {
            "status": "success",
            "deployment_result": deployment_result,
            "deployment_id": deployment_result["deployment_id"],
            "endpoint_url": deployment_result["endpoint_url"],
            "monitoring_config": deployment_result["monitoring_config"],
        }
    except Exception as e:
        logger.error(f"Error deploying model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to deploy model: {str(e)}")


@router.post("/experiment/track")
async def track_experiment(request: ExperimentTrackingRequest):
    """Track ML experiments with comprehensive logging"""
    try:
        experiment_tracking = mlops_engine.track_experiment(request.experiment_config)

        return {
            "status": "success",
            "experiment_tracking": experiment_tracking,
            "experiment_id": experiment_tracking["experiment_id"],
            "tracking_config": experiment_tracking["tracking_config"],
        }
    except Exception as e:
        logger.error(f"Error tracking experiment: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to track experiment: {str(e)}"
        )


@router.post("/feature-store/design")
async def design_feature_store(request: FeatureStoreRequest):
    """Design feature store with best practices"""
    try:
        feature_store = mlops_engine.design_feature_store(
            data_sources=request.data_sources, requirements=request.requirements
        )

        return {
            "status": "success",
            "feature_store": feature_store,
            "architecture": feature_store["architecture"],
            "feature_count": len(feature_store["feature_definitions"]),
        }
    except Exception as e:
        logger.error(f"Error designing feature store: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to design feature store: {str(e)}"
        )


@router.post("/data-quality/analyze")
async def analyze_data_quality(request: DataQualityRequest):
    """Detect data quality issues and provide remediation"""
    try:
        # Convert data to DataFrame (simplified)
        data_df = pd.DataFrame(request.data.get("data", []))

        quality_analysis = mlops_engine.detect_data_quality_issues(
            data=data_df, quality_config=request.quality_config
        )

        return {
            "status": "success",
            "quality_analysis": quality_analysis,
            "quality_score": quality_analysis["quality_score"],
            "recommendations": quality_analysis["recommendations"],
        }
    except Exception as e:
        logger.error(f"Error analyzing data quality: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze data quality: {str(e)}"
        )


@router.post("/rune/execute")
async def execute_rune(request: RuneExecutionRequest):
    """Execute a Rune for ML task"""
    try:
        # Find matching Rune
        matching_rune = orbs_runes_system.find_matching_rune(
            task_description=request.task_description, context=request.context
        )

        if not matching_rune:
            return {
                "status": "no_match",
                "message": "No matching Rune found",
                "openai_fallback_used": request.use_openai_fallback,
            }

        # Execute the Rune
        execution_result = matching_rune.execute(request.context)

        return {
            "status": "success",
            "rune_name": matching_rune.name,
            "execution_result": execution_result,
            "rune_metadata": matching_rune.metadata,
        }
    except Exception as e:
        logger.error(f"Error executing Rune: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to execute Rune: {str(e)}")


@router.post("/workflow/execute")
async def execute_workflow(
    request: WorkflowExecutionRequest, background_tasks: BackgroundTasks
):
    """Execute a complete AI/ML workflow"""
    try:
        if request.execute_async:
            # Execute in background
            background_tasks.add_task(
                ai_ml_workflows.execute_workflow,
                workflow=request.workflow,
                context=request.context,
            )

            return {
                "status": "started",
                "message": "Workflow execution started in background",
                "workflow_id": request.workflow.get("workflow_id"),
            }
        else:
            # Execute synchronously
            execution_result = ai_ml_workflows.execute_workflow(
                workflow=request.workflow, context=request.context
            )

            return {
                "status": "completed",
                "execution_result": execution_result,
                "workflow_id": execution_result["workflow_id"],
                "overall_metrics": execution_result["overall_metrics"],
            }
    except Exception as e:
        logger.error(f"Error executing workflow: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to execute workflow: {str(e)}"
        )


@router.post("/workflow/data/create")
async def create_data_workflow(request: DataWorkflowRequest):
    """Create comprehensive data workflow"""
    try:
        workflow = ai_ml_workflows.create_data_workflow(request.requirements)

        return {
            "status": "success",
            "workflow": workflow,
            "workflow_id": workflow["workflow_id"],
            "stages_count": len(workflow["stages"]),
        }
    except Exception as e:
        logger.error(f"Error creating data workflow: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create data workflow: {str(e)}"
        )


@router.post("/workflow/model/create")
async def create_model_workflow_route(request: ModelWorkflowRequest):
    """Create comprehensive model training workflow"""
    try:
        workflow = ai_ml_workflows.create_model_workflow(request.model_config)

        return {
            "status": "success",
            "workflow": workflow,
            "workflow_id": workflow["workflow_id"],
            "model_type": workflow["model_type"],
            "stages_count": len(workflow["stages"]),
        }
    except Exception as e:
        logger.error(f"Error creating model workflow: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create model workflow: {str(e)}"
        )


@router.post("/workflow/deployment/create")
async def create_deployment_workflow(request: DeploymentWorkflowRequest):
    """Create model deployment workflow"""
    try:
        workflow = ai_ml_workflows.create_deployment_workflow(request.deployment_config)

        return {
            "status": "success",
            "workflow": workflow,
            "workflow_id": workflow["workflow_id"],
            "platform": workflow["platform"],
            "stages_count": len(workflow["stages"]),
        }
    except Exception as e:
        logger.error(f"Error creating deployment workflow: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create deployment workflow: {str(e)}"
        )


@router.get("/orbs/search")
async def search_orbs(query: str):
    """Search Orbs by query"""
    try:
        results = orbs_runes_system.search_orbs(query)

        return {
            "status": "success",
            "query": query,
            "results": results,
            "total_results": len(results),
        }
    except Exception as e:
        logger.error(f"Error searching Orbs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search Orbs: {str(e)}")


@router.get("/orbs/{orb_name}/knowledge")
async def get_orb_knowledge(orb_name: str):
    """Get comprehensive knowledge from an Orb"""
    try:
        knowledge = orbs_runes_system.get_orb_knowledge(orb_name)

        return {"status": "success", "orb_name": orb_name, "knowledge": knowledge}
    except Exception as e:
        logger.error(f"Error getting Orb knowledge: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get Orb knowledge: {str(e)}"
        )


@router.post("/learning/feedback")
async def provide_feedback(
    rune_name: str, feedback_score: float, feedback_details: Dict[str, Any]
):
    """Provide feedback on a Rune execution"""
    try:
        orbs_runes_system.learn_from_feedback(
            rune_name, feedback_score, feedback_details
        )

        return {
            "status": "success",
            "message": "Feedback recorded successfully",
            "rune_name": rune_name,
            "feedback_score": feedback_score,
        }
    except Exception as e:
        logger.error(f"Error recording feedback: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to record feedback: {str(e)}"
        )


@router.post("/learning/test-failures")
async def learn_from_test_failures(test_results: List[Dict[str, Any]]):
    """Learn from test failures to improve Runes"""
    try:
        orbs_runes_system.learn_from_test_failures(test_results)

        return {
            "status": "success",
            "message": "Learning from test failures completed",
            "test_results_count": len(test_results),
        }
    except Exception as e:
        logger.error(f"Error learning from test failures: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to learn from test failures: {str(e)}"
        )


@router.post("/learning/solution-to-rune")
async def convert_solution_to_rune(solution_path: List[Dict[str, Any]], task_type: str):
    """Convert a sample solution path into an executable Rune"""
    try:
        rune = orbs_runes_system.convert_solution_to_rune(solution_path, task_type)

        return {
            "status": "success",
            "rune": rune.to_dict(),
            "rune_name": rune.name,
            "task_type": task_type,
        }
    except Exception as e:
        logger.error(f"Error converting solution to Rune: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to convert solution to Rune: {str(e)}"
        )


@router.get("/learning/insights")
async def get_learning_insights():
    """Get insights from learning history"""
    try:
        insights = orbs_runes_system.get_learning_insights()

        return {"status": "success", "insights": insights}
    except Exception as e:
        logger.error(f"Error getting learning insights: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get learning insights: {str(e)}"
        )


@router.post("/workflow/performance/analyze")
async def analyze_workflow_performance(workflow_results: List[Dict[str, Any]]):
    """Analyze workflow performance across multiple executions"""
    try:
        analysis = ai_ml_workflows.analyze_workflow_performance(workflow_results)

        return {
            "status": "success",
            "analysis": analysis,
            "workflow_results_count": len(workflow_results),
        }
    except Exception as e:
        logger.error(f"Error analyzing workflow performance: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze workflow performance: {str(e)}"
        )


@router.get("/ml-domains")
async def get_ml_domains():
    """Get available ML domains and capabilities"""
    try:
        domains = mlops_engine.ml_domains

        return {
            "status": "success",
            "ml_domains": domains,
            "total_domains": len(domains),
        }
    except Exception as e:
        logger.error(f"Error getting ML domains: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get ML domains: {str(e)}"
        )


@router.get("/workflow-types")
async def get_workflow_types():
    """Get available workflow types"""
    try:
        workflow_types = ai_ml_workflows.workflow_types

        return {
            "status": "success",
            "workflow_types": workflow_types,
            "total_types": len(workflow_types),
        }
    except Exception as e:
        logger.error(f"Error getting workflow types: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get workflow types: {str(e)}"
        )
