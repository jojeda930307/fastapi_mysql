from cryptography.fernet import Fernet

from src.models.address_model import AddressModel
from src.models.user_model import UserModel

key = Fernet.generate_key()
f = Fernet(key)


def db_list_address(skip, limit, db):
    return db.query(AddressModel).offset(skip).limit(limit).all()


def db_get_address_by_id(id, db):
    address = db.query(AddressModel).filter(AddressModel.id == id).first()
    if not address:
        return False
    return address


def db_create_address(user_id, addr, db):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return False
    db_address = AddressModel(
        city=addr.city,
        location=addr.location,
        street=addr.street,
        flat=addr.flat,
        door=addr.door,
        postal_code=addr.postal_code,
        user_id=user_id
    )
    db.add(db_address)
    db.commit()

    address_inserted = db.query(AddressModel).where(AddressModel.id == db_address.id).first()
    return address_inserted


def db_update_address(id, addr, db):
    address_data = db.query(AddressModel).filter(AddressModel.id == id).first()

    if not address_data:
        return False
    address_data.city = addr.city
    address_data.location = addr.location
    address_data.street = addr.street
    address_data.flat = addr.flat
    address_data.door = addr.door
    address_data.postal_code = addr.postal_code

    db.commit()

    address_updated = db.query(AddressModel).where(AddressModel.id == id).first()
    return address_updated


def db_delete_address(id, db):
    address_data = db.query(AddressModel).filter(AddressModel.id == id).first()
    if not address_data:
        return False
    db.delete(address_data)
    db.commit()
    return address_data
