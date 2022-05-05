import pika

params = pika.URLParameters('amqps://kwjmprch:i385gvPyDdV2UYvUr9VCU-Ql0gJUQ3Ft@mustang.rmq.cloudamqp.com/kwjmprch')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('recive from main')
    print(body)


channel.basic_consume(queue='main', on_message_callback=callback,auto_ack=True )
print('started consuming')
channel.start_consuming() 
channel.close()

callback()