from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.pedidos import Pedido as PedidoSchema
from models.pedidos  import Pedido
from sqlalchemy.orm   import Session
from models.database  import get_db
import uuid as uid

router = APIRouter()

@router.get("/pedidos")
def pesquisa_pedido_id(db:Session = Depends(get_db)):
    pedido_retorno_get = db.query(Pedido).all()
    
    if pedido_retorno_get == []:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Não existem pedidos.')
    else:
        return pedido_retorno_get



@router.get("/pedidos/{uuid}")
def pesquisa_pedido_id(uuid: str, db:Session = Depends(get_db)):
    pedido_retorno_get = db.query(Pedido).filter(Pedido.uuid == uuid)
    

    if pedido_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Pedido: {id} não existe.')
    else:
        return pedido_retorno_get.first()

@router.post("/pedidos")
def cria_pedidos(pedido: PedidoSchema, db: Session = Depends(get_db)):
    try:
        novo_Pedido = Pedido(uuid = uid.uuid4().hex, **pedido.model_dump())
        db.add(novo_Pedido)
        db.commit()
        db.refresh(novo_Pedido)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content = f"Problemas ao inserir Pedido")
    

@router.put("/pedidos/{uuid}")
def update(uuid: str, pedido:PedidoSchema, db:Session = Depends(get_db)):
    Pedido_retorno_post = db.query(Pedido).filter(Pedido.uuid == uuid)
    Pedido_retorno_post.first()

    if Pedido_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pedido: {id} does not exist')
    else:
        print(pedido.model_dump())
        Pedido_retorno_post.update(pedido.model_dump(), synchronize_session=False)
        db.commit()
    return Pedido_retorno_post.first()

@router.delete("/pedidos/{uuid}")
def delete(uuid:str ,db: Session = Depends(get_db)):
    Pedido_retorno_delete = db.query(Pedido).filter(Pedido.uuid == uuid)
    
    if Pedido_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido não existe")
    else:
        Pedido_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

