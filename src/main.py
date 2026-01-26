from resume_parser import extract_email, extract_skills, read_pdf, calculate_score

job_skills = ["Python", "Machine Learning", "NLP"]

resume_text = read_pdf("data/resumes/Ratna Resume (1).pdf")

email = extract_email(resume_text)
matched_skills = extract_skills(resume_text, job_skills)
score = calculate_score(matched_skills, len(job_skills))

print("Resume Analysis Result")
print("----------------------")
print(f"Email           : {email}")
print(f"Matched Skills  : {matched_skills}")
print(f"Resume Score   : {score}%")
