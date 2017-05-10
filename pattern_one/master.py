import pika, pickle, uuid
import numpy as np

host = "192.168.99.100"
queue_name = "sum_queue"
reply_queue_name = "reply_" + queue_name
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue=queue_name, durable=True)
channel.queue_declare(queue=reply_queue_name, exclusive=True)

size = 10
chunks_num = 3
min, max = 0, 100

A = np.random.randint(low=min, high=max, size=size)
chunks = np.array_split(A, chunks_num)
idList = []
replies = 0
for chunk in chunks:
    id = str(uuid.uuid4())
    idList.append(id)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body= pickle.dumps(chunk),
        properties=pika.BasicProperties(
            reply_to=reply_queue_name,
            correlation_id=id
        )
    )
    replies += 1
print("Send chunks")
print(results)
sum = 0
def OnReply(ch, method, props, buffer):
    print("Message")
    if results.has_key(props.correlation_id):
        results[props.correlation_id] =
        replies -= 1
        sum += pickle.loads(buffer)[0]
        print("OK")
channel.basic_consume(
    OnReply,
    no_ack=True,
    queue=reply_queue_name
)

while replies > 0:
    connection.process_data_events()
