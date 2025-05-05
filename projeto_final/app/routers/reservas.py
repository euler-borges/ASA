from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from routers.auth import verificar_token
from schemas.reservas import Reserva as ReservaSchema
from models.reservas    import Reserva
from models.voos       import Voo
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


@router.get("/reservas")
def pesquisa_reserva_id(db:Session = Depends(get_db)):
    reserva_retorno_get = db.query(Reserva)
    

    if reserva_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return reserva_retorno_get.all()

@router.post("/reservas")
def cria_reservas(reserva: ReservaSchema, db: Session = Depends(get_db), usuario: str = Depends(somente_admin)):
    try:
        voo = db.query(Voo).filter(Voo.id == reserva.id_voo).first()
        if not voo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if reserva.quantidade_passageiros > voo.vagas:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
        voo.vagas -= reserva.quantidade_passageiros

        nova_reserva = Reserva(**reserva.model_dump())
        db.add(nova_reserva)
        db.commit()
        db.refresh(nova_reserva)
        return Response(status_code=status.HTTP_201_CREATED) 
    except Exception as e:
        db.rollback()  # Rollback em caso de erro
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@router.get("/reservas/{id}")
def pesquisa_reserva_id(id: int, db:Session = Depends(get_db)):
    reserva_retorno_get = db.query(Reserva).filter(Reserva.id == id)
    

    if reserva_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return reserva_retorno_get.first()
