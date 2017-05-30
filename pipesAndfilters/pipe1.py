import pika, pickle, time
import numpy as np

host = "192.168.99.100"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

queue_name = "unfilternumders"
channel.queue_declare(queue=queue_name, durable=True)

delayInSeconds = 1
size = 10
min, max = -100, 100

print("[Info] Start Streaming Data. To exit press CTRL+C...")
while(True):
    A = np.random.randint(low=min, high=max, size=size)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body= pickle.dumps(A),
        properties=pika.BasicProperties()
    )
    print(A)
    time.sleep(delayInSeconds)
    
connection.close()
