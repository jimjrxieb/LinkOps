from fastapi import APIRouter
from logic.assistant import james_respond

router = APIRouter(prefix="/api/james", tags=["Chat"])

@router.post("/chat")
def respond_to_user(input: dict):
    text = input.get("message", "")
    response = james_respond(text)
    return {"james_response": response} 