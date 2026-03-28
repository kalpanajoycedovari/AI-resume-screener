# AI Resume Screener

An AI-powered resume screening API built with FastAPI and Claude AI.

## Features
- Upload and parse PDF resumes
- Extract skills, experience, education using Claude AI
- Score resumes against job descriptions
- Rank multiple candidates automatically

## Tech Stack
- Python 3.11
- FastAPI
- Claude API (Anthropic)
- pdfplumber

## Setup
1. Clone the repo
2. Create a virtual environment: python -m venv venv
3. Activate it: .\venv\Scripts\Activate.ps1
4. Install dependencies: pip install -r requirements.txt
5. Add your API key to .env
6. Run: uvicorn main:app --reload

## API Endpoints
- POST /jobs/ - Create a job description
- GET /jobs/ - List all jobs
- POST /resumes/extract - Extract info from a resume
- POST /resumes/screen/{job_id} - Score a resume against a job
- POST /resumes/rank/{job_id} - Rank multiple resumes
