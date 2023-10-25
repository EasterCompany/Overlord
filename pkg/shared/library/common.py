from .version import __version__
from .console import console
from . import time, settings

import os
import json
import base64
import socket
import secrets
import platform
import subprocess
from pathlib import Path as path
from sys import executable
from os import mkdir, rmdir, remove, walk, listdir, environ, makedirs as mkdirs, rename
from os.path import exists, realpath, dirname, isdir, abspath, basename, getsize, splitext
from shutil import rmtree, copy, copytree, make_archive, move
from urllib.parse import unquote
from uuid import uuid1
from time import sleep
from getpass import getpass
from cryptography.fernet import Fernet

# Shortcuts
from django.shortcuts import render

# App
from django.apps import AppConfig

# Core
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
from wsgiref.util import FileWrapper
from django.utils.crypto import get_random_string

# Views
from django.views.generic.base import RedirectView


def uuid() -> str:
  return str(uuid1())