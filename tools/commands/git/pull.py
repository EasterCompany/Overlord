# Std library
import os
from sys import path
# Overlord library
from web.settings import CLIENT_DATA, BASE_DIR


def branch_origins(branch, repo=None):
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

  print("\n\nOverlord")
  print("-------------------------\n")
  os.system("git pull --recurse-submodules")
  print("\n")

  for client in CLIENT_DATA:
    source_dir = CLIENT_DATA[client]["src"]
    if os.path.exists(f"{source_dir}/.git"):
      print(f"\n{client.title()}")
      print("-------------------------\n")
      os.system(f"cd {source_dir} && git pull --recurse-submodules && cd {BASE_DIR}")
      print("\n")
