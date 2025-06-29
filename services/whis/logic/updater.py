def generate_update_prompt(orb: dict, rune: dict) -> str:
    return (
        f"# Suggested update for agent logic\n"
        f"# Orb: {orb['title']}\n"
        f"# Rune:\n{rune['script']}"
    )


def update_training_data(input_type: str, payload: dict, category: str):
    """Update training data with new input"""
    # TODO: Implement actual training data storage
    # This could save to database, file, or trigger ML training

    print(f"[WHIS] Updating training data: {input_type} -> {category}")
    print(f"[WHIS] Payload keys: {list(payload.keys())}")

    # For now, just log the update
    # In a real implementation, you might:
    # - Save to database
    # - Update ML model weights
    # - Trigger retraining
    # - Update agent knowledge base

    return {
        "input_type": input_type,
        "category": category,
        "timestamp": "2024-01-01T00:00:00Z",  # TODO: Use actual timestamp
        "status": "updated",
    }
