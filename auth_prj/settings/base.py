"""
Django settings for auth_prj project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.conf import settings
from datetime import timedelta
import os
import environ


# Initialise environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
rabbitmq_host = env('RABBITMQ_HOST')

AUTH_USER_MODEL = 'auth_app.User'

LOGGER_NAME: str = "auth"
LOG_LEVEL: str = "DEBUG"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} | {asctime} | {name} | {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        LOGGER_NAME: {
            'handlers': ['console'],
            "level": LOG_LEVEL,
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_spectacular',
    'corsheaders',

    'auth_app'
]

MIDDLEWARE = [
    # CorsMiddleware doesn't support async making each request running in a new thread, destroying async benefits!
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'auth_prj.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`. This is the only backend by default
    "django.contrib.auth.backends.ModelBackend",
    # The following allauth setting needs to be present in order for allauth authentication to work properly.
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # It gets the jwt from the request header
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # It gets the jwt from the request cookie
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

LOGIN_URL = 'rest_framework:login'

# DJ_REST_AUTH settings
REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    # We can customize the jwt claim in the CustomTokenObtainPairSerializer and use that as the jwt_serializer
    "JWT_TOKEN_CLAIMS_SERIALIZER": "auth_app.serializers.CustomTokenObtainPairSerializer",
}
# these settings cause dj-rest-auth to return a Set-Cookie header to set the JWT cookies
# Set-Cookie: auth_prj_jwt_cookie=xxxxxxxxxxxxx; expires=Sat, 28 Mar 2020 18:59:00 GMT; HttpOnly; Max-Age=300; Path=/
# Have in mind that if you use a cookie to store the JWT you need to add CSRF protection. This means that you need to
# implement a "csrf get" endpoint.
# JWT_AUTH_COOKIE = 'auth_prj_jwt_cookie'
# JWT_AUTH_REFRESH_COOKIE = 'auth_prj_refresh_jwt_cookie'
# JWT_AUTH_SAMESITE = 'Lax'
# JWT_AUTH_COOKIE_USE_CSRF = True
# JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED = True

# SIMPLE_JWT settings
ACCESS_TOKEN_LIFETIME = timedelta(minutes=5)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Auth API',
    'DESCRIPTION': 'Authentication and Authorization API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# django-allauth settings
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_USERNAME_REQUIRED = False

