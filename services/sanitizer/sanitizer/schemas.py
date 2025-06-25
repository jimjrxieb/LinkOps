from pydantic import BaseModel
from typing import Literal

class SanitizationRequest(BaseModel):
    input_type: Literal["task", "qna", "info", "image", "fixlog", "solution_entry"]
    payload: dict 