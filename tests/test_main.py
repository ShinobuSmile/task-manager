from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_status():
    result = client.get("/status")
    assert result.status_code == 200
    data = result.json()
    assert data["status"] == "ok"
    assert data["service"] == "Task Manager API"