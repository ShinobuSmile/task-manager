from fastapi import APIRouter, Depends, status, HTTPException, Query
from datetime import date
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.auth import get_current_user
from app.users.model import User
from app.tasks.model import Task, PrioEnum
from app.tasks.schemas import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/tasks")
def view_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), title:Optional[str] = None, priority : Optional[PrioEnum]= None, completed : Optional[bool]= None, due_date : Optional[date]= None):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if title: query = query.filter(Task.title == title)
    if priority: query = query.filter(Task.priority == priority)
    if completed is not None: query = query.filter(Task.completed == completed)
    if due_date: query = query.filter(Task.due_date <= due_date)
    return query.all()

@router.post("/")
def add_tasks(task_data: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> TaskOut:
    uid = current_user.id
    task = Task(
        title = task_data.title,
        description = task_data.description,
        due_date = task_data.due_date,
        priority = task_data.priority,
        completed = False,
        user_id = uid,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
