from fastapi import APIRouter, Depends, status, HTTPException, Query, Response
from datetime import date
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.auth import get_current_user
from app.users.model import User
from app.tasks.model import Task, PrioEnum
from app.tasks.schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


#look for tasks by filters
@router.get("/tasks") 
def view_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), title:Optional[str] = None, priority : Optional[PrioEnum]= None, completed : Optional[bool]= None, due_date : Optional[date]= None):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if title: query = query.filter(Task.title == title)
    if priority: query = query.filter(Task.priority == priority)
    if completed is not None: query = query.filter(Task.completed == completed)
    if due_date: query = query.filter(Task.due_date <= due_date)
    return query.all()


#look for a specific task from ID
@router.get("/{task_id}") 
def get_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> TaskOut: 
    query = db.query(Task).filter(Task.user_id == current_user.id, Task.id == task_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO TASK FOUND")
    return query


#add task
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



#update task
@router.patch("/{task_id}")
def update_task(task_id:int, task_update: TaskUpdate, current_user: User = Depends(get_current_user), db:Session = Depends(get_db)) -> TaskOut:
    task = db.query(Task).filter(Task.user_id == current_user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO TASK FOUND")
    data = task_update.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


#delete task
@router.delete("/{task_id}")
def delete_task(task_id:int, current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.user_id == current_user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO TASK FOUND")
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)