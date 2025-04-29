from pydantic import BaseModel

class Aeroporto(BaseModel):
    nome            : str
    cidade          : str
    endereco        : str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "nome": "Aeroporto Internacional de São Paulo",
                "cidade": "São Paulo",
                "endereco": "Avenida do Aeroporto, 1234"
            }
        }


