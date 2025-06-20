import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_orb_from_text(task_id: str, dump: str) -> dict:
    prompt = f"""
    Turn the following information dump into a clean Orb.

    TASK ID: {task_id}

    CONTENT:
    {dump}

    Return JSON with:
    - name: concise orb name
    - description: 2-3 sentence summary
    - category: Kubernetes, AI/ML, or Platform Engineering
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an Orb Generator for a DevOps AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    try:
        json_result = response["choices"][0]["message"]["content"]
        return eval(json_result)  # Phase 1 only — replace with `json.loads()` if safe
    except Exception as e:
        return {"error": str(e)} 