"""
Enhanced Whis Logic Tests - AI/ML Capabilities
Tests for comprehensive ML operations, Orbs/Runes system, and workflows
"""

from ai_ml_workflows import ai_ml_workflows
from orbs_runes_system import orbs_runes_system
from mlops_engine import mlops_engine
import numpy as np
import pandas as pd
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Import the enhanced modules


class TestMLOpsEngine:
    """Test MLOps Engine capabilities"""

    def test_design_data_pipeline(self):
        """Test data pipeline design"""
        data_sources = [
            {
                "type": "database",
                "connection_string": "postgresql://",
                "query": "SELECT * FROM data",
            },
            {"type": "api", "endpoint": "https://api.example.com/data"},
        ]
        requirements = {"data_volume": "large", "real_time": False}

        pipeline = mlops_engine.design_data_pipeline(data_sources, requirements)

        assert "ingestion_layers" in pipeline
        assert "processing_stages" in pipeline
        assert "feature_store" in pipeline
        assert len(pipeline["ingestion_layers"]) == 2

    def test_create_ml_pipeline(self):
        """Test ML pipeline creation"""
        data_config = {"train_data": {}, "test_data": {}}
        model_config = {"model_type": "supervised", "algorithm": "random_forest"}

        pipeline = mlops_engine.create_ml_pipeline(
            "supervised_learning", data_config, model_config
        )

        assert "pipeline_id" in pipeline
        assert "stages" in pipeline
        assert "experiment_tracking" in pipeline
        assert len(pipeline["stages"]) > 0

    def test_train_model(self):
        """Test model training"""
        pipeline_config = {
            "stages": [
                {"stage": "data_preprocessing", "operations": []},
                {"stage": "model_training", "operations": []},
            ]
        }
        training_data = {"train_data": {}, "test_data": {}}

        result = mlops_engine.train_model(pipeline_config, training_data)

        assert "model_id" in result
        assert "training_status" in result
        assert "metrics" in result
        assert "recommendations" in result

    def test_evaluate_model(self):
        """Test model evaluation"""
        test_data = {"features": [], "targets": []}
        evaluation_config = {"metrics": ["accuracy", "precision"]}

        result = mlops_engine.evaluate_model("test_model", test_data, evaluation_config)

        assert "model_id" in result
        assert "evaluation_metrics" in result
        assert "bias_analysis" in result
        assert "recommendations" in result

    def test_deploy_model(self):
        """Test model deployment"""
        deployment_config = {"platform": "aks", "replicas": 3}

        result = mlops_engine.deploy_model("test_model", deployment_config)

        assert "deployment_id" in result
        assert "deployment_status" in result
        assert "monitoring_config" in result

    def test_track_experiment(self):
        """Test experiment tracking"""
        experiment_config = {
            "name": "test_experiment",
            "tracking_uri": "http://mlflow:5000",
        }

        result = mlops_engine.track_experiment(experiment_config)

        assert "experiment_id" in result
        assert "tracking_config" in result
        assert "metrics_logging" in result

    def test_design_feature_store(self):
        """Test feature store design"""
        data_sources = [{"type": "database", "name": "user_data"}]
        requirements = {"real_time": True, "offline": True}

        result = mlops_engine.design_feature_store(data_sources, requirements)

        assert "architecture" in result
        assert "feature_definitions" in result
        assert "ingestion_pipelines" in result

    def test_detect_data_quality_issues(self):
        """Test data quality detection"""
        # Create sample data
        data = pd.DataFrame(
            {
                "col1": [1, 2, np.nan, 4, 5],
                "col2": [1, 1, 2, 2, 2],
                "col3": [1, 2, 3, 4, 5],
            }
        )
        quality_config = {"outlier_method": "iqr"}

        result = mlops_engine.detect_data_quality_issues(data, quality_config)

        assert "data_shape" in result
        assert "missing_values" in result
        assert "quality_score" in result
        assert "recommendations" in result


class TestOrbsRunesSystem:
    """Test Orbs and Runes system"""

    def test_create_orb(self):
        """Test Orb creation"""
        orb = orbs_runes_system.create_orb(
            name="test_orb", description="Test orb for testing", domain="testing"
        )

        assert orb.name == "test_orb"
        assert orb.description == "Test orb for testing"
        assert orb.domain == "testing"
        assert "test_orb" in orbs_runes_system.orbs

    def test_create_rune(self):
        """Test Rune creation"""
        rune = orbs_runes_system.create_rune(
            name="test_rune",
            pattern="test_pattern",
            code="def test(): pass",
            metadata={"type": "test"},
        )

        assert rune.name == "test_rune"
        assert rune.pattern == "test_pattern"
        assert rune.code == "def test(): pass"
        assert "test_rune" in orbs_runes_system.runes

    def test_add_rune_to_orb(self):
        """Test adding Rune to Orb"""
        orb = orbs_runes_system.create_orb("test_orb", "Test orb", "testing")
        orbs_runes_system.create_rune("test_rune", "pattern", "code", {})

        orbs_runes_system.add_rune_to_orb("test_orb", "test_rune")

        assert len(orb.runes) == 1
        assert orb.runes[0].name == "test_rune"

    def test_find_matching_rune(self):
        """Test finding matching Rune"""
        rune = orbs_runes_system.create_rune(
            "ml_training",
            "train_model",
            "def train(): pass",
            {"task_type": "classification"},
        )

        matching_rune = orbs_runes_system.find_matching_rune(
            "I need to train a classification model", {"task_type": "classification"}
        )

        assert matching_rune is not None
        assert matching_rune.name == "ml_training"

    def test_learn_from_task(self):
        """Test learning from task"""
        solution_path = [
            {"operation": "load_data", "status": "success"},
            {"operation": "train_model", "status": "success"},
        ]

        orbs_runes_system.learn_from_task(
            task_description="Train ML model",
            solution_path=solution_path,
            success=True,
            feedback={"accuracy": 0.95},
        )

        assert len(orbs_runes_system.learning_history) > 0
        assert orbs_runes_system.learning_history[-1]["success"] is True

    def test_learn_from_feedback(self):
        """Test learning from feedback"""
        rune = orbs_runes_system.create_rune("test_rune", "pattern", "code", {})

        orbs_runes_system.learn_from_feedback(
            rune_name="test_rune",
            feedback_score=0.8,
            feedback_details={"accuracy": 0.8},
        )

        assert rune.feedback_score > 0
        assert "test_rune" in orbs_runes_system.feedback_system

    def test_learn_from_test_failures(self):
        """Test learning from test failures"""
        test_results = [
            {
                "test_name": "test_model_accuracy",
                "passed": False,
                "error": "AssertionError: Expected accuracy >= 0.9, got 0.85",
            }
        ]

        orbs_runes_system.learn_from_test_failures(test_results)

        # Check if recovery Rune was created
        recovery_runes = [
            r for r in orbs_runes_system.runes.values() if "recovery" in r.name
        ]
        assert len(recovery_runes) > 0

    def test_convert_solution_to_rune(self):
        """Test converting solution to Rune"""
        solution_path = [
            {"operation": "load_data", "parameters": {"file": "data.csv"}},
            {"operation": "preprocess", "parameters": {"normalize": True}},
            {"operation": "train", "parameters": {"algorithm": "random_forest"}},
        ]

        rune = orbs_runes_system.convert_solution_to_rune(
            solution_path, "classification"
        )

        assert rune.name.startswith("classification_solution")
        assert "load_data" in rune.pattern
        assert rune.metadata["task_type"] == "classification"

    def test_get_orb_knowledge(self):
        """Test getting Orb knowledge"""
        orbs_runes_system.create_orb("ml_orb", "ML knowledge", "machine_learning")
        orbs_runes_system.create_rune("ml_rune", "pattern", "code", {})
        orbs_runes_system.add_rune_to_orb("ml_orb", "ml_rune")

        knowledge = orbs_runes_system.get_orb_knowledge("ml_orb")

        assert "orb" in knowledge
        assert knowledge["total_runes"] == 1
        assert knowledge["orb"]["name"] == "ml_orb"

    def test_search_orbs(self):
        """Test searching Orbs"""
        orbs_runes_system.create_orb("ml_orb", "Machine learning knowledge", "ml")

        results = orbs_runes_system.search_orbs("machine learning")

        assert len(results) > 0
        assert results[0]["orb_name"] == "ml_orb"

    def test_get_learning_insights(self):
        """Test getting learning insights"""
        # Add some learning history
        orbs_runes_system.learn_from_task(
            "Test task", [{"operation": "test"}], True, {"accuracy": 0.9}
        )

        insights = orbs_runes_system.get_learning_insights()

        assert "total_tasks" in insights
        assert "success_rate" in insights
        assert insights["total_tasks"] > 0


class TestAIMLWorkflows:
    """Test AI/ML Workflows"""

    def test_create_data_workflow(self):
        """Test data workflow creation"""
        data_config = {
            "data_sources": [{"type": "database", "name": "user_data"}],
            "quality_thresholds": {"completeness": 0.95},
        }

        workflow = ai_ml_workflows.create_data_workflow(data_config)

        assert "workflow_id" in workflow
        assert "type" in workflow
        assert workflow["type"] == "data_workflow"
        assert len(workflow["stages"]) > 0

    def test_create_model_workflow(self):
        """Test model workflow creation"""
        model_config = {
            "model_type": "supervised",
            "task_type": "classification",
            "algorithm": "random_forest",
        }

        workflow = ai_ml_workflows.create_model_workflow(model_config)

        assert "workflow_id" in workflow
        assert "model_type" in workflow
        assert workflow["model_type"] == "supervised"
        assert len(workflow["stages"]) > 0

    def test_create_deployment_workflow(self):
        """Test deployment workflow creation"""
        deployment_config = {
            "platform": "aks",
            "replicas": 3,
            "resources": {"cpu": "1", "memory": "2Gi"},
        }

        workflow = ai_ml_workflows.create_deployment_workflow(deployment_config)

        assert "workflow_id" in workflow
        assert "workflow_id" in workflow
        assert "platform" in workflow
        assert workflow["platform"] == "aks"
        assert len(workflow["stages"]) > 0

    def test_execute_workflow(self):
        """Test workflow execution"""
        workflow = {
            "workflow_id": "test_workflow",
            "stages": [
                {
                    "stage": "test_stage",
                    "operations": [{"operation": "test_op", "config": {}}],
                }
            ],
        }
        context = {"test": "data"}

        result = ai_ml_workflows.execute_workflow(workflow, context)

        assert "workflow_id" in result
        assert "execution_status" in result
        assert "stages_results" in result
        assert len(result["stages_results"]) > 0

    def test_analyze_workflow_performance(self):
        """Test workflow performance analysis"""
        workflow_results = [
            {
                "execution_status": "completed",
                "stages_results": [{"status": "completed"}],
                "overall_metrics": {"total_execution_time": 100},
            },
            {
                "execution_status": "failed",
                "stages_results": [{"status": "failed"}],
                "overall_metrics": {"total_execution_time": 50},
            },
        ]

        analysis = ai_ml_workflows.analyze_workflow_performance(workflow_results)

        assert "total_executions" in analysis
        assert "success_rate" in analysis
        assert analysis["total_executions"] == 2
        assert analysis["success_rate"] == 0.5

    def test_workflow_types(self):
        """Test workflow types availability"""
        workflow_types = ai_ml_workflows.workflow_types

        assert "supervised_learning" in workflow_types
        assert "unsupervised_learning" in workflow_types
        assert "deep_learning" in workflow_types
        assert "reinforcement_learning" in workflow_types


class TestMLOperationsIntegration:
    """Test integration between ML components"""

    def test_end_to_end_ml_workflow(self):
        """Test end-to-end ML workflow integration"""
        # Create data workflow
        data_config = {"data_sources": [{"type": "database"}]}
        data_workflow = ai_ml_workflows.create_data_workflow(data_config)

        # Create model workflow
        model_config = {"model_type": "supervised", "algorithm": "random_forest"}
        model_workflow = ai_ml_workflows.create_model_workflow(model_config)

        # Create deployment workflow
        deployment_config = {"platform": "aks"}
        deployment_workflow = ai_ml_workflows.create_deployment_workflow(
            deployment_config
        )

        # Verify all workflows are created
        assert data_workflow["type"] == "data_workflow"
        assert model_workflow["model_type"] == "supervised"
        assert deployment_workflow["platform"] == "aks"

    def test_orbs_runes_ml_integration(self):
        """Test Orbs/Runes integration with ML operations"""
        # Create ML Orb
        ml_orb = orbs_runes_system.create_orb(
            "ml_operations", "ML operations", "machine_learning"
        )

        # Create ML Rune
        ml_rune = orbs_runes_system.create_rune(
            "train_classifier",
            "train_supervised_model",
            "def train_classifier(data): return model",
            {"task_type": "classification", "algorithm": "random_forest"},
        )

        # Add Rune to Orb
        orbs_runes_system.add_rune_to_orb("ml_operations", "train_classifier")

        # Find matching Rune for ML task
        matching_rune = orbs_runes_system.find_matching_rune(
            "I need to train a classification model", {"task_type": "classification"}
        )

        assert matching_rune is not None
        assert matching_rune.name == "train_classifier"

    def test_mlops_engine_integration(self):
        """Test MLOps engine integration with workflows"""
        # Design data pipeline
        data_sources = [{"type": "database"}]
        requirements = {"real_time": False}
        pipeline = mlops_engine.design_data_pipeline(data_sources, requirements)

        # Create workflow from pipeline
        workflow = ai_ml_workflows.create_data_workflow(requirements)

        # Verify integration
        assert "ingestion_layers" in pipeline
        assert "stages" in workflow
        assert workflow["type"] == "data_workflow"


if __name__ == "__main__":
    pytest.main([__file__])
