import json, sys, pika

startUrl = sys.argv[1]
maxdepth = int(sys.argv[2])
host = "192.168.99.100"

queue_name = "crawler"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True)

channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body= json.dumps({"url":startUrl,"depth":0,"maxdepth":maxdepth}),
    properties=pika.BasicProperties()
)

connection.close()
