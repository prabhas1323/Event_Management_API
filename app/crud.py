from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from fastapi import HTTPException, status

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def register_attendee(db: Session, attendee: schemas.AttendeeCreate):
    db_event = db.query(models.Event).filter(models.Event.event_id == attendee.event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if len(db_event.attendees) >= db_event.max_attendees:
        raise HTTPException(status_code=400, detail="Event is full")

    db_attendee = models.Attendee(**attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

def check_in_attendee(db: Session, attendee_id: int):
    attendee = db.query(models.Attendee).filter(models.Attendee.attendee_id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    attendee.check_in_status = True
    db.commit()
    return attendee

def list_events(db: Session, status=None, location=None):
    query = db.query(models.Event)
    if status:
        query = query.filter(models.Event.status == status)
    if location:
        query = query.filter(models.Event.location == location)
    return query.all()

def list_attendees(db: Session, event_id: int):
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id).all()

def auto_complete_events(db: Session):
    now = datetime.utcnow()
    db.query(models.Event).filter(
        models.Event.end_time < now,
        models.Event.status == models.EventStatus.scheduled
    ).update({models.Event.status: models.EventStatus.completed})
    db.commit()
            