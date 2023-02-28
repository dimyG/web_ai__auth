from django.apps import AppConfig
import os
from .consumer import start_consumer_thread


class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            print("Performing initialization actions...")
            # this code will be executed only once when the server starts
            consumer_thread = start_consumer_thread(exchange_name='payments', queue_name='payments')
