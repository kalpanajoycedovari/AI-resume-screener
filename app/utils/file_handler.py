import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_TYPES = ["application/pdf"]

async def save_upload(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Only PDF files are accepted")

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)

    if size_mb > settings.max_file_size_mb:
        raise HTTPException(400, f"File exceeds {settings.max_file_size_mb}MB limit")

    os.makedirs(settings.upload_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(settings.upload_dir, filename)

    with open(filepath, "wb") as f:
        f.write(content)

    return filepath

def delete_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
