from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# todo: set up a custom domain name for the API Gateway and remove the CORS
# if we need to allow calls from other domains we should include the corsheaders app
# INSTALLED_APPS.remove('corsheaders')
# MIDDLEWARE.remove('corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'  # todo: it does nothing, use a proper one

ACCOUNT_EMAIL_VERIFICATION = "none" # todo: set up email backend and set this to "mandatory"