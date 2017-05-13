import pika
import numpy as np
import pickle

host = "192.168.99.100"
queue_name = "sum_queue"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, prop, buffer):
    chunk = pickle.loads(buffer)
    sum = 0
    for n in chunk:
        sum += n
    print(sum)
    channel.basic_publish(
        exchange='',
        routing_key=prop.reply_to,
        body=pickle.dumps(np.array([sum])),
        properties=pika.BasicProperties(
            correlation_id=prop.correlation_id 
        )
    )
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
