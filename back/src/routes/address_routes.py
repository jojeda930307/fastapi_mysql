from fastapi import APIRouter, Response, Depends

from starlette.status import HTTP_204_NO_CONTENT

from src.config.database import get_db
from src.models.address_model import AddressModel
from src.schemas.address_schema import AddressSchema
from sqlalchemy.orm import Session

address = APIRouter()


@address.get('/getAddress', response_model=list[AddressSchema], tags=['Address'])
async def list_address(db: Session = Depends(get_db)):
    """ Devuelve todas las direcciones """

    return db.query(AddressModel).all()


@address.get("/address/{id}", response_model=AddressSchema, tags=['Address'])
async def get_address_by_id(id: str, db: Session = Depends(get_db)):
    """ Devuelve una direción por su ID """

    return db.query(AddressModel).filter(AddressModel.id == id).first()


@address.post('/address', response_model=AddressSchema, tags=['Address'])
async def create_address(addr: AddressSchema, db: Session = Depends(get_db)):
    db_address = AddressModel(
        city=addr.city,
        location=addr.location,
        street=addr.street,
        flat=addr.flat,
        door=addr.door,
        postal_code=addr.postal_code
    )
    db.add(db_address)
    db.commit()

    address_inserted = db.query(AddressModel).where(AddressModel.id == db_address.id).first()
    return address_inserted


@address.put('/address/{id}', response_model=AddressSchema, tags=['Address'])
async def update_address(id: str, addr: AddressSchema, db: Session = Depends(get_db)):
    address_data = db.query(AddressModel).filter(AddressModel.id == id).first()

    address_data.city = addr.city
    address_data.location = addr.location
    address_data.street = addr.street
    address_data.flat = addr.flat
    address_data.door = addr.door
    address_data.postal_code = addr.postal_code

    db.commit()

    address_updated = db.query(AddressModel).where(AddressModel.id == id).first()
    return address_updated


@address.delete('/address/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Address'])
async def delete_address(id: str, db: Session = Depends(get_db)):
    address_data = db.query(AddressModel).filter(AddressModel.id == id).first()
    db.delete(address_data)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)