import pika, sys, os, json

queue_pedidos = 'pedidos_para_almoxarifado'
chave = "empresa"
queue_analisada = 'pedidos_analisados'

def conectar_e_publicar(pedido):
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

    channel.queue_declare(queue=queue_analisada,)
    channel.queue_bind(exchange='amq.direct',
                    queue=queue_analisada,
                    routing_key=chave)

    print(pedido)
    i = pedido.uuid
    pedido_produto = pedido.produto
    pedido_quantidade = pedido.quantidade
    dado_pedido = {"id": i, "produto": pedido_produto,"quantidade":pedido_quantidade, "status": "processado almoxarifado"} 


    channel.basic_publish(exchange='amq.direct', routing_key=chave, body=json.dumps(dado_pedido).encode("utf-8"))
    print(" [x] Mensagem enviada!")
    connection.close()

