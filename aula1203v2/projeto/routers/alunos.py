from fastapi import APIRouter, Depends
from schemas.alunos import Aluno as AlunoSchema
from models.alunos    import Aluno
from sqlalchemy.orm   import Session
from models.database  import get_db

router = APIRouter()

@router.get("/alunos")
async def root():
    return {"mensagem": "Dentro de alunos"}

@router.get("/alunos/saudacao")
async def saudacao():
    return {"mensagem": "Dentro de saudacao"}

@router.post("/alunos")
def cria_alunos(aluno: AlunoSchema, db: Session = Depends(get_db)):
    novo_aluno = Aluno(**aluno.model_dump())
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno
