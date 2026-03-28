from pydantic import BaseModel

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: list[str] = []
    nice_to_have_skills: list[str] = []
    experience_years: int = 0
