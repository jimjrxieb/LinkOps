from typing import Dict

def analyze_platform_components(task_text: str, platform: str) -> Dict[str, bool]:
    platform_keywords = {
        "kubernetes": ["k8s", "kubernetes", "pod", "deployment", "service", "ingress"],
        "aws": ["aws", "ec2", "s3", "lambda", "rds", "vpc", "iam"],
        "azure": ["azure", "vm", "storage", "function", "sql", "vnet", "rbac"],
        "gcp": ["gcp", "gce", "storage", "function", "sql", "vpc", "iam"],
        "terraform": ["terraform", "infrastructure", "iac", "provisioning"],
        "security": ["security", "compliance", "audit", "scan", "vulnerability"],
        "automation": ["automation", "ci/cd", "pipeline", "deployment", "orchestration"],
    }

    components = {}
    task_lower = task_text.lower()

    for category, keywords in platform_keywords.items():
        components[category] = any(keyword in task_lower for keyword in keywords)

    components[platform] = True
    return components 