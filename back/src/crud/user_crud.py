from cryptography.fernet import Fernet
from passlib.context import CryptContext
from src.models.user_model import UserModel

key = Fernet.generate_key()
f = Fernet(key)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
            'postal_code': usr.address_[0].postal_code,
        } if usr.address_ else None,
        'order': [{
            'image': it.image,
            'description': it.description,
            'price': it.price,
        } if usr.user_order else None for it in usr.user_order]
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
            'postal_code': user.address_[0].postal_code,
        } if user.address_ else None,
        'order': [{
            'image': it.image,
            'description': it.description,
            'price': it.price,
        } if user.user_order else None for it in user.user_order]
    }


def db_get_user_by_email(email, db):
    user = db.query(UserModel).filter(UserModel.email == email).first()
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
            'postal_code': user.address_[0].postal_code,
        } if user.address_ else None,
        'order': [{
            'image': it.image,
            'description': it.description,
            'price': it.price,
        } if user.user_order else None for it in user.user_order]
    }


def db_create_user_from_json(user_, db):
    user_data = UserModel(name=user_.name, email=user_.email, password=pwd_context.hash(user_.password.encode('utf-8')))
    db.add(user_data)
    db.commit()

    user_inserted = db.query(UserModel).where(UserModel.id == user_data.id).first()
    return user_inserted


def db_create_user_from_form(name, email, password, db):
    user_data = UserModel(name=name, email=email, password=pwd_context.hash(password.encode('utf-8')))
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
