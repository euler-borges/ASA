from pydantic import BaseModel

class Voo(BaseModel):
    aeroporto_inicio: int
    aeroporto_destino: int
    duracao: str  # Assuming duration is a string in the format 'HH:MM:SS'
    horario_saida: str  # Assuming departure time is a string in the format 'HH:MM:SS'
    data: str  # Assuming date is a string in the format 'DD-MM-YYYY'
    vagas: int
    preco: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "aeroporto_inicio": 1,
                "aeroporto_destino": 2,
                "duracao": "02:30:00",
                "horario_saida": "15:00:00",
                "data": "01-10-2023",
                "vagas": 100
            }
        }