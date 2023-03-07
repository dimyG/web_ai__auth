from auth_app.consumer import start_consumer_thread
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start a consumer thread'

    # add two arguments to the command, one named 'exchange_name' and one named 'queue_name' and default to 'payments'
    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--exchange_name',
            action='store',
            dest='exchange_name',
            type=str,
            default='payments'
        )
        parser.add_argument(
            '-q',
            '--queue_name',
            action='store',
            dest='queue_name',
            type=str,
            default='payments'
        )

    def handle(self, *args, **options):
        exchange_name = options['exchange_name']
        queue_name = options['queue_name']
        self.stdout.write(self.style.SUCCESS(f'Starting a consumer thread for exchange {exchange_name} and queue {queue_name}...'))
        consumer_thread = start_consumer_thread(exchange_name=exchange_name, queue_name=queue_name)
        if consumer_thread:
            self.stdout.write(self.style.SUCCESS(f'Consumer thread started successfully.'))
        else:
            self.stdout.write(self.style.ERROR(f'Consumer thread could not be started.'))
