from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import database, models, schemas, dependencies
from typing import List
import uuid, datetime

router = APIRouter(
    prefix="/finance",
    tags=["Finance & Payments"]
)

@router.post("/invoices", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_invoice = models.Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.post("/pay/{invoice_id}")
def process_payment(invoice_id: int, method: str, db: Session = Depends(database.get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id, models.Invoice.status == "unpaid").first()
    if not invoice:
        raise HTTPException(status_code=400, detail="Invoce not found or already paid")
    
    # Mocking a payment transaction
    payment = models.Payment(
        invoice_id=invoice_id,
        amount=invoice.amount,
        method=method,
        transaction_id=str(uuid.uuid4())
    )
    invoice.status = "paid"
    db.add(payment)
    db.commit()
    return {"message": "Payment successful", "transaction_id": payment.transaction_id}

@router.post("/expenses", response_model=schemas.Expense)
def record_expense(expense: schemas.ExpenseBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.post("/batch-invoice-monthly")
def batch_invoice_monthly(amount: int, due_date: datetime.datetime, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    students = db.query(models.Student).all()
    invoices = []
    for student in students:
        invoice = models.Invoice(
            student_id=student.id,
            amount=amount,
            type="Monthly",
            due_date=due_date
        )
        db.add(invoice)
        invoices.append(invoice)
    db.commit()
    return {"message": f"Generated {len(invoices)} monthly invoices"}

@router.get("/report/income-expense")
def get_financial_report(db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    total_income = db.query(models.Payment).with_entities(func.sum(models.Payment.amount)).scalar() or 0
    total_expense = db.query(models.Expense).with_entities(func.sum(models.Expense.amount)).scalar() or 0
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_profit": total_income - total_expense
    }

@router.get("/ledger/student/{student_id}", response_model=List[schemas.Invoice])
def get_student_ledger(student_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Invoice).filter(models.Invoice.student_id == student_id).all()
