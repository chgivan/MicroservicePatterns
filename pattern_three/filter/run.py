import pika, pickle
import numpy as np

host = "192.168.99.100"
recieve_queue_name = "unfilternumders"
send_queue_name = "filternumders"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue=recieve_queue_name, durable=True)
channel.queue_declare(queue=send_queue_name, durable=True)
print(' [*] Waiting to filter. To exit press CTRL+C')

def callback(ch, method, prop, buffer):
    A = pickle.loads(buffer)
    temp = []
    for n in A:
        if n > 0:
            temp.append(n)
    B = np.array(temp)
    channel.basic_publish(
        exchange='',
        routing_key=send_queue_name,
        body=pickle.dumps(B),
        properties=pika.BasicProperties()
    )
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print("[Info] Filter Data")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=recieve_queue_name)

channel.start_consuming()
connection.close()
