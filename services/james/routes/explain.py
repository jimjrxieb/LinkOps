from fastapi import APIRouter
from logic.assistant import james_explain

router = APIRouter(prefix="/api/james", tags=["Explain"])

@router.post("/explain")
def explain_orb(payload: dict):
    context = payload.get("text", "")
    return {"explanation": james_explain(context)}

@router.post("/summarize")
def summarize_text(payload: dict):
    text = payload.get("text", "")
    return {"summary": james_explain(f"Summarize this text concisely: {text}")}

@router.post("/rephrase")
def rephrase_text(payload: dict):
    text = payload.get("text", "")
    return {"rephrased": james_explain(f"Rephrase this text in a clear, professional manner: {text}")} 