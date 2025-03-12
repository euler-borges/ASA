from pydantic import BaseModel

class Aluno(BaseModel):
    nome: str
    matricula: str
    curso: str
    