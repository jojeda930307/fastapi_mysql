from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: Optional[int]
    image: str
    description: str
    price: float
    user_id = int

    class Config:
        orm_mode = True


class ProductSchemaOut(BaseModel):
    image: str
    description: str
    price: float

    class Config:
        orm_mode = True