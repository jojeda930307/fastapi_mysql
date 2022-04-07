from fastapi import APIRouter, Response, Depends

from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED

from src.config.database import get_db
from src.crud.user_crud import db_list_users, db_get_user_by_id, db_create_user, db_update_user, db_delete_user
from src.schemas.user_schema import UserSchema, UserSchemaOut


user = APIRouter()


@user.get('/getUsers', response_model=list[UserSchemaOut], tags=['Users'])
async def list_users(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    """ Devuelve todos los usuarios """

    result = db_list_users(skip, limit, db)
    return result


@user.get("/user/{id}", response_model=UserSchemaOut, tags=['Users'])
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
    """ Devuelve un usuario por su ID """

    result = db_get_user_by_id(id, db)
    if not result:
        return Response(content='The user selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return result


@user.post('/user', response_model=UserSchema, tags=['Users'])
async def create_user(user_: UserSchema, db: Session = Depends(get_db)):
    """ Inserta un nuevo usuario en la base de datos """

    result = db_create_user(user_, db)
    return result


@user.put('/user/{id}', response_model=UserSchema, tags=['Users'])
async def update_user(id: int, user_: UserSchema, db: Session = Depends(get_db)):
    
    result = db_update_user(id, user_, db)
    if not result:
        return Response(content='The user selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return result


@user.delete('/user/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Users'])
async def delete_user(id: str, db: Session = Depends(get_db)):

    result = db_delete_user(id, db)
    if not result:
        return Response(content='The user selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return Response(status_code=HTTP_204_NO_CONTENT)

