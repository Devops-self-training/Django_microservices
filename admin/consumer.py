import pika, json, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")

django.setup()

from products.models import Product

params = pika.URLParameters('amqps://kwjmprch:i385gvPyDdV2UYvUr9VCU-Ql0gJUQ3Ft@mustang.rmq.cloudamqp.com/kwjmprch')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('recive from main')
    # this error    
    id = json.loads(body)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print('--product likes increased--')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack= True)
print('started consuming')
channel.start_consuming() 
channel.close()

