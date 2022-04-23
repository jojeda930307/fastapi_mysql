from fastapi import HTTPException, status

from src.models.user_model import UserModel
from src.schemas.user_schema import UserSchema
from src.security.test_auth_2.auth_service import get_password_hash


def create_user(user: UserSchema, db):
    """ Verifica que el usuario que se está creando no esté no base de datos en caso contrario
        devuelve un mensaje de que el usuario existe
    """

    get_user = db.query(UserModel).filter((UserModel.email == user.email) | (UserModel.name == user.name)).first()
    if get_user:
        msg = "Email already registered"
        if get_user.name == user.name:
            msg = "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    db_user = UserModel(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()

    user_inserted = db.query(UserModel).where(UserModel.id == db_user.id).first()

    return user_inserted




