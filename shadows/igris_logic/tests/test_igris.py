"""
Tests for Igris Platform Engineering Service
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from analyzer import analyze_platform_components  # noqa: E402
from infrastructure import (
    generate_infrastructure_solution,
    generate_configurations,
)  # noqa: E402
from security import generate_security_recommendations  # noqa: E402
from opendevin import simulate_opendevin_automation  # noqa: E402

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        """Test health endpoint returns correct service info"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "igris"
        assert "Platform Engineering" in data["specialization"]
        assert len(data["capabilities"]) > 0


class TestExecuteEndpoint:
    def test_execute_kubernetes_task(self):
        """Test executing a Kubernetes platform task"""
        task_data = {
            "task_id": "test-001",
            "task_text": "Deploy a Kubernetes cluster with security policies",
            "platform": "kubernetes",
            "action_type": "deploy",
        }

        response = client.post("/execute", json=task_data)
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "igris"
        assert "kubernetes" in data["task"].lower()
        assert "infrastructure_solution" in data
        assert "generated_configs" in data
        assert "security_recommendations" in data
        assert 0.0 <= data["confidence_score"] <= 1.0

    def test_execute_aws_task(self):
        """Test executing an AWS platform task"""
        task_data = {
            "task_id": "test-002",
            "task_text": "Set up AWS infrastructure with EC2 and S3",
            "platform": "aws",
            "action_type": "configure",
        }

        response = client.post("/execute", json=task_data)
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "igris"
        assert "aws" in data["infrastructure_solution"]["platform"]

    def test_execute_invalid_task(self):
        """Test handling invalid task data"""
        task_data = {
            "task_id": "test-003",
            "task_text": "",  # Empty task
            "platform": "invalid-platform",
        }

        response = client.post("/execute", json=task_data)
        assert response.status_code == 200  # Should still process


class TestOpenDevinEndpoint:
    def test_opendevin_automate(self):
        """Test OpenDevin automation integration"""
        task_data = {
            "task": "Automate infrastructure deployment",
            "platform": "kubernetes",
        }

        response = client.post("/opendevin/automate", json=task_data)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "automation_complete"
        assert "opendevin_insights" in data
        assert "automated_actions" in data
        assert "code_generated" in data
        assert "infrastructure_changes" in data


class TestEnhanceEndpoint:
    def test_enhance_agent(self):
        """Test agent enhancement endpoint"""
        enhancement_data = {
            "agent": "igris",
            "orb_id": "terraform-orb",
            "rune_patch": "enhanced-terraform-capabilities",
            "training_notes": "Added advanced Terraform modules",
        }

        response = client.post("/api/enhance", json=enhancement_data)
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "igris"
        assert data["orb_id"] == "terraform-orb"
        assert data["status"] == "enhancement_applied"
        assert data["capabilities_updated"] is True


class TestCapabilitiesEndpoint:
    def test_get_capabilities(self):
        """Test capabilities endpoint"""
        response = client.get("/capabilities")
        assert response.status_code == 200

        data = response.json()
        assert data["agent"] == "igris"
        assert "Platform Engineering" in data["specialization"]
        assert len(data["current_capabilities"]) > 0
        assert len(data["certifications"]) > 0
        assert len(data["focus_areas"]) > 0


class TestAnalyzerModule:
    def test_analyze_kubernetes_components(self):
        """Test platform component analysis for Kubernetes"""
        task_text = "Deploy a Kubernetes cluster with pods and services"
        platform = "kubernetes"

        components = analyze_platform_components(task_text, platform)

        assert components["kubernetes"] is True
        assert components["platform"] is True
        assert isinstance(components, dict)

    def test_analyze_aws_components(self):
        """Test platform component analysis for AWS"""
        task_text = "Set up AWS EC2 instances with S3 storage"
        platform = "aws"

        components = analyze_platform_components(task_text, platform)

        assert components["aws"] is True
        assert components["platform"] is True

    def test_analyze_security_components(self):
        """Test security component detection"""
        task_text = "Implement security scanning and compliance audit"
        platform = "kubernetes"

        components = analyze_platform_components(task_text, platform)

        assert components["security"] is True


class TestInfrastructureModule:
    def test_generate_infrastructure_solution(self):
        """Test infrastructure solution generation"""
        task_text = "Deploy Kubernetes cluster"
        platform_components = {"kubernetes": True, "terraform": True}
        platform = "kubernetes"

        solution = generate_infrastructure_solution(
            task_text, platform_components, platform
        )

        assert solution["platform"] == "kubernetes"
        assert solution["approach"] == "platform-native"
        assert "Kubernetes Cluster Management" in solution["components"]
        assert "Infrastructure as Code with Terraform" in solution["components"]

    def test_generate_configurations(self):
        """Test configuration generation"""
        task_text = "Deploy with Terraform and Kubernetes"
        platform_components = {"terraform": True, "kubernetes": True}
        platform = "kubernetes"

        configs = generate_configurations(task_text, platform_components, platform)

        assert isinstance(configs, list)
        assert len(configs) > 0


class TestSecurityModule:
    def test_generate_security_recommendations(self):
        """Test security recommendations generation"""
        task_text = "Secure Kubernetes deployment"
        platform_components = {"kubernetes": True, "terraform": True}
        platform = "kubernetes"

        recommendations = generate_security_recommendations(
            task_text, platform_components, platform
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert any("pod security policies" in rec.lower() for rec in recommendations)


class TestOpenDevinModule:
    def test_simulate_opendevin_automation(self):
        """Test OpenDevin automation simulation"""
        task = {"task": "Automate infrastructure", "platform": "kubernetes"}

        automation = simulate_opendevin_automation(task)

        assert "insights" in automation
        assert "actions" in automation
        assert "code_generated" in automation
        assert "infrastructure_changes" in automation
        assert isinstance(automation["insights"], list)
        assert isinstance(automation["actions"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
