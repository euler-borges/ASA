from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.voos import Voo as VooSchema
from models.voos    import Voo
from sqlalchemy.orm   import Session
from models.database  import get_db


router = APIRouter()

@router.get("/voos")
async def root():
    return {"mensagem": "Dentro de voos"}

@router.post("/voos")
def cria_voos(voo: VooSchema, db: Session = Depends(get_db)):
    try:
        novo_voo = Voo(**voo.model_dump())
        db.add(novo_voo)
        db.commit()
        db.refresh(novo_voo)
        return Response(status_code=status.HTTP_201_CREATED) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Probelmas ao inserir o voo")    

@router.get("/voos/{id}")
def pesquisa_voo_id(id: int, db:Session = Depends(get_db)):
    voo_retorno_get = db.query(Voo).filter(Voo.id == id)
    

    if voo_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'voo: {id} não existe.')
    else:
        return voo_retorno_get.first()

@router.put("/voos/{id}")
def update(id: int, voo:VooSchema, db:Session = Depends(get_db)):
    voo_retorno_post = db.query(Voo).filter(Voo.id == id)
    voo_retorno_post.first()

    if voo_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Voo: {id} does not exist')
    else:
        print(voo.model_dump())
        voo_retorno_post.update(voo.model_dump(), synchronize_session=False)
        db.commit()
    return voo_retorno_post.first()

@router.delete("/voos/{id}")
def delete(id:int ,db: Session = Depends(get_db)):
    voo_retorno_delete = db.query(Voo).filter(Voo.id == id)
    
    if voo_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Voo não existe")
    else:
        voo_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)