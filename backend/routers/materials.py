from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
import shutil
import os
from typing import List

router = APIRouter(
    prefix="/materials",
    tags=["Course Materials"]
)

UPLOAD_DIR = "uploads/materials"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_material(
    title: str,
    subject_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(dependencies.check_role(["teacher", "admin"]))
):
    file_path = os.path.join(UPLOAD_DIR, f"{subject_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "title": title, "path": file_path}
