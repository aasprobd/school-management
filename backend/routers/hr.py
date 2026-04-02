from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(prefix="/hr", tags=["Human Resources"])

@router.post("/appraisals", response_model=schemas.StaffAppraisal)
def create_appraisal(appraisal: schemas.StaffAppraisalBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    new_appraisal = models.StaffAppraisal(**appraisal.dict())
    db.add(new_appraisal)
    db.commit()
    db.refresh(new_appraisal)
    return new_appraisal

@router.get("/appraisals/{staff_id}", response_model=List[schemas.StaffAppraisal])
def get_staff_appraisals(staff_id: int, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    return db.query(models.StaffAppraisal).filter(models.StaffAppraisal.staff_id == staff_id).all()
