# Standard library
import json
from os import getcwd
from os.path import exists
# Overlord library
from core.library.version import Version
from .commands.install import (
  __init_config_directory__,
  __init_logs_directory__,
  make_clients_config,
  make_server_config,
  install_file
)
from .commands.node.share import __update_shared_files__

# Version Configuration
__version_control__ = {
  'major': 1,
  'minor': 2,
  'patch': 19
}
__version__ = Version(version_data=__version_control__)


def initialize_configurations():
  # Setup environment
  __init_config_directory__()
  __init_logs_directory__()

  # Default environment configuration
  client_data = make_clients_config()
  server_data = getcwd() + '/.config/server.json'

  if exists(server_data):
    with open(server_data) as server_data_file:
      server_data = json.loads(server_data_file.read())
  else:
    server_data = make_server_config()

  from web import settings
  settings.CLIENT_DATA = client_data
  settings.SERVER_DATA = server_data

  # Default start-up behavior
  __update_shared_files__()

  # Setup (web/urls.py)
  from core.library import url
  install_file('urls.py', '/web', getcwd(), log=False)
  load_order = url.make_client_load_order(client_data, server_data['INDEX'])
  url.write_urls(load_order, getcwd() + '/web/urls.py')

  # Generate (api/urls.py)
  statements = url.acquire_all_apis(client_data, getcwd())
  url.write_api_urls(statements, getcwd())
  url.write_api_models(statements, getcwd())

  # Initialize updater
  from core.tools.library import updater as __updater__
