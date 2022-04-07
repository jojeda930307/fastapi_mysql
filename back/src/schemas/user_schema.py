from typing import Optional

from pydantic import BaseModel

from src.schemas.address_schema import AddressSchema, AddressSchemaOut


class UserSchema(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserSchemaOut(BaseModel):
    name: str
    email: str
    password: str
    address: AddressSchemaOut = None

    class Config:
        orm_mode = True