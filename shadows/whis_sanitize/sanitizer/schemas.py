from pydantic import BaseModel
from typing import Literal, Dict, Any, Optional


class SanitizationRequest(BaseModel):
    input_type: Literal["task", "qna", "info", "image", "fixlog", "solution_entry", "youtube"]
    payload: dict


class YouTubeTranscriptRequest(BaseModel):
    raw_text: str
    source: str = "youtube"
    topic: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SanitizedResponse(BaseModel):
    cleaned_text: str
    topic: Optional[str] = None
    source: str
    metadata: Optional[Dict[str, Any]] = None
    sanitization_stats: Dict[str, Any]
