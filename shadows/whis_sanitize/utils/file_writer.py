import os
import json
from datetime import datetime

DATA_DIR = "data_lake/sanitized_inputs"
os.makedirs(DATA_DIR, exist_ok=True)


def write_clean_log(input_type: str, payload: dict):
    now = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    filename = f"{DATA_DIR}/{input_type}_{now}.json"
    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)
