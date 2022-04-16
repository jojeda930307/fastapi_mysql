import uvicorn
from fastapi import FastAPI

from src.routes.address_routes import address
from src.routes.order_routes import order
from src.routes.product_routes import product
from src.routes.user_routes import user

app = FastAPI()
app.include_router(user)
app.include_router(address)
#app.include_router(order)
app.include_router(product)

if __name__ == '__main__':
    uvicorn.run("app_server:app", host="127.0.0.1", port=8000, log_level="info", reload=True)