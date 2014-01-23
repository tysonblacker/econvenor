"""
Django settings for econvener project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&2ow6l#7kb*otqk%v0gcdmm@5jelpp$81af6+s^kb0l&8*$1(e'

# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() == 'web439.webfaction.com':
	DEBUG = False
	TEMPLATE_DEBUG = False
	ALLOWED_HOSTS =[
		'.econvenor.org',
	]
else:
	DEBUG = True
	TEMPLATE_DEBUG = True
	ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'core.templatetags',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'econvener.urls'

WSGI_APPLICATION = 'econvener.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if socket.gethostname() == 'web439.webfaction.com':
	DATABASES = {
    	'default': {
    	    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    	    'NAME': 'econvenor_db',
		'USER': 'econvenor_admin',
		'PASSWORD': 'VVYgTyJY)NPro<KaD2XX&<4<i',
    	}
	}
else:
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

if socket.gethostname() == 'web439.webfaction.com':
	STATIC_ROOT = '/home/econvenor/webapps/static_econvener/'
