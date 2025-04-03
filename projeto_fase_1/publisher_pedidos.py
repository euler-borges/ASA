import pika
import uuid
import json

from coneccoes import queue_name, chave

queue_name = 'pedidos_para_almoxarifado'
chave = "empresa"
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