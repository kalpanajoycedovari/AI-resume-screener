from app.models.resume import ScoredResume

def rank_candidates(scored_resumes: list[ScoredResume]) -> list[dict]:
    sorted_resumes = sorted(scored_resumes, key=lambda x: x.score, reverse=True)

    ranked = []
    for i, resume in enumerate(sorted_resumes, 1):
        ranked.append({
            "rank": i,
            "name": resume.name,
            "email": resume.email,
            "filename": resume.filename,
            "score": resume.score,
            "score_breakdown": resume.score_breakdown,
            "recommendation": resume.recommendation,
            "skills": resume.skills,
            "experience_years": resume.experience_years
        })

    return ranked
