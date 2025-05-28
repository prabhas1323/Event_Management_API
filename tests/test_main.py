from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/events/", json={
        "name": "Test Event",
        "description": "Testing",
        "start_time": "2025-06-01T10:00:00",
        "end_time": "2025-06-01T12:00:00",
        "location": "Online",
        "max_attendees": 10
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"
