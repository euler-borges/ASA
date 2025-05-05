from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey, Date
from .database import Base


class Reserva(Base):
    __tablename__ = 'reservas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_voo = Column(Integer, ForeignKey('voos.id'), nullable=False)
    id_usuario = Column(Integer, nullable=False)
    quantidade_passageiros = Column(Integer, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))