import os, json
from logic.categorizer import categorize_task
from logic.merger import dedupe_and_merge
from logic.recurrence import update_recurrence
from logic.updater import generate_update_prompt
from utils.io import save_orb, save_rune

SANITIZED_DIR = "data_lake/sanitized_inputs/"

def process_batch():
    processed = []
    for fname in os.listdir(SANITIZED_DIR):
        with open(os.path.join(SANITIZED_DIR, fname)) as f:
            data = json.load(f)

        # Step 1: Generate orb & rune
        orb, rune = generate_orb_and_rune(data)

        # Step 2: Categorize
        agent = categorize_task(data.get("task_description", ""))

        # Step 3: Deduplication + Refinement
        refined_orb, refined_rune = dedupe_and_merge(agent, orb, rune)

        # Step 4: Track recurrence
        updated_orb = update_recurrence(refined_orb)

        # Step 5: Suggest update
        prompt = generate_update_prompt(updated_orb, refined_rune)

        # Step 6: Save to agent logic
        save_orb(agent, updated_orb)
        save_rune(agent, refined_rune)
        save_approval_if_needed(agent, updated_orb, refined_rune)

        processed.append(fname)

    return processed

def generate_orb_and_rune(data):
    # TODO: Replace with OpenAI/Claude call
    orb = {
        "id": f"orb_{len(data)}",
        "title": f"Generated Orb for {data.get('input_type', 'unknown')}",
        "description": "Auto-generated best practices",
        "category": "auto"
    }
    
    rune = {
        "id": f"rune_{len(data)}",
        "script": f"# Auto-generated script\n# Based on: {data}",
        "language": "bash"
    }
    
    return orb, rune 