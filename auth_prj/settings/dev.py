from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# allow all hosts
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# django-cors-headers settings
# CORS_ALLOWED_ORIGINS = [
#     # env('CORS_ALLOWED_ORIGIN_01'),
#     # env('CORS_ALLOWED_ORIGIN_02'),
# ]
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.example\.com$",
# ]
CORS_ALLOW_ALL_ORIGINS = True


# django-allauth settings
ACCOUNT_EMAIL_VERIFICATION = "optional"  # "mandatory" in production


