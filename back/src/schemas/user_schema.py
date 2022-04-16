from typing import Optional, List

from pydantic import BaseModel

from src.schemas.address_schema import AddressSchemaOut
from src.schemas.product_schema import ProductSchemaOut


class UserSchema(BaseModel):
    id: Optional[int]
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
    order: List[ProductSchemaOut] = None

    class Config:
        orm_mode = True