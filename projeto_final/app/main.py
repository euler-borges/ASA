from fastapi import FastAPI
from typing import Optional
from routers.voos import router as router_voos
from routers.aeroportos import router as router_aeroportos
from routers.auth import router as router_auth
from routers.reservas import router as router_reservas
from models.database import Base, engine

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_aeroportos)
app.include_router(router_voos)
app.include_router(router_reservas)
Base.metadata.create_all(bind=engine)
