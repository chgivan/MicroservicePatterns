import pika, uuid

_host = "192.168.99.100"
_circuits = dict()
_connection = pika.BlockingConnection(pika.ConnectionParameters(host=_host))
_channel = _connection.channel()


class CircuitData (object):
    def __init__(self, block):
        self.block = block
        self.open = False


def addCircuit(name, queue, cb):
    if name in _circuits:
        return
    _channel.queue_declare(durable= True)
    _circuits[name] = new CircuitData(cb)



def call(self, n):
    self.response = None
    self.corr_id = str(uuid.uuid4())
    self.channel.basic_publish(exchange='',
                               routing_key='rpc_queue',
                               properties=pika.BasicProperties(
                                     reply_to = self.callback_queue,
                                     correlation_id = self.corr_id,
                                     ),
                               body=str(n))
    while self.response is None:
        self.connection.process_data_events()
    return int(self.response)
