import pika, pickle, uuid, sys
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
if len(sys.argv) > 1:
    size = int(sys.argv[1])
if len(sys.argv) > 2:
    chunks_num = int(sys.argv[2])
if len(sys.argv) > 3:
    min = int(sys.argv[3])
if len(sys.argv) > 4:
    max = int(sys.argv[4])

A = np.random.randint(low=min, high=max, size=size)
chunks = np.array_split(A, chunks_num)
idList = []
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
    print("[Info] Sended Chunk " + id)

replies = len(chunks)
sum = 0
def OnReply(ch, method, props, buffer):
    global replies, sum
    if props.correlation_id in idList:
        replies -= 1
        sum += pickle.loads(buffer)[0]
        print("[Info] Receive Chunk " + props.correlation_id)
channel.basic_consume(
    OnReply,
    no_ack=True,
    queue=reply_queue_name
)

while replies > 0:
    connection.process_data_events()
print("The sum is " + str(sum))
connection.close()
