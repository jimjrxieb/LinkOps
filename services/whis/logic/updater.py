def generate_update_prompt(orb: dict, rune: dict) -> str:
    return f"# Suggested update for agent logic\n# Orb: {orb['title']}\n# Rune:\n{rune['script']}" 