from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from app.tasks.model import PrioEnum

class TaskCreate(BaseModel):
    title: str = Field(description="Short description of the task", example="Buy groceries")
    description: Optional[str] = Field(default=None, description="Detailed notes about the task (optional)", example="Milk, eggs, bread, and butter")
    due_date: Optional[date] = Field(default=None, description="Deadline for completing the task (optional)", example="2026-08-15")
    priority: PrioEnum = Field(description="How urgent the task is", example="low")

class TaskOut(BaseModel):
    id: int = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    due_date: Optional[date] = Field(default=None, description="Due date")
    priority: PrioEnum = Field(description="Priority level")
    completed: bool = Field(description="Completion status")
    user_id: int = Field(description="Owner's user ID")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")

    model_config = {"from_attributes": True}

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="New title", example="Updated title")
    description: Optional[str] = Field(default=None, description="New description", example="Updated notes")
    due_date: Optional[date] = Field(default=None, description="New due date", example="2026-08-20")
    priority: Optional[PrioEnum] = Field(default=None, description="New priority (high, medium, low)", example="high")
    completed: Optional[bool] = Field(default=None, description="Mark as completed (true or false)", example="true")