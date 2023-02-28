import threading
import pika
from pika.exceptions import StreamLostError
import time
from auth_prj.settings import rabbitmq_host
import logging

logger = logging.getLogger('auth')

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
        logger.debug(f'ConsumerThread connecting to rabbitmq host: {rabbitmq_host} exchange: {self.exchange_name} queue: {self.queue_name}')

        num_retries = 0
        while num_retries < 5:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
                logger.debug(f'connection established')
                break
            except Exception as e:
                # when rabbitmq is not yet up and running we get a StreamLostError exception. We retry to connect.
                delay = 6
                logger.warning(f'{e}, retrying to connect to rabbitmq host: {rabbitmq_host} in {delay} seconds')
                time.sleep(delay)
                num_retries += 1
                # connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))

        channel = connection.channel()
        logger.debug(f'channel created')
        channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type(), durable=True)
        logger.debug(f'exchange declared {self.exchange_name} {self.exchange_type()}')
        result = channel.queue_declare(queue=self.queue_name, exclusive=True, durable=True)
        logger.debug(f'queue declared')
        # queue_name = result.method.queue
        channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
        logger.debug(f'queue bound to exchange')
        return channel

    def stop(self):
        self._is_interrupted = True

    def run(self):
        logger.debug(f'ConsumerThread started for exchange {self.exchange_name} queue: {self.queue_name}')
        channel = self.get_rabbitmq_channel()
        # we use channel.consume() and a loop instead of channel.start_consuming() to be able to interrupt the thread.
        # inactivity_timeout yields None whenever it's inactive for N secs. This way even if there are no messages
        # the channel.consume generator will yield None, the loop will run and the stop "command" will stop the thread.
        # channel.basic_consume(queue=args.queue, on_message_callback=queue_callback, auto_ack=True)
        for message in channel.consume(self.queue_name, inactivity_timeout=2):
            if self._is_interrupted:
                break
            if not all(message):
                logger.debug(f"message received: {message} (None, None, None) - inactivity_timeout")
                continue
            method, properties, body = message
            logger.debug(f"message received: {method} {properties} {body}")
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

