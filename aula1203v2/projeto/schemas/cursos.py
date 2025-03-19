from pydantic import BaseModel

class Curso(BaseModel):
    nome            : str
    carga_horaria   : int
    periodo         : int
    descricao       : str