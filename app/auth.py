import os
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.users.model import User
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key")


def create_access_token(user_id: int, expires_delta: Optional[timedelta]=None) -> str:
    sub = str(user_id)
    now = datetime.now(timezone.utc)
    if not expires_delta: #if timedelta is not specified by default the auth lasts 30 minutes
        exp = now + timedelta(minutes=30)
    else:
        exp = now + expires_delta
    to_encode = {
        "sub" : sub,
        "exp" : exp.timestamp(),
        "iat" : now.timestamp()
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)) ->User:
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"],)
        user_id = int(decoded_token["sub"])
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="USER DOES NOT EXIST")
    except (ExpiredSignatureError, JWTError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="EXPIRED TOKEN")
    return user