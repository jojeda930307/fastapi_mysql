import uvicorn
from fastapi import FastAPI

from src.routes.address_routes import address
from src.routes.product_routes import product
from src.routes.user_routes import user
from src.security.test_auth_1.routers.auth_routes import router_auth
from src.security.test_auth_2.user_router import router1

app = FastAPI()
app.include_router(user)
app.include_router(address)
#app.include_router(order)
app.include_router(product)
app.include_router(router_auth)
app.include_router(router1)

if __name__ == '__main__':
    uvicorn.run("app_server:app", host="127.0.0.1", port=8000, log_level="info", reload=True)