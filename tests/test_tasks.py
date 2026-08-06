from fastapi import Depends
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.users.model import User
from sqlalchemy.pool import StaticPool
from app.tasks.model import Task
from app.auth import create_access_token
from app.security import hash_password
from typing import Optional
from datetime import date
from app.tasks.model import PrioEnum
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

def create_user(username: str, email: str, password: str) -> User:
    db = SessionTest()
    hashed = hash_password(password)
    user = User(username=username, email=email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_task(user_id, title: str, priority: PrioEnum, description: Optional[str]=None, due_date: Optional[date]=None) -> Task:
    db = SessionTest()
    task = Task(title = title, description=description, due_date = due_date, priority = priority, completed = False, user_id = user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


#test for task creation
def test_create_task():
    user = create_user("taskuser", "task@example.com", "TaskPass123")
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"title": "Test task", "priority": "high"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["user_id"] == user.id
    assert data["completed"] == False

#test to get a single task from its id
def test_get_task():
    user = create_user("taskuser2", "task@example.com2", "TaskPass1232")
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}
    task = create_task(user_id=user.id, title="test2",priority="low",description="Test task2")
    response = client.get(f"/tasks/{task.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "priority" in data
    assert "user_id" in data
    assert data["id"] == task.id


#update only one field
def test_update_task():
    user = create_user("taskuser3", "task@example.com3", "TaskPass1233")
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}
    task = create_task(user_id=user.id, title="test3",priority="low",description="Test task3")
    update = {"title": "Updated Title"}
    response = client.patch(f"/tasks/{task.id}", json=update, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "priority" in data
    assert data["title"] == "Updated Title"
    assert data["id"] == task.id
    assert data ["user_id"] == task.user_id
    assert data["updated_at"] is not None


#update all fields
def test_update_task_all_fields():
    user = create_user("fullupdate", "full@example.com", "FullPass123")
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}
    task = create_task(
        user_id=user.id,
        title="original title",
        priority="low",
        description="original description"
    )
    update_data = {
        "title": "new title",
        "description": "new description",
        "priority": "high",
        "due_date": "2026-12-31",
        "completed": True
    }
    response = client.patch(f"/tasks/{task.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "new title"
    assert data["description"] == "new description"
    assert data["priority"] == "high"
    assert data["due_date"] == "2026-12-31"
    assert data["completed"] is True

    assert data["id"] == task.id
    assert data["user_id"] == task.user_id
    assert data["created_at"] == task.created_at.isoformat()

    assert data["updated_at"] is not None
    assert data["updated_at"] != task.updated_at  


#delete test
def test_delete_task():
    user = create_user("deleteuser", "delete@example.com", "DeletePass123")
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}
    task = create_task(user_id=user.id, title="Task to delete", priority="low")
    response = client.delete(f"/tasks/{task.id}", headers=headers)
    assert response.status_code == 204
    response = client.get(f"/tasks/{task.id}", headers=headers)
    assert response.status_code == 404

#filter list test
@pytest.mark.parametrize("priority_value", ["high", "medium", "low"])
def test_filter_tasks_by_priority(priority_value):
    user = create_user(f"filteruser_{priority_value}", f"filter_{priority_value}@example.com", "FilterPass123")
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}
    create_task(user_id=user.id, title="High priority task", priority="high")
    create_task(user_id=user.id, title="Medium priority task", priority="medium")
    create_task(user_id=user.id, title="Low priority task", priority="low")
    response = client.get(f"/tasks/tasks?priority={priority_value}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1     # We expect exactly one task matching the requested priority
    assert data[0]["priority"] == priority_value


#test authorization
def test_unauthorized_task_access():
    user1 = create_user("owner", "owner@example.com", "OwnerPass123")# two users
    user2 = create_user("intruder", "intruder@example.com", "IntruderPass123")
    task = create_task(user_id=user1.id, title="Private task", priority="high")#task from user 1
    token = create_access_token(user2.id)#token from user 2
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/tasks/{task.id}", headers=headers)#user 1's task with user 2's token
    assert response.status_code == 404  
    response = client.patch(f"/tasks/{task.id}", json={"title": "Hacked"}, headers=headers)#update user 1 task with user 2's token
    assert response.status_code == 404
    response = client.delete(f"/tasks/{task.id}", headers=headers)#delete user 1's task with user 2's token
    assert response.status_code == 404