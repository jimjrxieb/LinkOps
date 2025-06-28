from fastapi import APIRouter
from pydantic import BaseModel
from logic.generator import process_batch
from logic.categorizer import categorize_input
from logic.updater import update_training_data
import uuid
import random

router = APIRouter(prefix="/api/whis", tags=["Training"])


class TrainingPayload(BaseModel):
    input_type: str
    payload: dict


@router.post("/train")
def receive_training_data(data: TrainingPayload):
    """Receive training data from sanitizer and other services"""
    print(f"[WHIS] Received training data: {data.input_type}")

    # Special handling for solution_entry
    if data.input_type == "solution_entry":
        print("[WHIS] Received verified solution path")
        # Simulate Rune creation
        rune_id = f"rune-{uuid.uuid4().hex[:6]}"
        print(f"[WHIS] Created Rune: {rune_id}")

        # Auto-train without approvals for verified solutions
        try:
            # Extract solution information
            task_id = data.payload.get("task_id", str(uuid.uuid4()))
            # task_description = data.payload.get(
            #     "task_description", ""
            # )  # unused
            solution_path = data.payload.get("solution_path", [])
            result = data.payload.get("result", "Success")

            # Categorize the solution
            category = categorize_input(data.input_type, data.payload)

            # Update training data immediately
            update_training_data(data.input_type, data.payload, category)

            return {
                "status": "rune_created",
                "type": data.input_type,
                "category": category,
                "rune_id": rune_id,
                "task_id": task_id,
                "solution_steps": len(solution_path),
                "result": result,
                "message": (
                    f"Solution rune created and auto-trained: {rune_id}"
                ),
            }
        except Exception as e:
            print(f"[WHIS] Error processing solution entry: {str(e)}")
            return {
                "status": "error",
                "type": data.input_type,
                "error": str(e)
            }

    # Regular training logic for other input types
    try:
        # Extract task information
        task_id = data.payload.get("task_id", str(uuid.uuid4()))
        # description = data.payload.get("task_description", "")  # unused
        # variable

        # Categorize the input
        category = categorize_input(data.input_type, data.payload)

        # Update training data
        update_training_data(data.input_type, data.payload, category)

        # Check if we have a match (placeholder logic)
        match_found = random.choice(
            [True, False]
        )  # TODO: Replace with real matching logic

        if match_found:
            # Generate Orb and Rune IDs
            orb_id = f"orb-{task_id[:8]}"
            rune_id = f"rune-{task_id[:8]}"

            result = {
                "status": "match_found",
                "type": data.input_type,
                "category": category,
                "orb_id": orb_id,
                "rune_id": rune_id,
                "autonomous": True,
                "message": "Existing pattern matched, ready for deployment",
            }
        else:
            result = {
                "status": "no_match",
                "type": data.input_type,
                "category": category,
                "reason": "New task pattern",
                "needs_approval": True,
                "message": "New pattern detected, requires manual review",
            }

        return result

    except Exception as e:
        print(f"[WHIS] Error processing training data: {str(e)}")
        return {"status": "error", "type": data.input_type, "error": str(e)}


@router.post("/train-nightly")
def trigger_training():
    """Trigger nightly batch training process"""
    processed = process_batch()
    return {"status": "done", "processed": len(processed)}
