from fastapi import FastAPI
from typing import Optional
from routers.voos import router as router_voos
from routers.aeroportos import router as router_aeroportos
from models.database import Base, engine

app = FastAPI()
app.include_router(router_aeroportos)
app.include_router(router_voos)
Base.metadata.create_all(bind=engine)
