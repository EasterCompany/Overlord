# Overlord library
from core.library import exists, mkdir, console, sleep
from web.settings import BASE_DIR

config_dir = f"{BASE_DIR}/.config"
workspaces_dir = f"{BASE_DIR}/.config/ws"
workspace = lambda cn: f"{workspaces_dir}/{cn}.code-workspace"
new_workspace = lambda cn: """{
  "folders": [
    {
      "path": "../../clients/{cn}",
      "name": "Client"
    },
    {
      "path": "../../api/{cn}",
      "name": "API"
    }
  ],
  "settings": {}
}""".replace('{cn}', cn)

if not exists(config_dir):
  mkdir(config_dir)

if not exists(workspaces_dir):
  mkdir(workspaces_dir)


def create(client:str) -> int:
  """
  Create a workspace if it doesn't already exist

  :param client str: name of the client associated with the workspace
  :return int: 0 = created, 1 = already exists
  """
  if exists(workspace(client)):
    with open(workspace(client), 'r') as ws_file:
      if not ws_file.read() == "":
        return 1
  with open(workspace(client), 'w') as ws_file:
    ws_file.write(new_workspace(client))
  return 0


def start(client:str) -> None:
  """
  Starts a workspace if it exists and creates one if it doesn't

  :param client str: name of the client associated with the workspace
  :return None:
  """
  r = create(client)
  if r == 0:
    sleep(1)
  console.out("  workspace includes an API", "green")
  return console.input(f"code {workspace(client)}")
