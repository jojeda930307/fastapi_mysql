from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED

from src.config.database import get_db
from src.crud.product_crud import db_delete_product, db_update_product, db_list_product, db_get_product_by_id, \
    db_create_product
from src.schemas.product_schema import ProductSchema

product = APIRouter()


@product.get('/getProducts', response_model=list[ProductSchema], tags=['Products'])
async def list_products(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    """ Devuelve todos los productos """
    result = db_list_product(skip, limit, db)
    return result


@product.get("/product/{product_id}", response_model=ProductSchema, tags=['Products'])
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """ Devuelve un producto por su ID """
    result = db_get_product_by_id(product_id, db)
    if not result:
        return Response(content='The user selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return result


@product.post('/product/{user_id}', response_model=ProductSchema, tags=['Products'])
async def create_product(user_id: int, product_: ProductSchema, db: Session = Depends(get_db)):
    """ Inserta un producto en la base de datos """
    result = db_create_product(user_id, product_, db)
    return result


@product.put('/product/{product_id}', response_model=ProductSchema, tags=['Products'])
async def update_product(product_id: int, prod_: ProductSchema, db: Session = Depends(get_db)):
    """ Actualiza los datos de un producto """
    result = db_update_product(product_id, prod_, db)
    if not result:
        return Response(content='The user selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return result


@product.delete('/product/{product_id}', status_code=HTTP_204_NO_CONTENT, tags=['Products'])
async def delete_product(product_id, db: Session = Depends(get_db)):
    """ Elimina los datos de un producto """
    result = db_delete_product(product_id, db)
    if not result:
        return Response(content='The user selected not exits in database', status_code=HTTP_202_ACCEPTED)
    return Response(status_code=HTTP_204_NO_CONTENT)