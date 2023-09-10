'''
React Native & Web (Client) Code Sharing Tool

Share your apps, assets, components and libraries across multiple React clients.
All sharable components will be housed in `clients/shared` directory and any client they
are shared with will be automatically updated with the latest version any time a change
is made to the shared directory version of that file.

For our commands we will require two arguments, the first being a path to a module or file
from within the `clients/shared` directory - and the second being the name of a client
within the `clients` root directory.

Example Usage (template):

    to share an entire folder

  ./o share -"module_path" -"client_name"

    or for a single file

  ./o share -"file_path" -"client_name"

Example Usage (working example):

    to share an entire folder

  ./o share -library/server -e_panel

    or for a single file

  ./o share -library/server/request.ts -e_panel
'''
import json
import threading
from time import sleep
from shutil import copy
from os import mkdir, remove, walk
from os.path import exists, isdir, getmtime
from distutils.dir_util import copy_tree
from core.library import console
from web import settings
from web.settings import BASE_DIR

client_log = lambda client: settings.CLIENT_DATA[client]['src'] + '/shared.json'


def get_client_log(client):
  _log_path = client_log(client)
  _src_path = f"clients/{client}/src/shared" if exists(f"clients/{client}/src") else f"clients/{client}/shared"

  if exists(_log_path):
    with open(_log_path, 'r') as log_file:
      _log = json.load(log_file)

  else:
    _log = {
      "path": _src_path,
      "file": [],
      "module": []
    }

  return _log


def get_log():
  _log = {}
  for client in settings.CLIENT_DATA:
    try:
      _log[client] = get_client_log(client)
    except:
      pass
  return _log


def save_client_log(client, log_content):
  _log_path = client_log(client)
  with open(_log_path, 'w+') as log_file:
    json.dump(log_content, log_file, indent=2)


def save_log(log_content):
  for client in log_content:
    save_client_log(client, log_content[client])


def add_to_log(shared_path, client_name, share_type):
  log = get_log()

  # All shared files must be within the directory
  if not shared_path.startswith('/'):
    shared_path = '/' + shared_path

  # Prevents sharing of the .log file
  if shared_path == '/.log':
    console.out("You can't share the log file.", "red")
    return None

  # Append client to log
  if client_name not in log:
    _path = 'clients/' + client_name + '/shared'            # Native Client Shared Directory

    if exists(f'clients/{client_name}/src'):
      _path = 'clients/' + client_name + '/src/shared'    # Web Client Shared Directory

    log[client_name] = {
      "path": _path,
      "file": [],
      "module": []
    }

  # Optimize file sharing
  for ms in log[client_name]['module']:
    if shared_path.startswith(ms):
      print('''
  {path} is already shared with {name} via a module.
      '''.format(
      path=console.out(shared_path, 'yellow'),
      name=console.out(client_name, 'yellow')
        )
      )
      return

  # Write to log file
  if shared_path not in log[client_name][share_type]:
    if exists(BASE_DIR + '/clients/shared/' + shared_path):
      if exists(BASE_DIR + '/clients/' + client_name):
        log[client_name][share_type].append(shared_path)
      else:
        return console.out(f"\n    '{client_name}' client does not exist", "red")
    else:
      return console.out(f"\n    '{shared_path}' does not exist in the shared directory", "red")
  else:
    console.out(
      "\n    {path} is already shared with {name}".format(
        path=console.out(shared_path, 'yellow', False),
        name=console.out(client_name, 'yellow', False)
      )
    )
    return

  # Optimize module sharing
  if share_type == 'module':

    removed_files = []
    for fs in log[client_name]['file']:
      if fs.startswith(shared_path):
        log[client_name]['file'].remove(fs)
        removed_files.append(fs)

    removed_modules = []
    for ms in log[client_name]['module']:
      if ms.startswith(shared_path) and not ms == shared_path:
        log[client_name]['module'].remove(ms)
        removed_modules.append(ms)

    if len(removed_files) > 0:
      print('''
  Removed {x} file(s) from {name} because they're
  included within {path}'''.format(
    x=console.out(str(len(removed_files)), 'blue', False),
    path=console.out(shared_path, 'blue', False),
    name=console.out(client_name, 'blue', False)
  ))

    if len(removed_modules) > 0:
      print('''
  Removed {x} submodule(s) from {name} because they're
  included within {path}'''.format(
    x=console.out(str(len(removed_modules)), 'blue', False),
    path=console.out(shared_path, 'blue', False),
    name=console.out(client_name, 'blue', False)
  ))

  # Save log file
  save_log(log)

  # Return success!
  return print("\n    shared {path} with {name}".format(
    path=console.out(shared_path, 'green', False),
    name=console.out(client_name, 'green', False)
  )), __update_shared_files__()


def share_module(module_path, client):
  if module_path.startswith('/'):
    mdirs = module_path.split('/')[1:]
  else:
    mdirs = module_path.split('/')
  share = '/'.join(mdirs)
  if not share.endswith('/'):
    share += '/'
  add_to_log(share, client, 'module')


def share_file(file_path, client):
  if file_path.startswith('/'):
    fdirs = file_path.split('/')[1:-1]
  else:
    fdirs = file_path.split('/')[:-1]
  fname = file_path.split('/')[-1]
  share = '/'.join(fdirs) + '/' + fname
  add_to_log(share, client, 'file')


def target(path_to_target, client):
  if isdir(BASE_DIR + '/clients/shared/' + path_to_target):
    return share_module(path_to_target, client)
  return share_file(path_to_target, client)


def __update_clients_files__(client, logs, spath):
  """
  This is the background worker function for the share tool
  from this function we check for updated /shared/... files and then
  re-share them with their targeted clients within this servers scope.
  """
  if client not in logs or client not in settings.CLIENT_DATA or 'path' not in logs[client]:
    return None

  cpath = BASE_DIR + '/' + logs[client]['path'] + '/'

  def do_copy(orig, dest, is_dir=False):

    def get_dir_time(dir_path):
      update_times = [0, ]
      for root,_,fs in walk(dir_path):
        if not root.endswith('/'):
          root += '/'
        for f in fs:
          if exists(root + f):
            update_times.append(
              int(getmtime(root + f))
            )
      return max(update_times)

    if is_dir:
      orig_time = get_dir_time(orig)
    else:
      orig_time = getmtime(orig)

    if exists(dest):
      if is_dir:
        dest_time = get_dir_time(dest)
      else:
        dest_time = getmtime(dest)
    else:
      dest_time = 0

    if orig_time > dest_time:
      if is_dir:
        return copy_tree(orig, dest)
      return copy(orig, dest)

  for mod in logs[client]["module"]:
    do_copy(spath + mod, cpath + mod, True)
    if exists(cpath + mod + '/.log'):
      remove(cpath + mod + '/.log')
    # Delete files from client-shared if deleted from shared-root
    for root,_,fs in walk(cpath + mod):
      if not root.endswith('/'):
        root += '/'
      sroot = root.replace(cpath, spath)
      for f in fs:
        if not exists(sroot + f):
          remove(root + f)

  for fls in logs[client]["file"]:
    dirs = fls.split('/')
    for i in range(len(dirs)):
      npath = cpath + '/'.join(dirs[:i])
      if not exists(npath):
        mkdir(npath)
    do_copy(spath + fls, cpath + fls, False)


def __update_shared_files__(force_update_clients_json=False):
  if force_update_clients_json:
    from core.tools import make_clients_config
    settings.CLIENT_DATA = make_clients_config(BASE_DIR)
  logs = get_log()
  spath = BASE_DIR + '/clients/shared/'
  for client in logs:
    __update_clients_files__(client, logs, spath)


def file_updater_thread():
  spath = BASE_DIR + '/clients/shared/'

  def get_clients():
    clients = []
    for threads in threading.enumerate():
      if threads.name.endswith('-client'):
        client = ''.join(threads.name.split('-client')[:-1])
        clients.append(client)
    return clients

  def background_process():
    clients = get_clients()
    while len(clients) > 0:
      logs = get_log()
      for client in clients:
        __update_clients_files__(client, logs, spath)
      sleep(.5)
      clients = get_clients()

  thread = threading.Thread(
    None,
    background_process,
    'shared-files-updater',
    ()
  )
  return thread.start(), sleep(6)


def error_message():
  return print('''
  `SHARE` tool requires 2 arguments beginning with `-`

  ./o share -"path_to_folder" -"client_name"

  or

  ./o share -"path_to_file" -"client_name"
  ''')
