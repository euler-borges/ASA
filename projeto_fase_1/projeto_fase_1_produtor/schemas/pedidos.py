from pydantic import BaseModel

class Pedido(BaseModel):
    uuid: str
    produto: str
    quantidade: int
    status: str