from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/staff",
    tags=["Staff Management"]
)

@router.post("/leave", response_model=schemas.LeaveRequest)
def request_leave(
    request: schemas.LeaveRequestBase,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    new_request = models.LeaveRequest(**request.dict(), user_id=current_user.id)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/leave", response_model=List[schemas.LeaveRequest])
def get_leave_requests(
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(dependencies.check_admin)
):
    return db.query(models.LeaveRequest).all()

@router.patch("/leave/{request_id}")
def update_leave_status(
    request_id: int,
    status: str,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(dependencies.check_admin)
):
    req = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = status
    db.commit()
    return {"message": f"Leave request {status}"}
