import pika, sys, os, json

def callback(ch, method, properties, body):
    data = body.decode("utf-8")

    json_data = json.loads(data)
    print(" [x] Mensagem Recebida %r" % json_data)

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
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



