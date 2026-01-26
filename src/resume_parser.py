import re
from PyPDF2 import PdfReader


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_skills(text, job_skills):
    found_skills = []
    text_lower = text.lower()

    for skill in job_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills
def calculate_score(matched_skills, total_skills):
    if total_skills == 0:
        return 0
    return round((len(matched_skills) / total_skills) * 100, 2)


