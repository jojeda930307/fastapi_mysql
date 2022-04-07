from fastapi import APIRouter, Response, Depends

from starlette.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED

from src.config.database import get_db
from src.crud.address_crud import db_list_address, db_get_address_by_id, db_create_address, db_update_address, \
    db_delete_address

from src.schemas.address_schema import AddressSchema, AddressSchemaOut
from sqlalchemy.orm import Session

address = APIRouter()


@address.get('/getAddress', response_model=list[AddressSchema], tags=['Address'])
async def list_address(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """ Devuelve todas las direcciones """

    result = db_list_address(skip, limit, db)
    return result


@address.get("/address/{id}", response_model=AddressSchema, tags=['Address'])
async def get_address_by_id(id: str, db: Session = Depends(get_db)):
    """ Devuelve una direción por su ID """

    result = db_get_address_by_id(id, db)
    if not result:
        return Response(content='The address selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return result


@address.post('/address/{user_id}', response_model=AddressSchemaOut, tags=['Address'])
async def create_address(user_id: int, addr: AddressSchema, db: Session = Depends(get_db)):

    result = db_create_address(user_id, addr, db)
    if not result:
        return Response(content='Cannot create an address if the user that does not exist', status_code=HTTP_202_ACCEPTED)
    return result


@address.put('/address/{id}', response_model=AddressSchema, tags=['Address'])
async def update_address(id: str, addr: AddressSchema, db: Session = Depends(get_db)):

    result = db_update_address(id, addr, db)
    if not result:
        return Response(content='The address selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return result


@address.delete('/address/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Address'])
async def delete_address(id: str, db: Session = Depends(get_db)):

    result = db_delete_address(id, db)
    if not result:
        return Response(content='The address selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return Response(status_code=HTTP_204_NO_CONTENT)