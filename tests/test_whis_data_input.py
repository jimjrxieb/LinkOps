#!/usr/bin/env python3
"""
Tests for Whis Data Input Service
Tests the data collection endpoints for various input types
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import the app from the service
try:
    from services.whis_data_input.main import app
except ImportError:
    # Fallback for when running tests from different directory
    import sys

    sys.path.append("shadows/whis_data_input")
    from main import app

client = TestClient(app)


class TestWhisDataInputHealth:
    """Test health check endpoints"""

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "whis_data_input" in data["service"]


class TestWhisDataInputCollection:
    """Test data collection endpoints"""

    def test_collect_task(self):
        """Test task collection endpoint"""
        payload = {
            "input_type": "task",
            "content": "Deploy a Kubernetes pod with nginx image",
        }

        with patch(
            "services.whis_data_input.utils.kafka_producer.send_to_kafka"
        ) as mock_kafka:
            response = client.post("/api/collect/task", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["source"] == "task"
        mock_kafka.assert_called_once()

    def test_collect_qna(self):
        """Test Q&A collection endpoint"""
        payload = {
            "input_type": "qna",
            "content": {
                "question": "What is a pod?",
                "answer": "A pod is the smallest deployable unit in Kubernetes.",
            },
        }

        with patch(
            "services.whis_data_input.utils.kafka_producer.send_to_kafka"
        ) as mock_kafka:
            response = client.post("/api/collect/qna", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["source"] == "qna"
        mock_kafka.assert_called_once()

    def test_collect_fixlog(self):
        """Test fixlog collection endpoint"""
        payload = {
            "input_type": "fixlog",
            "content": {
                "log_entry": "ERROR: Database connection failed",
                "severity": "high",
                "component": "database",
            },
        }

        with patch(
            "services.whis_data_input.utils.kafka_producer.send_to_kafka"
        ) as mock_kafka:
            response = client.post("/api/collect/fixlog", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["source"] == "fixlog"
        mock_kafka.assert_called_once()

    def test_collect_info_dump(self):
        """Test info dump collection endpoint"""
        payload = {
            "input_type": "info",
            "content": "This is a sample information dump for testing purposes.",
        }

        with patch(
            "services.whis_data_input.utils.kafka_producer.send_to_kafka"
        ) as mock_kafka:
            response = client.post("/api/collect/info", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["source"] == "info"
        mock_kafka.assert_called_once()

    def test_collect_image(self):
        """Test image collection endpoint"""
        payload = {
            "input_type": "image",
            "content": {
                "image_path": "path/to/image.jpg",
                "extracted_text": "Sample extracted text from image",
            },
        }

        with patch(
            "services.whis_data_input.utils.kafka_producer.send_to_kafka"
        ) as mock_kafka:
            response = client.post("/api/collect/image", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["source"] == "image"
        mock_kafka.assert_called_once()


class TestWhisDataInputValidation:
    """Test input validation"""

    def test_invalid_input_type(self):
        """Test with invalid input type"""
        payload = {"input_type": "invalid_type", "content": "Some content"}

        response = client.post("/api/collect/task", json=payload)
        assert response.status_code == 422  # Validation error

    def test_missing_content(self):
        """Test with missing content"""
        payload = {
            "input_type": "task"
            # Missing content field
        }

        response = client.post("/api/collect/task", json=payload)
        assert response.status_code == 422  # Validation error

    def test_empty_content(self):
        """Test with empty content"""
        payload = {"input_type": "task", "content": ""}

        response = client.post("/api/collect/task", json=payload)
        assert response.status_code == 422  # Validation error


class TestWhisDataInputErrorHandling:
    """Test error handling scenarios"""

    def test_kafka_unavailable(self):
        """Test behavior when Kafka is unavailable"""
        payload = {"input_type": "task", "content": "Test task"}

        with patch(
            "services.whis_data_input.utils.kafka_producer.send_to_kafka"
        ) as mock_kafka:
            mock_kafka.side_effect = Exception("Kafka connection failed")
            response = client.post("/api/collect/task", json=payload)

        assert response.status_code == 500
        data = response.json()
        assert "error" in data

    def test_malformed_json(self):
        """Test with malformed JSON"""
        response = client.post(
            "/api/collect/task",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
