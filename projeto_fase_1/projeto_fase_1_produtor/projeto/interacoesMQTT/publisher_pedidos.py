import pika, uuid, sys, os, json

from coneccoes import queue_name, chave

def conectar_e_publicar():
    """
    Conecta ao RabbitMQ e publica uma mensagem na fila especificada.
    """
    # Conexão com o RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                        5672,
                                        '/',
                                        credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name,)
    channel.queue_bind(exchange='amq.direct',
                    queue=queue_name,
                    routing_key=chave)

    i = uuid.uuid4()

    dado_pedido = {"id": i.hex, "produto":"batata", "quantidade": 10, "status":"enviado_aloxarifado"} 


    channel.basic_publish(exchange='amq.direct', routing_key=chave, body=json.dumps(dado_pedido).encode("utf-8"))
    print(" [x] Mensagem enviada!")
    connection.close()


def main():
    conectar_e_publicar()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)