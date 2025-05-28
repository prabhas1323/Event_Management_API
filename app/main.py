from fastapi import FastAPI
from .database import Base, engine
from .routers import events, attendees
from .crud import auto_complete_events
from sqlalchemy.orm import Session
from .database import SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

app.include_router(events.router)
app.include_router(attendees.router)

@app.on_event("startup")
def auto_update_event_status():
    db = SessionLocal()
    auto_complete_events(db)
