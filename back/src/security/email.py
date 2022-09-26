import uuid

from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from src.security.redis.storage import save_dict

router_email = APIRouter(
    prefix="/api/v1",
    tags=["email"]
)


conf = ConnectionConfig(
    MAIL_USERNAME="email.fastapi@gmail.com",
    MAIL_PASSWORD="wsuihvagjhlooutz",  # Contraseña de aplicación obtenida en la configuración de la cuenta de Google.
    MAIL_FROM="email.fastapi@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Ojeda_Signature",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


def get_confirmation_code():
    return str(uuid.uuid4())[24:]


async def simple_send(user):
    confirmation_code = get_confirmation_code()

    message = MessageSchema(
        subject="Ojeda App",
        recipients=[user.email],  # List of recipients, as many as you can pass
        body=f"""Código de confirmación: {confirmation_code}""",
        subtype="text"
        )

    fm = FastMail(conf)
    await fm.send_message(message)

    save_data = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "confirmation_code": confirmation_code
    }
    save_dict(save_data["confirmation_code"], save_data)
    return {"message": "Introduzca el código de confirmación enviado a tú correo"}