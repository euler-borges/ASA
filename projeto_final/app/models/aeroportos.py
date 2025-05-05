from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Aeroporto(Base):
    __tablename__ = 'aeroportos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    endereco = Column(String(50), nullable=False)    
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
