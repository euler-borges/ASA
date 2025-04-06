from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.pedidos import Pedido as PedidoSchema
from models.pedidos  import Pedido
from sqlalchemy.orm   import Session
from models.database  import get_db
from interacoesMQTT.publisher_pedidos import conectar_e_publicar

router = APIRouter()

# OBS: O código abaixo está comentado, pois não é necessário para o funcionamento do sistema, visto que implementa conexão com o banco de dados.

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

#primeiro posta o pedido na fila, depois deleta no banco de dados
@router.post("/pedidos/{uuid}")
def cria_pedidos(uuid : str, db: Session = Depends(get_db)):
    try:
        Pedido_retorno_delete = db.query(Pedido).filter(Pedido.uuid == uuid)
        #primeiro testa existencia no banco, depois  posta na fila, depois deleta no banco de dados
        if Pedido_retorno_delete.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido não existe")
        else:
            conectar_e_publicar(Pedido_retorno_delete.first())


            Pedido_retorno_delete.delete(synchronize_session=False)
            db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content = f"Problemas ao inserir Pedido")
    
#Sem put e delete visto que ele envia as mensagenst para a fila
# @router.put("/pedidos/{uuid}")
# def update(uuid: str, pedido:PedidoSchema, db:Session = Depends(get_db)):
#     Pedido_retorno_post = db.query(Pedido).filter(Pedido.uuid == uuid)
#     Pedido_retorno_post.first()

#     if Pedido_retorno_post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Pedido: {id} does not exist')
#     else:
#         print(pedido.model_dump())
#         Pedido_retorno_post.update(pedido.model_dump(), synchronize_session=False)
#         db.commit()
#     return Pedido_retorno_post.first()

# @router.delete("/pedidos/{uuid}")
# def delete(uuid:str ,db: Session = Depends(get_db)):
#     Pedido_retorno_delete = db.query(Pedido).filter(Pedido.uuid == uuid)
    
#     if Pedido_retorno_delete.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido não existe")
#     else:
#         Pedido_retorno_delete.delete(synchronize_session=False)
#         db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.post("/processado")
# def processa_pedido(pedido: PedidoSchema, db: Session = Depends(get_db)):
#     try:
#         uid_produto = uid.uuid4().hex
#         novo_Pedido = Pedido(uuid = uid_produto, **pedido.model_dump())
#         db.add(novo_Pedido)
#         db.commit()
#         db.refresh(novo_Pedido)
#         conectar_e_publicar(uid_produto, pedido.model_dump())
#         return Response(status_code=status.HTTP_201_CREATED)
#     except Exception as e:
#         print(e)
#         return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content = f"Problemas ao inserir Pedido")