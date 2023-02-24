# web/settings.py
#   automatically generated file
#   do not remove (although edits are acceptable)

# Standard library
import os
import mimetypes
from json import loads

# Overlord library
from core.library import numbers
from core.tools.commands.install import (
    __init_config_directory__,
    __init_logs_directory__,
    make_clients_config,
    make_server_config,
    make_secrets_file
)

# Default Project Configuration
BASE_DIR = os.getcwd()
LOGGER_DIR = f"{BASE_DIR}/.logs/logger"
SECRET_DATA = {
    'SERVER_KEY': 'no secret key',
}

# Load JSON Configuration Files
__init_config_directory__()
__init_logs_directory__()

# Initialize Server File
if not os.path.exists(BASE_DIR + '/.config/server.json'):
    make_server_config()
with open(BASE_DIR + '/.config/server.json') as SERVER_FILE:
    SERVER_DATA = loads(SERVER_FILE.read())

# Initialize Clients File
if not os.path.exists(BASE_DIR + '/.config/clients.json'):
    make_clients_config()
with open(BASE_DIR + '/.config/clients.json') as CLIENT_FILE:
    CLIENT_DATA = loads(CLIENT_FILE.read())

# Initialize Secrets Files
if not os.path.exists(BASE_DIR + '/.config/secret.json'):
    make_secrets_file()
with open(BASE_DIR + '/.config/secret.json') as SECRET_FILE:
    SECRET_DATA = loads(SECRET_FILE.read())

# Set Administration Configuration
ROOT_EMAIL = SECRET_DATA['ROOT_EMAIL']
SERVER_KEY = SECRET_DATA['SERVER_KEY']
SECRET_KEY = SECRET_DATA['SERVER_KEY']
PUBLIC_KEY = SECRET_DATA['PUBLIC_KEY']

# Set Server Configuration
INDEX = SERVER_DATA['INDEX']
DEBUG = SERVER_DATA['DEBUG']
LOCAL_BRANCH = SERVER_DATA['LOCAL_BRANCH']
STAGING_BRANCH = SERVER_DATA['STAGING_BRANCH']
PRODUCTION_BRANCH = SERVER_DATA['PRODUCTION_BRANCH']
LANGUAGE_CODE = SERVER_DATA['LANGUAGE_CODE']
TIME_ZONE = SERVER_DATA['TIME_ZONE']
USE_I18N = True
USE_TZ = True

ALLOWED_HOSTS = SERVER_DATA['ALLOWED_HOSTS'] if not DEBUG else ['*']
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

STATIC_URL = SERVER_DATA['STATIC_URL']
STATICFILES_DIRS = [ SERVER_DATA['STATIC_DIR'], ]

MEDIA_ROOT = BASE_DIR + '/assets'
MEDIA_URL = '/assets/'

CORS_ORIGIN_ALLOW_ALL = SERVER_DATA['CORS_ORIGIN_ALLOW_ALL']

if DEBUG:
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3000',    # Default Django development server (standalone)
        'http://localhost:8000',    # Default Django development server
        'http://localhost:8100',    # Default React development client
        'http://localhost:45678'    # React-snap chrome client
    ] + [
        'http://localhost:81' + numbers.zero_prefixed_integer(x, 2) for x in range(1, 100)
        # Ports 8100 - 8199 are reserved for react development clients
    ]
else:
    CORS_ORIGIN_WHITELIST = [
        'https://www.easter.company'    # Allows this application to be managed by E-Panel
    ]

# Sets mime types for specific file types
mimetypes.add_type("text/html", "", True)
mimetypes.add_type("text/javascript", ".js", True)
mimetypes.add_type("text/css", ".css", True)
