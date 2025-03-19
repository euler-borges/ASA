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

@router.get("/alunos/{id}")
def pesquisa_aluno_id(id: int, db:Session = Depends(get_db)):
    aluno_retorno_get = db.query(Aluno).filter(Aluno.id == id)
    

    if aluno_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Aluno: {id} não existe.')
    else:
        return aluno_retorno_get.first()

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
    

@router.put("/alunos/{id}")
def update(id: int, aluno:AlunoSchema, db:Session = Depends(get_db)):
    aluno_retorno_post = db.query(Aluno).filter(Aluno.id == id)
    aluno_retorno_post.first()

    if aluno_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Aluno: {id} does not exist')
    else:
        print(aluno.model_dump())
        aluno_retorno_post.update(aluno.model_dump(), synchronize_session=False)
        db.commit()
    return aluno_retorno_post.first()

@router.delete("/alunos/{id}")
def delete(id:int ,db: Session = Depends(get_db)):
    aluno_retorno_delete = db.query(Aluno).filter(Aluno.id == id)
    
    if aluno_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno não existe")
    else:
        aluno_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

