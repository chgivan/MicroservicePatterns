import sys, json, pika

available = int(sys.argv[1])

host = "192.168.99.100"

queue_name = "pool_pulbic_queue"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True)

def callback(ch, method, prop, buffer):
    body = json.loads(buffer)
    n = body.get("n")
    type = body.get("type")

    if type == "put":
        available += n
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    if available < n:
        channel.basic_publish(
            exchange='',
            routing_key=prop.reply_to,
            body=json.dumps({"type":"wait"}),
            properties=pika.BasicProperties()
        )
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    available -= n
    channel.basic_publish(
        exchange='',
        routing_key=prop.reply_to,
        body=json.dumps{"type":"ok","n":n},
        properties=pika.BasicProperties()
    )
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos()
channel.basic_consume(callback, queue=queue_name)
connection.close()
