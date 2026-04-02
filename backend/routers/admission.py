from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/admission",
    tags=["Admission Management"]
)

@router.post("/apply", response_model=schemas.AdmissionApplication)
def submit_application(application: schemas.AdmissionApplicationBase, db: Session = Depends(database.get_db)):
    db_application = models.AdmissionApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.get("/applications", response_model=List[schemas.AdmissionApplication])
def get_applications(db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    return db.query(models.AdmissionApplication).all()

@router.patch("/applications/{app_id}/status")
def update_application_status(app_id: int, status: str, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_app = db.query(models.AdmissionApplication).filter(models.AdmissionApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    db_app.status = status
    db.commit()
    return {"message": f"Application status updated to {status}"}

@router.get("/merit-list", response_model=List[schemas.AdmissionApplication])
def get_merit_list(limit: int = 50, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    return db.query(models.AdmissionApplication).order_by(models.AdmissionApplication.merit_score.desc()).limit(limit).all()
