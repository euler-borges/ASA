import pika, sys, os

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='UFU')

    def callback(ch, method, properties, body):
        print(" [x] Mensagem Recebida %r" % body.decode("utf-8"))

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



