from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user

@router.get("/teachers", response_model=List[schemas.Teacher])
def read_teachers(db: Session = Depends(database.get_db)):
    return db.query(models.Teacher).all()

@router.post("/teachers/profile", response_model=schemas.Teacher)
def create_teacher_profile(
    profile: schemas.TeacherCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["teacher", "admin"]))
):
    db_profile = models.Teacher(**profile.dict(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/students", response_model=List[schemas.Student])
def read_students(db: Session = Depends(database.get_db)):
    return db.query(models.Student).all()

@router.get("/student/{student_id}/id-card")
def generate_id_card(student_id: int, db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # In a real app, this might generate a PDF or a specific JSON blob for a printer
    return {
        "institution": "Global International School & College",
        "name": student.user.full_name,
        "admission_no": student.admission_number,
        "grade": student.grade_level,
        "valid_until": "2027-12-31"
    }
