from pydantic import BaseModel

class Reserva(BaseModel):
    id_voo: int
    id_usuario: int
    quantidade_passageiros: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "id_voo": 1,
                "id_usuario": 1,
                "data_reserva": "01-10-2023",
                "quantidade_passageiros": 2
            }
        }