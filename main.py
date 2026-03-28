from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import resume, jobs

app = FastAPI(
    title="AI Resume Screener",
    description="Screen, score and rank resumes against job descriptions using Claude AI",
    version="1.0.0"
)

app.include_router(jobs.router)
app.include_router(resume.router)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", tags=["UI"])
def root():
    return FileResponse("frontend/index.html")
