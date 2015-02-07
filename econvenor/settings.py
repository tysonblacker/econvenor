"""
Django settings for econvenor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Set the templates directory
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, '../utilities/management/commands/templates'),
    )

# Get the environment (development/test/production)
ENVIRONMENT= os.environ['ECONVENOR_ENVIRONMENT']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['ECONVENOR_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'development':
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS =[
        '.econvenor.org',
    ]

# Application definition
# --------------------------------------------------------

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',

    'accounts',
    'authentication',
    'bugs',
    'common',
    'dashboard',
    'decisions',
    'docs',
    'help',
    'landing',
    'meetings',
    'participants',
    'tasks',
    'registration',
    'templatetags',
    'utilities',
)

try:
    import django_extensions
    INSTALLED_APPS += (
        'django_extensions',
    )
except ImportError:
    pass

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'authentication.backends.EmailModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'econvenor.urls'

WSGI_APPLICATION = 'econvenor.wsgi.application'

ADMINS = (('Error Notifications', 'errors@econvenor.org'),)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASE_PASSWORD = os.environ['ECONVENOR_DATABASE_PASSWORD']
DATABASE_USER = os.environ['ECONVENOR_DATABASE_USER']
DATABASE_NAME = os.environ['ECONVENOR_DATABASE_NAME']

if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'commonstatic'),
)

if ENVIRONMENT == 'production':
    STATIC_ROOT = '/home/econvenor/webapps/econvenor_static/'
elif ENVIRONMENT == 'test':
    STATIC_ROOT = '/home/econvenor/webapps/test_econvenor_static/'
elif ENVIRONMENT == 'development':
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Media files
# https://docs.djangoproject.com/en/dev/howto/static-files/

MEDIA_URL = '/media/'

if ENVIRONMENT == 'production':
    MEDIA_ROOT = '/home/econvenor/webapps/econvenor_media/'
elif ENVIRONMENT == 'test':
    MEDIA_ROOT = '/home/econvenor/webapps/test_econvenor_media/'
elif ENVIRONMENT == 'development':
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Email
# https://docs.djangoproject.com/en/1.6/topics/email/

if ENVIRONMENT == 'production':
    EMAIL_HOST = 'smtp.webfaction.com'
    EMAIL_PORT = os.environ['ECONVENOR_EMAIL_PORT']
    EMAIL_HOST_USER = 'econvenor_noreply'
    EMAIL_HOST_PASSWORD = os.environ['ECONVENOR_EMAIL_PASSWORD']
    DEFAULT_FROM_EMAIL = 'noreply@econvenor.org'
    SERVER_EMAIL = 'mail@econvenor.org'
elif ENVIRONMENT == 'test':
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/home/econvenor/webapps/test_econvenor/test_data/emails'
elif ENVIRONMENT == 'development':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Dates and times
# --------------------------------------------------------

DATE_FORMAT = 'd M Y'

DATE_INPUT_FORMATS = (
    '%d %b %Y',
)

TIME_FORMAT = 'g:i a'

TIME_INPUT_FORMATS = (
    '%I:%M %p',
)

# Fixtures
# https://docs.djangoproject.com/en/1.6/howto/initial-data/#providing-initial-data-with-fixtures

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
    )
