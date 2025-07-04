from fastapi import FastAPI, Request
from routes import clean

app = FastAPI(title="Sanitizer Service")

app.include_router(clean.router)


@app.post("/sanitize")
async def sanitize_input(request: Request):
    """
    Sanitize task input for the learning pipeline.
    """
    raw = await request.json()

    # Minimal sanitizer for now - can be enhanced with NLP, spellchecking, etc.
    sanitized = {
        "task_id": raw.get("task_id"),
        "title": raw.get("title", "").strip(),
        "description": raw.get("description", "").strip().replace("\n", " "),
        "priority": raw.get("priority", "medium"),
        "category": raw.get("category", "general"),
        "tags": raw.get("tags", []),
        "source": raw.get("source", "unknown"),
        "status": "clean",
        "sanitized_at": "2024-01-15T12:00:00Z",  # Would be datetime.utcnow().isoformat()
    }

    return {"sanitized": sanitized}


@app.get("/health")
def health():
    """Basic health check"""
    return {"status": "healthy", "service": "whis_sanitize"}
