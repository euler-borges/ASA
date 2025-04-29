from fastapi import APIRouter, Depends
from schemas.alunos import Aluno
from models.database import get_db
from sqlalchemy.orm   import Session
import logging
import colorlog

# Configuração básica do logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

logger = colorlog.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

router = APIRouter()

@router.get("/alunos")
async def root():
    logger.info("Rota de alunos")
    return {"mensagem": "Dentro de alunos"}

@router.get("/alunos/saudacao")
async def saudacao():
    logger.info("Testando a rota de saudação")
    return {"mensagem": "Dentro de saudacao"}

@router.post("/alunos")
async def criar_aluno(aluno: Aluno, db: Session = Depends(get_db)):
    logger.info(aluno)
    novo_aluno = Aluno(**aluno.model_dump())
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno
