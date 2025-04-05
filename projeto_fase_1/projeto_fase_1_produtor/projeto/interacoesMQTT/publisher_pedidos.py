import pika, sys, os, json

from interacoesMQTT.coneccoes import queue_name, chave

def conectar_e_publicar(uid_produto, model_dump):
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

    i = uid_produto

    dado_pedido = {"id": i, **model_dump} 


    channel.basic_publish(exchange='amq.direct', routing_key=chave, body=json.dumps(dado_pedido).encode("utf-8"))
    print(" [x] Mensagem enviada!")
    connection.close()

