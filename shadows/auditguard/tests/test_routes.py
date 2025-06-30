"""Tests for AuditGuard service routes."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "AuditGuard"
        assert "endpoints" in data

    def test_audit_health(self):
        """Test audit health endpoint."""
        response = client.get("/audit/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "auditguard-audit"

    def test_compliance_health(self):
        """Test compliance health endpoint."""
        response = client.get("/compliance/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "auditguard-compliance"

    def test_security_health(self):
        """Test security health endpoint."""
        response = client.get("/security/health")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "auditguard-security"


class TestSecurityRoutes:
    """Test security scanning routes."""

    @patch("routes.security._run_trivy_scan")
    def test_trivy_scan(self, mock_trivy):
        """Test Trivy vulnerability scan."""
        mock_trivy.return_value = {
            "scan_type": "trivy",
            "target": "/tmp/test",
            "high_risk": 2,
            "medium_risk": 1,
            "low_risk": 0,
            "total_vulnerabilities": 3,
            "scan_successful": True,
        }

        response = client.post(
            "/security/scan",
            json={
                "task_id": "test-123",
                "scan_type": "trivy",
                "target": "/tmp/test",
                "auto_approve": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == "test-123"
        assert data["action"] == "trivy scan complete"

    def test_invalid_scan_type(self):
        """Test invalid scan type returns 400."""
        response = client.post(
            "/security/scan",
            json={
                "task_id": "test-123",
                "scan_type": "invalid",
                "target": "/tmp/test",
            },
        )
        assert response.status_code == 400


class TestComplianceRoutes:
    """Test compliance audit routes."""

    @patch("routes.compliance._audit_soc2")
    def test_soc2_audit(self, mock_soc2):
        """Test SOC2 compliance audit."""
        mock_soc2.return_value = {
            "status": "audited",
            "issues": [],
            "recommendations": ["Implement access controls"],
            "score": 0.85,
        }

        response = client.post(
            "/compliance/audit",
            json={
                "task_id": "test-123",
                "compliance_scope": ["SOC2"],
                "target": "test-target",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == "test-123"
        assert "SOC2" in data["compliance_scope"]


class TestAuditRoutes:
    """Test repository audit routes."""

    @patch("routes.audit._check_for_secrets")
    @patch("routes.audit._check_for_credentials")
    @patch("routes.audit._check_for_sensitive_files")
    def test_repository_audit(
        self, mock_sensitive_files, mock_credentials, mock_secrets
    ):
        """Test repository security audit."""
        mock_secrets.return_value = []
        mock_credentials.return_value = []
        mock_sensitive_files.return_value = []

        response = client.post(
            "/audit/repository",
            json={
                "task_id": "test-123",
                "repository_path": "/tmp/repo",
                "audit_scope": ["secrets", "credentials"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == "test-123"
        assert data["repository_path"] == "/tmp/repo"
