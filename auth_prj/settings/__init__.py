from .base import *


# set the AUTH_PRJ_MODE environment variable in your OS
if os.environ.get('AUTH_PRJ_MODE') == 'prod':
    print('production')
    from .prod import *
elif os.environ.get('AUTH_PRJ_MODE') == 'stage':
    print('stage')
    from .stage import *
else:
    print('development')
    from .dev import *
