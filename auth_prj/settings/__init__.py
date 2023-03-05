from .base import *
import logging

logger = logging.getLogger('auth')

# set the AUTH_PRJ_MODE environment variable in your OS
if os.environ.get('AUTH_PRJ_MODE') == 'prod':
    logger.info('production')
    from .prod import *
elif os.environ.get('AUTH_PRJ_MODE') == 'stage':
    logger.info('stage')
    from .stage import *
else:
    logger.info('development')
    from .dev import *
