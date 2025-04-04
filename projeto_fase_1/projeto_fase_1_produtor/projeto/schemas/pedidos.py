from pydantic import BaseModel

class Pedido(BaseModel):
    produto: str
    quantidade: int
    status: str