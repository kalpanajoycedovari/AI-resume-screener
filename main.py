from fastapi import FastAPI
from app.routers import resume, jobs

app = FastAPI(
    title="AI Resume Screener",
    description="Screen, score and rank resumes against job descriptions using Claude AI",
    version="1.0.0"
)

app.include_router(jobs.router)
app.include_router(resume.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "running", "message": "AI Resume Screener API is live"}
