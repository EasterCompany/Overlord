# Standard library
import subprocess
from json import loads
from time import sleep
from shutil import rmtree
from os.path import exists
from threading import Thread
from datetime import datetime
from os import chdir, system, rename, remove
# Overlord library
from ..install import (
  __init_config_directory__,
  __init_logs_directory__,
  make_clients_config,
  make_server_config
)
from ..node.share import __update_shared_files__
from core.library import console, executable, is_alphanumeric, to_alphanumeric
from web.settings import BASE_DIR

# Variable app meta data
meta_data = {
  'time_of_last_build': datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
}


# Client build meta data
def update_client_meta_data(app_data):
  # Read index.html file content
  if BASE_DIR in app_data['static']:
    index_path = f"{app_data['static']}/index.html"
  else:
    index_path = f"{BASE_DIR}{app_data['static']}/index.html"

  # ERROR handling when index.html is not generated
  if not exists(index_path):
    index_path = index_path.replace('/index.html', '/index')

  # Read Content
  with open(index_path, 'r') as index_file:
    index_file_content = index_file.read()

  # Iterate over all variable meta data
  for tag in meta_data:
    index_file_content = \
      index_file_content.replace('{#' + tag + '#}', meta_data[tag])

  # Write new index.html file content
  with open(index_path, 'w+') as index_file:
    index_file.write(index_file_content)

  # Rename html tag from built index file
  rename(index_path, index_path.replace('.html', ''))

  # Remove status code specific html files
  if exists(app_data['static'] + '/200.html'):
    remove(app_data['static'] + '/200.html')
  if exists(app_data['static'] + '/404.html'):
    remove(app_data['static'] + '/404.html')
  return True


def client(app_data, build=False, app_name=""):
  """
  Runs a client using npm in development mode, not to be used on a live server unless using the 'build'
  parameter which builds the client for production

  :return None:
  """
  if build and 'build' in app_data:
    print(f"\n> {app_name} @ {clients_json[app_name]['version']}")

    console.out(f"  {console.wait} Installing", end="\r")
    subprocess.run(
      "npm install",
      shell=True,
      cwd=app_data['src'],
      bufsize=1,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
      universal_newlines=True
    )
    console.out("  ✅ Installed     ", "success")

    console.out(f"  {console.wait} Compiling", end="\r")
    subprocess.run(
      "npm run build",
      shell=True,
      cwd=app_data['src'],
      bufsize=1,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
      universal_newlines=True
    )
    console.out("  ✅ Compiled      ", "success")

    console.out(f"  {console.wait} Post-Processing", end="\r")
    update_client_meta_data(app_data)
    console.out("  ✅ Post-Processed    ", "success")

  elif not build and 'start' in app_data:
    subprocess.call("npm run start", shell=True, cwd=app_data['src'])


# Create client thread
new_client = lambda app_name, app_data, build: Thread(
  None,
  client,
  app_name + '-client',
  (app_data, build)
)

clients_json = {}


def update_client_json():
  global clients_json
  # All clients data from config file
  if exists(BASE_DIR + '/.config/clients.json'):
    with open(BASE_DIR + '/.config/clients.json') as clients_file:
      clients_json = loads(clients_file.read())
  else:
    clients_json = {}
  return clients_json


update_client_json()


# Initialize client
def initialize(target=None):
  return console.input(
    f'''{executable} -c "try:\n  '''
    f'''from core.tools import tools;from clients import {target};{target}.Client();\n'''
    f'''except: print('    > Error occurred when initializing {target}')"''',
    cwd=BASE_DIR,
    show_output=True
  )


def install(target:str = None) -> None:
  """
  Installs a specific client if a target is set and installs all clients if the target is None by
  downloading node modules, initializing the python init file and distributing any required shared
  files

  :param target str|None: specified client name
  :return None:
  """
  if target is None:
    console.out(f"\n> Installing All Clients")

  def run_install(client_path):
    console.out(f"  {console.wait} Downloading Node Modules", end="\r")
    console.input("npm install", cwd=client_path)
    console.out(f"  ✅ Downloaded Node Modules             ", "success")

  def init_client(client):
    console.out(f"  {console.wait} Initializing", end="\r")
    initialize(client)
    console.out(f"  ✅ Initialized             ", "success")

  def share_code(client):
    console.out(f"  {console.wait} Distributing Shared Files", end="\r")
    __update_shared_files__()
    console.out(f"  ✅ Distributed Shared Files             ", "success")

  update_client_json()

  if target is None:
    for client in clients_json:
      console.out(f"\n  - {client}")
      run_install(clients_json[client]['src'])
      init_client(client)
      share_code(client)
  else:
    console.out(f"\n> Installing `{target}`")
    run_install(clients_json[target]['src'])
    init_client(target)
    share_code(target)


# Run client
def run(name:str, build:bool, new_thread:bool):
  if name not in clients_json:
    print(f'\n    Client `{name}` does not exist\n')
    x = [ clients_json.keys(), None ]
    for client_name in x[0]:
      if name in client_name and x[1] is None: x[1] = name
      elif name in client_name and x[1] is not None: x[1] = None
    if x[1] is None:
      return 'Err0'
    else:
      return console.out()

  client_data = clients_json[name]
  if new_thread:
    thread = new_client(name, client_data, build)
    thread.start()
    sleep(3)
    return chdir(BASE_DIR)

  return client(client_data, build)


# Run all clients on a separate thread except the last one
def run_all(none_on_main_thread=False):
  for index, client in enumerate(clients_json):
    if index < len(clients_json) - 1 or none_on_main_thread:
      run(client, build=False, new_thread=True)
    else:
      run(client, build=False, new_thread=False)
  sleep(5)
  system('clear')
  return print('Running all clients ...\n')


# Build specific client on the main thread
def build(name):
  client(clients_json[name], build=True, app_name=name)


# Build all clients on the main thread
def build_all():
  console.out("\n> Global Build Options")

  console.out(f"  {console.wait} Updating shared files", end="\r")
  __update_shared_files__()
  console.out("  ✅ Updated Shared Files      ", "success")

  for _ in clients_json:
    client(clients_json[_], build=True, app_name=_)


# Create new client
def create(name:str, native:bool = False, custom_repo:str = None):
  """
  Create a new client from the basic web or native client templates or download a custom repo

  :param name str: name of the client (raw)
  :param native bool: is this a native client
  :param custom_repo str|None: ssh link for custom repo
  """
  if not is_alphanumeric(name):
    console.out(
      "\n[WARNING] Client names may only contain alphanumeric characters\n"
      "          including underscores and must be URL safe.\n\n"
      "          Any non-alphanumeric or underscore characters will be\n"
      "          purged from the name.",
      "yellow"
    )
    name = to_alphanumeric(name)

  def download_repo(repo_link, name):
    console.out(f"  {console.wait} Downloading ... ", end="\r")
    console.input(f"git clone {repo_link} {name}", cwd=BASE_DIR+'/clients')
    console.out(f"  ✅ Downloaded                  ", "success")

  def update_overlord_configuration():
    from core.library import url

    # Setup environment
    console.out(f"  {console.wait} Updating .config/*", end="\r")
    __init_config_directory__()
    __init_logs_directory__()

    # Default environment configuration
    client_data = make_clients_config(BASE_DIR)
    server_data = BASE_DIR + '/.config/server.json'

    if exists(server_data):
      with open(server_data) as server_data_file:
        server_data = loads(server_data_file.read())
    else:
      server_data = make_server_config(BASE_DIR)

    # Default start-up behavior
    __update_shared_files__()
    load_order = url.make_client_load_order(client_data, server_data['INDEX'])
    url.write_django_urls(load_order, BASE_DIR + '/web/urls.py')
    return console.out("  ✅ Updated .config/*        ", "success")

  # Make directory checks
  if exists(f'clients/{name}'):
    return console.out(f"[ERROR] Client with name `{name}` already exists.")

  # Fetch react-native app template from github
  if native:
    console.out("\n> Download Native Client Template")
    download_repo('git@github.com:EasterCompany/Overlord-Native-Client.git', name)

  # Fetch custom or existing client template from any git HTML or SSH repository link
  elif custom_repo is not None:
    console.out(f"\n> Download `{name}`")
    download_repo(custom_repo, name)
    update_overlord_configuration()
    install(name)
    return console.out("\nDone!", "success")

  # Fetch default react-web template from github
  else:
    console.out("\n> Download Web Client Template")
    download_repo('git@github.com:EasterCompany/Overlord-Web-Client.git', name)

  # De-git repository
  console.out(f"  {console.wait} Removing .git/*", end="\r")
  rmtree(f'clients/{name}/.git')
  console.out("  ✅ Removed .git/*              ", "success")

  # Update meta_data
  if exists(f'clients/{name}/public/static/app-name'):
    console.out(f"  {console.wait} Updating meta file", end="\r")
    rename(f'clients/{name}/public/static/app-name', f'clients/{name}/public/static/{name}')
    console.out("  ✅ Updated meta file            ", "success")

  if native:
    # Update native app.json
    console.out(f"  {console.wait} Updating app.json", end="\r")
    with open(f'clients/{name}/app.json') as package:
      content = package.read()
      content = content.replace('app-name', name.lower())
      with open(f'clients/{name}/app.json', 'w') as new_file:
        new_file.write(content)
    console.out("  ✅ Updated app.json              ", "success")

  else:
    # Update index.html
    console.out(f"  {console.wait} Updating public/index.html", end="\r")
    with open(f'clients/{name}/public/index.html') as index_content:
      content = index_content.read()
      content = content.replace('{#app_name#}', name)
      with open(f'clients/{name}/public/index.html', 'w') as new_file:
        new_file.write(content)
    console.out("  ✅ Updated public/index.html              ", "success")

    # Update manifest.json
    console.out(f"  {console.wait} Updating public/manifest.json", end="\r")
    with open(f'{BASE_DIR}/clients/{name}/public/manifest.json') as manifest:
      content = manifest.read()
      content = content.replace('app-name', name)
      with open(f'{BASE_DIR}/clients/{name}/public/manifest.json', 'w') as new_file:
        new_file.write(content)
    console.out("  ✅ Updated public/manifest.json              ", "success")

  # Update package.json
  console.out(f"  {console.wait} Updating package.json", end="\r")
  with open(f'{BASE_DIR}/clients/{name}/package.json') as package:
    content = package.read()
    content = content.replace('app-name', name)
    with open(f'{BASE_DIR}/clients/{name}/package.json', 'w') as new_file:
      new_file.write(content)
  console.out("  ✅ Updated package.json              ", "success")

  # Update shared.json
  if exists(f"{BASE_DIR}/clients/{name}/shared.json"):
    console.out(f"  {console.wait} Updating shared.json", end="\r")
    with open(f'{BASE_DIR}/clients/{name}/shared.json') as shared:
      content = shared.read()
      content = content.replace('overlord_web_client', name)
      with open(f'{BASE_DIR}/clients/{name}/shared.json', 'w') as new_file:
        new_file.write(content)
    console.out("  ✅ Updated shared.json              ", "success")

  update_overlord_configuration()
  return install(name)


def error_message():
  """
  Outputs an instructional error message to the console interface
  """
  return console.out("""
  `CLIENTS` tool requires at least one argument beginning with `-`

    ./o run
    ./o run -client_name
    ./o runclient -client_name
    ./o build -client_name

  or use -all to effect all clients

    ./o run -all
    ./o build -all

  to view details on the `create` command enter:

    ./o create
  """)


def create_cmd_error_message() -> None:
  """
  Outputs an instructional error message to the console interface
  """
  return console.out("""
  The `CREATE` command requires 1 or 2 arguments

  to create a custom client enter a repo link as an argument

    ./o create -<git_repo_link>

    or use a custom name

    ./o create -<git_repo_link> -<client_name>

  to create a web client enter a name as an argument

    ./o create -<client_name>

  to create a native client use the `-native` argument first

    ./o create -native -<client_name>

  to create an API use the `-api` argument first

    ./o create -api -<api_name>

    or use a custom template

    ./o create -api -<git_repo_link>

    or use a custom template with a custom name

    ./o create -api -<git_repo_link> -<api_name>
  """)
