# Standard library
from os import system, chdir
# Overlord library
from web.settings import CLIENT_DATA, BASE_DIR


def install(target_client:str, package_name:str, uninstall:bool=False):
  package = package_name.strip()
  client_src = CLIENT_DATA[target_client]['src']
  if uninstall:
    return chdir(client_src), system(f"npm uninstall {package}"), chdir(BASE_DIR)
  else:
    return chdir(client_src), system(f"npm install {package}"), chdir(BASE_DIR)
