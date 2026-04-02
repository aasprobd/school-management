from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance Management"]
)

@router.post("/", response_model=schemas.Attendance)
def record_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["teacher", "admin"]))
):
    new_record = models.Attendance(**attendance.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/student/{student_id}", response_model=List[schemas.Attendance])
def read_student_attendance(student_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Attendance).filter(models.Attendance.student_id == student_id).all()

@router.get("/class/{class_id}", response_model=List[schemas.Attendance])
def read_class_attendance(class_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Attendance).filter(models.Attendance.class_id == class_id).all()
