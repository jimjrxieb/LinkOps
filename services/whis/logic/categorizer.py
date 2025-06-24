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