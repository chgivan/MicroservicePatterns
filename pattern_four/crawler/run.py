import redis, json, pika
from utils import getLinks

host = "192.168.99.100"
port = 6379
db = 0

redisDB = redis.StrictRedis(host=host, port=port, db=db)

queue_name = "crawler"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True)
print("Start crawler....")

def callback(ch, method, prop, buffer):
    body = json.loads(buffer)
    depth = body.get("depth")
    url = body.get("url")
    maxdepth = body.get("maxdepth")

    if depth > maxdepth or redisDB.exists(url):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    links = getLinks(url)
    if links is None:
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    redisDB.set(url, json.dumps(links))
    print("Passing " + str(depth))
    for link in links:
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body= json.dumps({"url":url,"depth":depth+1,"maxdepth":maxdepth}),
            properties=pika.BasicProperties()
        )


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)
channel.start_consuming()
connection.close()
