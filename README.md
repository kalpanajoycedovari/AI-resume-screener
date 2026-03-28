# AI Resume Screener 🤖

An AI-powered resume screening web application built with FastAPI and Claude AI. Upload resumes, define job requirements, and get intelligent candidate rankings automatically.

🔗 **Live Demo:** [https://ai-resume-screener-x5c1.onrender.com](https://ai-resume-screener-x5c1.onrender.com)  
📁 **GitHub:** [https://github.com/kalpanajoycedovari/AI-resume-screener](https://github.com/kalpanajoycedovari/AI-resume-screener)

---

## What It Does

- 📄 **Parse PDF Resumes** — Extracts text from any PDF resume automatically
- 🧠 **AI Extraction** — Uses Claude AI to extract name, email, skills, experience and education
- 🎯 **Smart Scoring** — Scores each candidate against your job description (out of 100)
- 🏆 **Candidate Ranking** — Ranks multiple candidates from best to worst fit
- 🌐 **Beautiful UI** — Clean, minimal frontend anyone can use without technical knowledge

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python 3.11 + FastAPI | REST API framework |
| AI | Claude API (Anthropic) | Resume extraction & scoring |
| PDF Parsing | pdfplumber | Extract text from PDF resumes |
| Data Validation | Pydantic v2 + pydantic-settings | Request/response models |
| Server | Uvicorn | ASGI server |
| Frontend | HTML + CSS + Vanilla JS | User interface |
| Deployment | Render.com | Free cloud hosting |
| Version Control | Git + GitHub | Source control |

---

## Project Structure

```
AI-resume-screener/
├── app/
│   ├── __init__.py
│   ├── config.py              # Environment settings
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── resume.py          # Resume endpoints
│   │   └── jobs.py            # Job endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py      # PDF text extraction
│   │   ├── claude_service.py  # Claude AI integration
│   │   ├── scorer.py          # Resume scoring logic
│   │   └── ranker.py          # Candidate ranking logic
│   ├── models/
│   │   ├── __init__.py
│   │   ├── resume.py          # Resume data models
│   │   └── job.py             # Job data models
│   └── utils/
│       ├── __init__.py
│       └── file_handler.py    # File upload handling
├── frontend/
│   ├── index.html             # Main UI page
│   ├── style.css              # Styling
│   └── app.js                 # Frontend logic
├── uploads/                   # Temporary PDF storage
├── tests/
│   ├── test_resume.py
│   └── test_scorer.py
├── .env                       # Environment variables (not committed)
├── .gitignore
├── .python-version            # Pins Python 3.11.9 for Render
├── render.yaml                # Render deployment config
├── requirements.txt
└── main.py                    # FastAPI app entry point
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/` | Serves the frontend UI |
| POST | `/jobs/` | Create a new job description |
| GET | `/jobs/` | List all created jobs |
| GET | `/jobs/{job_id}` | Get a specific job |
| POST | `/resumes/extract` | Extract info from a single resume |
| POST | `/resumes/screen/{job_id}` | Score one resume against a job |
| POST | `/resumes/rank/{job_id}` | Rank multiple resumes against a job |

Interactive API docs available at: `/docs`

---

## Scoring Breakdown

Each resume is scored out of 100 by Claude AI:

| Category | Max Score |
|---------|-----------|
| Skills match | 40 points |
| Experience match | 25 points |
| Education match | 20 points |
| Overall fit | 15 points |

---

## Local Setup

### Prerequisites
- Python 3.11 (important — see [Challenges](#challenges-and-solutions) below)
- Git
- Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/kalpanajoycedovari/AI-resume-screener.git
cd AI-resume-screener

# 2. Create virtual environment with Python 3.11
py -3.11 -m venv venv

# 3. Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
echo ANTHROPIC_API_KEY=your_key_here > .env

# 6. Run the server
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` for the UI or `http://127.0.0.1:8000/docs` for the API docs.

---

## How to Use

### Step 1 — Create a Job
- Click **Create Job** in the navbar
- Fill in the job title, description, required skills and experience
- Click **Create Job** — you will get a job ID back

### Step 2 — Upload Resumes
- Click **Screen** in the navbar
- Select the job you just created from the dropdown
- Upload one or more PDF resumes
- Click **Rank All Candidates** or **Screen Single Resume**

### Step 3 — View Rankings
- The page automatically scrolls to **Rankings**
- Each candidate card shows their score, skills, and AI recommendation
- Candidates are sorted from highest to lowest score

---

## Challenges and Solutions

### Challenge 1 — Python Version Incompatibility

**Problem:** The project was initially built with Python 3.14 (the latest version). Both `PyMuPDF` and `pydantic-core` require compilation from source on Python 3.14 because no pre-built wheels exist yet. This caused errors like:

```
Exception: Unable to find Visual Studio
Exception: Failed to find python matching cpu=x64
error: metadata-generation-failed → pydantic-core
```

**Solution:**
- Switched from Python 3.14 to **Python 3.11** which has pre-built binary wheels for all packages
- Replaced `PyMuPDF` with `pdfplumber` — a pure Python PDF library that requires zero compilation and works on any Python version
- Added `.python-version` file to pin Python 3.11.9 for Render deployment

---

### Challenge 2 — Git Username Conflict After Renaming GitHub Account

**Problem:** After renaming the GitHub username, the local repo still pointed to the old remote URL, causing push failures:

```
error: failed to push some refs to 'https://github.com/old-username/AI-resume-screener.git'
```

**Solution:**
```bash
git remote set-url origin https://github.com/kalpanajoycedovari/AI-resume-screener.git
git push origin main --force
```

---

### Challenge 3 — Git Rebase Conflict on Clean Slate

**Problem:** When wiping the old codebase and pushing fresh code, a rebase conflict appeared because the remote had a newer README.md commit:

```
CONFLICT (modify/delete): README.md deleted in local and modified in HEAD
error: could not apply commit... chore: wipe old code
```

**Solution:**
```bash
git rebase --abort
git fetch origin
git reset --hard origin/main
# delete conflicting file, then force push
git push origin main --force
```

---

### Challenge 4 — Render Deploying with Python 3.14

**Problem:** Render's default Python version was 3.14, causing the same pydantic-core compilation failure in the cloud even though it worked locally on 3.11.

**Solution:**
- Added `.python-version` file containing `3.11.9`
- Added `pythonVersion: "3.11.9"` to `render.yaml`

```yaml
services:
  - type: web
    name: ai-resume-screener
    runtime: python
    pythonVersion: "3.11.9"
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
```

---

## Environment Variables

| Variable | Description |
|---------|-------------|
| `ANTHROPIC_API_KEY` | Your Claude API key from console.anthropic.com |
| `MAX_FILE_SIZE_MB` | Maximum PDF upload size in MB (default: 10) |
| `UPLOAD_DIR` | Directory for temporary file storage (default: uploads) |

---

## Deployment (Render.com)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repository
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Instance Type:** Free
5. Add environment variable: `ANTHROPIC_API_KEY`
6. Click **Deploy**

Render automatically redeploys on every `git push` to `main`.

---

## Dependencies

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
pdfplumber==0.11.4
anthropic==0.34.2
pydantic==2.8.2
pydantic-settings==2.4.0
python-dotenv==1.0.1
pytest==8.3.2
httpx==0.27.2
```

---

## License

MIT License — feel free to use this project for learning or portfolio purposes.

---

## Author

**Kalpana Joyce Dovari**  
GitHub: [@kalpanajoycedovari](https://github.com/kalpanajoycedovari)

---

*Built from scratch with FastAPI + Claude AI + pdfplumber. Deployed on Render.*