import anthropic
import json
from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

def extract_resume_data(raw_text: str) -> dict:
    prompt = f"""Extract structured information from this resume text.
Return ONLY valid JSON with these exact keys:
{{
  "name": "full name or empty string",
  "email": "email or empty string",
  "skills": ["skill1", "skill2"],
  "experience_years": 0.0,
  "education": ["degree1"],
  "summary": "2 sentence professional summary"
}}

Resume text:
{raw_text}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{{"role": "user", "content": prompt}}]
    )

    response_text = message.content[0].text.strip()
    if response_text.startswith("`"):
        response_text = response_text.split("`")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]

    return json.loads(response_text.strip())


def score_resume(resume_data: dict, job_data: dict) -> dict:
    prompt = f"""You are an expert recruiter. Score this candidate against the job description.

JOB:
Title: {job_data['title']}
Description: {job_data['description']}
Required Skills: {job_data['required_skills']}
Nice to Have: {job_data['nice_to_have_skills']}
Experience Required: {job_data['experience_years']} years

CANDIDATE:
Name: {resume_data['name']}
Skills: {resume_data['skills']}
Experience: {resume_data['experience_years']} years
Education: {resume_data['education']}
Summary: {resume_data['summary']}

Return ONLY valid JSON:
{{
  "total_score": 85.5,
  "score_breakdown": {{
    "skills_match": 40.0,
    "experience_match": 25.0,
    "education_match": 10.0,
    "overall_fit": 10.5
  }},
  "recommendation": "Brief recommendation here."
}}

Scores: skills_match out of 40, experience_match out of 25, education_match out of 20, overall_fit out of 15."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{{"role": "user", "content": prompt}}]
    )

    response_text = message.content[0].text.strip()
    if response_text.startswith("`"):
        response_text = response_text.split("`")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]

    return json.loads(response_text.strip())
