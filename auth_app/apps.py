from django.apps import AppConfig
import os
import logging
from .consumer import start_consumer_thread


logger = logging.getLogger('auth')

class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        # Notice: When running under gunicorn this RUN_MAIN environment variable is not set and the thread
        # starts with an external command in the entrypoint.sh file.
        if os.environ.get('RUN_MAIN'):
            # The `RUN_MAIN` environment variable is a private API, not something that
            # should be used or overwritten by users.
            logger.info("Performing initialization actions...")
            # this code will be executed only once when the server starts
            consumer_thread = start_consumer_thread(exchange_name='payments', queue_name='payments')
        else:
            logger.info("Skipping initialization actions...")
            # this code will be executed every time the server reloads
            pass