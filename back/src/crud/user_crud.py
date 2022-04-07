from cryptography.fernet import Fernet

from src.models.user_model import UserModel

key = Fernet.generate_key()
f = Fernet(key)


def db_list_users(skip, limit, db):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return [{
        'name': usr.name,
        'email': usr.email,
        'password': usr.password,
        'address': {
            'city': usr.address_[0].city,
            'location': usr.address_[0].location,
            'street': usr.address_[0].street,
            'flat': usr.address_[0].flat,
            'door': usr.address_[0].door,
            'postal_code': usr.address_[0].postal_code
        } if usr.address_ else None
    } for usr in users]


def db_get_user_by_id(id, db):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        return False
    return {
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'address': {
            'city': user.address_[0].city,
            'location': user.address_[0].location,
            'street': user.address_[0].street,
            'flat': user.address_[0].flat,
            'door': user.address_[0].door,
            'postal_code': user.address_[0].postal_code
        } if user.address_ else None
    }


def db_create_user(user_, db):
    user_data = UserModel(name=user_.name, email=user_.email, password=f.encrypt(user_.password.encode('utf-8')))
    db.add(user_data)
    db.commit()

    user_inserted = db.query(UserModel).where(UserModel.id == user_data.id).first()
    return user_inserted


def db_update_user(id, user_, db):
    user_data = db.query(UserModel).filter(UserModel.id == id).first()

    if not user_data:
        return False
    user_data.name = user_.name
    user_data.email = user_.email
    user_data.password = f.encrypt(user_.password.encode('utf-8'))

    db.commit()

    user_updated = db.query(UserModel).where(UserModel.id == id).first()
    return user_updated


def db_delete_user(id, db):
    user_data = db.query(UserModel).filter(UserModel.id == id).first()
    if not user_data:
        return False
    db.delete(user_data)
    db.commit()
    return user_data
