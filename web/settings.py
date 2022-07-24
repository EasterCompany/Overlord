# web/settings.py
#   automatically generated file
#   do not edit or delete

# Standard Library
import os
from sys import path
from json import loads

# Overlord Library
from core.library import numbers

# Overlord tools
from tools.commands.install import (
    __init_config_directory__,
    __init_logs_directory__,
    make_clients_config,
    make_server_config
)

# Load Custom Project Settings
BASE_DIR = path[0]
SECRET_DATA = {
    'SERVER_KEY': 'no secret key',
}

# Load Settings
__init_config_directory__()
__init_logs_directory__()

if not os.path.exists(BASE_DIR + '/.config/server.json'):
    make_server_config()

with open(BASE_DIR + '/.config/server.json') as SERVER_FILE:
    SERVER_DATA = loads(SERVER_FILE.read())

if not os.path.exists(BASE_DIR + '/.config/clients.json'):
    make_clients_config()

with open(BASE_DIR + '/.config/clients.json') as CLIENT_FILE:
    CLIENT_DATA = loads(CLIENT_FILE.read())

if not os.path.exists(BASE_DIR + '/.config/secret.json'):
    SECRET_DATA = {
        'ROOT_EMAIL': '',
        'SERVER_KEY': '',
        'PA_USER_ID': '',
        'PA_API_KEY': '',
        'DOMAIN_URL': ''
    }
else:
    with open(BASE_DIR + '/.config/secret.json') as SECRET_FILE:
        SECRET_DATA = loads(SECRET_FILE.read())

# Set Settings
ROOT_EMAIL = SECRET_DATA['ROOT_EMAIL']
SERVER_KEY = SECRET_DATA['SERVER_KEY']
SECRET_KEY = SECRET_DATA['SERVER_KEY']

INDEX = SERVER_DATA['INDEX']
DEBUG = SERVER_DATA['DEBUG']
LANGUAGE_CODE = SERVER_DATA['LANGUAGE_CODE']
TIME_ZONE = SERVER_DATA['TIME_ZONE']
USE_I18N = True
USE_TZ = True

ALLOWED_HOSTS = SERVER_DATA['ALLOWED_HOSTS']
INSTALLED_APPS = SERVER_DATA['INSTALLED_APPS']
MIDDLEWARE = SERVER_DATA['MIDDLEWARE']
ROOT_URLCONF = SERVER_DATA['ROOT_URLCONF']
WSGI_APPLICATION = SERVER_DATA['WSGI_APPLICATION']
TEMPLATES = [
    {
        'BACKEND': SERVER_DATA['BACKEND_TEMPLATE'],
        'DIRS': [
            os.path.join(BASE_DIR, 'static', client) for client in CLIENT_DATA
        ],
        'APP_DIRS': SERVER_DATA['APP_DIRS_TEMPLATE'],
        'OPTIONS': SERVER_DATA['OPTIONS_TEMPLATE']
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

STATIC_ROOT = BASE_DIR + '/static/.temp'
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR + '/static' ]

MEDIA_ROOT = BASE_DIR + '/assets'
MEDIA_URL = '/assets/'

CORS_ORIGIN_ALLOW_ALL = SERVER_DATA['CORS_ORIGIN_ALLOW_ALL']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',    # Default Django development server (standalone)
    'http://localhost:8000',    # Default Django development server
    'http://localhost:8100',    # Default React development client
    'http://localhost:45678'    # React-snap chrome client
] + [
    'http://localhost:81' + numbers.zero_prefixed_integer(x, 2) for x in range(1, 100)
    # Ports 8100 - 8199 are reserved for react development clients
]
