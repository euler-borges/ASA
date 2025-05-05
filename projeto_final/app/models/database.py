from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import psycopg2
from psycopg2 import OperationalError

# Obtem a URL do banco de dados a partir da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Função para esperar o PostgreSQL estar pronto
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(dsn=SQLALCHEMY_DATABASE_URL)
            conn.close()
            print("PostgreSQL está pronto para conexões.")
            break
        except OperationalError:
            print("Aguardando o PostgreSQL estar pronto...")
            time.sleep(1)

# Aguarda o banco de dados antes de iniciar a engine
wait_for_postgres()

# Inicializa a engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
