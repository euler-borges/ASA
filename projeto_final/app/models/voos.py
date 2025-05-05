from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey, Date
from .database import Base

class Voo(Base):
    __tablename__ = 'voos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    aeroporto_inicio = Column(Integer, ForeignKey('aeroportos.id'), nullable=False)
    aeroporto_destino = Column(Integer, ForeignKey('aeroportos.id'), nullable=False)
    duracao = Column(String(50), nullable=False)
    horario_saida = Column(String(50), nullable=False)
    data = Column(String(50), nullable=False)
    vagas = Column(Integer, nullable=False)
    preco = Column(Integer, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))