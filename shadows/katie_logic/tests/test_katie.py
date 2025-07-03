"""
Tests for Katie Kubernetes AI Agent
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kubeops.describe import k8s_describer  # noqa: E402
from kubeops.logs import k8s_log_analyzer  # noqa: E402
from kubeops.patch import k8s_patcher  # noqa: E402
from kubeops.scale import k8s_scaler  # noqa: E402
from main import app  # noqa: E402

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

    def test_describe_pod(self):
        """Test pod description endpoint"""
        response = client.get("/describe/pod/default/test-pod")
        assert response.status_code == 200

        data = response.json()
        assert "pod_name" in data
        assert "namespace" in data
        assert "status" in data
        assert "details" in data

    def test_describe_deployment(self):
        """Test deployment description endpoint"""
        response = client.get("/describe/deployment/default/test-deployment")
        assert response.status_code == 200

        data = response.json()
        assert "deployment_name" in data
        assert "namespace" in data
        assert "status" in data
        assert "details" in data

    def test_describe_service(self):
        """Test service description endpoint"""
        response = client.get("/describe/service/default/test-service")
        assert response.status_code == 200

        data = response.json()
        assert "service_name" in data
        assert "namespace" in data
        assert "status" in data
        assert "details" in data

    def test_describe_namespace(self):
        """Test namespace description endpoint"""
        response = client.get("/describe/namespace/default")
        assert response.status_code == 200

        data = response.json()
        assert "namespace" in data
        assert "status" in data
        assert "details" in data

    def test_describe_all_pods(self):
        """Test all pods description endpoint"""
        response = client.get("/describe/pods/default")
        assert response.status_code == 200

        data = response.json()
        assert "namespace" in data
        assert "pod_count" in data
        assert "pods" in data


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

    def test_scale_deployment(self):
        """Test deployment scaling endpoint"""
        response = client.post(
            "/scale/deployment/default/test-deployment?replicas=3&dry_run=false"
        )
        assert response.status_code == 200

        data = response.json()
        assert "deployment_name" in data
        assert "namespace" in data
        assert "new_replicas" in data
        assert "status" in data
        assert "details" in data

    def test_scale_statefulset(self):
        """Test statefulset scaling endpoint"""
        response = client.post(
            "/scale/statefulset/default/test-statefulset?replicas=2&dry_run=false"
        )
        assert response.status_code == 200

        data = response.json()
        assert "statefulset_name" in data
        assert "namespace" in data
        assert "new_replicas" in data
        assert "status" in data

    def test_setup_autoscaling(self):
        """Test autoscaling setup endpoint"""
        response = client.post(
            "/scale/autoscale/default/test-deployment?min_replicas=1&max_replicas=10&target_cpu=80"
        )
        assert response.status_code == 200

        data = response.json()
        assert "deployment_name" in data
        assert "namespace" in data
        assert "min_replicas" in data
        assert "max_replicas" in data
        assert "target_cpu" in data
        assert "status" in data


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

    def test_get_pod_logs(self):
        """Test pod logs endpoint"""
        response = client.get("/logs/pod/default/test-pod?tail_lines=100")
        assert response.status_code == 200

        data = response.json()
        assert "pod_name" in data
        assert "namespace" in data
        assert "log_count" in data
        assert "logs" in data
        assert "details" in data

    def test_get_deployment_logs(self):
        """Test deployment logs endpoint"""
        response = client.get("/logs/deployment/default/test-deployment?tail_lines=50")
        assert response.status_code == 200

        data = response.json()
        assert "deployment_name" in data
        assert "namespace" in data
        assert "log_count" in data
        assert "logs" in data
        assert "details" in data

    def test_search_logs(self):
        """Test log search endpoint"""
        response = client.post(
            "/logs/search/default",
            json={
                "search_pattern": "error",
                "pod_selector": "app=test",
                "max_results": 100,
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert "namespace" in data
        assert "search_pattern" in data
        assert "results_count" in data
        assert "results" in data

    def test_analyze_errors(self):
        """Test error analysis endpoint"""
        response = client.get("/logs/errors/default?pod_name=test-pod&hours_back=24")
        assert response.status_code == 200

        data = response.json()
        assert "namespace" in data
        assert "pod_name" in data
        assert "hours_back" in data
        assert "error_analysis" in data
        assert "details" in data

    def test_get_log_summary(self):
        """Test log summary endpoint"""
        response = client.get(
            "/logs/summary/default?deployment_name=test-deployment&hours_back=1"
        )
        assert response.status_code == 200

        data = response.json()
        assert "namespace" in data
        assert "deployment_name" in data
        assert "hours_back" in data
        assert "summary" in data
        assert "details" in data


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
        patch_data = {"spec": {"replicas": 5}}
        response = client.post(
            "/patch/deployment/default/test-deployment?dry_run=true", json=patch_data
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "dry_run"
        assert data["patch_applied"] is True

    def test_patch_configmap(self):
        """Test configmap patching endpoint"""
        patch_data = {"data": {"key": "value"}}
        response = client.post(
            "/patch/configmap/default/test-configmap?dry_run=false", json=patch_data
        )
        assert response.status_code == 200

        data = response.json()
        assert "configmap_name" in data
        assert "namespace" in data
        assert "patch_applied" in data
        assert "status" in data

    def test_patch_service(self):
        """Test service patching endpoint"""
        patch_data = {"spec": {"type": "ClusterIP"}}
        response = client.post(
            "/patch/service/default/test-service?dry_run=false", json=patch_data
        )
        assert response.status_code == 200

        data = response.json()
        assert "service_name" in data
        assert "namespace" in data
        assert "patch_applied" in data
        assert "status" in data


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

    def test_apply_manifest(self):
        """Test manifest application endpoint"""
        manifest_yaml = """
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
"""
        response = client.post(
            "/apply/manifest?namespace=default&dry_run=false",
            json={"manifest_yaml": manifest_yaml},
        )
        assert response.status_code == 200

        data = response.json()
        assert "namespace" in data
        assert "manifest_applied" in data
        assert "status" in data
        assert "details" in data

    def test_apply_manifest_dry_run(self):
        """Test manifest application with dry run"""
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
      - name: nginx
        image: nginx:latest
"""
        response = client.post(
            "/apply/manifest?namespace=default&dry_run=true",
            json={"manifest_yaml": manifest_yaml},
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "dry_run"
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


class TestCKAEndpoints:
    def test_analyze_cluster_health(self):
        """Test cluster health analysis endpoint"""
        cluster_config = {
            "nodes": [
                {
                    "metadata": {"name": "node-1"},
                    "status": {"conditions": [{"type": "Ready", "status": "True"}]},
                }
            ],
            "pods": [{"metadata": {"name": "pod-1"}, "status": {"phase": "Running"}}],
        }
        response = client.post("/cka/cluster-health", json=cluster_config)
        assert response.status_code == 200

        data = response.json()
        assert "analysis" in data
        assert "status" in data
        assert "overall_status" in data

    def test_troubleshoot_pod_failures(self):
        """Test pod failure troubleshooting endpoint"""
        pod_info = {
            "metadata": {"name": "test-pod", "namespace": "default"},
            "status": {"phase": "Failed", "containerStatuses": []},
        }
        response = client.post("/cka/troubleshoot-pod", json=pod_info)
        assert response.status_code == 200

        data = response.json()
        assert "troubleshooting" in data
        assert "status" in data
        assert "pod_name" in data

    def test_analyze_resource_misconfigurations(self):
        """Test resource misconfiguration analysis endpoint"""
        resources = [
            {
                "kind": "Pod",
                "metadata": {"name": "test-pod"},
                "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]},
            }
        ]
        response = client.post("/cka/resource-misconfigurations", json=resources)
        assert response.status_code == 200

        data = response.json()
        assert "misconfigurations" in data
        assert "status" in data
        assert "total_resources" in data

    def test_recommend_best_practices(self):
        """Test best practices recommendation endpoint"""
        resource_config = {
            "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]}
        }
        response = client.post(
            "/cka/best-practices?resource_type=Pod", json=resource_config
        )
        assert response.status_code == 200

        data = response.json()
        assert "recommendations" in data
        assert "status" in data
        assert "resource_type" in data

    def test_analyze_helm_chart(self):
        """Test Helm chart analysis endpoint"""
        response = client.post("/cka/helm-analysis?chart_path=./test-chart")
        assert response.status_code == 200

        data = response.json()
        assert "chart_analysis" in data
        assert "status" in data
        assert "chart_path" in data

    def test_analyze_argocd_application(self):
        """Test ArgoCD application analysis endpoint"""
        app_manifest = {
            "metadata": {"name": "test-app"},
            "spec": {
                "project": "default",
                "source": {"repoURL": "https://github.com/test/repo"},
            },
        }
        response = client.post("/cka/argocd-analysis", json=app_manifest)
        assert response.status_code == 200

        data = response.json()
        assert "app_analysis" in data
        assert "status" in data
        assert "application_name" in data

    def test_generate_terraform_aks_config(self):
        """Test Terraform AKS configuration generation endpoint"""
        cluster_config = {
            "cluster_name": "test-cluster",
            "resource_group": "test-rg",
            "location": "East US",
            "node_count": 3,
        }
        response = client.post("/cka/terraform-aks", json=cluster_config)
        assert response.status_code == 200

        data = response.json()
        assert "terraform_config" in data
        assert "status" in data
        assert "cluster_name" in data

    def test_explain_yaml_manifest(self):
        """Test YAML manifest explanation endpoint"""
        manifest_yaml = """
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
"""
        response = client.post(
            "/cka/explain-manifest", json={"manifest_yaml": manifest_yaml}
        )
        assert response.status_code == 200

        data = response.json()
        assert "explanation" in data
        assert "status" in data
        assert "manifest_length" in data


class TestCKSEndpoints:
    def test_analyze_security(self):
        """Test security analysis endpoint"""
        cluster_config = {
            "rbac": {"roles": []},
            "network_policies": [],
            "pods": [],
            "secrets": [],
        }
        response = client.post(
            "/cks/security-analysis",
            json={"cluster_config": cluster_config, "compliance_standard": "cis"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "security_analysis" in data
        assert "status" in data
        assert "compliance_standard" in data

    def test_enforce_security_policies(self):
        """Test security policy enforcement endpoint"""
        config = {"network_policies": True, "pod_security": True}
        response = client.post(
            "/cks/enforce-policies?namespace=default&policy_type=network_policy",
            json=config,
        )
        assert response.status_code == 200

        data = response.json()
        assert "enforcement" in data
        assert "status" in data
        assert "namespace" in data
        assert "policy_type" in data

    def test_scan_vulnerabilities(self):
        """Test vulnerability scanning endpoint"""
        resources = [
            {
                "kind": "Pod",
                "metadata": {"name": "test-pod"},
                "spec": {"containers": [{"name": "nginx", "image": "nginx:latest"}]},
            }
        ]
        response = client.post("/cks/vulnerability-scan", json=resources)
        assert response.status_code == 200

        data = response.json()
        assert "vulnerability_scan" in data
        assert "status" in data
        assert "total_resources" in data

    def test_detect_threats(self):
        """Test threat detection endpoint"""
        threat_data = {
            "cluster_events": [
                {
                    "type": "Warning",
                    "reason": "Failed",
                    "message": "Pod failed to start",
                }
            ],
            "logs": ["2024-01-01 ERROR: Authentication failed"],
        }
        response = client.post("/cks/threat-detection", json=threat_data)
        assert response.status_code == 200

        data = response.json()
        assert "threat_detection" in data
        assert "status" in data
        assert "threats_detected" in data


class TestCapabilitiesEndpoint:
    def test_get_capabilities(self):
        """Test capabilities endpoint"""
        response = client.get("/capabilities")
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "katie"
        assert "Kubernetes AI Agent" in data["role"]
        assert "CKA" in data["specialization"]
        assert len(data["current_capabilities"]) > 0
        assert len(data["certifications"]) > 0
        assert len(data["focus_areas"]) > 0


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
