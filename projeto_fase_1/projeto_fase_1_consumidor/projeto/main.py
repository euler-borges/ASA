from fastapi import FastAPI
from typing import Optional
from routers.pedidos import router as router_pedidos
#from models.database import Base, engine

app = FastAPI()
app.include_router(router_pedidos)
#Base.metadata.create_all(bind=engine)
