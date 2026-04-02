from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/academic",
    tags=["Academic Management"]
)

# New Exam endpoints
@router.post("/exams", response_model=schemas.Exam)
def create_exam(
    exam: schemas.ExamCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_admin)
):
    new_exam = models.Exam(**exam.dict())
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam

@router.get("/exams", response_model=List[schemas.Exam])
def read_exams(db: Session = Depends(database.get_db)):
    return db.query(models.Exam).all()

# New Grade/Result endpoints
@router.post("/grades", response_model=schemas.Grade)
def record_grade(
    grade: schemas.GradeCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["teacher", "admin"]))
):
    new_grade = models.Grade(**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

@router.get("/grades/student/{student_id}", response_model=List[schemas.Grade])
def read_student_grades(student_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    # Simple security: Students can only see their own grades unless admin/teacher
    if current_user.role == "student" and current_user.student_profile.id != student_id:
        raise HTTPException(status_code=403, detail="Forbidden - Cannot view other students grades")
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()

@router.get("/student/{student_id}/transcript")
def get_academic_transcript(student_id: int, db: Session = Depends(database.get_db)):
    from services.document_service import DocumentService
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    grades = db.query(models.Grade).filter(models.Grade.student_id == student_id).all()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return DocumentService.generate_transcript_summary(student.user.full_name, grades)

@router.post("/student/{student_id}/certificate")
def issue_certificate(student_id: int, type: str, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    from services.document_service import DocumentService
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    cert = models.Certificate(student_id=student_id, type=type)
    db.add(cert)
    db.commit()
    
    return DocumentService.generate_certificate_metadata(student.user.full_name, type)
