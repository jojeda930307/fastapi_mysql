from typing import Optional

from pydantic import BaseModel


class AddressSchema(BaseModel):
    """ El schema es la forma que tienen los datos de entrada/salida que usa la api para leer
    desde el cliente y devolver al mismo """

    id: Optional[int]
    city: str
    location: str
    street: str
    flat: str
    door: str
    postal_code: str
    user_id = int

    class Config:
        """ Configurando el orm_mode = True podemos interactuar con los datos de nuestro modelo,
        los datos de nuestro schema se adaptan al de nuestro modelo los cuales constituyen las
        tablas en base de datos """

        orm_mode = True


class AddressSchemaOut(BaseModel):
    city: str
    location: str
    street: str
    flat: str
    door: str
    postal_code: str
    user_id = int

    class Config:
        orm_mode = True