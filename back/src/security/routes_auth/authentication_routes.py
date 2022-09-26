import json
import time

from fastapi import Depends, APIRouter, Form
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from src.config.database import get_db
from src.crud.user_crud import db_get_user_by_email, db_create_user_from_json
from src.schemas.token_schema import Token
from src.schemas.user_schema import UserSchema
from src.security.email import simple_send
from src.security.exceptions.user_exceptions import incorrect_password_exception, token_exception, \
    user_not_found_exception, user_already_exists_exception, error_sending_confirmation_code, error_confirmation_code
from src.security.helpers.auth_helpers import verify_password
from src.security.redis.storage import save_dict, get_data, delete_data

"""
Note: This is just a basic example how to enable cookies.
This is vulnerable to CSRF attacks, and should not be used this example.
"""

MINUTE = 60

router_auth = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


class User(BaseModel):
    username: str
    password: str


class ConfirmationCode(BaseModel):
    confirmation_code: str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()


@router_auth.post("/register_json", status_code=status.HTTP_200_OK)
async def init_register_user(user: UserSchema, db: Session = Depends(get_db)):
    usr = db_get_user_by_email(user.email, db)
    if usr:
        raise user_already_exists_exception
    try:
        email_sender = await simple_send(user)

        return {"message": email_sender.get('message')}
    except Exception as e:
        raise error_sending_confirmation_code


@router_auth.post("/register_json/verifyCode", status_code=status.HTTP_200_OK)
def verify_confirmation_code(code: ConfirmationCode, db: Session = Depends(get_db)):
    try:
        get_registration_data = json.loads(get_data(code.confirmation_code))
        usr = UserSchema
        usr.name = get_registration_data['name']
        usr.email = get_registration_data['email']
        usr.password = get_registration_data['password']

        user = db_create_user_from_json(usr, db)
        delete_data(code.confirmation_code)
    except Exception as e:
        raise error_confirmation_code

    return {"message": "User created", "user": user}


@router_auth.post('/login')
def login(user: User, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    username = user.username
    password = user.password

    usr = db_get_user_by_email(username, db)
    if data := get_data(usr.get('id')):
        expire_access_token = json.loads(data)['expire_access_token']
        timestamp = int(time.time())
        transurido_access_token = int((expire_access_token - timestamp) / MINUTE)
        if transurido_access_token < 0:
            delete_data(usr.get('id'))
        else:
            return {"message": "You have a started session"}

    if not usr:
        raise user_not_found_exception

    if not verify_password(password, usr.get('password')):
        raise incorrect_password_exception

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    save_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expire_access_token": Authorize.get_raw_jwt(access_token)['exp'],
        "expire_refresh_token": Authorize.get_raw_jwt(refresh_token)['exp']

    }

    save_dict(key=usr.get('id'), value=save_data)

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login", "token": Token(access_token=f'Bearer {access_token}')}


@router_auth.post("/login_form", status_code=status.HTTP_200_OK, response_model=Token)
def login(username: str = Form(default="email"),
          password: str = Form(default="password"),
          Authorize: AuthJWT = Depends(),
          db: Session = Depends(get_db)):

    user = db_get_user_by_email(username, db)
    if not user:
        raise user_not_found_exception
    if not verify_password(password, user.get('password')):
        raise incorrect_password_exception
    access_token = Authorize.create_access_token(subject=username)
    return Token(access_token=f"Bearer {access_token}")


@router_auth.delete('/logout')
def logout(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """

    try:
        Authorize.jwt_required()
    except Exception:
        raise token_exception

    current_user = Authorize.get_jwt_subject()
    usr = db_get_user_by_email(current_user, db)
    if get_data(usr.get('id')):
        delete_data(usr.get('id'))
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


@router_auth.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}


@router_auth.get('/protected', status_code=status.HTTP_200_OK, response_model=UserSchema)
def protected(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise token_exception

    current_user = Authorize.get_jwt_subject()
    usr = db_get_user_by_email(current_user, db)

    if not usr:
        raise user_not_found_exception
    return usr