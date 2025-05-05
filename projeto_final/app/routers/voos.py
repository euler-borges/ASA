from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from routers.auth import verificar_token
from schemas.voos import Voo as VooSchema
from models.voos    import Voo
from sqlalchemy.orm   import Session
from models.database  import get_db


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


@router.get("/voos")
def pesquisa_voo_id(db:Session = Depends(get_db)):
    voo_retorno_get = db.query(Voo)
    

    if voo_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return voo_retorno_get.all()

@router.post("/voos")
def cria_voos(voo: VooSchema, db: Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    try:
        novo_voo = Voo(**voo.model_dump())
        db.add(novo_voo)
        db.commit()
        db.refresh(novo_voo)
        return Response(status_code=status.HTTP_201_CREATED) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@router.get("/voos/{id}")
def pesquisa_voo_id(id: int, db:Session = Depends(get_db)):
    voo_retorno_get = db.query(Voo).filter(Voo.id == id)
    

    if voo_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return voo_retorno_get.first()

@router.get("/voos/destinos/{id_inicio}")
def pesquisa_destino_id(id_inicio: int, db:Session = Depends(get_db)):
    voo_retorno_get = db.query(Voo).filter(Voo.aeroporto_inicio == id_inicio)
    

    if voo_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return voo_retorno_get.all()

@router.get("/voos/data/{data_voo}")
def pesquisa_data_voo(data_voo: str, db:Session = Depends(get_db)):
    voo_retorno_get = db.query(Voo).filter(Voo.data == data_voo)
    

    if voo_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return voo_retorno_get.all()

@router.put("/voos/{id}")
def update(id: int, voo:VooSchema, db:Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    voo_retorno_post = db.query(Voo).filter(Voo.id == id)
    voo_retorno_post.first()

    if voo_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        print(voo.model_dump())
        voo_retorno_post.update(voo.model_dump(), synchronize_session=False)
        db.commit()
    return voo_retorno_post.first()

@router.delete("/voos/{id}")
def delete(id:int ,db: Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    voo_retorno_delete = db.query(Voo).filter(Voo.id == id)
    
    if voo_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        voo_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)