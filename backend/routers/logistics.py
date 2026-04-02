from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(prefix="/logistics", tags=["Logistics & Facilities"])

@router.post("/transport", response_model=schemas.TransportRoute)
def add_route(route: schemas.TransportRouteBase, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    new_route = models.TransportRoute(**route.dict())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@router.get("/transport", response_model=List[schemas.TransportRoute])
def get_routes(db: Session = Depends(database.get_db)):
    return db.query(models.TransportRoute).all()

@router.post("/hostel/rooms")
def add_hostel_room(room_no: str, capacity: int, db: Session = Depends(database.get_db), admin: models.User = Depends(dependencies.check_admin)):
    new_room = models.HostelRoom(room_no=room_no, capacity=capacity)
    db.add(new_room)
    db.commit()
    return {"message": "Room added"}
