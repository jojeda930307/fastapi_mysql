import uvicorn
from fastapi import FastAPI


from src.routes_crud.address_routes import address
from src.routes_crud.product_routes import product
from src.routes_crud.user_routes import user

from src.security.routes_auth.authentication_routes import router_auth
from src.security.email import router_email

app = FastAPI()

app.include_router(user)
app.include_router(address)
#app.include_router(order)
app.include_router(product)
#app.include_router(router_auth)
app.include_router(router_auth)
app.include_router(router_email)

if __name__ == '__main__':
    uvicorn.run("app_server:app", host="127.0.0.1", port=8000, log_level="info", reload=True)