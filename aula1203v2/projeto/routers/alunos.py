from fastapi import APIRouter, Depends, HTTPException, Response, status
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
    try:
        novo_aluno = Aluno(**aluno.model_dump())
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Problemas ao inserir aluno")