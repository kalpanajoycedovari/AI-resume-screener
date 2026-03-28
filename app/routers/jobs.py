from fastapi import APIRouter, HTTPException
from app.models.job import JobDescription

router = APIRouter(prefix="/jobs", tags=["Jobs"])

job_store: dict[str, JobDescription] = {}

@router.post("/", summary="Create a job description")
def create_job(job: JobDescription):
    job_id = job.title.lower().replace(" ", "_")
    job_store[job_id] = job
    return {"job_id": job_id, "job": job}

@router.get("/", summary="List all jobs")
def list_jobs():
    return {"jobs": list(job_store.keys())}

@router.get("/{job_id}", summary="Get a job by ID")
def get_job(job_id: str):
    if job_id not in job_store:
        raise HTTPException(404, f"Job '{job_id}' not found")
    return job_store[job_id]
