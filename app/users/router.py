from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.users.schemas import UserLogin, Token, UserCreate
from app.users.model import User
from app.security import hash_password, verify_password
from app.auth import create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # checks wheter username or email already exist
    db_user = User(
        username = user.username,
        email = user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_login.username, User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Credentials")
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Credentials")
    access_token = create_access_token(user.id)
    return {"access_token" : access_token, "token_type": "bearer"}

@router.get("/me")
def user_logged_in(current_user: User = Depends(get_current_user)) -> dict:
    user_credentials = {
        "id" : current_user.id,
        "username" : current_user.username,
        "email" : current_user.email
    }
    return user_credentials