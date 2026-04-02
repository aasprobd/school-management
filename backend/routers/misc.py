from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/misc",
    tags=["Miscellaneous Management"]
)

@router.get("/events", response_model=List[schemas.Event])
def get_events(db: Session = Depends(database.get_db)):
    return db.query(models.Event).all()

@router.post("/events", response_model=schemas.Event)
def create_event(event: schemas.EventBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/clubs", response_model=List[schemas.Club])
def get_clubs(db: Session = Depends(database.get_db)):
    return db.query(models.Club).all()

@router.post("/discipline", response_model=schemas.DisciplinaryRecord)
def record_discipline(record: schemas.DisciplinaryRecordBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_record = models.DisciplinaryRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
