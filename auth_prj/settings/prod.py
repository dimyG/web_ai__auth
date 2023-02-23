from .base import *

ALLOWED_HOSTS = ['*']

# if we need to allow calls from other domains we should include the corsheaders app
INSTALLED_APPS.remove('corsheaders')
MIDDLEWARE.remove('corsheaders.middleware.CorsMiddleware')
# CORS_ALLOW_ALL_ORIGINS = True