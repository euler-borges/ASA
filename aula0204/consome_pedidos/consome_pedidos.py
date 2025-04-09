import pika, sys, os
import json
import json_tricks
from pedido import Pedido


def callback(ch, method, properties, body):
    data = json_tricks.loads(body.decode("utf-8"))
    print(data.pedido)

def main():
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('172.30.0.10',
                                       5672,
                                       '/',
                                       credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='UFU')
    channel.basic_consume(queue='UFU', on_message_callback=callback, auto_ack=True)
    print(' [*] Aguardando mensagens. CTRL+C para sair')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)







