from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

usuarios = {"admin": "1234", "joao": "senha123"}
tokens_validos = {}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = form_data.username
    senha = form_data.password

    if usuario in usuarios and usuarios[usuario] == senha:
        token = f"token-{usuario}"
        tokens_validos[token] = usuario
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

# continua igual:
def verificar_token(token: str):
    return tokens_validos.get(token, None)
