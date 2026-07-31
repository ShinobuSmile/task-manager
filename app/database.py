from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#stringa di connessione per PostgreSQL
DATABASE_URL = "postgresql://postgres:Elboss.2@localhost:5432/taskmanager"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass