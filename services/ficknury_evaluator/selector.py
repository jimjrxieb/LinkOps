def select_agent_for_task(task_description: str, capabilities: dict):
    """Select the best agent for a given task based on capabilities"""
    desc = task_description.lower()

    # Simple keyword matching - in production, use ML/NLP
    if any(
        word in desc
        for word in ["kubernetes", "pod", "deployment", "service", "storageclass"]
    ):
        return "katie"
    elif any(
        word in desc for word in ["terraform", "infrastructure", "cloud", "provision"]
    ):
        return "igris"
    elif any(word in desc for word in ["ml", "model", "training", "fine-tune", "ai"]):
        return "whis"
    elif any(word in desc for word in ["audit", "security", "compliance", "scan"]):
        return "audit"
    else:
        return "links"
