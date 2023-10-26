from web.settings import BASE_DIR
from core.library import console, listdir, isdir


def ls_project(dirs:list|None = None):
  if dirs is None: dirs = ['api', '.config', 'clients']
  base_dir = sorted(listdir(BASE_DIR))
  api_dir = sorted(listdir(BASE_DIR + '/api'))
  config_dir = sorted(listdir(BASE_DIR + '/.config'))
  clients_dir = sorted(listdir(BASE_DIR + '/clients'))

  for _dir in base_dir:

    if _dir == "api" and _dir in dirs:
      console.out(f"\n  {_dir}", "green")
      for _api in api_dir:
        if isdir(BASE_DIR + '/api/' + _api) and not _api == '__pycache__' and not _api == 'migrations':
          console.out(f"    ↳ {_api}", "green")

    elif _dir == (".config"):
      if _dir in dirs or 'config' in dirs:
        console.out(f"\n  \33[31;2;2m{_dir}\33[0m")
        if _dir == ".config":
          for _file in config_dir:
            if not isdir(BASE_DIR + '/.config/' + _file):
              console.out(f"    \33[31;2;2m↳ {_file}\33[0m")

    elif _dir == "clients" and _dir in dirs:
      console.out(f"\n  {_dir}", "blue")
      for _client in clients_dir:
        console.out(f"    ↳ {_client}", "blue")


def error_message() -> str:
  return console.out("""
  `ls` requires either a single, or no arguments.
  If an argument is provided it must either be

    ls -api

    or

    ls -clients

  otherwise, the default functionality is to list
  both the api and clients directories, along with
  the base level of the project directory.
  """)
