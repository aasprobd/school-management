from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import database, models, dependencies

router = APIRouter(prefix="/analytics", tags=["Reporting & Analytics"])

@router.get("/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    return {
        "total_students": db.query(models.Student).count(),
        "total_teachers": db.query(models.Teacher).count(),
        "active_notices": db.query(models.Notice).count(),
        "unpaid_invoices": db.query(models.Invoice).filter(models.Invoice.status == "unpaid").count(),
        "total_revenue": db.query(models.Payment).with_entities(func.sum(models.Payment.amount)).scalar() or 0
    }

@router.get("/fee-analysis")
def get_fee_analysis(db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    # Compares income vs pending fees
    collected = db.query(models.Payment).with_entities(func.sum(models.Payment.amount)).scalar() or 0
    pending = db.query(models.Invoice).filter(models.Invoice.status == "unpaid").with_entities(func.sum(models.Invoice.amount)).scalar() or 0
    return {
        "collected_fees": collected,
        "pending_fees": pending,
        "collection_rate": (collected / (collected + pending)) * 100 if (collected + pending) > 0 else 0
    }
