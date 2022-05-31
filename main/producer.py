import json

import pika

params = pika.URLParameters(
    'amqps://kwjmprch:i385gvPyDdV2UYvUr9VCU-Ql0gJUQ3Ft@mustang.rmq.cloudamqp.com/kwjmprch')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin',body= json.dumps(body), properties=properties)
