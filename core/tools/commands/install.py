# Standard library
import json
import secrets
from sys import path
from os import scandir, mkdir, system
from os.path import exists, join as pathjoin
# Overlord library
from core.library.time import timestamp


# --------------------------- CREATE & CONFIRM CONFIG EXISTS --------------------------- #
def __init_config_directory__(project_path='.'):
  if not exists(project_path + '/.config'):
    mkdir(project_path + '/.config')


# -------------------------- CREATE & CONFIRM LOGS DIR EXISTS -------------------------- #
def __init_logs_directory__(project_path='.'):
  if not exists(project_path + '/.logs'):
    mkdir(project_path + '/.logs')
  if not exists(project_path + '/.logs/requests.json'):
    with open(project_path + '/.logs/requests.json', 'w+') as req_json:
      req_json.write('{\n}')
  if not exists(project_path + '/.logs/logger'):
    with open(project_path + '/.logs/logger', 'w+') as logger:
      logger.write(f'[{timestamp()}] Created log file')


# -------------------------- CONFIRM CONFIG JSON FILE EXISTS --------------------------- #
def dump_json(filename, data, project_path='.'):
  file_path = project_path + '/.config/' + filename + '.json'
  with open(file_path, 'w') as conf_file:
    json.dump(
      data,
      conf_file,
      indent=2
    )


def install_file(filename, destination, project_path='.', log=True):
  if log:
    print('Installing', filename, 'to', destination, '...')
  with open(project_path + '/core/tools/assets/' + filename) as base:
    with open(project_path + destination + '/' + filename, 'w+') as new_file:
      new_file.write(base.read())


def make_clients_config(project_path='.'):
  client_paths  = sorted([
    f.path for f in scandir(project_path + "/clients") if f.is_dir()
  ])
  clients = {}

  for client in client_paths:
    files = [
      f.path.split("/")[-1] for f in scandir(client) if not f.is_dir()
    ]

    node = "package.json" in files
    scripts = {
      "api-git": None,
      "test": None,
      "start": None,
      "build": None,
      "version": None,
    }

    if node:
      package = open(client + "/package.json")
      package_json = json.load(package)

      if 'version' in package_json:
        scripts['version'] = package_json['version']

      if 'api-git' in package_json:
        scripts['api-git'] = package_json['api-git']

      for key in package_json["scripts"]:
        if key in scripts:
          scripts[key] = package_json["scripts"][key]

    if client.split("/")[-1] != 'shared':
      clients[client.split("/")[-1]] = {
        "src": client,
        "api": scripts["api-git"],
        "static": f'{path[0]}/static/{client.split("/")[-1]}',
        "node": node,
        "test": scripts["test"],
        "start": scripts["start"],
        "build": scripts["build"],
        "version": scripts["version"]
      }

  dump_json('clients', clients, project_path)
  return clients


def make_server_config(project_path='.'):
  print('Generating server config...')

  server_core_data = {
    "INDEX": 'e_panel',
    "DEBUG": True,
    "STANDALONE": False,
    "LANGUAGE_CODE": 'en-gb',
    "TIME_ZONE": 'UTC',
    "ALLOWED_HOSTS": [
      '.0.0.0.0',
      '.127.0.0.1',
      '.localhost',
      '.easter.company',
      '.eastercompany.eu.pythonanywhere.com',
    ],
    "INSTALLED_APPS": [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'django_extensions',
      'corsheaders',
    ],
    "MIDDLEWARE": [
      "corsheaders.middleware.CorsMiddleware",
      "django.middleware.common.CommonMiddleware",
      "django.middleware.security.SecurityMiddleware",
      "django.contrib.sessions.middleware.SessionMiddleware",
      "django.contrib.auth.middleware.AuthenticationMiddleware",
      "django.contrib.messages.middleware.MessageMiddleware",
      "whitenoise.middleware.WhiteNoiseMiddleware"
    ],
    "ROOT_URLCONF": 'web.urls',
    "WSGI_APPLICATION": 'web.wsgi.application',
    "BACKEND_TEMPLATE": 'django.template.backends.django.DjangoTemplates',
    "OPTIONS_TEMPLATE": {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
    "APP_DIRS_TEMPLATE": True,
    "STATIC_URL": '/static/',
    "STATIC_DIR": pathjoin(path[0], 'static'),
    "CORS_ORIGIN_ALLOW_ALL": True,
  }

  def is_app(f):
    ignored_dirs = (
      'assets', 'clients', 'static', 'tasks', 'tools', 'web'
    )
    if f.is_dir() and not f.name.startswith('.') and not f.name in ignored_dirs:
      return True
    return False

  installed_apps = [
    f.path.split("/")[-1] for f in scandir(project_path) if is_app(f)
  ]

  server_core_data["INSTALLED_APPS"] += installed_apps

  dump_json('server', server_core_data, project_path)
  return server_core_data


def django_files(project_path='.'):
  install_file('settings.py', '/web', project_path)
  install_file('urls.py', '/web', project_path)


def secrets_file(project_path='.'):
  print('Generating secrets config...')
  token_data = {
    "ROOT_EMAIL": "root@example.com",
    "SERVER_KEY": secrets.token_urlsafe(),
    "PUBLIC_KEY": secrets.token_urlsafe(),
    "PA_USER_ID": "",
    "PA_API_KEY": "",
    "DOMAIN_URL": "",
    "EMAIL_USER": "",
    "EMAIL_PASS": "",
    "REDIS-USER": "",
    "REDIS-PASS": "",
    "REDIS-HTTP": ""
  }
  return dump_json('secret', token_data, project_path)


def o_file(project_path='.'):
  print("Generating o file...")
  with open(f"{project_path}/o", "w") as o_file:
    o_file.write(f"""#!/bin/bash
cd {project_path}
clear
/usr/bin/python3 -c "
from sys import path;from os import environ;from core.tools import tools;
if project_home not in path: path.insert(0, {project_path});
from django.core.wsgi import get_wsgi_application;
application = get_wsgi_application();
tools.run();
"
""")
  system("chmod +x ./o")
