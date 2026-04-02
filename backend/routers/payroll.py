from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/payroll",
    tags=["Payroll Management"]
)

@router.get("/", response_model=List[schemas.Payroll])
def get_payroll_history(db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    return db.query(models.Payroll).all()

@router.post("/disburse")
def disburse_salary(user_id: int, amount: int, month: int, year: int, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    # Check if payroll already exists for this person/month/year
    existing = db.query(models.Payroll).filter(
        models.Payroll.user_id == user_id, 
        models.Payroll.month == month, 
        models.Payroll.year == year
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Salary already disbursed for this month")
    
    payroll = models.Payroll(user_id=user_id, amount=amount, month=month, year=year)
    db.add(payroll)
    db.commit()
    return {"message": "Salary disbursed"}
