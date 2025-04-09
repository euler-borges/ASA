import pika
import uuid
import json
import json_tricks
from pedido import Pedido

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
print(i.hex)

dado_aluno = {"id": i.hex, "nome": "Pedro Silva", "endereco": "Rua X, 333"}
print(dado_aluno)
pedido = Pedido('COCA COLA ZERO', 3)

print(type(pedido))

# print(json.dumps(dado_aluno).encode())
# print(json.dumps(dado_aluno))


channel.basic_publish(exchange='amq.direct', 
                      routing_key='ufu', 
                      body=json_tricks.dumps(pedido).encode('utf-8'))
print(" [x] Mensagem enviada!")
connection.close()


#body=json_tricks.dumps(pedido).encode('utf-8')
