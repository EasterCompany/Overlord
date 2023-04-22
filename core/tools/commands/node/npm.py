# Standard library
from os import system, chdir
# Overlord library
from core.library import console
from web.settings import CLIENT_DATA, BASE_DIR


def install(target_client:str, package_name:str, uninstall:bool=False) -> None:
  package = package_name.strip()
  client_src = CLIENT_DATA[target_client]['src']
  if uninstall:
    return console.input(f"npm uninstall {package}", cwd=client_src)
  else:
    return chdir(client_src), system(f"npm install {package}"), chdir(BASE_DIR)


def install_all() -> None:
  for client in CLIENT_DATA:
    install(client, '', False)


def install_expo_cli(target_client:str) -> console.input:
  return console.input("npm install --global expo-cli")
