from fastapi import HTTPException, status, Header, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.config.database import get_db
import os

from src.security.test_auth_1.exceptions.user_exceptions import token_exception
from src.security.test_auth_1.settings import Settings

settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire


async def is_autheticated(authorization: str = Header(...), db: Session = Depends(get_db)):
    token: str = authorization.split()[-1]
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload.get("email")
    except JWTError:
        raise token_exception