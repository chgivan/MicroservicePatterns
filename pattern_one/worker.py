import pika, pickle, logging
import numpy as np

host = "rabbitmq"
queue_name = "sum_queue"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)
logging.info(' [Info] Waiting for chucks. To exit press CTRL+C')

def callback(ch, method, prop, buffer):
    chunk = pickle.loads(buffer)
    sum = 0
    for n in chunk:
        sum += n
    logging.info(
        "[Info] Receive chuck {0} (sum: {1})".format(
        prop.correlation_id, sum)
    )
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
connection.close()
