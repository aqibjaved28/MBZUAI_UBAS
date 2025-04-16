from fastapi.testclient import TestClient
from main import app
import uuid
from datetime import datetime, timezone

client = TestClient(app)

def test_track_event_minimal():
    response = client.post("/track-event", json={
        "id": str(uuid.uuid4()),
        "user_id": "test121",
        "event_type": "click",
        "page_url": "https://example.com",
        "device_type": "desktop",
        "metadata": {"section": "header"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip_address": "127.0.0.1"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_track_event_sample_data():
    sample_data = {
        "id": str(uuid.uuid4()),
        "user_id": "user122",
        "event_type": "click",
        "page_url": "https://example.com",
        "device_type": "mobile",
        "metadata": {
            "button_id": "btn-42",
            "duration": 3.5
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip_address": "192.168.0.1"
    }
    response = client.post("/track-event", json=sample_data)
    assert response.status_code == 200
    assert "message" in response.json()

def test_missing_user_id():
    response = client.post("/track-event", json={
        "event_type": "click"
    })
    assert response.status_code == 422

def test_invalid_timestamp():
    data = {
        "id": str(uuid.uuid4()),
        "user_id": "user123",
        "event_type": "click",
        "page_url": "https://example.com",
        "device_type": "mobile",
        "metadata": {},
        "timestamp": "invalid-timestamp",
        "ip_address": "127.0.0.1"
    }
    response = client.post("/track-event", json=data)
    assert response.status_code == 422

def test_query_events():
    response = client.get("/query-events")
    assert response.status_code == 200
    assert "results" in response.json()

def test_aggregate_events():
    response = client.get("/aggregate-events")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
