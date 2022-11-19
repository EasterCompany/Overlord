# Standard library
from os import system, chdir
# Overlord library
from web.settings import CLIENT_DATA, BASE_DIR


def install(target_client:str, package_name:str):
  package = package_name.strip()
  client_src = CLIENT_DATA[target_client]['src']
  return chdir(client_src), system(f"npm i {package}"), chdir(BASE_DIR)
