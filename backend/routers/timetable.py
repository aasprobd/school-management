from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/timetable",
    tags=["Timetable Management"]
)

@router.post("/", response_model=schemas.Timetable)
def create_timetable_entry(
    entry: schemas.TimetableCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_admin)
):
    # Basic check for conflicts could be added here
    new_entry = models.Timetable(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/class/{class_id}", response_model=List[schemas.Timetable])
def read_class_timetable(class_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Timetable).filter(models.Timetable.class_id == class_id).all()

@router.get("/teacher/{teacher_id}", response_model=List[schemas.Timetable])
def read_teacher_timetable(teacher_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Timetable).filter(models.Timetable.teacher_id == teacher_id).all()
