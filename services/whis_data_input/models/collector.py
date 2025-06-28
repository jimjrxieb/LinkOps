from pydantic import BaseModel
from typing import Optional


class TaskInput(BaseModel):
    task_id: str
    task_description: str
    orb: Optional[str] = None
    rune: Optional[str] = None
    data: Optional[str] = None


class QnAInput(BaseModel):
    task_id: str
    question: str
    correct_answer: str


class InfoDumpInput(BaseModel):
    source: Optional[str]
    content: str


class ImageTextInput(BaseModel):
    image_id: str
    extracted_text: str


class FixLogInput(BaseModel):
    error: str
    solution: str
    guide: str
