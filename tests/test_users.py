from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.users.model import User
from sqlalchemy.pool import StaticPool

client = TestClient(app)


DATABASE_TEST_URL = "sqlite:///:memory:"
engine_test = create_engine(
    DATABASE_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
Base.metadata.create_all(bind=engine_test)


def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_register_user():
    result = client.post("/users/",json={ "username": "testuser", "email": "test@example.com", "password": "TestPass123"})
    assert result.status_code == 200
    data = result.json()
    assert data["id"] == 1
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"