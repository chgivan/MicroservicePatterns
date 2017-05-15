import pika, pickle
import numpy as np

host = "192.168.99.100"
queue_name = "filternumders"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)
print(' [*] Waiting to pipe2. To exit press CTRL+C')

def callback(ch, method, prop, buffer):
    A = pickle.loads(buffer)
    print(A)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
connection.close()
