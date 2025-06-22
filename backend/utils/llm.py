import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

# Use the new OpenAI client
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_orb_from_text(task_id: str, dump: str) -> dict:
    prompt = f"""
    Turn the following information dump into a clean Orb.

    TASK ID: {task_id}

    CONTENT:
    {dump}

    Return a JSON object with these exact fields (no nesting):
    {{
        "name": "concise orb name",
        "description": "2-3 sentence summary", 
        "category": "Kubernetes, AI/ML, or Platform Engineering"
    }}
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an Orb Generator for a DevOps AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        json_result = response.choices[0].message.content
        return json.loads(json_result)
    except Exception as e:
        return {"error": str(e)}

def generate_rune_from_orb(orb_data: dict, original_text: str) -> dict:
    """
    Generate a rune (script) based on the orb data and original text
    """
    prompt = f"""
    Based on this Orb and the original text, generate a practical script or configuration.

    ORB DATA:
    - Name: {orb_data.get('name', 'Unknown')}
    - Description: {orb_data.get('description', 'No description')}
    - Category: {orb_data.get('category', 'Unknown')}

    ORIGINAL TEXT:
    {original_text}

    Generate a practical script that implements or demonstrates the concept.
    Return a JSON object with these fields:
    {{
        "script_content": "the actual script/code content",
        "language": "bash, yaml, python, or other appropriate language",
        "description": "brief description of what this script does"
    }}

    For Kubernetes tasks, generate kubectl commands or YAML manifests.
    For AI/ML tasks, generate Python scripts or configuration files.
    For Platform Engineering, generate infrastructure as code or automation scripts.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a DevOps Script Generator. Generate practical, executable scripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        json_result = response.choices[0].message.content
        return json.loads(json_result)
    except Exception as e:
        return {"error": str(e)}

def sanitize_input(text: str) -> str:
    """Sanitize input text by removing comments and empty lines"""
    return "\n".join([
        line.strip() for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ])

def infer_agent_category(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ["kubernetes", "pod", "deployment", "apiversion"]):
        return "katie"
    elif any(k in text for k in ["terraform", "cicd", "snyk", "devsecops", "jenkins"]):
        return "igris"
    elif any(k in text for k in ["mlflow", "model", "pipeline", "prometheus"]):
        return "whis"
    return "james"

def generate_rune_with_openai(task_text: str) -> str:
    """Generate executable code from task description using OpenAI"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
Convert the following explanation or Q&A into an executable code block or infrastructure config.

Task:
{task_text}

Output format: Plain code only (YAML, Python, Terraform, etc.)
"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a DevOps engineer helping convert descriptions into code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI generation failed: {e}")
        return task_text  # Fallback to original text

def contains_code(text: str) -> bool:
    """Simple check if text contains code patterns"""
    code_indicators = [
        "apiVersion:", "kind:", "metadata:", "spec:",  # Kubernetes
        "terraform {", "resource", "provider",  # Terraform
        "def ", "import ", "from ", "class ",  # Python
        "dockerfile", "from ", "run ", "copy ",  # Docker
        "#!/", "function ", "const ", "let ",  # Scripts
        "yaml", "json", "xml", "html"  # Data formats
    ]
    
    text_lower = text.lower()
    return any(indicator in text_lower for indicator in code_indicators) 