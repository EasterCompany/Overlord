# Std library
import os
from sys import path
# Overlord library
from core.library import console
from web.settings import CLIENT_DATA, BASE_DIR


def branch_origins(branch, repo=None):
  """
  Changes the branch that this repository defaults to when pushing & pulling
  """
  if repo is not None:
    os.chdir(path[0] + '/' + repo)
  os.system('git branch --set-upstream-to=origin/{branch} {branch}'.format(
    branch=branch
  ))
  return os.chdir(path[0])


def all():
  """
  Pulls the latest changes to & from every repository found within this projects scope
  """
  os.chdir(BASE_DIR)

  console.out("\nOVERLORD", "yellow")
  print("-------------------------")
  os.system("git pull --recurse-submodules")

  for client in CLIENT_DATA:
    print("\n")
    source_dir = CLIENT_DATA[client]["src"]
    source_api = BASE_DIR + f'/api/{client}'

    if os.path.exists(f"{source_dir}/.git"):
      console.out(f"{client.upper()} (CLIENT)", "yellow")
      print("-------------------------")
      os.system(f"cd {source_dir} && git pull --recurse-submodules && cd {BASE_DIR}")
      print("\n")

    if os.path.exists(f"{source_api}/.git"):
      console.out(f"{client.upper()} (API)", "yellow")
      print("-------------------------")
      os.system(f"cd {source_api} && git pull --recurse-submodules && cd {BASE_DIR}")
