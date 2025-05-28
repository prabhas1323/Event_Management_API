from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    return crud.update_event(db, event_id, event)

@router.get("/", response_model=list[schemas.EventResponse])
def get_events(status: str = None, location: str = None, db: Session = Depends(get_db)):
    return crud.list_events(db, status, location)
