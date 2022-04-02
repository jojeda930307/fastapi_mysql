from fastapi import APIRouter


product = APIRouter()


@product.get('/getProducts', tags=['Products'])
async def list_products():
    """ Devuelve todos los productos """
    pass


@product.get("/product/{product_id}", tags=['Products'])
async def get_product_by_id():
    """ Devuelve un producto por su ID """
    pass


@product.post('/product', tags=['Products'])
async def create_product():
    """ Inserta un producto en la base de datos """
    pass


@product.put('/product/{product_id}', tags=['Products'])
async def update_product():
    """ Actualiza los datos de un producto """
    pass


@product.delete('/product/{product_id}', tags=['Products'])
async def delete_product():
    """ Elimina los datos de un producto """
    pass