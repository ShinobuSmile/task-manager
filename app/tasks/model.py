from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


#CLASS FOR PRIORITY ENUM
class PrioEnum(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


#CREATING THE TABLE "TASKS"
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    priority = Column(Enum(PrioEnum), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())