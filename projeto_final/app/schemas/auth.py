from pydantic import BaseModel


class LoginData(BaseModel):
    usuario: str
    senha: str