"""
Tests for Katie Kubernetes AI Agent
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from kubeops.describe import k8s_describer
from kubeops.scale import k8s_scaler
from kubeops.logs import k8s_log_analyzer
from kubeops.patch import k8s_patcher

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        """Test health endpoint returns correct service info"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "katie"
        assert "Kubernetes AI Agent" in data["role"]
        assert len(data["capabilities"]) > 0
        assert "CKA" in data["certifications"]


class TestExecuteEndpoint:
    def test_execute_describe_pod(self):
        """Test executing a pod describe task"""
        task_data = {
            "task_id": "test-001",
            "task_type": "describe",
            "resource_type": "pod",
            "resource_name": "test-pod",
            "namespace": "default",
        }

        with patch.object(k8s_describer, "describe_pod") as mock_describe:
            mock_describe.return_value = {
                "agent": "katie",
                "operation": "describe_pod",
                "pod_name": "test-pod",
                "status": "success",
            }

            response = client.post("/execute", json=task_data)
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert "describe" in data["task"]
            assert data["operation_result"]["status"] == "success"

    def test_execute_scale_deployment(self):
        """Test executing a deployment scale task"""
        task_data = {
            "task_id": "test-002",
            "task_type": "scale",
            "resource_type": "deployment",
            "resource_name": "test-deployment",
            "namespace": "default",
            "parameters": {"replicas": 3},
        }

        with patch.object(k8s_scaler, "scale_deployment") as mock_scale:
            mock_scale.return_value = {
                "agent": "katie",
                "operation": "scale_deployment",
                "status": "success",
                "new_replicas": 3,
            }

            response = client.post("/execute", json=task_data)
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert "scale" in data["task"]

    def test_execute_logs_operation(self):
        """Test executing a logs task"""
        task_data = {
            "task_id": "test-003",
            "task_type": "logs",
            "resource_type": "pod",
            "resource_name": "test-pod",
            "namespace": "default",
            "parameters": {"tail_lines": 50},
        }

        with patch.object(k8s_log_analyzer, "get_pod_logs") as mock_logs:
            mock_logs.return_value = {
                "agent": "katie",
                "operation": "get_pod_logs",
                "log_count": 50,
                "status": "success",
            }

            response = client.post("/execute", json=task_data)
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert "logs" in data["task"]


class TestDescribeEndpoints:
    def test_describe_pod_endpoint(self):
        """Test describe pod endpoint"""
        with patch.object(k8s_describer, "describe_pod") as mock_describe:
            mock_describe.return_value = {
                "agent": "katie",
                "operation": "describe_pod",
                "pod_name": "test-pod",
                "status": "success",
            }

            response = client.get("/describe/pod/default/test-pod")
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["pod_name"] == "test-pod"

    def test_describe_deployment_endpoint(self):
        """Test describe deployment endpoint"""
        with patch.object(k8s_describer, "describe_deployment") as mock_describe:
            mock_describe.return_value = {
                "agent": "katie",
                "operation": "describe_deployment",
                "deployment_name": "test-deployment",
                "status": "success",
            }

            response = client.get("/describe/deployment/default/test-deployment")
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["deployment_name"] == "test-deployment"


class TestScaleEndpoints:
    def test_scale_deployment_endpoint(self):
        """Test scale deployment endpoint"""
        with patch.object(k8s_scaler, "scale_deployment") as mock_scale:
            mock_scale.return_value = {
                "agent": "katie",
                "operation": "scale_deployment",
                "status": "success",
                "new_replicas": 3,
            }

            response = client.post(
                "/scale/deployment/default/test-deployment?replicas=3"
            )
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["new_replicas"] == 3

    def test_scale_deployment_dry_run(self):
        """Test scale deployment with dry run"""
        with patch.object(k8s_scaler, "scale_deployment") as mock_scale:
            mock_scale.return_value = {
                "agent": "katie",
                "operation": "scale_deployment",
                "status": "dry_run",
                "new_replicas": 3,
            }

            response = client.post(
                "/scale/deployment/default/test-deployment?replicas=3&dry_run=true"
            )
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "dry_run"


class TestLogsEndpoints:
    def test_get_pod_logs_endpoint(self):
        """Test get pod logs endpoint"""
        with patch.object(k8s_log_analyzer, "get_pod_logs") as mock_logs:
            mock_logs.return_value = {
                "agent": "katie",
                "operation": "get_pod_logs",
                "log_count": 100,
                "status": "success",
            }

            response = client.get("/logs/pod/default/test-pod?tail_lines=100")
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["log_count"] == 100

    def test_search_logs_endpoint(self):
        """Test search logs endpoint"""
        with patch.object(k8s_log_analyzer, "search_logs") as mock_search:
            mock_search.return_value = {
                "agent": "katie",
                "operation": "search_logs",
                "total_matches": 5,
                "status": "success",
            }

            response = client.post(
                "/logs/search/default?search_pattern=error&max_results=10"
            )
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["total_matches"] == 5


class TestPatchEndpoints:
    def test_patch_deployment_endpoint(self):
        """Test patch deployment endpoint"""
        patch_data = {"spec": {"replicas": 3}}

        with patch.object(k8s_patcher, "patch_deployment") as mock_patch:
            mock_patch.return_value = {
                "agent": "katie",
                "operation": "patch_deployment",
                "patch_applied": True,
                "status": "success",
            }

            response = client.post(
                "/patch/deployment/default/test-deployment", json=patch_data
            )
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["patch_applied"] is True

    def test_patch_deployment_dry_run(self):
        """Test patch deployment with dry run"""
        patch_data = {"spec": {"replicas": 3}}

        with patch.object(k8s_patcher, "patch_deployment") as mock_patch:
            mock_patch.return_value = {
                "agent": "katie",
                "operation": "patch_deployment",
                "status": "dry_run",
            }

            response = client.post(
                "/patch/deployment/default/test-deployment?dry_run=true",
                json=patch_data,
            )
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "dry_run"


class TestApplyEndpoints:
    def test_apply_manifest_endpoint(self):
        """Test apply manifest endpoint"""
        manifest_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
    spec:
      containers:
      - name: test
        image: nginx:latest
"""

        with patch.object(k8s_patcher, "apply_manifest") as mock_apply:
            mock_apply.return_value = {
                "agent": "katie",
                "operation": "apply_manifest",
                "manifest_applied": True,
                "status": "success",
            }

            response = client.post(
                "/apply/manifest", json={"manifest_yaml": manifest_yaml}
            )
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["manifest_applied"] is True


class TestRollbackEndpoints:
    def test_rollback_deployment_endpoint(self):
        """Test rollback deployment endpoint"""
        with patch.object(k8s_patcher, "rollback_deployment") as mock_rollback:
            mock_rollback.return_value = {
                "agent": "katie",
                "operation": "rollback_deployment",
                "rollback_successful": True,
                "status": "success",
            }

            response = client.post("/rollback/deployment/default/test-deployment")
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert data["rollback_successful"] is True


class TestRecommendationsEndpoints:
    def test_get_scaling_recommendations_endpoint(self):
        """Test get scaling recommendations endpoint"""
        with patch.object(
            k8s_scaler, "get_scaling_recommendations"
        ) as mock_recommendations:
            mock_recommendations.return_value = {
                "agent": "katie",
                "operation": "get_scaling_recommendations",
                "recommendations": [
                    {
                        "type": "scale_up",
                        "priority": "medium",
                        "description": "Consider scaling up for better performance",
                    }
                ],
                "status": "success",
            }

            response = client.get("/recommendations/default/test-deployment")
            assert response.status_code == 200

            data = response.json()
            assert data["agent"] == "katie"
            assert len(data["recommendations"]) > 0


class TestCapabilitiesEndpoint:
    def test_get_capabilities(self):
        """Test capabilities endpoint"""
        response = client.get("/capabilities")
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "katie"
        assert "Kubernetes AI Agent" in data["role"]
        assert len(data["current_capabilities"]) > 0
        assert "CKA" in data["certifications"]


class TestK8sDescriber:
    def test_describe_pod_analysis(self):
        """Test pod description analysis"""
        with patch("kubeops.describe.client.CoreV1Api") as mock_api:
            mock_pod = MagicMock()
            mock_pod.status.phase = "Running"
            mock_pod.status.container_statuses = []
            mock_pod.metadata.name = "test-pod"

            mock_api.return_value.read_namespaced_pod.return_value = mock_pod

            result = k8s_describer.describe_pod("default", "test-pod")
            assert result["agent"] == "katie"
            assert result["pod_name"] == "test-pod"

    def test_describe_deployment_analysis(self):
        """Test deployment description analysis"""
        with patch("kubeops.describe.client.AppsV1Api") as mock_api:
            mock_deployment = MagicMock()
            mock_deployment.spec.replicas = 3
            mock_deployment.status.replicas = 3
            mock_deployment.status.ready_replicas = 3
            mock_deployment.metadata.name = "test-deployment"

            mock_api.return_value.read_namespaced_deployment.return_value = (
                mock_deployment
            )

            result = k8s_describer.describe_deployment("default", "test-deployment")
            assert result["agent"] == "katie"
            assert result["deployment_name"] == "test-deployment"


class TestK8sScaler:
    def test_scale_deployment_analysis(self):
        """Test deployment scaling analysis"""
        with patch("kubeops.scale.client.AppsV1Api") as mock_api:
            mock_deployment = MagicMock()
            mock_deployment.spec.replicas = 2

            mock_api.return_value.read_namespaced_deployment.return_value = (
                mock_deployment
            )
            mock_api.return_value.patch_namespaced_deployment.return_value = (
                mock_deployment
            )

            result = k8s_scaler.scale_deployment("default", "test-deployment", 3)
            assert result["agent"] == "katie"
            assert result["new_replicas"] == 3

    def test_scale_deployment_dry_run(self):
        """Test deployment scaling dry run"""
        with patch("kubeops.scale.client.AppsV1Api") as mock_api:
            mock_deployment = MagicMock()
            mock_deployment.spec.replicas = 2

            mock_api.return_value.read_namespaced_deployment.return_value = (
                mock_deployment
            )

            result = k8s_scaler.scale_deployment(
                "default", "test-deployment", 3, dry_run=True
            )
            assert result["agent"] == "katie"
            assert result["status"] == "dry_run"


class TestK8sLogAnalyzer:
    def test_log_analysis(self):
        """Test log analysis functionality"""
        with patch("kubeops.logs.client.CoreV1Api") as mock_api:
            mock_api.return_value.read_namespaced_pod_log.return_value = (
                "INFO: Application started\nERROR: Connection failed"
            )

            result = k8s_log_analyzer.get_pod_logs("default", "test-pod")
            assert result["agent"] == "katie"
            assert result["log_count"] == 2

    def test_error_pattern_analysis(self):
        """Test error pattern analysis"""
        with patch("kubeops.logs.client.CoreV1Api") as mock_api:
            mock_api.return_value.list_namespaced_pod.return_value.items = []

            result = k8s_log_analyzer.analyze_error_patterns(
                "default", pod_name="test-pod"
            )
            assert result["agent"] == "katie"
            assert "error_analysis" in result


class TestK8sPatcher:
    def test_patch_validation(self):
        """Test patch validation"""
        patch_data = {"spec": {"replicas": 3}}

        with patch("kubeops.patch.client.AppsV1Api") as mock_api:
            mock_deployment = MagicMock()
            mock_deployment.spec.replicas = 2

            mock_api.return_value.read_namespaced_deployment.return_value = (
                mock_deployment
            )
            mock_api.return_value.patch_namespaced_deployment.return_value = (
                mock_deployment
            )

            result = k8s_patcher.patch_deployment(
                "default", "test-deployment", patch_data
            )
            assert result["agent"] == "katie"
            assert result["patch_applied"] is True

    def test_manifest_validation(self):
        """Test manifest validation"""
        manifest_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test
spec:
  replicas: 3
"""

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "deployment.apps/test created"

            result = k8s_patcher.apply_manifest(manifest_yaml, "default")
            assert result["agent"] == "katie"
            assert result["manifest_applied"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
