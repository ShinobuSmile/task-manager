from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(30), nullable=False) #temporarily not encrypted