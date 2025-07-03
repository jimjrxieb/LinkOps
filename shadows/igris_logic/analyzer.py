from typing import Dict


def analyze_platform_components(task_text: str, platform: str) -> Dict[str, bool]:
    platform_keywords = {
        "kubernetes": ["k8s", "kubernetes", "pod", "deployment", "service", "ingress"],
        "aws": ["aws", "ec2", "s3", "lambda", "rds", "vpc", "iam"],
        "azure": ["azure", "vm", "storage", "function", "sql", "vnet", "rbac"],
        "gcp": ["gcp", "gce", "storage", "function", "sql", "vpc", "iam"],
        "terraform": ["terraform", "infrastructure", "iac", "provisioning"],
        "security": ["security", "compliance", "audit", "scan", "vulnerability"],
        "automation": [
            "automation",
            "ci/cd",
            "pipeline",
            "deployment",
            "orchestration",
        ],
    }

    # Specific component keywords for detailed analysis
    specific_components = {
        "pods": ["pod", "pods", "container"],
        "services": ["service", "services", "svc"],
        "deployments": ["deployment", "deployments", "deploy"],
        "ec2": ["ec2", "instance", "instances"],
        "s3": ["s3", "bucket", "storage"],
        "lambda": ["lambda", "function", "serverless"],
        "vpc": ["vpc", "network", "subnet"],
    }

    components = {"platform": True}  # Always include platform: True
    task_lower = task_text.lower()

    # Check platform-specific keywords
    for category, keywords in platform_keywords.items():
        components[category] = any(keyword in task_lower for keyword in keywords)

    # Check specific components
    for component, keywords in specific_components.items():
        components[component] = any(keyword in task_lower for keyword in keywords)

    # Always set the main platform to True
    components[platform] = True

    return components
