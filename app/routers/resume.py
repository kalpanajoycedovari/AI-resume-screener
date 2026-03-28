from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_handler import save_upload, delete_file
from app.services.pdf_parser import parse_pdf
from app.services.claude_service import extract_resume_data
from app.services.scorer import score_candidate
from app.services.ranker import rank_candidates
from app.models.resume import ExtractedResume
from app.routers.jobs import job_store

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/extract", summary="Upload and extract info from a resume")
async def extract_resume(file: UploadFile = File(...)):
    filepath = await save_upload(file)
    try:
        raw_text = parse_pdf(filepath)
        extracted = extract_resume_data(raw_text)
        return {"filename": file.filename, "extracted": extracted}
    finally:
        delete_file(filepath)


@router.post("/screen/{job_id}", summary="Screen a single resume against a job")
async def screen_resume(job_id: str, file: UploadFile = File(...)):
    if job_id not in job_store:
        raise HTTPException(404, f"Job '{job_id}' not found")

    job = job_store[job_id]
    filepath = await save_upload(file)

    try:
        raw_text = parse_pdf(filepath)
        extracted = extract_resume_data(raw_text)
        resume = ExtractedResume(filename=file.filename, raw_text=raw_text, **extracted)
        scored = score_candidate(resume, job)
        return scored
    finally:
        delete_file(filepath)


@router.post("/rank/{job_id}", summary="Upload multiple resumes and rank them")
async def rank_resumes(job_id: str, files: list[UploadFile] = File(...)):
    if job_id not in job_store:
        raise HTTPException(404, f"Job '{job_id}' not found")

    if len(files) > 20:
        raise HTTPException(400, "Maximum 20 resumes at once")

    job = job_store[job_id]
    scored_list = []

    for file in files:
        filepath = await save_upload(file)
        try:
            raw_text = parse_pdf(filepath)
            extracted = extract_resume_data(raw_text)
            resume = ExtractedResume(filename=file.filename, raw_text=raw_text, **extracted)
            scored = score_candidate(resume, job)
            scored_list.append(scored)
        finally:
            delete_file(filepath)

    ranked = rank_candidates(scored_list)
    return {"job": job.title, "total_candidates": len(ranked), "rankings": ranked}
