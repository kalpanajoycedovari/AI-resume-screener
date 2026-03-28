from pydantic import BaseModel

class ExtractedResume(BaseModel):
    filename: str
    raw_text: str
    name: str = ""
    email: str = ""
    skills: list[str] = []
    experience_years: float = 0
    education: list[str] = []
    summary: str = ""

class ScoredResume(BaseModel):
    filename: str
    name: str
    email: str
    skills: list[str]
    experience_years: float
    score: float
    score_breakdown: dict
    recommendation: str
