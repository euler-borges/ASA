from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from schemas.aeroportos import Aeroporto as AeroportoSchema
from models.aeroportos  import Aeroporto
from sqlalchemy.orm   import Session
from models.database  import get_db
from routers.auth import verificar_token


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def auth_dependencia(token: str = Depends(oauth2_scheme)):
    usuario = verificar_token(token)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return usuario

def somente_admin(token: str = Depends(oauth2_scheme)):
    usuario = verificar_token(token)
    if usuario != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao administrador"
        )
    return usuario


@router.get("/aeroportos")
def pesquisa_aeroporto_id(db:Session = Depends(get_db)):
    aeroporto_retorno_get = db.query(Aeroporto)
    

    if aeroporto_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return aeroporto_retorno_get.all()

@router.get("/aeroportos/{id}")
def pesquisa_aeroporto_id(id: int, db:Session = Depends(get_db)):
    aeroporto_retorno_get = db.query(Aeroporto).filter(Aeroporto.id == id)
    

    if aeroporto_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return aeroporto_retorno_get.first()

@router.post("/aeroportos")
def cria_aeroportos(aeroporto: AeroportoSchema, db: Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    try:
        novo_aeroporto = Aeroporto(**aeroporto.model_dump())
        db.add(novo_aeroporto)
        db.commit()
        db.refresh(novo_aeroporto)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.put("/aeroportos/{id}")
def update(id: int, aeroporto:AeroportoSchema, db:Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    aeroporto_retorno_post = db.query(Aeroporto).filter(Aeroporto.id == id)
    aeroporto_retorno_post.first()

    if aeroporto_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        print(aeroporto.model_dump())
        aeroporto_retorno_post.update(aeroporto.model_dump(), synchronize_session=False)
        db.commit()
    return aeroporto_retorno_post.first()

@router.delete("/aeroportos/{id}")
def delete(id:int ,db: Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    aeroporto_retorno_delete = db.query(Aeroporto).filter(Aeroporto.id == id)
    
    if aeroporto_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        aeroporto_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

