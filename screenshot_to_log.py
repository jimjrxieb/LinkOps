import sys
import uuid
import requests
from PIL import Image
import pytesseract

API_URL = "http://localhost:8000/api/logs"

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def send_to_linkops(image_path, task_id="screenshot_task", agent="katie"):
    text = extract_text_from_image(image_path)
    payload = {
        "agent": agent,
        "task_id": task_id,
        "action": f"Extracted screenshot: {image_path}",
        "result": text
    }
    res = requests.post(API_URL, json=payload)
    return res.status_code, res.text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screenshot_to_log.py <image_path> [task_id]")
        sys.exit(1)

    img_path = sys.argv[1]
    task = sys.argv[2] if len(sys.argv) > 2 else str(uuid.uuid4())
    code, msg = send_to_linkops(img_path, task)
    print(f"[+] Status: {code} | Response: {msg}") 