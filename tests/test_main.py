from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.database import Base

client = TestClient(app)
DATABASE_TEST_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_TEST_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def test_status():
    result = client.get("/status")
    assert result.status_code == 200
    data = result.json()
    assert data["status"] == "ok"
    assert data["service"] == "Task Manager API"