from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Engenharia da Computação!"}

@app.get("/alunos/{aluno_id}")
def read_aluno(aluno_id: int, q: str = None):
    return {"aluno_id": aluno_id, "nome": nome}

@app.post("/alunos/")
def create_aluno(aluno: dict):
    return {"aluno": aluno}


