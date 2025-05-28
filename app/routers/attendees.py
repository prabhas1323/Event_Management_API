from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/attendees", tags=["Attendees"])

@router.post("/", response_model=schemas.AttendeeResponse)
def register_attendee(attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    return crud.register_attendee(db, attendee)

@router.post("/{attendee_id}/checkin", response_model=schemas.AttendeeResponse)
def checkin_attendee(attendee_id: int, db: Session = Depends(get_db)):
    return crud.check_in_attendee(db, attendee_id)

@router.get("/event/{event_id}", response_model=list[schemas.AttendeeResponse])
def get_attendees(event_id: int, db: Session = Depends(get_db)):
    return crud.list_attendees(db, event_id)
