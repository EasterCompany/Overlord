#  Core Wrapper Library
#    contains wrapper functions used for
#    integrating with other libraries

# Standard library
import json
import secrets
import subprocess
from pathlib import Path
from sys import executable
from os import mkdir, rmdir, remove
from os.path import exists, realpath, dirname
from urllib.parse import unquote
from uuid import uuid1 as uuid
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
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Conf
from django.conf import settings
from django.conf.urls.static import static

# Database
from django.db import models

# Http
from django.http import JsonResponse, HttpResponse

# Template
from django.template import loader as html_loader

# Urls
from django.urls import path, re_path, include

# Utils
from django.utils.crypto import get_random_string
