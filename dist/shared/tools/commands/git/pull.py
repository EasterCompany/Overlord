# Std library
import os
from sys import path
# Overlord library
from core.library import console, listdir, isdir
from web.settings import CLIENT_DATA, BASE_DIR, PROJECT_NAME


def branch_origins(branch, repo=None):
  ''' Changes the branch that this repository defaults to when pushing & pulling '''
  if repo is not None:
    os.chdir(f'{path[0]}/{repo}')
  os.system(f'git branch --set-upstream-to=origin/{branch} {branch}')
  return os.chdir(path[0])


def all():
  ''' Pulls the latest changes to & from every repository found within this projects scope '''
  console.out(f"\n> {PROJECT_NAME.upper()}", "amber")
  console.input(
    "git pull --recurse-submodules",
    cwd=BASE_DIR,
    show_output=True
  )

  pulled_apis = []
  api_dir = f"{BASE_DIR}/api"

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if os.path.exists(f"{source_dir}/.git"):
      console.out(f"\n> {client.upper()} (CLIENT)", "amber")
      console.input(
        f"git pull --recurse-submodules",
        cwd=source_dir,
        show_output=True
      )

    if os.path.exists(f"{source_api}/.git"):
      pulled_apis.append(client)
      console.out(f"\n> {client.upper()} (API)", "amber")
      console.input(
        f"git pull --recurse-submodules",
        cwd=source_api,
        show_output=True
      )

  potential_apis = listdir(api_dir)
  for dir in potential_apis:
    if (dir_path := f"{BASE_DIR}/api/{dir}") and isdir(dir_path) and (contents := listdir(dir_path)):
      if '.git' in contents and dir not in pulled_apis:
        console.out(f"\n> {dir.upper()} (API)", "amber")
        console.input(
          f"git pull --recurse-submodules",
          cwd=dir_path,
          show_output=True
        )
