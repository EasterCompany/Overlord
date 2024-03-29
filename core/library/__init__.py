#  Core Wrapper Library
#    contains wrapper functions used for
#    integrating with other libraries

# Standard library
import json
import base64
import socket
import secrets
import subprocess
from pathlib import Path
from sys import executable
from os import mkdir, rmdir, remove, walk, listdir, environ, makedirs as mkdirs, rename
from os.path import exists, realpath, dirname, isdir, abspath, basename, getsize, splitext
from shutil import rmtree, copy, make_archive, move
from urllib.parse import unquote
from uuid import uuid1
from time import sleep

# Shortcuts
from django.shortcuts import render

# App
from django.apps import AppConfig

# Core
from core.library.regex import is_alphanumeric, to_alphanumeric
from core.library.console_lib import console
from core.library.api import get_api_url, get_arg, get_body, get_json, get_user
from core.library.cryptography import encrypt, decrypt
from core.library.time import get_datetime_string
from django.core.asgi import get_asgi_application as __asgi_application__
from django.core.management import execute_from_command_line
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import default_storage

# Channels
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer, AsyncWebsocketConsumer, \
  AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer, InvalidChannelLayerError

# Conf
from django.conf import settings
from django.conf.urls.static import static

# Contrib
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

# Database
from django.db import models, DatabaseError, IntegrityError

# Http
from django.http import JsonResponse, HttpResponse, FileResponse

# Template
from django.template import loader as html_loader

# Urls
from django.urls import path, re_path, include, URLResolver

# Utils
from django.utils.crypto import get_random_string

# Views
from django.views.generic.base import RedirectView


def uuid() -> str:
  return str(uuid1())


def asgi_interface():
  environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
  return ASGIStaticFilesHandler(__asgi_application__())


def asgi_with_channels_interface() -> ProtocolTypeRouter:
  import django
  environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
  django.setup(set_prefix=False)
  from api.urls import SOCKETS
  return ProtocolTypeRouter({
    'http': __asgi_application__(),
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(SOCKETS))),
  })


hostname = socket.gethostname()
local_ip = None

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as _s:
  try:
    _s.connect(("8.8.8.8", 80))
    local_ip = _s.getsockname()[0]
  except:
    local_ip = None
