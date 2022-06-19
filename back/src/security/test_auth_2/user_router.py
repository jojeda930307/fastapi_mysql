from fastapi import APIRouter, Depends, Body, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.config.database import get_db
from src.schemas.user_schema import UserSchema
from src.security.test_auth_2 import auth_service, user_service
from src.security.test_auth_2.token_schema import Token

router1 = APIRouter(prefix="/api/v1")


@router1.post(
    "/user/")
def create_user(user: str = Form(default="Username"), passwd: str = Form(default="Password"), db: Session = Depends(get_db)):
    """
    ## Create a new user in the app

    ### Args
    The app can recive next fields into a JSON
    - email: A valid email
    - name: Unique username
    - password: Strong password for authentication

    ### Returns
    - user: User info
    """
    return user_service.create_user(username, password, db)


@router1.post(
    "/test_auth_1",
    tags=["test_auth_users"],
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    ## Login for access token

    ### Args
    The app can recive next fields by form data
    - username: Your username or email
    - password: Your password

    ### Returns
    - access token and token type
    """
    access_token = auth_service.generate_token(form_data.username, form_data.password, db)
    return Token(access_token=access_token, token_type="bearer")