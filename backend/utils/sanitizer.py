from typing import Union, Dict

def sanitize_task(content: Union[str, Dict]) -> dict:
    if isinstance(content, str):
        return {
            "agent": "auto", 
            "task_id": "task_xyz", 
            "description": content.strip()
        }
    else:
        return {
            "agent": "auto",
            "task_id": "task_xyz",
            "description": str(content).strip()
        }

def sanitize_qna(content: Union[str, Dict]) -> dict:
    if isinstance(content, dict):
        return {
            "question": content.get("question", "").strip(),
            "answer": content.get("answer", "").strip()
        }
    else:
        return {
            "question": str(content).strip(),
            "answer": ""
        }

def sanitize_dump(content: Union[str, Dict]) -> dict:
    if isinstance(content, str):
        return {
            "extracted": content.strip()[:1000]  # limit preview
        }
    else:
        return {
            "extracted": str(content).strip()[:1000]  # limit preview
        }

def sanitize_image(content: Union[str, Dict]) -> dict:
    """Sanitize extracted image text for Whis training"""
    if isinstance(content, str):
        return {
            "source": "image-ocr",
            "extracted_text": content.strip(),
            "preview": content.strip()[:500]  # limit preview
        }
    else:
        return {
            "source": "image-ocr",
            "extracted_text": str(content).strip(),
            "preview": str(content).strip()[:500]  # limit preview
        }
