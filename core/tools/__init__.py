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
    'type': 'DEV',
    'major': 1,
    'minor': 2,
    'patch': 0,
    'release': 1
}
__version__ = Version(version_data=__version_control__)

# Setup environment
__init_config_directory__()
__init_logs_directory__()

# Default environment configuration
client_data = make_clients_config(getcwd())
server_data = getcwd() + '/.config/server.json'

if exists(server_data):
    with open(server_data) as server_data_file:
        server_data = json.loads(server_data_file.read())
else:
    server_data = make_server_config(getcwd())

# Default start-up behavior
__update_shared_files__()

# Setup (web/urls.py) installed clients config file
install_file('urls.py', '/web', getcwd(), log=False)

from core.library import url
load_order = url.make_client_load_order(client_data, server_data['INDEX'])
url.write_django_urls(load_order, getcwd() + '/web/urls.py')
