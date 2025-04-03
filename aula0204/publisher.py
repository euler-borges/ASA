import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.queue_declare(queue='UFU')
channel.queue_bind(exchange='amq.direct',
                   queue='UFU',
                   routing_key='ufu')

channel.basic_publish(exchange='amq.direct', routing_key='ufu', body='Engenharia da Computação')
print(" [x] Mensagem enviada!")
connection.close()