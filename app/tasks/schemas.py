from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.tasks.model import PrioEnum

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: PrioEnum

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: PrioEnum
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}