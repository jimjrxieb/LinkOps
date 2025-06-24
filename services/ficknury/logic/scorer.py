def score_task(task: dict):
    # Fake scoring based on keyword + capabilities list
    desc = task.get("task_description", "").lower()
    capabilities = load_agent_capabilities()

    if "storageclass" in desc and "create storageclass" in capabilities.get("katie", []):
        return {"score": 1.0, "automatable": True, "agent": "katie"}
    return {"score": 0.6, "automatable": False, "agent": "links"}

def load_agent_capabilities():
    # TODO: Load from Whis-generated orbs/runes
    return {
        "katie": ["create storageclass", "deploy pod", "scale deployment"],
        "igris": ["create terraform", "provision infrastructure"],
        "whis": ["train model", "fine-tune", "generate runes"],
        "audit": ["security scan", "compliance check"]
    } 