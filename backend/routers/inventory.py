from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Management"]
)

@router.get("/", response_model=List[schemas.InventoryItem])
def get_inventory(db: Session = Depends(database.get_db)):
    return db.query(models.InventoryItem).all()

@router.post("/", response_model=schemas.InventoryItem)
def add_inventory_item(item: schemas.InventoryItemBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_item = models.InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.patch("/{item_id}/update-stock")
def update_stock(item_id: int, quantity: int, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.quantity += quantity
    db.commit()
    return {"message": "Stock updated", "new_quantity": db_item.quantity}
