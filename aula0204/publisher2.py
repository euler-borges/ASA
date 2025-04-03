import pika
import uuid
import json

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

i = uuid.uuid4()

dado_aluno = {"id": i.hex, "nome":"ze", "endereco":"rua"} 


channel.basic_publish(exchange='amq.direct', routing_key='ufu', body=json.dumps(dado_aluno).encode("utf-8"))
print(" [x] Mensagem enviada!")
connection.close()