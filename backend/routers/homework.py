from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/homework",
    tags=["Homework & Assignments"]
)

@router.post("/", response_model=schemas.Homework)
def create_homework(
    homework: schemas.HomeworkCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["teacher", "admin"]))
):
    new_hw = models.Homework(**homework.dict(), teacher_id=current_user.id)
    db.add(new_hw)
    db.commit()
    db.refresh(new_hw)
    return new_hw

@router.get("/class/{class_id}", response_model=List[schemas.Homework])
def read_class_homework(class_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Homework).filter(models.Homework.class_id == class_id).all()

@router.post("/submit", response_model=schemas.Submission)
def submit_homework(
    submission: schemas.SubmissionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["student"]))
):
    # Check if student belongs to the class of the homework
    hw = db.query(models.Homework).filter(models.Homework.id == submission.homework_id).first()
    if not hw:
        raise HTTPException(status_code=404, detail="Homework not found")
    
    new_sub = models.Submission(
        **submission.dict(),
        student_id=current_user.student_profile.id
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@router.patch("/grade/{submission_id}", response_model=schemas.Submission)
def grade_submission(
    submission_id: int,
    marks: int,
    feedback: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["teacher", "admin"]))
):
    db_sub = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    db_sub.marks = marks
    db_sub.feedback = feedback
    db.commit()
    db.refresh(db_sub)
    return db_sub
