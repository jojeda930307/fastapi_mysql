from fastapi import APIRouter, Response, Depends

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from src.config.database import get_db
from src.models.user_model import UserModel
from src.schemas.user_schema import UserSchema


key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get('/getUsers', response_model=list[UserSchema], tags=['Users'])
async def list_users(db: Session = Depends(get_db)):
    """ Devuelve todos los usuarios """

    return db.query(UserModel).all()


@user.get("/user/{id}", response_model=UserSchema, tags=['Users'])
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
    """ Devuelve un usuario por su ID """

    return db.query(UserModel).filter(UserModel.id == id).first()


@user.post('/user', response_model=UserSchema, tags=['Users'])
async def create_user(user_: UserSchema, db: Session = Depends(get_db)):
    """ Inserta un nuevo usuario en la base de datos """

    user_data = UserModel(name=user_.name, email=user_.email, password=f.encrypt(user_.password.encode('utf-8')))
    db.add(user_data)
    db.commit()

    user_inserted = db.query(UserModel).where(UserModel.id == user_data.id).first()
    return user_inserted


@user.put('/user/{id}', response_model=UserSchema, tags=['Users'])
async def update_user(id: str, user_: UserSchema, db: Session = Depends(get_db)):
    
    user_data = db.query(UserModel).filter(UserModel.id == id).first()

    user_data.name = user_.name
    user_data.email = user_.email
    user_data.password = user_.password

    db.commit()

    user_updated = db.query(UserModel).where(UserModel.id == id).first()
    return user_updated


@user.delete('/user/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Users'])
async def delete_user(id: str, db: Session = Depends(get_db)):

    user_data = db.query(UserModel).filter(UserModel.id == id).first()
    db.delete(user_data)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

