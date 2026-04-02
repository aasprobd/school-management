from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(prefix="/cms", tags=["Website CMS"])

@router.get("/pages/{slug}", response_model=schemas.PageContent)
def get_page(slug: str, db: Session = Depends(database.get_db)):
    page = db.query(models.PageContent).filter(models.PageContent.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.post("/pages", response_model=schemas.PageContent)
def update_page(page: schemas.PageContentBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_page = db.query(models.PageContent).filter(models.PageContent.slug == page.slug).first()
    if db_page:
        db_page.title = page.title
        db_page.body = page.body
    else:
        db_page = models.PageContent(**page.dict())
        db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page
