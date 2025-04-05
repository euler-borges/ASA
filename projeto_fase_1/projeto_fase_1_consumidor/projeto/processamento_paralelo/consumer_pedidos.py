#No consumidor, esse é  um processo separado

import pika, sys, os, json, uuid
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey


queue_pedidos = 'pedidos_para_almoxarifado'
chave = "empresa"
#conexão com o banco
DATABASE_URL = "postgresql://postgres:banco123@localhost:5433/pedidos"
SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(50), nullable=False, default=lambda: uuid.uuid4().hex, unique=True)
    produto = Column(String(50), nullable=False)
    quantidade = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)    
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))





def callback(ch, method, properties, body):
    data = body.decode("utf-8")

    json_data = json.loads(data)
    print(" [x] Mensagem Recebida %r" % json_data)

    db: Session = SessionLocal()

    try:
        # Gera UUID e cria o objeto Pedido
        novo_pedido = Pedido(
            uuid=json_data["id"],
            produto=json_data["produto"],
            quantidade=json_data["quantidade"],
            status=json_data["status"]
        )

        db.add(novo_pedido)
        db.commit()
        db.refresh(novo_pedido)
        print(f" [✓] Pedido inserido com UUID: {novo_pedido.uuid}")

    except Exception as e:
        print("Erro ao inserir no banco de dados: ", e)
        db.rollback()
    finally:
        db.close()


def conectar_e_consumir():
    """
    Conecta ao RabbitMQ e consome mensagens da fila especificada.
    """
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue=queue_pedidos)


    channel.basic_consume(queue=queue_pedidos, on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens. CTRL+C para sair')
    channel.start_consuming()


def main():
    conectar_e_consumir()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)



