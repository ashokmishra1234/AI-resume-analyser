from pydantic import BaseModel
from typing import List

class ResumeResponse(BaseModel):
    ats_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    summary: str
    suggestions: List[str]
