def categorize_task(text: str) -> str:
    text = text.lower()
    if "kubernetes" in text or "pod" in text:
        return "katie"
    elif "audit" in text or "cve" in text:
        return "audit"
    elif "platform" in text or "infrastructure" in text:
        return "igris"
    elif "ml" in text or "fine-tune" in text:
        return "whis"
    return "links"


def categorize_input(input_type: str, payload: dict) -> str:
    """Categorize input based on type and content"""
    if input_type == "task":
        # Extract task description from payload
        task_desc = payload.get("task_description", "") or payload.get(
            "description", ""
        )
        return categorize_task(task_desc)
    elif input_type == "qna":
        # Categorize based on question content
        question = payload.get("question", "")
        return categorize_task(question)
    elif input_type == "info":
        # Information dumps might be general
        return "links"
    elif input_type == "image":
        # Image inputs might need special handling
        return "whis"
    elif input_type == "fixlog":
        # Fix logs might indicate issues
        return "audit"
    elif input_type == "solution_entry":
        # Solution entries are categorized based on the problem they solve
        task_desc = payload.get("task_description", "")
        solution_path = payload.get("solution_path", [])

        # Combine task description and solution steps for better categorization
        combined_text = f"{task_desc} {' '.join(solution_path)}".lower()
        return categorize_task(combined_text)
    else:
        return "links"
