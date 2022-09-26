from fastapi import APIRouter


order = APIRouter()


@order.get('/getOrders', tags=['Orders'])
async def list_orders():
    """ Devuelve todos los pedidos """
    pass


@order.get("/order/{order_id}", tags=['Orders'])
async def get_order_by_id():
    """ Devuelve un pedido por su ID """
    pass


@order.post('/order', tags=['Orders'])
async def create_order():
    """ Inserta un pedido en la pase de datos """
    pass


@order.put('/order/{order_id}', tags=['Orders'])
async def update_order():
    """ Actualiza los datos de un pedido """
    pass


@order.delete('/order/{order_id}', tags=['Orders'])
async def delete_order():
    """ Elimina los datos de un pedido """
    pass