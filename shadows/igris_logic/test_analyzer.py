#!/usr/bin/env python3
"""Simple test script for analyzer function"""

from analyzer import analyze_platform_components


def test_analyzer():
    # Test Kubernetes
    print("Testing Kubernetes analysis...")
    k8s_result = analyze_platform_components(
        "Deploy a Kubernetes cluster with pods and services", "kubernetes"
    )
    print(f"Kubernetes result: {k8s_result}")

    # Test AWS
    print("\nTesting AWS analysis...")
    aws_result = analyze_platform_components(
        "Set up AWS EC2 instances with S3 storage", "aws"
    )
    print(f"AWS result: {aws_result}")

    # Verify expected results
    print("\nVerifying results...")

    # Kubernetes test
    assert k8s_result["platform"] is True, "platform should be True"
    assert k8s_result["kubernetes"] is True, "kubernetes should be True"
    assert k8s_result["pods"] is True, "pods should be True"
    assert k8s_result["services"] is True, "services should be True"
    print("✓ Kubernetes test passed")

    # AWS test
    assert aws_result["platform"] is True, "platform should be True"
    assert aws_result["aws"] is True, "aws should be True"
    assert aws_result["ec2"] is True, "ec2 should be True"
    assert aws_result["s3"] is True, "s3 should be True"
    print("✓ AWS test passed")

    print("\nAll tests passed!")


if __name__ == "__main__":
    test_analyzer()
