from fastapi import Header
from fastapi_jwt_auth import AuthJWT
from jose import JWTError

from src.security.exceptions.user_exceptions import token_exception
from src.security.settings import Settings

settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire


# Probar hacer un is_init_register y guardar los códigos de confirmación en un token que se devolverá al cliente
# luego el cliente enviará dicho token en en un header o cookie junto con el código de confirmación en una petición
# POST. Comprobamos que sean iguales y creamos el usuario. De esta manera nos ahorramos usar redis.

async def is_autheticated(authorization: str = Header(...)):
    token: str = authorization.split()[-1]
    auth_token = AuthJWT()
    try:
        jti = auth_token.get_raw_jwt(encoded_token=token)
        return jti
    except JWTError:
        raise token_exception

