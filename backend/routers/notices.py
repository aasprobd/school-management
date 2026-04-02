from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/notices",
    tags=["Notice Board"]
)

@router.get("/", response_model=List[schemas.Notice])
def get_notices(db: Session = Depends(database.get_db)):
    return db.query(models.Notice).all()

@router.post("/", response_model=schemas.Notice)
def create_notice(
    notice: schemas.NoticeCreate, 
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(dependencies.check_admin)
):
    new_notice = models.Notice(
        title=notice.title,
        content=notice.content,
        author_id=admin.id
    )
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

@router.delete("/{notice_id}")
def delete_notice(
    notice_id: int, 
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(dependencies.check_admin)
):
    db_notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if not db_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    db.delete(db_notice)
    db.commit()
    return {"message": "Notice deleted"}
