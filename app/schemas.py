from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from .models import EventStatus

# Attendee Schemas
class AttendeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class AttendeeCreate(AttendeeBase):
    event_id: int

class AttendeeResponse(AttendeeBase):
    attendee_id: int
    check_in_status: bool

    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    status: EventStatus

class EventResponse(EventBase):
    event_id: int
    status: EventStatus
    attendees: List[AttendeeResponse] = []

    class Config:
        orm_mode = True
