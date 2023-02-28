import threading
import pika
from auth_prj.settings import rabbitmq_host

threads = []

exchanges = {
    'payments': 'fanout',
}

class ConsumerThread(threading.Thread):
    def __init__(self, exchange_name: str, queue_name: str):
        super(ConsumerThread, self).__init__()
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self._is_interrupted = False

    def exchange_type(self):
        return exchanges.get(self.exchange_name)

    def get_rabbitmq_channel(self):
        print(f'ConsumerThread connecting to rabbitmq host: {rabbitmq_host} exchange: {self.exchange_name} queue: {self.queue_name}')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        print(f'connection established {connection}')
        channel = connection.channel()
        print(f'channel created {channel}')
        channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type(), durable=True)
        print(f'exchange declared {self.exchange_name} {self.exchange_type()}')
        result = channel.queue_declare(queue=self.queue_name, exclusive=True)
        print(f'queue declared {result}')
        # queue_name = result.method.queue
        channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
        print(f'queue bound {self.exchange_name} {self.queue_name}')
        return channel

    def stop(self):
        self._is_interrupted = True

    def run(self):
        print(f'ConsumerThread started for exchange {self.exchange_name} queue: {self.queue_name}')
        channel = self.get_rabbitmq_channel()
        # we use channel.consume() and a loop instead of channel.start_consuming() to be able to interrupt the thread.
        # inactivity_timeout yields None whenever it's inactive for N secs. This way even if there are no messages
        # the channel.consume generator will yield None, the loop will run and the stop "command" will stop the thread.
        # channel.basic_consume(queue=args.queue, on_message_callback=queue_callback, auto_ack=True)
        for message in channel.consume(self.queue_name, inactivity_timeout=30):
            if self._is_interrupted:
                break
            if not all(message):
                print(f"message received: {message} (None, None, None) - inactivity_timeout")
                continue
            method, properties, body = message
            print(f"message received: {method} {properties} {body}")
            channel.basic_ack(method.delivery_tag)


def start_consumer_thread(exchange_name: str, queue_name: str):
    thread = ConsumerThread(exchange_name=exchange_name, queue_name=queue_name)
    thread.start()
    threads.append(thread)
    return thread

def stop_consumer_thread(thread: ConsumerThread):
    thread.stop()
    thread.join()
    threads.remove(thread)

