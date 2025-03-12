from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    matricula = Column(String(50), nullable=False)
    curso = Column(String(50), server_default="Engenharia da Computação")
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
