from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.users.model import User
from sqlalchemy.pool import StaticPool
import pytest

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


#test for user registration
def test_register_user():
    result = client.post("/users/",json={"username": "testuser", "email": "test@example.com", "password": "TestPass123"})
    assert result.status_code == 200
    data = result.json()
    assert data["id"] == 1
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


#test for login
def test_login_user():
    result = client.post("/users/login", json={"username": "testuser", "email": "test@example.com", "password": "TestPass123"})
    assert result.status_code == 200
    data = result.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0
    assert data["token_type"] == "bearer"



#test for login with wrong credentials
@pytest.mark.parametrize("username, email, password, expected_status", [
    ("wrong", "test@example.com", "TestPass123", 401),
    ("testuser", "wrong@example.com", "TestPass123", 401),
    ("testuser", "test@example.com", "WrongPass", 401),
])
def test_login_failures(username, email, password, expected_status):
    result = client.post("/users/login", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert result.status_code == expected_status