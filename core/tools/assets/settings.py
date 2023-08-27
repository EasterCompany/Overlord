# web/settings.py
#   automatically generated file
#   do not remove (although edits are acceptable)

# Standard library
import os
import mimetypes
from json import loads

# Overlord library
from core.tools.commands.install import (
  __init_config_directory__,
  __init_logs_directory__,
  make_clients_config,
  make_server_config,
  make_secrets_file
)

# Default Project Configuration
BASE_DIR = os.getcwd()
PROJECT_NAME = os.path.basename(BASE_DIR)
LOGGER_DIR = f"{BASE_DIR}/.logs/logger"
SECRET_DATA = {
  'SECRET_KEY': 'no secret key',
}

# Load JSON Configuration Files
__init_config_directory__()
__init_logs_directory__()

# Initialize Server File
if not os.path.exists(BASE_DIR + '/.config/server.json'):
  make_server_config()
with open(BASE_DIR + '/.config/server.json', 'r') as SERVER_FILE:
  SERVER_DATA = loads(SERVER_FILE.read())

# Initialize Clients File
if not os.path.exists(BASE_DIR + '/.config/clients.json'):
  make_clients_config()
with open(BASE_DIR + '/.config/clients.json', 'r') as CLIENT_FILE:
  CLIENT_DATA = loads(CLIENT_FILE.read())

# Initialize Secrets Files
if not os.path.exists(BASE_DIR + '/.config/secret.json'):
  make_secrets_file()
with open(BASE_DIR + '/.config/secret.json', 'r') as SECRET_FILE:
  SECRET_DATA = loads(SECRET_FILE.read())

# Set Administration Configuration
ROOT_EMAIL = SECRET_DATA['ROOT_EMAIL']
SECRET_KEY = SECRET_DATA['SECRET_KEY']
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
ASGI_APPLICATION = SERVER_DATA['ASGI_APPLICATION']

if not DEBUG:
  from core.library import redis

CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels.layers.InMemoryChannelLayer'
  }
} if DEBUG else {
  "default": {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
      "hosts": [(redis.host, redis.port)],
    },
  },
}

TEMPLATES = [
  {
    'BACKEND': SERVER_DATA['BACKEND_TEMPLATE'],
    'DIRS': [f"{BASE_DIR}/static/{client}" for client in CLIENT_DATA],
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

STATIC_FILES = BASE_DIR + '/static'
STATIC_ROOT = STATIC_FILES if not DEBUG else None
STATIC_URL = SERVER_DATA['STATIC_URL']
STATICFILES_DIRS = [] if not DEBUG else [ STATIC_FILES ]

MEDIA_ROOT = SERVER_DATA['MEDIA_DIR']
MEDIA_URL = SERVER_DATA['MEDIA_URL']
DATA_UPLOAD_MAX_MEMORY_SIZE = 20000000000

if not os.path.exists(STATIC_FILES):
  os.mkdir(STATIC_FILES)

if not os.path.exists(MEDIA_ROOT):
  os.mkdir(MEDIA_ROOT)

CORS_ORIGIN_ALLOW_ALL = True if DEBUG else SERVER_DATA['CORS_ORIGIN_ALLOW_ALL']
CORS_ORIGIN_WHITELIST = SERVER_DATA['CORS_ORIGIN_WHITELIST']

# Set default mime type assumptions
mimetypes.add_type("text/html", "", True)
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/x-javascript", ".js", True)
