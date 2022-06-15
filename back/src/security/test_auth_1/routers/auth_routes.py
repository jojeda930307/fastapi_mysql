from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from src.security.test_auth_1.helpers.auth_helpers import create_access_token, verify_password
from src.schemas.user_schema import UserSchema
from src.schemas.token_schema import Token
from src.crud.user_crud import db_get_user_by_id, db_create_user, db_get_user_by_email
from src.config.database import get_db
from src.security.test_auth_1.middleware.auth_middleware import is_autheticated
from src.security.test_auth_1.settings import Settings
from src.security.test_auth_1.exceptions.user_exceptions import user_not_found_exception, incorrect_password_exception, user_already_exists_exception


settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire

router_auth = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router_auth.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    user = db_get_user_by_email(email, db)
    if not user:
        raise user_not_found_exception
    if not verify_password(password, user.get('password')):
        raise incorrect_password_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": user.get('id'),
            "email" : user.get('email')
        },
        expires_delta=access_token_expires
    )
    return Token(access_token=f"Bearer {access_token}")


@router_auth.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
def register(body: UserSchema, db: Session = Depends(get_db)):
    user = db_create_user(body, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": user.id,
            "email" : user.email
        },
        expires_delta=access_token_expires
    )
    return Token(access_token=f"Bearer {access_token}")


@router_auth.get("/user", status_code=status.HTTP_200_OK, response_model=UserSchema)
def get_user(user_id: int = Depends(is_autheticated), db: Session = Depends(get_db)):
    user = db_get_user_by_email(user_id, db)
    print(user)
    if not user:
        raise user_not_found_exception
    return user