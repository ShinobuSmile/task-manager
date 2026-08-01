import os
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

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