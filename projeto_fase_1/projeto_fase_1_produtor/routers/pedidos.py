from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.pedidos import Pedido as PedidoSchema
from models.pedidos  import Pedido
from sqlalchemy.orm   import Session
from models.database  import get_db

router = APIRouter()

@router.get("/pedidos")
async def root():
    return {"mensagem": "Dentro de pedidos"}


@router.get("/pedidos/{id}")
def pesquisa_pedido_id(id: int, db:Session = Depends(get_db)):
    pedido_retorno_get = db.query(Pedido).filter(Pedido.id == id)
    

    if pedido_retorno_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Pedido: {id} não existe.')
    else:
        return pedido_retorno_get.first()

@router.post("/pedidos")
def cria_pedidos(Pedido: PedidoSchema, db: Session = Depends(get_db)):
    try:
        novo_Pedido = Pedido(**Pedido.model_dump())
        db.add(novo_Pedido)
        db.commit()
        db.refresh(novo_Pedido)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f"Problemas ao inserir Pedido")
    

@router.put("/pedidos/{id}")
def update(id: int, Pedido:PedidoSchema, db:Session = Depends(get_db)):
    Pedido_retorno_post = db.query(Pedido).filter(Pedido.id == id)
    Pedido_retorno_post.first()

    if Pedido_retorno_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pedido: {id} does not exist')
    else:
        print(Pedido.model_dump())
        Pedido_retorno_post.update(Pedido.model_dump(), synchronize_session=False)
        db.commit()
    return Pedido_retorno_post.first()

@router.delete("/pedidos/{id}")
def delete(id:int ,db: Session = Depends(get_db)):
    Pedido_retorno_delete = db.query(Pedido).filter(Pedido.id == id)
    
    if Pedido_retorno_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido não existe")
    else:
        Pedido_retorno_delete.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

