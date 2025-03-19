from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.cursos import Curso as CursoSchema
from models.cursos    import Curso
from sqlalchemy.orm   import Session
from models.database  import get_db


router = APIRouter()

@router.get("/cursos")
async def root():
    return {"mensagem": "Dentro de cursos"}

@router.post("/cursos")
def cria_cursos(curso: CursoSchema, db: Session = Depends(get_db)):
    try:
        novo_curso = Curso(**curso.model_dump())
        db.add(novo_curso)
        db.commit()
        db.refresh(novo_curso)
        return Response(status_code=status.HTTP_201_CREATED) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Probelmas ao inserir o curso")    

@router.get("/cursos/{id}")
def pesquisa_curso_id(id: int, db:Session = Depends(get_db)):
    curso_retorno_get = db.query(Curso).filter(Curso.id == id)
    

    if curso_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'curso: {id} não existe.')
    else:
        return curso_retorno_get.first()

@router.put("/cursos/{id}")
def update(id: int, curso:CursoSchema, db:Session = Depends(get_db)):
    curso_retorno_post = db.query(Curso).filter(Curso.id == id)
    curso_retorno_post.first()

    if curso_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Curso: {id} does not exist')
    else:
        print(curso.model_dump())
        curso_retorno_post.update(curso.model_dump(), synchronize_session=False)
        db.commit()
    return curso_retorno_post.first()

@router.delete("/cursos/{id}")
def delete(id:int ,db: Session = Depends(get_db)):
    curso_retorno_delete = db.query(Curso).filter(Curso.id == id)
    
    if curso_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso não existe")
    else:
        curso_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)