from fastapi import APIRouter, Depends
from schemas.alunos import Aluno

router = APIRouter()

@router.get("/alunos")
async def root():
    return {"mensagem": "Dentro de alunos"}

@router.get("/alunos/saudacao")
async def saudacao():
    return {"mensagem": "Dentro de saudacao"}

@router.post("/alunos")
async def criar_aluno(aluno: Aluno):
    print(aluno)
    return {"mensagem": aluno}

