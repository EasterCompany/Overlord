import os
import mimetypes
from pathlib import Path

BASE_DIR = os.getcwd()
PROJECT_NAME = os.path.basename(BASE_DIR)
INDEX = "olt"
DEBUG = True
SECRET_KEY = ""
PUBLIC_KEY = ""
LOCAL_BRANCH = "development"
STAGING_BRANCH = "staging"
PRODUCTION_BRANCH = "production"
LANGUAGE_CODE = ""
TIME_ZONE = ""
USE_I18N = True
USE_TZ = True
ALLOWED_HOSTS = [] if not DEBUG else ['*']

INSTALLED_APPS = [
  'daphne',
  'corsheaders',

  'channels',
  'channels.auth',
  'channels.db',
  'channels.security',
  'channels.layers',
  'channels.auth.auth_middleware',
  'channels.auth.channel_session',
  'channels.auth.channel_auth',
  'channels.routing',

  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django_extensions',

  'shared.user',
  'shared.olt',
]

MIDDLEWARE = [
  "corsheaders.middleware.CorsMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "whitenoise.middleware.WhiteNoiseMiddleware"
]

ROOT_URLCONF = "conf.urls"
WSGI_APPLICATION = "conf.wsgi.application"
ASGI_APPLICATION = "conf.asgi.application"
CHANNEL_LAYERS = {
  "default": {
    "BACKEND": "channels_redis.core.RedisChannelLayer",
    "CONFIG": {
      "hosts": [("localhost", "6379")],
    }
  }
}

TEMPLATES = [
  {
    'BACKEND': "django.template.backends.django.DjangoTemplates",
    'DIRS': [f"{BASE_DIR}/static/{client}" for client in CLIENT_DATA],
    'APP_DIRS': True,
    'OPTIONS':{
      "context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages"
      ]
    },
  },
]

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '',
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
STATIC_URL = "/static/"
STATICFILES_DIRS = [] if not DEBUG else [ STATIC_FILES ]
MEDIA_ROOT = STATIC_FILES + '/shared'
MEDIA_URL = '/shared/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 1000000000

if not os.path.exists(STATIC_FILES):
  os.mkdir(STATIC_FILES)

if not os.path.exists(MEDIA_ROOT):
  os.mkdir(MEDIA_ROOT)

if not os.path.exists(Path(f"{STATIC_FILES}{MEDIA_URL}")):
  os.symlink(
    Path(MEDIA_ROOT),
    Path(f"{STATIC_FILES}{MEDIA_URL}"),
    target_is_directory=True
  )

CORS_ORIGIN_ALLOW_ALL = True if DEBUG else False
CORS_ORIGIN_WHITELIST = ["https://olt.easter.company"] if not DEBUG else ["*"]
mimetypes.add_type("text/html", "", True)
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/x-javascript", ".js", True)
