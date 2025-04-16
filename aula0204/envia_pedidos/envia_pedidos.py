import pika
import uuid
import json
import json_tricks
from pedido import Pedido
import time
import logging
logging.basicConfig(level=logging.INFO)


def main():

    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('rabbitmq',
                                       5672,
                                       '/',
                                       credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    channel.queue_declare(queue='UFU')
    channel.queue_bind(exchange='amq.direct',
                    queue='UFU',
                    routing_key='ufu')
    i = 0
    while True:
        str_pedido = f'PEDIDO {i}'
        pedido = Pedido(str_pedido, i)
        i = i + 1
        channel.basic_publish(exchange='amq.direct', 
                    routing_key='ufu', 
                    body=json_tricks.dumps(pedido).encode('utf-8'))
        logging.info(" [x] Mensagem enviada!")
        time.sleep(15)
        
if __name__ == "__main__":
    main()
