from fastapi import FastAPI
from app.routers import users, categoria, productos, cliente, precios, pedidos
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(users.router)
app.include_router(categoria.router)
app.include_router(productos.router)
app.include_router(cliente.router)
app.include_router(precios.router)
app.include_router(pedidos.router)



