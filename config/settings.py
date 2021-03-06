"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',

    # Internal Apps
    'src.apps.SrcConfig',
    'api.apps.ApiConfig',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'src.libraries.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'src.libraries.CustomPagination',
    'PAGE_SIZE': 10,
}

# CORS HEADER CONFIGURATION
# ------------------------------------------------------------------------------
# default False  if True, the whitelist will not be used and all origins
# will be accepted
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST: specify a list of origin hostnames that are authorized
# to make a cross-site HTTP request
# CORS_ORIGIN_WHITELIST = (
#         'google.com',
#         'hostname.example.com'
#     )
CORS_ORIGIN_WHITELIST = ()

# CORS_ORIGIN_REGEX_WHITELIST: specify a regex list of origin hostnames
# that are authorized to make a cross-site HTTP request;
# Useful when you have a large amount of subdomains for instance.
# CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(\w+\.)?google\.com$', )
CORS_ORIGIN_REGEX_WHITELIST = ()

# CORS_URLS_REGEX: specify a URL regex for which to enable
# the sending of CORS headers;
# Useful when you only want to enable CORS for specific URLs, e. g.
# for a REST API under /api/.
# CORS_URLS_REGEX = r'^/api/.*$'
CORS_URLS_REGEX = '^.*$'

# CORS_ALLOW_METHODS: specify the allowed HTTP methods that can be used when
# making the actual request
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)
# CORS_ALLOW_HEADERS: specify which non-standard HTTP headers can be used when
# making the actual request
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)
# CORS_EXPOSE_HEADERS: specify which HTTP headers are to be exposed to the browser
CORS_EXPOSE_HEADERS = ()

# CORS_PREFLIGHT_MAX_AGE: specify the number of seconds a client/browser
# can cache the preflight response
CORS_PREFLIGHT_MAX_AGE = 86400

# CORS_ALLOW_CREDENTIALS: specify whether or not cookies are allowed
# to be included in cross-site HTTP requests (CORS).
CORS_ALLOW_CREDENTIALS = False


try:
    from local_settings import *
except ImportError:
    pass
