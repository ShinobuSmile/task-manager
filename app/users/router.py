from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.users import schemas
from app.users.model import User
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # checks wheter username or email already exist
    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}