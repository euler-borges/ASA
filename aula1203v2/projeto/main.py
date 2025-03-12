from fastapi import FastAPI
from typing import Optional
from routers.alunos import router as router_alunos
from models.database import Base, engine

app = FastAPI()
app.include_router(router_alunos)
Base.metadata.create_all(bind=engine)

