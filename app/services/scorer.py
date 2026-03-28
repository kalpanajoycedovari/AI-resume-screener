from app.services.claude_service import score_resume
from app.models.resume import ExtractedResume, ScoredResume
from app.models.job import JobDescription

def score_candidate(resume: ExtractedResume, job: JobDescription) -> ScoredResume:
    result = score_resume(resume.model_dump(), job.model_dump())

    return ScoredResume(
        filename=resume.filename,
        name=resume.name,
        email=resume.email,
        skills=resume.skills,
        experience_years=resume.experience_years,
        score=result["total_score"],
        score_breakdown=result["score_breakdown"],
        recommendation=result["recommendation"]
    )
