from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_track_event():
    response = client.post("/track-event", json={
        "user_id": "test123",
        "event_type": "click",
        "page_url": "https://example.com",
        "device_type": "desktop",
        "metadata": {"section": "header"}
    })
    assert response.status_code == 200
    assert "message" in response.json()

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
