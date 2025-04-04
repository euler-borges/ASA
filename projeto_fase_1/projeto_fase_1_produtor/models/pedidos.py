from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(50), nullable=False, unique=True)
    produto = Column(String(50), nullable=False)
    quantidade = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)    
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
