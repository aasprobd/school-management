from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from services.notification_service import NotificationService
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications & Alerts"])

@router.get("/", response_model=List[schemas.Notification])
def get_my_notifications(db: Session = Depends(database.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).all()

@router.post("/send")
def send_custom_notification(user_id: int, message: str, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Save to DB
    new_notif = models.Notification(user_id=user_id, message=message)
    db.add(new_notif)
    db.commit()
    
    # Trigger Gateway
    NotificationService.send_notification(user.email, message)
    
    return {"status": "sent"}
