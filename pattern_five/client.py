import pika, json, sys

host = "192.168.99.100"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)
callback_queue = result.method.queue
